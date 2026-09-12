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
        self.assertEqual(out[-1], "Hello there.")

    def test_reply_with_grounding_appends_sources(self):
        web = types.SimpleNamespace(uri="https://dgip.gov.pk", title="DGIP")
        gm = types.SimpleNamespace(grounding_chunks=[types.SimpleNamespace(web=web)])
        client = self._mock_stream([make_chunk("Answer.", grounding_metadata=gm)])
        with patch("app.get_client", return_value=client):
            out = list(app.respond("hi", []))
        self.assertIn("Sources", out[-1])
        self.assertIn("dgip.gov.pk", out[-1])

    def test_api_error_shows_friendly_message_not_a_crash(self):
        client = MagicMock()
        client.models.generate_content_stream.side_effect = RuntimeError("boom")
        with patch("app.get_client", return_value=client):
            out = list(app.respond("hi", []))
        self.assertIn("something went wrong", out[-1])

    def test_missing_api_key_is_handled_gracefully(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("GEMINI_API_KEY", None)
            app._client = None
            out = list(app.respond("hi", []))
        self.assertIn("something went wrong", out[-1])


class SystemPromptTests(unittest.TestCase):
    def test_hard_rules_present(self):
        self.assertIn("NADRA", app.SYSTEM_PROMPT)
        self.assertIn("DGIP", app.SYSTEM_PROMPT)
        self.assertIn("Never invent fees", app.SYSTEM_PROMPT)

    def test_knowledge_base_injected(self):
        self.assertIn("NICOP", app.SYSTEM_PROMPT)
        self.assertIn("B-FORM", app.SYSTEM_PROMPT)


if __name__ == "__main__":
    unittest.main()
