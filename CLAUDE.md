# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this project is

Shanakht (شناخت) is a bilingual (Urdu/English) chatbot that gives Pakistani citizens
plain-language guidance on CNIC (NADRA) and passport (DGIP) processes. Built for the
PakAngels GenAI hackathon. Full requirements live in `docs/Shanakht_PRD.md`; the full
build story, tools, and architecture live in `docs/APPLICATION_JOURNEY.md`.

Stack: Gradio `ChatInterface` (`app.py`) + Google Gemini via the `google-genai` SDK,
grounded by a hand-curated knowledge base (`knowledge.py`) injected into the system
prompt. No RAG, no database, no user accounts.

## Golden rules (do not violate these while implementing any task)

1. **Two different departments.** NADRA issues the CNIC. DGIP issues the passport
   (using NADRA records for identity). Never say NADRA issues the passport, or blur
   the two agencies together.
2. **Never invent facts.** Answers must come from `knowledge.py` plus well-known public
   facts about these specific topics. If a fee, timeline, or rule is missing, or the
   question is outside CNIC/passport/NADRA/DGIP scope, say so and point to the official
   site rather than guessing.
   - This applies to me (Claude Code) too: never fill in a fee or timeline with a
     guessed number. Research it from official sources or ask the user for the
     verified figure, the way the current figures in `knowledge.py` were sourced.
3. **Reply in the user's language.** Same language they wrote in (Urdu, English, or
   Roman Urdu). This must keep working through any change to prompt, streaming, or
   grounding logic.
4. **Numbered steps for processes.** Any "how do I apply/renew/correct" answer must be
   short, ordered steps, not a paragraph.
5. **Verify reminder.** Any answer that gives a fee, a timeline, or a full process must
   add a short reminder to check nadra.gov.pk (CNIC) or dgip.gov.pk (passport).
6. **No sensitive data.** Never ask the user for a CNIC number, passport number, OTP, or
   password. If a user shares one, gently remind them not to share sensitive numbers.
   Do not add any feature that stores or logs user-submitted personal data.
7. **No RAG, no database.** The knowledge base is a single plain-text Python string in
   `knowledge.py`, editable by a non-developer. Do not introduce a vector store, external
   document corpus, or persistence layer as part of the hackathon scope.
8. **Keep it a helper, not an authority.** Shanakht does not process applications, take
   payments, or give legal rulings. Do not add features that imply otherwise.

If any request conflicts with a rule above, the rule above wins — flag the conflict
instead of silently resolving it.

## Working style for this repo

- Work in small, incremental steps. Show diffs/changes before wiring up anything that
  touches the model call, streaming, or the system prompt, and wait for confirmation on
  anything non-trivial.
- Never put an API key in code, docs, or git history. `GEMINI_API_KEY` is an environment
  variable locally and a Space secret on Hugging Face — nowhere else.
- Keep `requirements.txt` minimal; only add a package if the task truly needs it.
- `knowledge.py` is content, not code — prefer asking the user for verified figures over
  editing its facts yourself.
- This is a free-tier demo app: keep dependencies and architecture simple enough to run
  on a free hosting tier without extra services. Deployment target is Render (see below),
  not Hugging Face Spaces — HF now requires a paid plan for a Gradio SDK Space.

## Current state (update as work progresses)

- `app.py`: working Gradio chat UI with streaming Gemini responses, the system prompt
  encoding the rules above, optional Google Search grounding (off by default — requires
  a billed Google Cloud project), and a UI polish pass (theme, RTL-aware Urdu rendering,
  logo, mobile fixes). Binds to `0.0.0.0` + the platform `PORT` env var for hosting
  outside Hugging Face.
- `knowledge.py`: FAQ content complete, including fee/timeline figures for CNIC, FRC,
  passport, and the PTA SIM-check method (sourced from official sites where reachable,
  cross-checked across independent sources otherwise — see the file's own header note).
- `.python-version` pins Python 3.12 for deployment (Render's newer default lacked
  prebuilt wheels for some dependencies).
- **Deployed and live** at https://shanakhtapp.onrender.com (Render free tier — see
  README.md section 3 for why Render instead of HF Spaces, and its cold-start tradeoff).
- `test_app.py`: wiring tests (message history parsing, source formatting, error
  handling) with a mocked client — no API key or network needed. Run with
  `python test_app.py`.
- `docs/TEST_CHECKLIST.md`: plain-language accuracy checklist to run against the live
  app. `docs/DEMO_SCRIPT.md`: the live demo script and backup screenshot list.
- Everything in the original task list is done. See `docs/APPLICATION_JOURNEY.md` for
  the full build story if picking this project back up later.
