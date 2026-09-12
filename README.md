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

## 3. Deploy for a public demo link

**Live demo:** https://shanakhtapp.onrender.com (Render, free tier)

As of September 2026, Hugging Face Spaces requires a paid plan to run a Gradio SDK Space
on CPU Basic (a policy change from mid-2026 — Static Spaces are still free, but a Gradio
app is not), so this project deploys to **Render** instead:

1. Make a free account at render.com (GitHub sign-in is easiest).
2. New → Web Service → Public Git Repository → paste this repo's URL.
3. Render auto-detects Python. Set:
   - **Start Command**: `python app.py` (Render's default `gunicorn` placeholder is wrong
     for a Gradio app — replace it).
   - **Instance type**: Free.
4. Add an environment variable: name `GEMINI_API_KEY`, value your key (use "Add from
   .env" to import it directly instead of retyping it). Do **not** commit your `.env`
   file — it is gitignored on purpose.
5. Deploy. Render currently requires a card on file even for the free tier (a temporary
   $1 authorization hold, not a real charge — standard anti-abuse verification, same as
   most cloud free tiers now use).
6. Free instances spin down after inactivity; the first request after idle time can take
   ~30-60s to wake back up. Open the link yourself a few minutes before a live demo so
   it's already warm.

`.python-version` pins Python to 3.12 in this repo — Render's newer default (3.14 at the
time of writing) lacks prebuilt wheels for some dependencies, making builds much slower.

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
