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


def respond(message, history):
    """Stream the assistant reply token by token."""
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
        partial = ""
        grounding_metadata = None
        for chunk in stream:
            if getattr(chunk, "text", None):
                partial += chunk.text
                yield partial
            for candidate in getattr(chunk, "candidates", None) or []:
                gm = getattr(candidate, "grounding_metadata", None)
                if gm:
                    grounding_metadata = gm
        if not partial:
            yield "Sorry, I could not generate an answer. Please try rephrasing."
        else:
            sources = extract_sources(grounding_metadata)
            if sources:
                yield partial + sources
    except Exception as e:  # keep the demo alive even if the API call fails
        yield (
            "Sorry, something went wrong while contacting the AI service. "
            "Please try again in a moment.\n\n"
            f"(Technical detail: {e})"
        )


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
    "Ask your question in **Urdu** or **English** — مجھ سے اردو یا انگریزی میں سوال پوچھیں۔"
)

# A balanced mix of Urdu, Roman Urdu, and English, covering both CNIC and passport.
EXAMPLES = [
    "How do I renew my expired CNIC?",
    "میرا شناختی کارڈ گم ہو گیا ہے، میں کیا کروں؟",
    "What documents do I need for a new passport?",
    "نیا پاسپورٹ بنوانے کا طریقہ کیا ہے؟",
    "Urgent passport ki fee kitni hai?",
]

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

HEADER_HTML = f"""
<div style="
    display:flex; align-items:flex-start; gap:14px;
    padding:16px 20px; margin-bottom:6px;
    background:var(--block-background-fill);
    border:1px solid var(--block-border-color);
    border-radius:var(--block-radius, 12px);
">
  <div style="color:var(--body-text-color); margin-top:2px;">{LOGO_SVG}</div>
  <div>
    <div style="font-size:1.4rem; font-weight:600; line-height:1.25;">Shanakht (شناخت)</div>
    <div style="font-size:0.9rem; color:var(--body-text-color-subdued); margin:2px 0 8px;">
      CNIC &amp; Passport Assistant
    </div>
    <div style="font-size:0.9rem; line-height:1.5; color:var(--body-text-color);">
      {DESCRIPTION}
    </div>
  </div>
</div>
"""

with gr.Blocks(title="Shanakht (شناخت): CNIC & Passport Assistant") as demo:
    gr.HTML(HEADER_HTML)
    gr.ChatInterface(
        fn=respond,
        chatbot=gr.Chatbot(
            placeholder=CHATBOT_PLACEHOLDER,
            label="Shanakht",
            show_label=False,
            min_height=320,
        ),
        examples=EXAMPLES,
    )

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft(), css=CUSTOM_CSS)
