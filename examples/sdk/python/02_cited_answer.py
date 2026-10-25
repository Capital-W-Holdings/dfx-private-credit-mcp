"""Print every claim with the document it comes from.

A claim names a row (`claim.row`, for example "r1"). The row carries the subject, the object, the amounts, the date and
`cite.url`, the primary document. Join them yourself: the SDK keeps the server payload unchanged under `.raw`.
"""
import os

from dfx_intel import Client

dfx = Client(user_agent_suffix=os.environ.get("DFX_EXAMPLE_UA_SUFFIX"))


def rows_by_id(raw):
    """Every row in a research payload that a claim can point at, keyed by its id."""
    out = {}
    for key in ("relationships", "facts", "events", "identities"):
        rows = raw.get(key)
        for row in rows if isinstance(rows, list) else []:
            if isinstance(row, dict) and row.get("id"):
                out[row["id"]] = row
    return out


def money(v):
    return f"${v / 1e6:,.1f}M" if isinstance(v, (int, float)) else "n/a"


r = dfx.research("Which BDCs hold the loans of Hyland Software and when do they mature?")
print(r.state, "|", r.answer, "\n")
rows = rows_by_id(r.raw)
for c in r.claims:
    row = rows.get(c.row, {})
    cite = row.get("cite") or {}
    who = (row.get("subject") or {}).get("name")
    what = (row.get("object") or {}).get("name")
    print(f"[{c.claim_type}] {c.predicate}: {who} -> {what}")
    if c.predicate == "LENDER_TO_AMOUNT_USD":
        print(f"    fair value {money(row.get('amount_usd'))}, principal {money(row.get('principal_usd'))},"
              f" as of {row.get('as_of')}")
        if row.get("tranches"):
            print(f"    tranches: {row['tranches']}")
    print(f"    source: {cite.get('url') or 'uncited'} ({cite.get('granularity')})")

check = r.raw.get("citation_check") or {}
print("\ncitation check:", check.get("verdict"), "| cited rows", check.get("cited_rows"), "of", check.get("rows"))
for line in r.raw.get("do_not_conclude") or []:
    print("do not conclude:", line)
