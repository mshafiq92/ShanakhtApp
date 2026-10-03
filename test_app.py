# -*- coding: utf-8 -*-
"""
Wiring tests for app.py.

These do not call the real Gemini API. They use a mocked client, so they run without a
GEMINI_API_KEY and without any network access. They check that the code plumbing is
correct: message history parsing, source link formatting, and the streaming loop, not
whether the model's answers are factually good. For that, use docs/TEST_CHECKLIST.md
against the live app.

Run with:
    python test_app.py
"""

import os
import types
import unittest
from unittest.mock import MagicMock, patch

os.environ.setdefault("GEMINI_API_KEY", "test-key-not-real")

import app


def make_chunk(text=None, grounding_metadata=None):
    """Build a fake streaming chunk shaped like the real Gemini SDK response."""
    candidate = types.SimpleNamespace(grounding_metadata=grounding_metadata)
    return types.SimpleNamespace(text=text, candidates=[candidate])


class ExtractTextTests(unittest.TestCase):
    def test_plain_string(self):
        self.assertEqual(app._extract_text("hello"), "hello")

    def test_list_of_text_parts(self):
        # This is the shape Gradio 6's ChatInterface actually sends for history
        # messages. A prior bug assumed content was always a plain string, which
        # crashed on the second turn of any real conversation.
        content = [{"type": "text", "text": "hello"}, {"type": "text", "text": " world"}]
        self.assertEqual(app._extract_text(content), "hello world")

    def test_empty_or_unknown_shape(self):
        self.assertEqual(app._extract_text(None), "")
        self.assertEqual(app._extract_text(123), "")


class ToGeminiContentsTests(unittest.TestCase):
    def test_empty_history(self):
        contents = app.to_gemini_contents([], "hi")
        self.assertEqual(contents, [{"role": "user", "parts": [{"text": "hi"}]}])

    def test_messages_format_with_list_content(self):
        history = [
            {"role": "user", "content": [{"type": "text", "text": "Q1"}]},
            {"role": "assistant", "content": [{"type": "text", "text": "A1"}]},
        ]
        contents = app.to_gemini_contents(history, "Q2")
        self.assertEqual(
            contents,
            [
                {"role": "user", "parts": [{"text": "Q1"}]},
                {"role": "model", "parts": [{"text": "A1"}]},
                {"role": "user", "parts": [{"text": "Q2"}]},
            ],
        )

    def test_tuples_format(self):
        history = [["Q1", "A1"]]
        contents = app.to_gemini_contents(history, "Q2")
        self.assertEqual(
            contents,
            [
                {"role": "user", "parts": [{"text": "Q1"}]},
                {"role": "model", "parts": [{"text": "A1"}]},
                {"role": "user", "parts": [{"text": "Q2"}]},
            ],
        )


class ExtractSourcesTests(unittest.TestCase):
    def test_no_metadata(self):
        self.assertEqual(app.extract_sources(None), "")

    def test_dedupes_and_formats_links(self):
        chunk1 = types.SimpleNamespace(
            web=types.SimpleNamespace(uri="https://nadra.gov.pk", title="NADRA")
        )
        chunk2 = types.SimpleNamespace(
            web=types.SimpleNamespace(uri="https://nadra.gov.pk", title="NADRA again")
        )
        gm = types.SimpleNamespace(grounding_chunks=[chunk1, chunk2])
        result = app.extract_sources(gm)
        self.assertEqual(result.count("nadra.gov.pk"), 1)
        self.assertTrue(result.startswith("\n\n**Sources:**"))


class RespondTests(unittest.TestCase):
    def _mock_stream(self, chunks):
        client = MagicMock()
        client.models.generate_content_stream.return_value = iter(chunks)
        return client

    def test_plain_reply_no_sources(self):
        client = self._mock_stream([make_chunk("Hello "), make_chunk("there.")])
        with patch("app.get_client", return_value=client):
            out = list(app.respond("hi", []))
        self.assertEqual(out[-1][0], "Hello there.")

    def test_reply_with_grounding_appends_sources(self):
        web = types.SimpleNamespace(uri="https://dgip.gov.pk", title="DGIP")
        gm = types.SimpleNamespace(grounding_chunks=[types.SimpleNamespace(web=web)])
        client = self._mock_stream([make_chunk("Answer.", grounding_metadata=gm)])
        with patch("app.get_client", return_value=client):
            out = list(app.respond("hi", []))
        self.assertIn("Sources", out[-1][0])
        self.assertIn("dgip.gov.pk", out[-1][0])

    def test_api_error_shows_friendly_message_not_a_crash(self):
        client = MagicMock()
        client.models.generate_content_stream.side_effect = RuntimeError("boom")
        with patch("app.get_client", return_value=client):
            out = list(app.respond("hi", []))
        self.assertIn("something went wrong", out[-1][0])

    def test_missing_api_key_is_handled_gracefully(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("GEMINI_API_KEY", None)
            app._client = None
            out = list(app.respond("hi", []))
        self.assertIn("something went wrong", out[-1][0])

    def test_followup_chips_appear_and_marker_never_shown(self):
        client = self._mock_stream(
            [
                make_chunk("Renew online. [[FOLLOW"),
                make_chunk("UPS]] How much is the fee? | Where do I collect it?"),
            ]
        )
        with patch("app.get_client", return_value=client):
            out = list(app.respond("hi", []))
        for text, *_ in out:
            self.assertNotIn("[[", text)
            self.assertNotIn("FOLLOWUPS", text)
        final_text, *chips = out[-1]
        self.assertEqual(final_text, "Renew online.")
        self.assertEqual(chips[0]["value"], "How much is the fee?")
        self.assertEqual(chips[1]["value"], "Where do I collect it?")
        self.assertFalse(chips[2]["visible"])


class ChatTurnTests(unittest.TestCase):
    def test_empty_message_is_ignored(self):
        out = app.user_turn("   ", [])
        self.assertEqual(out[0], "")
        self.assertEqual(out[1], [])

    def test_question_stored_as_parts_list_is_sent_as_plain_text(self):
        history = [{"role": "user", "content": [{"type": "text", "text": "How do I renew CNIC?"}]}]
        client = MagicMock()
        client.models.generate_content_stream.return_value = iter([make_chunk("Answer.")])
        with patch("app.get_client", return_value=client):
            list(app.bot_turn(history))
        contents = client.models.generate_content_stream.call_args.kwargs["contents"]
        self.assertEqual(contents[-1]["parts"][0]["text"], "How do I renew CNIC?")

    def test_turn_adds_question_then_answer_with_chips(self):
        history = app.user_turn("hi", [])[1]
        self.assertEqual(history, [{"role": "user", "content": "hi"}])
        client = MagicMock()
        client.models.generate_content_stream.return_value = iter(
            [make_chunk("Hello. [[FOLLOWUPS]] Next? | Later?")]
        )
        with patch("app.get_client", return_value=client):
            outputs = list(app.bot_turn(history))
        final_history, *chips = outputs[-1]
        self.assertEqual(final_history[-1], {"role": "assistant", "content": "Hello."})
        self.assertEqual(chips[0]["value"], "Next?")
        self.assertEqual(chips[1]["value"], "Later?")


class FollowupParsingTests(unittest.TestCase):
    def test_valid_line_gives_up_to_three_questions(self):
        visible, qs = app.split_followups("Answer.\n[[FOLLOWUPS]] a? | b? | c? | d?")
        self.assertEqual(visible, "Answer.")
        self.assertEqual(qs, ["a?", "b?", "c?"])

    def test_missing_line_gives_no_chips(self):
        visible, qs = app.split_followups("Just an answer.")
        self.assertEqual(visible, "Just an answer.")
        self.assertEqual(qs, [])

    def test_empty_or_malformed_line_gives_no_chips(self):
        self.assertEqual(app.split_followups("Answer.\n[[FOLLOWUPS]]")[1], [])
        self.assertEqual(app.split_followups("Answer.\n[[FOLLOWUPS]] | | ")[1], [])

    def test_partial_marker_is_held_back_while_streaming(self):
        self.assertEqual(app.visible_while_streaming("Hi [[FOLLOW").rstrip(), "Hi")
        self.assertEqual(app.visible_while_streaming("Hi [").rstrip(), "Hi")
        self.assertEqual(app.visible_while_streaming("Hi there"), "Hi there")


class SystemPromptTests(unittest.TestCase):
    def test_hard_rules_present(self):
        self.assertIn("NADRA", app.SYSTEM_PROMPT)
        self.assertIn("DGIP", app.SYSTEM_PROMPT)
        self.assertIn("Never invent fees", app.SYSTEM_PROMPT)

    def test_knowledge_base_injected(self):
        self.assertIn("NICOP", app.SYSTEM_PROMPT)
        self.assertIn("B-FORM", app.SYSTEM_PROMPT)


class FeeSourceTests(unittest.TestCase):
    def test_knowledge_text_uses_fee_figures(self):
        from fees import CNIC_CATEGORIES, PASSPORT_MRP_FEES, rs
        import knowledge

        for info in CNIC_CATEGORIES.values():
            self.assertIn(rs(info["fee"]), knowledge.KNOWLEDGE)
        self.assertIn(rs(PASSPORT_MRP_FEES[5][36][0]), knowledge.KNOWLEDGE)

    def test_quick_reference_tables_use_fee_figures(self):
        from fees import CNIC_CATEGORIES, rs

        for info in CNIC_CATEGORIES.values():
            self.assertIn(rs(info["fee"]), app.CNIC_FEE_TABLE_MD)
        self.assertIn("nadra.gov.pk", app.CNIC_FEE_TABLE_MD)
        self.assertIn("dgip.gov.pk", app.PASSPORT_FEE_TABLE_MD)


class ChecklistTests(unittest.TestCase):
    def test_every_service_builds_with_verify_reminder(self):
        from checklists import SERVICE_NAMES, SERVICES, build_checklist

        for service in SERVICE_NAMES:
            text = build_checklist(service)
            self.assertIn(service, text)
            self.assertIn("Verify the current fees", text)
            self.assertIn(SERVICES[service]["agency"], text)

    def test_missing_details_point_to_official_site(self):
        from checklists import CHECK_OFFICIAL, build_checklist

        text = build_checklist("NICOP")
        self.assertIn(CHECK_OFFICIAL, text)

    def test_new_passport_uses_fee_table(self):
        from checklists import build_checklist
        from fees import PASSPORT_MRP_FEES, rs

        text = build_checklist("New passport")
        self.assertIn(rs(PASSPORT_MRP_FEES[5][36][0]), text)
        self.assertIn("Valid CNIC or NICOP", text)


if __name__ == "__main__":
    unittest.main()
