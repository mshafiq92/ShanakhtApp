# -*- coding: utf-8 -*-
"""
Shanakht: an AI assistant for CNIC (NADRA) and passport (DGIP) questions in Pakistan.
Bilingual (Urdu and English). Built for the PakAngels GenAI hackathon.

Run locally:
    pip install -r requirements.txt
    export GEMINI_API_KEY="your_key_here"      # Windows: set GEMINI_API_KEY=your_key_here
    python app.py

On Hugging Face Spaces:
    Add a Secret named GEMINI_API_KEY in the Space settings. Spaces runs app.py for you.
"""

import os
import gradio as gr
from google import genai
from google.genai import types
from knowledge import KNOWLEDGE
from fees import CNIC_CATEGORIES, CNIC_COURIER_FEE, PASSPORT_TIMELINES, rs
from checklists import SERVICE_NAMES, build_checklist
import tempfile


def _load_dotenv():
    """Load KEY=VALUE lines from a local .env file into os.environ, if present.

    Local convenience only (no python-dotenv dependency needed for this). Real
    environment variables and Hugging Face Space secrets always take priority,
    since this only fills in variables that are not already set.
    """
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.isfile(env_path):
        return
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


_load_dotenv()

# The current free-tier Flash model. If this name is rejected, open
# aistudio.google.com, check the model list, and paste the exact current
# free Flash model id here (for example a newer gemini-*-flash).
MODEL = "gemini-3.6-flash"

# Turn Gemini's built-in Google Search grounding on or off. When on, the model may call
# Google Search to check current information (for example, a fee that may have changed
# since the knowledge base was written) before answering.
#
# Default is OFF: since January 2026, Grounding with Google Search on Gemini 3.x models
# requires a billing-enabled Google Cloud project (it includes a free allowance of 5,000
# grounded queries/month, then a per-query charge). A plain free-tier key with no billing
# linked gets a 429 RESOURCE_EXHAUSTED error on every request that includes this tool, which
# would break the whole chatbot for anyone without billing set up. Set the
# WEB_SEARCH_GROUNDING environment variable to "1" or "true" to turn it on, once billing is
# linked to the project behind your GEMINI_API_KEY.
WEB_SEARCH_GROUNDING = os.environ.get("WEB_SEARCH_GROUNDING", "false").strip().lower() in (
    "1",
    "true",
    "yes",
)

SYSTEM_PROMPT = f"""
You are Shanakht, a friendly assistant that helps the Pakistani public understand how to
get and manage their CNIC and passport. Your job is to give clear, correct, simple answers.

HARD RULES:
1. Answer using the KNOWLEDGE BASE below and well-known public facts about these topics.
   If you are not sure, or the question is outside CNIC / passport / NADRA / DGIP, say you
   are not sure and tell the user to check the official site. Never invent fees, timelines,
   or rules.
2. Two different departments: the CNIC is issued by NADRA, the passport is issued by DGIP
   (using NADRA records). Never say NADRA issues the passport.
3. Reply in the SAME language the user writes in. If they write in Urdu, reply in simple
   Urdu. If in English, reply in simple English. If they use Roman Urdu, you may reply in
   Roman Urdu or Urdu script, whichever is clearer.
4. For any process (how to apply, renew, correct, etc.), answer in short numbered steps.
5. Keep answers short and to the point. Do not overwhelm with detail that was not asked.
6. Whenever you give a fee, a timeline, or a full process, add a short reminder to verify
   on the official site: nadra.gov.pk for CNIC, dgip.gov.pk for passport.
7. Privacy: never ask the user for their CNIC number, passport number, OTP, password, or
   other sensitive personal data. If a user shares such a number, gently remind them not to
   share sensitive numbers in a chat.
8. Be polite and respectful.
9. Follow-up suggestions: end EVERY answer with one final line, on its own, in this exact
   form: [[FOLLOWUPS]] question one | question two | question three
   Give up to three short follow-up questions the user might ask next, in the same language
   as the user's question. Never put the | character inside a question. If there is no
   useful follow-up, write the line with nothing after the marker.

KNOWLEDGE BASE:
{KNOWLEDGE}
"""

_client = None


def get_client():
    """Create the Gemini client lazily so the app can be imported without a key set."""
    global _client
    if _client is None:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. Set it as an environment variable "
                "(locally) or as a Space Secret (on Hugging Face)."
            )
        _client = genai.Client(api_key=api_key)
    return _client


def _extract_text(content):
    """Get plain text out of a Gradio message 'content' field.

    Gradio's ChatInterface (messages format) may store content as a plain string, or as
    a list of content-part dicts like [{'type': 'text', 'text': '...'}] for multimodal
    support. We only handle text here, so flatten either shape into one string.
    """
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        pieces = []
        for part in content:
            if isinstance(part, dict) and isinstance(part.get("text"), str):
                pieces.append(part["text"])
            elif isinstance(part, str):
                pieces.append(part)
        return "".join(pieces)
    return ""


def to_gemini_contents(history, message):
    """Convert Gradio chat history + new message into Gemini contents.

    Handles both the newer 'messages' format (list of {role, content} dicts)
    and the older 'tuples' format (list of [user, assistant] pairs).
    """
    contents = []
    for turn in history or []:
        if isinstance(turn, dict):
            role = "user" if turn.get("role") == "user" else "model"
            text = _extract_text(turn.get("content", ""))
            if text:
                contents.append({"role": role, "parts": [{"text": text}]})
        elif isinstance(turn, (list, tuple)) and len(turn) == 2:
            user_text, bot_text = turn
            user_text = _extract_text(user_text)
            bot_text = _extract_text(bot_text)
            if user_text:
                contents.append({"role": "user", "parts": [{"text": user_text}]})
            if bot_text:
                contents.append({"role": "model", "parts": [{"text": bot_text}]})
    contents.append({"role": "user", "parts": [{"text": message}]})
    return contents


def extract_sources(grounding_metadata):
    """Build a short markdown 'Sources' block from Gemini grounding metadata, if any."""
    if not grounding_metadata:
        return ""
    links = []
    seen = set()
    for gc in getattr(grounding_metadata, "grounding_chunks", None) or []:
        web = getattr(gc, "web", None)
        uri = getattr(web, "uri", None) if web else None
        if not uri or uri in seen:
            continue
        seen.add(uri)
        title = getattr(web, "title", None) or uri
        links.append(f"- [{title}]({uri})")
    if not links:
        return ""
    return "\n\n**Sources:**\n" + "\n".join(links)


FOLLOWUP_MARKER = "[[FOLLOWUPS]]"
MAX_FOLLOWUPS = 3


def split_followups(raw):
    """Return (visible answer, follow-up questions) from a full model reply."""
    idx = raw.find(FOLLOWUP_MARKER)
    if idx == -1:
        return raw.strip(), []
    visible = raw[:idx].rstrip()
    tail = raw[idx + len(FOLLOWUP_MARKER):].strip().split("\n")[0]
    questions = [q.strip() for q in tail.split("|") if q.strip()][:MAX_FOLLOWUPS]
    return visible, questions


def visible_while_streaming(raw):
    """Return the part of a partial reply that is safe to show, hiding any marker."""
    idx = raw.find(FOLLOWUP_MARKER)
    if idx != -1:
        return raw[:idx].rstrip()
    for k in range(len(FOLLOWUP_MARKER) - 1, 0, -1):
        if raw.endswith(FOLLOWUP_MARKER[:k]):
            return raw[:-k]
    return raw


def followup_updates(questions):
    updates = []
    for i in range(MAX_FOLLOWUPS):
        if i < len(questions):
            updates.append(gr.update(value=questions[i], visible=True))
        else:
            updates.append(gr.update(value="", visible=False))
    return tuple(updates)


def respond(message, history):
    """Stream the reply, then show follow-up chips. Yields (text, *chip updates)."""
    contents = to_gemini_contents(history, message)
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        temperature=0.3,
        tools=[types.Tool(google_search=types.GoogleSearch())] if WEB_SEARCH_GROUNDING else None,
    )
    try:
        client = get_client()
        stream = client.models.generate_content_stream(
            model=MODEL,
            contents=contents,
            config=config,
        )
        raw = ""
        grounding_metadata = None
        for chunk in stream:
            if getattr(chunk, "text", None):
                raw += chunk.text
                yield (visible_while_streaming(raw), *followup_updates([]))
            for candidate in getattr(chunk, "candidates", None) or []:
                gm = getattr(candidate, "grounding_metadata", None)
                if gm:
                    grounding_metadata = gm
        visible, questions = split_followups(raw)
        if not visible:
            yield ("Sorry, I could not generate an answer. Please try rephrasing.", *followup_updates([]))
        else:
            sources = extract_sources(grounding_metadata)
            yield (visible + sources, *followup_updates(questions))
    except Exception as e:  # keep the demo alive even if the API call fails
        yield (
            "Sorry, something went wrong while contacting the AI service. "
            "Please try again in a moment.\n\n"
            f"(Technical detail: {e})",
            *followup_updates([]),
        )


def make_checklist(service):
    text = build_checklist(service)
    slug = service.lower().replace(" ", "_").replace("(", "").replace(")", "")
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", prefix=f"shanakht_{slug}_", delete=False, encoding="utf-8"
    ) as f:
        f.write(text)
    return text, f.name


def user_turn(message, history):
    history = list(history or [])
    if not (message or "").strip():
        return "", history, *followup_updates([])
    return "", history + [{"role": "user", "content": message}], *followup_updates([])


def bot_turn(history):
    prior, question = history[:-1], history[-1]["content"]
    for text, *chips in respond(question, prior):
        yield [*prior, {"role": "assistant", "content": text}], *chips


DESCRIPTION = (
    "Ask about CNIC (NADRA) and passport (DGIP): types, documents, fees, renewal, "
    "modification, overseas ID, tracking, and safety tips. You can ask in Urdu or English. "
    "This is a helper, not an official source. Always verify on nadra.gov.pk and dgip.gov.pk."
)

# Shown centered in the chat window before the first message. Tells users up front,
# in both languages, that they can type in either one. Kept to one short line (no repeat
# of the "Shanakht" title, already shown in the header card above) since a taller
# placeholder can get clipped in the chatbot's centered box on short mobile screens.
CHATBOT_PLACEHOLDER = (
    "Ask your question in **Urdu** or **English**, مجھ سے اردو یا انگریزی میں سوال پوچھیں۔"
)

# Two each in English, Urdu script, and Roman Urdu, covering CNIC and passport.
EXAMPLES = [
    "How do I renew my expired CNIC?",
    "What documents do I need for a new passport?",
    "میرا شناختی کارڈ گم ہو گیا ہے، میں کیا کروں؟",
    "نیا پاسپورٹ بنوانے کا طریقہ کیا ہے؟",
    "CNIC ki renewal ke liye kya documents chahiye?",
    "Urgent passport ki fee kitni hai?",
]

# Chip label -> starter question that fills the input when clicked.
CATEGORY_CHIPS = {
    "CNIC": "How do I apply for a new CNIC?",
    "Passport": "How do I apply for a new passport?",
    "Smart Card": "What is a Smart CNIC and how do I get one?",
    "NICOP & POC": "How can I get a NICOP while living abroad?",
    "Fees": "What are the current CNIC and passport fees?",
    "Tracking": "How do I track my CNIC or passport application?",
    "Safety": "What safety tips should I follow with my CNIC and passport?",
}

OFFICIAL_LINKS = [
    ("NADRA (CNIC)", "https://nadra.gov.pk"),
    ("Pak-ID portal and app", "https://id.nadra.gov.pk"),
    ("DGIP (passport)", "https://dgip.gov.pk"),
    ("CNIC tracking", "https://id.nadra.gov.pk"),
]
NADRA_HELPLINE = "1777"
FOOTER_MD = (
    "Shanakht is a helper, not an official source. Always verify on nadra.gov.pk and "
    "dgip.gov.pk.\n\n"
    + " · ".join(f"[{label}]({url})" for label, url in OFFICIAL_LINKS[:3])
    + f" · Helpline {NADRA_HELPLINE}\n\n"
    "<small>Built by Team Shanakht for the PakAngels GenAI and Agentic AI Training Program "
    "hackathon.</small>"
)
CNIC_FEE_TABLE_MD = (
    "**CNIC (NADRA)**\n\n"
    "| Category | Fee | Timeline |\n"
    "|---|---|---|\n"
    + "\n".join(
        f"| {name} | {rs(info['fee'])} | {info['timeline']} |"
        for name, info in CNIC_CATEGORIES.items()
    )
    + f"\n\nCourier delivery: {rs(CNIC_COURIER_FEE)}. A first-ever CNIC is free under Normal "
    "processing. Verify on nadra.gov.pk before paying, since fees change."
)
PASSPORT_FEE_TABLE_MD = (
    "**Passport (DGIP)**\n\n"
    "| Category | Timeline |\n"
    "|---|---|\n"
    + "\n".join(f"| {name} | {timeline} |" for name, timeline in PASSPORT_TIMELINES.items())
    + "\n\nThe exact fee depends on validity (5 or 10 years) and page count (36, 72, or 100). "
    "Verify the current figure on dgip.gov.pk before paying, since fees change."
)
OFFICIAL_LINKS_MD = (
    "\n".join(f"- [{label}]({url})" for label, url in OFFICIAL_LINKS)
    + f"\n- NADRA helpline: {NADRA_HELPLINE}\n\n"
    "Shanakht is a helper, not an official source. Always verify on the official sites."
)

# Gradio hardcodes the chat panel to `direction: ltr`, which misrenders Urdu script
# (right-to-left) since replies mix English and Urdu in the same conversation.
# `unicode-bidi: plaintext` makes each message's direction follow its own text instead
# of the fixed container direction, so English stays LTR and Urdu becomes RTL automatically.
# `!important` is needed because Gradio's built-in rules match with equal or higher
# CSS specificity.
CUSTOM_CSS = """
.gradio-container {
    max-width: 900px !important;
    margin: 0 auto !important;
}
.message-wrap, .message-wrap .bot, .message-wrap .user, .message-wrap .prose {
    unicode-bidi: plaintext !important;
}
.message-wrap .bot, .message-wrap .user {
    text-align: start !important;
}
.category-chip button, .followup-chip button {
    border-radius: 999px !important;
}
#followup-chips {
    flex-wrap: wrap !important;
    gap: 8px !important;
}
#category-chips {
    flex-wrap: wrap !important;
    gap: 8px !important;
}
@media (max-width: 480px) {
    .gradio-container {
        padding-left: 12px !important;
        padding-right: 12px !important;
    }
    .shanakht-hero {
        padding: 14px !important;
        gap: 10px !important;
    }
    .shanakht-hero .hero-title {
        font-size: 1.25rem !important;
    }
    .category-chip button {
        font-size: 0.8rem !important;
        padding: 4px 10px !important;
    }
}
"""

# A simple inline ID-card icon (no separate image file, so nothing extra to upload or
# host when deploying). `currentColor` makes it inherit the surrounding text color, so
# it stays legible in both light and dark themes automatically.
LOGO_SVG = """
<svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"
     style="flex-shrink:0;">
  <rect x="2" y="4.5" width="20" height="15" rx="2.5" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="7.5" cy="10.5" r="2" stroke="currentColor" stroke-width="1.5"/>
  <path d="M4.5 16c0-1.66 1.34-3 3-3s3 1.34 3 3" stroke="currentColor" stroke-width="1.5"
        stroke-linecap="round"/>
  <line x1="13" y1="9" x2="19" y2="9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="13" y1="12" x2="19" y2="12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="13" y1="15" x2="17" y2="15" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
</svg>
"""

GREEN = gr.themes.Color(
    c50="#EEF7F2", c100="#D5EDE0", c200="#AEDCC4", c300="#7CC4A0",
    c400="#4DA97E", c500="#1B8A5A", c600="#177650", c700="#125F42",
    c800="#0B4F32", c900="#093D28", c950="#05271A", name="shanakht-green",
)
GOLD = gr.themes.Color(
    c50="#FBF7E8", c100="#F5ECC6", c200="#EDDC95", c300="#E3CA65",
    c400="#D8B840", c500="#C9A227", c600="#A8841E", c700="#86681A",
    c800="#654E15", c900="#463611", c950="#2A2109", name="shanakht-gold",
)
BRAND_THEME = gr.themes.Soft(
    primary_hue=GREEN,
    secondary_hue=GOLD,
    neutral_hue="slate",
    font=[
        gr.themes.GoogleFont("Inter"),
        gr.themes.GoogleFont("Noto Sans Arabic"),
        gr.themes.Font("ui-sans-serif"),
        gr.themes.Font("system-ui"),
        gr.themes.Font("sans-serif"),
    ],
)

HEADER_HTML = f"""
<div class="shanakht-hero" style="
    display:flex; align-items:center; gap:16px;
    padding:20px 22px; margin-bottom:8px;
    background:linear-gradient(135deg, #0B4F32 0%, #1B8A5A 100%);
    border-bottom:3px solid #C9A227;
    border-radius:var(--block-radius, 12px);
    color:#FFFFFF;
">
  <div style="flex-shrink:0; color:#C9A227;">{LOGO_SVG}</div>
  <div>
    <div class="hero-title" style="font-size:1.6rem; font-weight:700; line-height:1.2;">
      Shanakht <span style="font-weight:500;">(شناخت)</span>
    </div>
    <div style="font-size:0.95rem; opacity:0.9; margin:2px 0 8px;">
      CNIC and Passport Assistant
    </div>
    <div style="font-size:0.9rem; line-height:1.5; opacity:0.95;">
      {DESCRIPTION}
    </div>
  </div>
</div>
"""

with gr.Blocks(
    title="Shanakht (شناخت): CNIC & Passport Assistant",
    analytics_enabled=False,
) as demo:
    gr.HTML(HEADER_HTML)
    with gr.Row(elem_id="category-chips"):
        chip_buttons = [
            (question, gr.Button(label, size="sm", variant="secondary", elem_classes="category-chip"))
            for label, question in CATEGORY_CHIPS.items()
        ]
    chatbot = gr.Chatbot(
        placeholder=CHATBOT_PLACEHOLDER,
        label="Shanakht",
        show_label=False,
        min_height=320,
        buttons=["copy"],
    )
    with gr.Row(elem_id="followup-chips"):
        followup_btns = [
            gr.Button(size="sm", variant="secondary", visible=False, elem_classes="followup-chip")
            for _ in range(MAX_FOLLOWUPS)
        ]
    msg = gr.Textbox(
        show_label=False,
        placeholder="Type your question here...",
        submit_btn=True,
        elem_id="chat-input",
    )
    gr.Examples(examples=[[example] for example in EXAMPLES], inputs=msg)

    msg.submit(user_turn, [msg, chatbot], [msg, chatbot, *followup_btns], queue=False).then(
        bot_turn, chatbot, [chatbot, *followup_btns]
    )
    for btn in followup_btns:
        btn.click(user_turn, [btn, chatbot], [msg, chatbot, *followup_btns], queue=False).then(
            bot_turn, chatbot, [chatbot, *followup_btns]
        )
    for question, button in chip_buttons:
        button.click(lambda q=question: q, inputs=None, outputs=msg)
    with gr.Accordion("Official links and helpline", open=False):
        gr.Markdown(OFFICIAL_LINKS_MD)
    with gr.Accordion("Document checklist generator", open=False):
        service_pick = gr.Dropdown(choices=SERVICE_NAMES, value=SERVICE_NAMES[0], label="Service")
        generate_btn = gr.Button("Generate checklist", variant="primary")
        checklist_text = gr.Textbox(
            label="Checklist (English). You can paste any line into the chat to ask about it in Urdu.",
            lines=18,
            max_lines=30,
            interactive=False,
        )
        download_btn = gr.DownloadButton("Download as .txt")
        generate_btn.click(
            fn=make_checklist, inputs=service_pick, outputs=[checklist_text, download_btn]
        )
    with gr.Accordion("Fee and timeline quick reference", open=False):
        gr.Markdown(CNIC_FEE_TABLE_MD)
        gr.Markdown(PASSPORT_FEE_TABLE_MD)
    gr.Markdown(FOOTER_MD)

if __name__ == "__main__":
    # 0.0.0.0 + the platform's PORT env var is required on hosts like Render or Cloud
    # Run, which route traffic to a container by port and expect it to listen on all
    # interfaces. Falls back to the usual local port when PORT isn't set.
    demo.launch(
        theme=BRAND_THEME,
        css=CUSTOM_CSS,
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860)),
    )
