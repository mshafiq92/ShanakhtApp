# Shanakht: CNIC & Passport Assistant

An AI chatbot that answers the Pakistani public's questions about CNIC (NADRA) and
passport (DGIP) in simple Urdu and English. Built for the PakAngels GenAI hackathon.

It uses Google Gemini plus a curated, verified FAQ (in `knowledge.py`). It gives
step-by-step answers and always points users to the official sites. No RAG, no database.

## Files

- `app.py` : the chatbot (Gradio chat UI + Gemini).
- `knowledge.py` : the bot's facts. Edit this to change what the bot knows.
- `requirements.txt` : Python packages.
- `CLAUDE.md` : golden rules and working notes for AI-assisted development on this repo.
- `docs/` : the product requirements document and the task prompts used to build this.

## 1. Get a free API key

1. Go to aistudio.google.com/app/apikey and sign in with a Google account.
2. Click Create API key and copy it.
3. Keep it private. Never paste it into the code, docs, or commit it — see step 2 below
   for where it actually goes.

## 2. Run on your computer

```
pip install -r requirements.txt
```

Create a file named `.env` in the project root (already excluded by `.gitignore`, so it
is never committed) with this one line:

```
GEMINI_API_KEY=your_key_here
```

Then run:

```
python app.py
```

and open the local link it prints (usually http://127.0.0.1:7860).

(Alternatively, set `GEMINI_API_KEY` as a regular environment variable instead of using
`.env` — `export GEMINI_API_KEY="your_key_here"` on Linux/Mac, or
`$env:GEMINI_API_KEY = "your_key_here"` in PowerShell.)

## 3. Deploy free on Hugging Face Spaces (public link for the demo)

1. Make a free account at huggingface.co.
2. Click New, then Space. Choose the Gradio SDK. Give it a name.
3. Push this repo to the Space with git (or upload the files through the web UI).
4. In the Space, go to Settings, then Variables and secrets, and add a secret:
   name `GEMINI_API_KEY`, value your key. Do **not** upload your `.env` file — it is
   gitignored on purpose and Spaces secrets are the correct place for the key.
5. The Space builds and runs automatically and gives you a public URL for the demo.

## 4. Edit what the bot knows

Open `knowledge.py` and edit the text inside `KNOWLEDGE`. Fees and timelines were
researched from official sources (dgip.gov.pk directly; NADRA figures cross-checked
across multiple independent public sources, since nadra.gov.pk blocks automated
fetches) — see the note at the top of the file. Re-verify before relying on this for
anything beyond the hackathon demo, since government fees change over time.

## 5. Optional: live web search grounding

Set the `WEB_SEARCH_GROUNDING` environment variable (or `.env` line) to `true` to let
Gemini use Google Search to check current information before answering. It is **off by
default** because, since January 2026, Grounding with Google Search on Gemini 3.x models
requires a billing-enabled Google Cloud project (free up to 5,000 grounded queries/month,
then billed). A plain free-tier key with no billing linked will error on every message if
this is turned on.

## Notes

- If the model name is rejected, open aistudio.google.com, check the current free
  Flash model, and update the `MODEL` value near the top of `app.py`.
- Free tier has rate limits (a few requests per minute), which is fine for a demo.
- This is a helper, not an official source. It reminds users to verify on nadra.gov.pk
  and dgip.gov.pk.
