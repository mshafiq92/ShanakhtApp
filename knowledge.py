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
  - Fee and timeline numbers live in fees.py. Change them there, not here.
"""

from fees import (
    CNIC_CATEGORIES,
    CNIC_COURIER_FEE,
    PASSPORT_EPASSPORT_FEES,
    PASSPORT_FAST_TRACK_FEES,
    PASSPORT_MRP_FEES,
    PASSPORT_TIMELINES,
    rs,
)

_CNIC_FEE_LINES = "\n".join(
    f"{name} ({info['timeline']}): {rs(info['fee'])}." for name, info in CNIC_CATEGORIES.items()
)
_PASSPORT_TIMELINE_LINES = "\n".join(
    f"{name}: {timeline}" for name, timeline in PASSPORT_TIMELINES.items()
)
_MRP_LINES = "\n".join(
    f"MRP, {years}-year validity: "
    + "; ".join(
        f"{pages} pages {rs(normal)} Normal / {rs(urgent)} Urgent"
        for pages, (normal, urgent) in by_pages.items()
    )
    + "."
    for years, by_pages in PASSPORT_MRP_FEES.items()
)
_FAST_TRACK_LINES = "\n".join(
    f"Fast Track, {years}-year validity: "
    + ", ".join(f"{pages} pages {rs(fee)}" for pages, fee in by_pages.items())
    + "."
    for years, by_pages in PASSPORT_FAST_TRACK_FEES.items()
)
_EPASSPORT_LINES = "\n".join(
    f"e-passport, {years}-year validity: "
    + "; ".join(
        f"{pages} pages {rs(normal)} Normal / {rs(urgent)} Urgent"
        for pages, (normal, urgent) in by_pages.items()
    )
    + "."
    for years, by_pages in PASSPORT_EPASSPORT_FEES.items()
)

KNOWLEDGE = f"""
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
{_CNIC_FEE_LINES}
Courier delivery (if not collected in person from the NADRA Registration Center): {rs(CNIC_COURIER_FEE)}.
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
Three processing categories, with their timelines:
{_PASSPORT_TIMELINE_LINES}
Fast Track is available at Executive Passport Offices in major cities. Courier delivery
time to remote areas is on top of these timelines.

{_MRP_LINES}
{_FAST_TRACK_LINES}
{_EPASSPORT_LINES}
The 100 page e-passport fee is not published in the sources checked, so check dgip.gov.pk
for it. Always verify the exact current figure for your chosen validity and page count on
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
