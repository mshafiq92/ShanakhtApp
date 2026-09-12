# -*- coding: utf-8 -*-
"""
Shanakht knowledge base.

verified CNIC and passport FAQ text between the triple quotes below.

Rules for good content:
  - Every fee and timeline below is sourced from nadra.gov.pk / dgip.gov.pk or, where the
    official site could not be scraped directly, cross-checked across multiple independent
    public sources. Re-verify before a real deployment, since these figures change.
  - Keep it plain and simple. The model will translate to Urdu automatically.
  - The more accurate and complete this text is, the better the bot answers.
"""

KNOWLEDGE = """
=== CNIC (issued by NADRA) ===

WHAT IS A CNIC
The Computerized National Identity Card is the main proof of identity for Pakistani
citizens. Needed for a bank account, passport, SIM, voting, and government services.
NADRA now issues the chip-based Smart National Identity Card (SNIC).

ELIGIBILITY AND VALIDITY
Every Pakistani citizen aged 18 or above is eligible. Under 18, a child is on a B-Form.
A CNIC is normally valid for 10 years, then must be renewed. Some cards (for example
senior citizens) may be lifetime.

NEW CNIC
Apply at a NADRA Registration Center (NRC) or online via the Pak Identity portal / PakID
app. Give biometrics (fingerprints, photo) and required documents (usually B-Form,
parents' CNIC numbers, proof of address). Card is couriered or collected.

CNIC RENEWAL
Renew when the card has expired, ideally within 6 months before expiry. Use the PakID app
or an NRC. Confirm or update your details, give biometrics if required, pay, receive the
new card.

CNIC MODIFICATION AND CORRECTIONS
To correct name, date of birth, or address, apply for a modification with supporting
documents. A new card is issued. If the error was NADRA's own mistake (card does not match
your form), the correction should be free and at the fastest tier.

LOST OR DAMAGED CNIC
Apply for a duplicate at an NRC or online. Report a lost card quickly.

FEES AND TIMELINES (CNIC)
A first-ever CNIC for a new applicant is free of cost under Normal processing.
For a new Smart NIC, renewal, duplicate, or modification, three categories apply:
Normal (about 30 days): Rs 750.
Urgent (about 12 days): Rs 1,500.
Executive (about 7 days): Rs 2,500.
Courier delivery (if not collected in person from the NADRA Registration Center): Rs 165.
Processing time starts only after fee payment is confirmed. Always verify the current
figures on nadra.gov.pk before paying, since fees can change.

=== CHILD AND FAMILY DOCUMENTS ===

B-FORM (Child Registration Certificate)
Official record for children under 18. Needed for school, family records, and a child's
passport. Apply at an NRC with the child's birth certificate and both parents' CNICs.

FRC (Family Registration Certificate)
Shows your family composition (by birth or marriage). Often needed for visas and foreign
immigration. Fee: Rs 1,000 for a single family category, or Rs 2,000 for "by all" (a
combined certificate covering more than one category). Usually issued within about 1
working day once family records are verified, so there is no separate urgent fee.

=== OVERSEAS PAKISTANIS ===

NICOP
National Identity Card for Overseas Pakistanis, for Pakistanis living/working/studying
abroad and dual nationals. Works as identity proof and allows visa-free entry to Pakistan.

POC (Pakistan Origin Card)
For foreign nationals of Pakistani origin. Allows visa-free entry and certain rights.

APPLYING FROM ABROAD
Apply online via the Pak Identity portal / PakID app, or at a Pakistani embassy/consulate.

=== PASSPORT (issued by DGIP, using NADRA records) ===

WHO ISSUES IT
The Directorate General of Immigration and Passports (DGIP), Ministry of Interior. Any
citizen with a valid CNIC or NICOP is eligible.

TYPES
Ordinary (green) passport for citizens, plus official and diplomatic for certain officials.
Available as Machine Readable Passport (MRP) and the newer chip-based e-passport, in
5-year and 10-year validity, and 36, 72, or 100 pages.

APPLY OR RENEW
Apply online via the DGIP e-passport portal, or at a passport office. Steps: fill the
application, pay the fee, give biometrics and photo (if required), then collect or receive.
Need a valid CNIC/NICOP and your old passport if renewing.

CHILD PASSPORT
Uses the child's B-Form and parents' documents.

FEES AND TIMELINES (PASSPORT)
Three processing categories: Normal (about 21 working days), Urgent (about 5 working
days), and Fast Track (about 2 working days, available at Executive Passport Offices in
major cities). Courier delivery time to remote areas is on top of these timelines.

Machine Readable Passport (MRP), 5-year validity: 36 pages Rs 4,500 Normal / Rs 7,500
Urgent; 72 pages Rs 8,200 Normal / Rs 13,500 Urgent; 100 pages Rs 9,000 Normal / Rs 18,000
Urgent.
MRP, 10-year validity: 36 pages Rs 6,700 Normal / Rs 11,200 Urgent; 72 pages Rs 12,400
Normal / Rs 20,200 Urgent; 100 pages Rs 13,500 Normal / Rs 27,000 Urgent.
Fast Track fee (by page count): roughly Rs 12,500 to Rs 23,000 for 5-year validity, and
Rs 16,200 to Rs 32,000 for 10-year validity.
e-passport fee (by page count): roughly Rs 9,000 to Rs 16,500 for 5-year validity, and
Rs 13,500 to Rs 24,750 for 10-year validity.
Always verify the exact current figure for your chosen validity and page count on
dgip.gov.pk before paying, since fees can change.

=== COMMON QUESTIONS ===

TRACKING
CNIC: track at id.nadra.gov.pk or the PakID app with your tracking ID.
Passport: use the DGIP tracking service.

PAYMENT
Pay online (for example Raast / bank transfer in the app) or at designated banks.

NO AGENTS NEEDED
All of this can be done directly with NADRA or DGIP. Agents and touts often overcharge.
Pay only through official channels.

OFFICIAL SITES AND HELPLINE
CNIC/identity: nadra.gov.pk (helpline commonly cited as 1777). Passport: dgip.gov.pk.

=== SAFETY TIPS ===

CNIC SAFETY
- Write the purpose and date on any photocopy, for example "for bank account only, [date]".
- Never post your CNIC number or photo on social media or send it to unknown people.
- Check how many SIMs are registered on your CNIC and block unknown ones. Use PTA's
  official channels: the web portal at cnic.sims.pk, an SMS of your 13-digit CNIC number
  (no dashes) to 668, or dialing *668# from your phone. A maximum of 8 SIMs is allowed per
  CNIC.
- Report a lost card quickly and apply for a duplicate.
- NADRA, DGIP, and banks never ask for your OTP or PIN, or a fee to a personal account.
  Never share an OTP.
- Apply only on official sites, not third-party agent websites.

PASSPORT SAFETY
- Keep the original safe. It remains government property.
- Never give your passport to an agent or employer as security or collateral.
- Check the expiry early. Many countries require 6 months validity to enter.
- Report a lost or stolen passport to DGIP and police at once. If abroad, contact the
  nearest Pakistani embassy or consulate.
- Keep copies separate from the original when travelling.
- Do not bend, cut, or heat the card or e-passport, as this damages the chip.
"""
