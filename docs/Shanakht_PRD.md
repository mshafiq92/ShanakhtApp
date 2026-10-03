# Product Requirements Document: Shanakht

**Product name:** Shanakht (شناخت), the CNIC and Passport Public Assistant
**Document status:** Draft for review
**Version:** 2.0
**Date:** October 4, 2026
**Owner:** Team Shanakht
**Program:** PakAngels GenAI and Agentic AI Training Program, Cohort 11 (Hackathon)

---

## 1. Executive Summary

Shanakht is an AI chatbot that gives Pakistani citizens instant, plain language answers
about how to get and manage their CNIC and passport. It replies in both Urdu and English,
is free to use, and is available at any time. The bot answers from a curated, verified
knowledge base written with real government domain expertise, so the information is
accurate. It gives step by step guidance for common processes and always points users to
the official sources for final confirmation.

The product is built for the PakAngels GenAI hackathon as a working, deployed demonstration
of a Generative AI application with an agentic layer. It maps directly to United Nations
Sustainable Development Goal 16, specifically target 16.9 on legal identity for all.

---

## 2. Problem Statement

Getting a CNIC or a passport in Pakistan is simple in theory but confusing in practice.
Citizens are often unsure about:

- Which card, booklet, or category applies to their case.
- What documents are required for a new application, a renewal, or a modification.
- The current fees, and the difference between normal, urgent, and executive or fast track.
- How overseas Pakistanis should proceed (NICOP, POC, e-passport from abroad).

The information is public, but it is scattered across different sources, often available
only in English, and hard for an ordinary citizen to piece together quickly. As a result,
people rely on rumors, on agents and touts who overcharge, on long helpline queues, and on
repeated office visits. This wastes their time and money and creates room for exploitation.

---

## 3. Goals and Objectives

**Primary goal:** Help any Pakistani citizen get correct, clear answers about CNIC and
passport processes in their own language, without needing an agent.

**Objectives:**

1. Provide accurate answers for the most common CNIC and passport questions.
2. Serve answers in both Urdu and English.
3. Guide users through key processes in simple, ordered steps.
4. Reduce dependence on touts and reduce misinformation.
5. Always direct users to official sources so they can verify.
6. Demonstrate a clean, deployed GenAI and agentic application for the hackathon.

**Non-goals:**

- Shanakht is not an official government service and does not process applications.
- Shanakht does not store user data or handle payments.
- Shanakht does not give legal rulings or guaranteed outcomes.

---

## 4. Target Users

**Primary users:**

- General public in Pakistan applying for or renewing a CNIC or passport for the first
  time or after expiry.
- Citizens who are more comfortable in Urdu than in English.
- People with low familiarity with government portals who need plain guidance.

**Secondary users:**

- Overseas Pakistanis needing NICOP, POC, or passport guidance from abroad.
- Family members helping elderly relatives or children with documents.

**Representative personas:**

1. Ayesha, 22, applying for her first passport, unsure which pages and validity to choose.
2. Kamran, 45, whose CNIC just expired, wants the fastest way to renew.
3. Bilal, 30, working in Dubai, needs to know how to get a NICOP from abroad.

---

## 5. Scope

**In scope for the hackathon MVP:**

- A chat interface where users type questions in Urdu or English.
- Accurate answers for 15 or more core CNIC and passport questions.
- Coverage of: card and passport types, documents, fees, new application, renewal,
  modification, lost or duplicate, B-Form, FRC, NICOP, POC, tracking, and safety tips.
- Step by step answers for common processes.
- A visible reminder to verify on the official sites.
- A public demo link.

**Stretch scope (if time allows):**

- A live web search grounding tool so answers can reflect current information.
- A dedicated guided wizard for the top processes.
- Voice input and WhatsApp access.

**Out of scope:**

- Real time integration with NADRA or DGIP systems.
- Application submission, payment, or status changes.
- Any collection or storage of personal or sensitive user data.

---

## 6. Functional Requirements

| ID | Requirement | Priority |
| ---- | ------------- | ---------- |
| FR1 | The user can send a text question and receive an answer in a chat interface. | Must |
| FR2 | The bot answers from a curated, verified knowledge base plus general knowledge. | Must |
| FR3 | The bot replies in the same language the user writes in (Urdu or English). | Must |
| FR4 | The bot gives process answers as short, numbered steps. | Must |
| FR5 | The bot adds a reminder to verify on nadra.gov.pk or dgip.gov.pk when giving fees, timelines, or a full process. | Must |
| FR6 | The bot correctly separates NADRA (CNIC) and DGIP (passport) and never confuses the two. | Must |
| FR7 | The bot declines politely and points to official sources when a question is outside scope or uncertain, rather than inventing facts. | Must |
| FR8 | The bot does not ask for sensitive data, and warns the user if they share a CNIC number, passport number, or OTP. | Must |
| FR9 | The bot shows example questions to help users get started. | Should |
| FR10 | The bot streams its reply so the user sees progress. | Should |
| FR11 | The bot can call a live web search to ground answers in current information. Built, but off by default because it needs a billing-linked Google Cloud project. | Could (stretch) |
| FR12 | The chat has category quick-pick chips (CNIC, Passport, Smart Card, NICOP & POC, Fees, Tracking, Safety) that fill the input with a starter question. | Should |
| FR13 | The bot suggests up to three follow-up questions after each answer, as chips the user can click to send. Built from the same reply, so it uses no extra model call. | Should |
| FR14 | An official links and helpline panel lists the NADRA and DGIP sites, the Pak-ID portal, and helpline 1777. | Must |
| FR15 | A fee and timeline quick reference shows CNIC and passport figures, drawn from one fee source so the chatbot and the table always agree. | Should |
| FR16 | A document checklist generator gives a plain text checklist for ten services, with a download option. It only uses verified facts and says "check the official site" where the notes are silent. | Should |
| FR17 | Answers have a copy button, and the layout works on phone widths. | Should |
| FR18 | The interface uses a Pakistan identity colour theme, a clear hero header, and Urdu text that renders right to left. | Should |

---

## 7. Non-Functional Requirements

- **Accuracy:** Answers must reflect the verified knowledge base. Wrong facts are the most
  serious failure for this product.
- **Usability:** Plain, simple language suitable for a wide public audience.
- **Availability:** Reachable through a public link during the demo and judging period.
- **Performance:** A typical answer should begin appearing within a few seconds.
- **Cost:** Runs on free tier services so there is no cost to operate the demo.
- **Maintainability:** The knowledge base is kept in a single file that a non developer can
  edit without touching the application code.
- **Accessibility:** Bilingual support and a clean, uncluttered interface.

---

## 8. User Stories

1. As a citizen, I want to ask in Urdu how to renew my expired CNIC, so that I understand
   the steps without needing an agent.
2. As a first time applicant, I want to know exactly which documents I need, so that I do
   not make a wasted trip to the office.
3. As an overseas Pakistani, I want to know how to apply for a NICOP from abroad, so that
   I can plan the process from my country.
4. As a cautious user, I want the bot to remind me to confirm fees on the official site,
   so that I am not misled by an outdated number.
5. As a privacy conscious user, I want the bot to never ask for my CNIC number, so that I
   feel safe using it.

---

## 9. User Experience and Primary Flow

1. The user opens the public link and sees a short description and example questions.
2. The user types a question in Urdu or English, or taps an example.
3. The bot detects the intent and the language.
4. For a factual question, the bot gives a short, direct answer.
5. For a process question, the bot gives numbered steps.
6. When fees, timelines, or a full process are involved, the bot adds a short reminder to
   verify on the official site.
7. The user can ask follow up questions, and the bot keeps the context of the conversation.

---

## 10. System Architecture and Technology

**Approach:** The product does not use RAG, because no document corpus is provided. Instead,
accuracy comes from a curated knowledge base written into the model system prompt, combined
with the language model's own knowledge, and an optional live web search tool.

**Components:**

- **Chat interface:** Gradio, providing a simple web chat with streaming replies.
- **Language model:** Google Gemini (current free tier Flash model) through the google-genai
  Python SDK.
- **Knowledge base:** a single editable file holding the verified CNIC and passport content.
- **System prompt:** defines behavior, language handling, step by step style, safety rules,
  and injects the knowledge base.
- **Optional grounding:** Gemini built in Google Search grounding for current information
  (stretch feature).

**Hosting and delivery:**

- **Source control:** GitHub (https://github.com/mshafiq92/ShanakhtApp).
- **Deployment:** Render free web service, which gives a free public link
  (https://shanakhtapp.onrender.com). The original plan was Hugging Face Spaces, but
  Gradio Spaces became a paid feature on the free CPU tier in mid 2026, so the app moved
  to Render. Render sleeps the app after 15 minutes without traffic, so the first request
  after a quiet period takes about 30 to 60 seconds. The app should be opened a few minutes
  before a live demo.
- **Secrets:** the API key is stored as a Render environment variable, never in the code
  or the repository. Local development uses a `.env` file that git ignores.
- **Python version:** pinned to 3.12 (`.python-version`), because the newer default on
  the host lacked prebuilt packages and built very slowly.

**Version 2 additions to the architecture:**

- The chat is built from a chatbot, a row of chips, and an input box, so follow-up chips
  can sit directly under each answer.
- The system prompt asks the model to end each reply with a machine readable line of
  follow-up questions. The app removes that line from the visible text, even while
  streaming, and turns it into chips. No second model call is made.
- Fee and timeline figures live in one module (`fees.py`). The knowledge base and the
  quick reference table both read from it.
- The document checklists live in a separate content module (`checklists.py`) and use
  only verified facts. Where the notes are silent, the checklist says to check the
  official site.

---

## 11. Data and Knowledge Base

- The knowledge base is the single source of truth for the bot's facts.
- It is verified by a subject matter expert before use.
- Fees and timelines are treated as the highest risk items, since they change and differ
  across public sources, and must be confirmed against official schedules.
- The content is maintained in plain text so it is easy to review and update.

---

## 12. Safety, Privacy, and Compliance

- **No personal data collection:** the bot does not request or store CNIC numbers, passport
  numbers, OTPs, passwords, or other sensitive data.
- **Fraud awareness:** the bot reminds users that official bodies never ask for OTPs or fees
  to personal accounts, and that agents are not required.
- **Honest positioning:** the bot clearly states that it is a helper, not an official
  authority, and directs users to nadra.gov.pk and dgip.gov.pk.
- **Accuracy guardrails:** the bot avoids inventing facts and defers to official sources
  when uncertain.

---

## 13. Success Metrics

**For the hackathon demo:**

- The bot correctly answers a set of prepared test questions across CNIC and passport.
- The bot answers correctly in both Urdu and English.
- The bot is reachable through a working public link.
- The bot handles at least one full multi step process cleanly during the live demo.

**For a future real deployment:**

- Share of questions answered without the user needing to contact a helpline.
- User satisfaction rating on answer clarity.
- Reduction in repeat questions on the same topic.

---

## 14. Assumptions, Constraints, and Dependencies

**Assumptions:**

- Public information about CNIC and passport processes is sufficient to answer common
  questions.
- A subject matter expert verifies the knowledge base.

**Constraints:**

- No document corpus is provided, so RAG is not used.
- The build and deployment happen within the hackathon time window.
- Free tier rate limits apply to the language model.

**Dependencies:**

- Availability of the Google Gemini free tier and API key.
- Availability of Hugging Face Spaces for hosting.

---

## 15. Risks and Mitigations

| Risk | Impact | Mitigation |
| ------ | -------- | ------------ |
| Outdated or wrong fees and timelines | High | Mark all such items for verification, confirm with the expert, and add a verify reminder. |
| Model gives a confident wrong answer | High | Strong system prompt rules to defer to official sources and avoid inventing facts. |
| Free tier rate limit during demo | Medium | Keep the demo focused, and have backup screenshots ready. |
| Live service failure during judging | Medium | Graceful error message in the app, plus recorded or screenshot backup of the demo. |
| Users share sensitive data | Medium | The bot warns users not to share sensitive numbers. |
| Free daily model quota runs out during the demo | High | A new Google project has a small daily cap (20 requests a day was observed). Check the quota page before a demo, stop testing a few hours before, and use the backup screenshots if needed. |
| Live web search needs a billing account | Medium | The feature is built but off by default. It can be switched on once billing is linked. |
| Free host sleeps when idle | Medium | Open the link a few minutes before the demo. The first load after a quiet period can take about a minute. |
| Model retired or renamed mid project | Medium | Check the model name before every demo. The app shows the exact error from the API, and the model name is a single setting in app.py. |

---

## 16. Release Plan and Milestones

1. **Topic and scope locked.** Complete.
2. **Pitch deck prepared.** Complete.
3. **Knowledge base drafted and verified.** Complete. Fees and timelines were researched
   from official sites and cross checked sources, and kept in one fee module.
4. **Base chatbot built and tested.** Complete.
5. **Optional web search grounding added.** Complete, off by default (needs billing).
6. **Code uploaded to GitHub.** Complete.
7. **Deployed with a public link.** Complete on Render (see section 10). Hugging Face
   Spaces was the original plan but became a paid option for this app.
8. **Demo rehearsed with backup screenshots.** Planned.
9. **Version 2 improvements built and tested.** Complete (see the Version 2 section below).

---

## 16A. Version 2 Changes

Version 2 keeps the same scope and the same free tier design, and adds a visual upgrade
plus features that make the app easier to use:

- **Look and feel:** a Pakistan identity colour theme, a clear hero header with the Urdu
  name, the Inter font with an Urdu script fallback, a footer, and a phone width layout.
- **Quick help:** category chips for common topics, an official links and helpline panel,
  a fee and timeline reference, and a copy button on answers.
- **Follow-up suggestions:** after each answer, up to three follow-up questions appear as
  chips in the same language as the question.
- **Document checklists:** a generator for ten services (New CNIC, CNIC renewal, CNIC
  modification, lost or duplicate CNIC, child B-Form, FRC, new passport, passport renewal,
  child passport, and NICOP), with a plain text download.
- **Unchanged rules:** no database, no stored personal data, no RAG, the same golden
  rules, and the same two department distinction between NADRA and DGIP.

## 17. Future Roadmap

- Full guided wizards for the most common processes.
- Voice input for users who prefer speaking.
- WhatsApp access for the widest public reach.
- Expansion to more government services in a single assistant.

---

## 18. Appendix: Glossary

- **CNIC:** Computerized National Identity Card, issued by NADRA.
- **Smart NIC:** the chip based version of the CNIC.
- **NADRA:** National Database and Registration Authority.
- **DGIP:** Directorate General of Immigration and Passports, which issues the passport.
- **NICOP:** National Identity Card for Overseas Pakistanis.
- **POC:** Pakistan Origin Card.
- **B-Form:** Child Registration Certificate for children under 18.
- **FRC:** Family Registration Certificate.
- **MRP:** Machine Readable Passport.
- **e-passport:** the chip based biometric passport.
-
