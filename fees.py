# -*- coding: utf-8 -*-
"""
Fee and timeline figures for CNIC and passport.

knowledge.py and the quick reference table in app.py both read from this file, so each
number is changed in one place. Figures come from dgip.gov.pk (passport) and cross
checked public sources (NADRA's own site blocks automated reads). Re-verify before
relying on them, since government fees change.
"""


def rs(amount):
    return f"Rs {amount:,}"


CNIC_CATEGORIES = {
    "Normal": {"fee": 750, "timeline": "about 30 days"},
    "Urgent": {"fee": 1500, "timeline": "about 12 days"},
    "Executive": {"fee": 2500, "timeline": "about 7 days"},
}
CNIC_COURIER_FEE = 165

PASSPORT_TIMELINES = {
    "Normal": "about 21 working days",
    "Urgent": "about 5 working days",
    "Fast Track": "about 2 working days",
}

# Machine Readable Passport: (Normal fee, Urgent fee) by validity in years, then pages.
PASSPORT_MRP_FEES = {
    5: {36: (4500, 7500), 72: (8200, 13500), 100: (9000, 18000)},
    10: {36: (6700, 11200), 72: (12400, 20200), 100: (13500, 27000)},
}

# Fast Track MRP fee by validity in years, then pages.
PASSPORT_FAST_TRACK_FEES = {
    5: {36: 12500, 72: 18500, 100: 23000},
    10: {36: 16200, 72: 25200, 100: 32000},
}

# e-passport (Normal fee, Urgent fee) by validity in years, then pages.
# 100 pages is not published in the sources checked, so it is left out on purpose.
PASSPORT_EPASSPORT_FEES = {
    5: {36: (9000, 15000), 72: (16500, 27000)},
    10: {36: (13500, 22500), 72: (24750, 40500)},
}
