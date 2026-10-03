# -*- coding: utf-8 -*-
"""
Document checklists for the checklist generator in app.py.

Only facts from knowledge.py and fees.py are used here. Where the verified notes do not
list the documents, fee, or timeline for a service, the checklist says to check the
official site instead of guessing.
"""

from fees import CNIC_CATEGORIES, CNIC_COURIER_FEE, PASSPORT_MRP_FEES, PASSPORT_TIMELINES, rs

CHECK_OFFICIAL = "Not in our verified notes. Check the official site before you apply."

CNIC_FEE_TEXT = "; ".join(
    f"{name} {rs(info['fee'])} ({info['timeline']})" for name, info in CNIC_CATEGORIES.items()
)
PASSPORT_TIMELINE_TEXT = "; ".join(f"{name} {timeline}" for name, timeline in PASSPORT_TIMELINES.items())
MRP_FEE_TEXT = "; ".join(
    f"{years}-year, {pages} pages: {rs(normal)} Normal / {rs(urgent)} Urgent"
    for years, by_pages in PASSPORT_MRP_FEES.items()
    for pages, (normal, urgent) in by_pages.items()
)

NADRA = "nadra.gov.pk"
DGIP = "dgip.gov.pk"

SERVICES = {
    "New CNIC": {
        "agency": NADRA,
        "where": "NADRA Registration Center (NRC), or online through the Pak Identity portal or PakID app.",
        "documents": [
            "Biometrics: fingerprints and photo",
            "B-Form (usually)",
            "Parents' CNIC numbers",
            "Proof of address",
        ],
        "fees": f"First-ever CNIC is free under Normal processing. Other categories: {CNIC_FEE_TEXT}. "
        f"Courier delivery: {rs(CNIC_COURIER_FEE)}.",
        "timeline": "Processing starts only after the fee payment is confirmed.",
        "notes": [],
    },
    "CNIC renewal": {
        "agency": NADRA,
        "where": "PakID app or an NRC.",
        "documents": [
            "Your existing card details, confirmed or updated",
            "Biometrics, if NADRA asks for them",
        ],
        "fees": f"{CNIC_FEE_TEXT}. Courier delivery: {rs(CNIC_COURIER_FEE)}.",
        "timeline": "Processing starts only after the fee payment is confirmed.",
        "notes": ["Renew when the card has expired, ideally within 6 months before expiry."],
    },
    "CNIC modification": {
        "agency": NADRA,
        "where": CHECK_OFFICIAL,
        "documents": [CHECK_OFFICIAL],
        "fees": f"{CNIC_FEE_TEXT}. If NADRA made the mistake, the correction should be free and at the fastest tier.",
        "timeline": "Processing starts only after the fee payment is confirmed.",
        "notes": ["A new card is issued after the correction.", "Supporting documents depend on what you are correcting."],
    },
    "Lost or duplicate CNIC": {
        "agency": NADRA,
        "where": "NRC, or online.",
        "documents": [CHECK_OFFICIAL],
        "fees": f"{CNIC_FEE_TEXT}. Courier delivery: {rs(CNIC_COURIER_FEE)}.",
        "timeline": "Processing starts only after the fee payment is confirmed.",
        "notes": ["Report a lost card quickly."],
    },
    "Child B-Form": {
        "agency": NADRA,
        "where": "NRC.",
        "documents": ["Child's birth certificate", "Both parents' CNICs"],
        "fees": CHECK_OFFICIAL,
        "timeline": CHECK_OFFICIAL,
        "notes": ["A B-Form is the record for children under 18."],
    },
    "FRC (Family Registration Certificate)": {
        "agency": NADRA,
        "where": CHECK_OFFICIAL,
        "documents": [CHECK_OFFICIAL],
        "fees": "Rs 1,000 for a single family category, or Rs 2,000 for \"by all\" (combined categories).",
        "timeline": "Usually issued within about 1 working day once family records are verified.",
        "notes": ["Often needed for visas and foreign immigration."],
    },
    "New passport": {
        "agency": DGIP,
        "where": "DGIP e-passport portal, or a passport office.",
        "documents": [
            "Valid CNIC or NICOP",
            "Biometrics and photo, if required",
            "Old passport, if renewing",
        ],
        "fees": f"Depends on validity and page count. {MRP_FEE_TEXT}. Fast Track and e-passport fees "
        "are listed on dgip.gov.pk.",
        "timeline": PASSPORT_TIMELINE_TEXT + ".",
        "notes": ["Fill in the application, pay the fee, then give biometrics and photo if required."],
    },
    "Passport renewal": {
        "agency": DGIP,
        "where": "DGIP e-passport portal, or a passport office.",
        "documents": ["Valid CNIC or NICOP", "Your old passport"],
        "fees": f"Depends on validity and page count. {MRP_FEE_TEXT}.",
        "timeline": PASSPORT_TIMELINE_TEXT + ".",
        "notes": [],
    },
    "Child passport": {
        "agency": DGIP,
        "where": "DGIP e-passport portal, or a passport office.",
        "documents": ["Child's B-Form", "Parents' documents"],
        "fees": f"Depends on validity and page count. {MRP_FEE_TEXT}. Confirm the child fee on dgip.gov.pk.",
        "timeline": PASSPORT_TIMELINE_TEXT + ".",
        "notes": [],
    },
    "NICOP": {
        "agency": NADRA,
        "where": "Pak Identity portal or PakID app online, or a Pakistani embassy or consulate abroad.",
        "documents": [CHECK_OFFICIAL],
        "fees": CHECK_OFFICIAL,
        "timeline": CHECK_OFFICIAL,
        "notes": ["NICOP is for Pakistanis living, working, or studying abroad, and for dual nationals."],
    },
}

SERVICE_NAMES = list(SERVICES)


def build_checklist(service):
    info = SERVICES[service]
    lines = [
        f"SHANAKHT CHECKLIST: {service}",
        "",
        "WHERE TO APPLY",
        info["where"],
        "",
        "DOCUMENTS TO BRING",
    ]
    lines += [f"[ ] {doc}" for doc in info["documents"]]
    lines += ["", "FEES", info["fees"], "", "TIMELINE", info["timeline"]]
    if info["notes"]:
        lines += ["", "NOTES"] + [f"- {note}" for note in info["notes"]]
    lines += [
        "",
        f"Verify the current fees and documents on {info['agency']} before you go.",
        "Tip: paste any line into the chat to ask about it in Urdu.",
    ]
    return "\n".join(lines) + "\n"
