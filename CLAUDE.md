# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this project is

Shanakht (شناخت) is a bilingual (Urdu/English) chatbot that gives Pakistani citizens
plain-language guidance on CNIC (NADRA) and passport (DGIP) processes. Built for the
PakAngels GenAI hackathon. Full requirements live in `docs/Shanakht_PRD.md`; the staged
task list lives in `docs/PROMPTS.md`.

Stack: Gradio `ChatInterface` (`app.py`) + Google Gemini via the `google-genai` SDK,
grounded by a hand-curated knowledge base (`knowledge.py`) injected into the system
prompt. No RAG, no database, no user accounts.

## Golden rules (do not violate these while implementing any task)

1. **Two different departments.** NADRA issues the CNIC. DGIP issues the passport
   (using NADRA records for identity). Never say NADRA issues the passport, or blur
   the two agencies together.
2. **Never invent facts.** Answers must come from `knowledge.py` plus well-known public
   facts about these specific topics. If a fee, timeline, or rule is missing, tagged
   `[CONFIRM]`/`[REPLACE WITH VERIFIED FIGURES]`, or the question is outside CNIC/passport/
   NADRA/DGIP scope, say so and point to the official site rather than guessing.
   - This applies to me (Claude Code) too: never fill in a placeholder fee/timeline with
     a guessed number. Ask the user for the verified figure.
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

If any task prompt (including those in `docs/PROMPTS.md`) conflicts with a rule above,
the rule above wins — flag the conflict instead of silently resolving it.

## Working style for this repo

- Work in the small, incremental steps described in `docs/PROMPTS.md`. Show diffs/changes
  before wiring up anything that touches the model call, streaming, or the system prompt,
  and wait for confirmation on anything non-trivial.
- Never put an API key in code, docs, or git history. `GEMINI_API_KEY` is an environment
  variable locally and a Space secret on Hugging Face — nowhere else.
- Keep `requirements.txt` minimal; only add a package if the task truly needs it.
- `knowledge.py` is content, not code — prefer asking the user for verified figures over
  editing its facts yourself.
- This is a free-tier demo app: keep dependencies and architecture simple enough to run
  on Hugging Face Spaces' free tier without extra services.

## Current state (update as work progresses)

- `app.py`: working Gradio chat UI with streaming Gemini responses and the system prompt
  encoding the rules above.
- `knowledge.py`: FAQ content complete, including fee/timeline figures for CNIC, FRC,
  passport, and the PTA SIM-check method (sourced from official sites where reachable,
  cross-checked across independent sources otherwise — see the file's own header note).
- Not yet done: live web search grounding, UI polish pass, `.gitignore`/GitHub prep,
  Hugging Face deployment, self-test script, demo script. See `docs/PROMPTS.md` for the
  order of these tasks.
