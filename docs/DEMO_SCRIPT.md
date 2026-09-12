# Shanakht: Live Demo Script

A tight 3 to 5 minute script for the hackathon demo. No new features, just a good order
to show what already works.

## Before you start

- Open https://shanakhtapp.onrender.com yourself, about 5 minutes before you go on
  stage. The free hosting sleeps when nobody visits it, and the first visit after that
  can take up to a minute to wake up. Opening it early means it is already warm when
  the judges see it.
- Have the backup screenshots ready (list at the bottom) in case the live service has
  a problem during judging.
- Note: the live web search feature is off by default in this deployment, because
  Google now requires a billing linked account to use it. If you have not linked
  billing, skip the web search part of the script below and go straight from the
  process demo to the impact statement.

---

## Spoken script

**1. Problem (about 45 seconds)**

"Getting a CNIC or a passport in Pakistan is simple on paper, but confusing in real
life. People are not sure which document type they need, what papers to bring, or
what the real fee is. This information exists, but it is spread across different
websites, mostly in English, and hard to piece together fast. So people end up asking
agents who charge extra, or they stand in long lines just to ask a simple question."

**2. Solution (about 30 seconds)**

"We built Shanakht, which means recognition or identity in Urdu. It is a free chatbot
that answers CNIC and passport questions in plain Urdu or English, gives step by step
guidance, and always tells you to double check on the official NADRA or DGIP site. It
is a helper, not a replacement for the government service."

**3. Live demo (about 2 minutes)**

Type these one at a time, in this order:

1. `How do I renew my expired CNIC?`
   Shows a clear, numbered answer in English, with the verify reminder at the end.

2. `میرا شناختی کارڈ گم ہو گیا ہے، میں کیا کروں؟`
   Same question style, but now in Urdu, and the bot replies fully in Urdu. This
   shows the bilingual support without switching any setting.

3. `Urgent passport ki fee kitni hai?`
   Roman Urdu question, shows the bot understands mixed script, and gives an actual
   fee figure with the reminder to confirm on dgip.gov.pk.

4. (Only if web search is enabled) `What is the current NADRA CNIC fee?`
   Shows the model using live web search and listing its sources, so answers can
   stay current even if a fee changes after this hackathon.

**4. Impact (about 30 to 45 seconds)**

"This maps directly to UN Sustainable Development Goal 16, target 16.9, which is
about legal identity for all. Shanakht cuts the time and confusion for something
every citizen eventually has to do, reduces reliance on agents who overcharge, and
does it in the language people are actually comfortable in. It runs on free tools
end to end, so there is no cost barrier to keep it running."

**5. Close (about 15 seconds)**

"That is Shanakht. Thank you."

---

## Backup screenshots to capture now

Take these before the demo, in case the live link has a problem:

1. The empty chat screen, showing the title, the logo, and the example questions.
2. The answer to `How do I renew my expired CNIC?` in English.
3. The answer to `میرا شناختی کارڈ گم ہو گیا ہے، میں کیا کروں؟` in Urdu, showing the
   right to left text rendering.
4. The answer to `Urgent passport ki fee kitni hai?` with the fee and the verify
   reminder.
5. (If enabled) An answer that shows the Sources list from web search grounding.

Save these somewhere you can pull up fast, like a phone photo album or a slide at the
end of the pitch deck marked "backup".
