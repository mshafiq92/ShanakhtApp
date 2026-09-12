# Shanakht: Task Prompts for Claude Code

Use these prompts one at a time in Claude Code. Paste one, let it finish, verify the result,
then move to the next. Each prompt is written to be self contained. Read `CLAUDE.md` first.

Before you start: make sure `GEMINI_API_KEY` is set in your environment and that you have
run the app once so you know the base chatbot works.

---

## Prompt 0: Orientation

```
Read CLAUDE.md and every file in this repository. Summarize back to me, in a few lines,
what this project is, the golden rules, the current state, and the remaining tasks. Do not
change any code yet. Wait for my go ahead.
```

---

## Prompt 1: Add live web search grounding (the agentic feature)

```
Add an optional live web search grounding feature to app.py using Gemini's built in Google
Search grounding tool from the google-genai SDK.

Requirements:
- Add the Google Search tool to the generate_content config so the model can ground answers
  in current information when useful.
- Keep it behind a simple flag or setting so it is easy to turn on or off.
- When grounding is used and sources are returned, show a short "Sources" note under the
  answer with the links, if the SDK provides them.
- Do not break streaming, the bilingual behavior, or any golden rule in CLAUDE.md.
- Update requirements.txt only if a new package is truly needed.

Work in small steps. First show me the exact code change for the config and the tool, explain
it, and wait for my approval before wiring in the sources display. Then help me test it with
a real query once I confirm my key is set.
```

---

## Prompt 2: Polish the chat experience (optional)

```
Improve the chat interface polish without adding scope:
- A clear title and one line description that states this is a helper, not an official source.
- A balanced set of example questions, some in Urdu and some in English, covering CNIC and
  passport.
- A short first message or placeholder that tells users they can ask in Urdu or English.

Keep it simple and clean. Show me the diff before applying. Do not add themes or assets that
would complicate deployment.
```

---

## Prompt 3: Prepare the repository for GitHub

```
Get this repository ready for a clean first push to GitHub.

- Confirm .gitignore excludes __pycache__, .env, virtual environment folders, and any local
  secrets.
- Confirm no API key or secret appears anywhere in the code or docs. Search the whole repo to
  be sure.
- Make sure README.md is accurate for the current code, including run and deploy steps.
- Suggest a clear, conventional commit message for the initial commit.

Do not run any destructive git commands. Show me the git status and the exact commands you
propose, and let me run the push myself.
```

---

## Prompt 4: Deploy to Hugging Face Spaces

```
Help me deploy this as a Gradio app on Hugging Face Spaces to get a public demo link.

- Confirm app.py is a valid Gradio Spaces entry point and that requirements.txt is complete.
- Tell me the exact steps to create the Space, choose the Gradio SDK, upload or push these
  files, and set GEMINI_API_KEY as a Space secret.
- Explain how to read the build logs and fix the most common errors (wrong model name,
  missing secret, package version issues).
- After I say the Space is live, give me five test questions in Urdu and English to run on
  the public link to confirm it works.

Do not put the key anywhere in the repo. The key goes only in the Space secret.
```

---

## Prompt 5: Build a self test for accuracy

```
Create a short test script or checklist that runs a set of prepared questions against the
bot and lets me check the answers for accuracy and correct language.

- Cover CNIC and passport, new and renewal, overseas, fees, tracking, and one safety tip.
- Include at least three Urdu questions.
- For each question, note what a correct answer must include (for example the verify reminder,
  the NADRA vs DGIP distinction, or numbered steps).

If you write a script, it should use a mocked model for wiring checks, since the live call
needs my key. Keep the checklist simple enough for a non developer to run during the demo.
```

---

## Prompt 6: Prepare the demo

```
Help me prepare a smooth 3 to 5 minute live demo.

- Give me a short spoken script that matches the pitch deck: problem, solution, live demo,
  impact.
- List the exact questions to type during the demo, in a good order, to show bilingual
  answers, a step by step process, and the agentic web search.
- Tell me exactly which screenshots to capture as a backup in case the live service fails.

Keep it tight and practical. No new features.
```

---

## Reminders

- If a prompt result conflicts with a golden rule in CLAUDE.md, the golden rule wins.
- If a fee or timeline is missing or still tagged, ask me for the verified figure. Do not
  guess.
- Keep every change small and verified before moving on.
