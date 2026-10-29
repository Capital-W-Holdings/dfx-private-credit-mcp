"""What changed for a borrower since the prior quarter: the second session, one call, no key.

    pip install dfx-intel
    python 07_what_changed.py [dfx_id] [since]

The SDK wraps research, verify and resolve; every other tool is one `call_tool` away. The changes feed,
search_private_credit_changes, is listed on the full profile (/mcp), not on /mcp/core (the SDK's default), so this
client points at /mcp. The borrower id is the one example 01 resolved (Hyland Software); `since` defaults to the
quarter end before the newest one BDCs have filed.

BDCs file a quarter's 10-Q about 40 to 45 days after it ends. Run this yourself after each filing season (a cron
job, a scheduled agent task). DFX keeps no list of your borrowers, runs no loop for you and sends nothing.
"""
import datetime as dt
import os
import sys

from dfx_intel import Client

# DFX_EXAMPLE_UA_SUFFIX is only for DFX's own test runs, so they can be excluded from usage counts. Leave it unset.
dfx = Client(mcp_path="/mcp", user_agent_suffix=os.environ.get("DFX_EXAMPLE_UA_SUFFIX"))

HYLAND = "dfx:pc:fa47c51b-e087-6631-d0cd-ae3158ba0421"     # from 01_research_anonymous: identities.subject.dfx_id
FILING_LAG_DAYS = 45


def quarter_end_before(day: dt.date) -> dt.date:
    """The last calendar quarter end strictly before `day`."""
    q_month = ((day.month - 1) // 3) * 3                    # 0, 3, 6 or 9
    if q_month == 0:
        return dt.date(day.year - 1, 12, 31)
    return dt.date(day.year, q_month + 1, 1) - dt.timedelta(days=1)


def prior_quarter_end(today: dt.date) -> str:
    """The quarter end before the newest one whose filings are due by now (today minus the filing lag)."""
    newest_filed = quarter_end_before(today - dt.timedelta(days=FILING_LAG_DAYS) + dt.timedelta(days=1))
    return quarter_end_before(newest_filed).isoformat()


dfx_id = sys.argv[1] if len(sys.argv) > 1 else HYLAND
since = sys.argv[2] if len(sys.argv) > 2 else prior_quarter_end(dt.datetime.now(dt.timezone.utc).date())

payload, meta, fallback = dfx.call_tool("search_private_credit_changes",
                                        {"dfx_id": dfx_id, "since": since, "by": "effective"})
p = payload or {}
state = p.get("state") or fallback
print(f"changes on {dfx_id} effective on or after {since}")
print("state:", state, "| on this page:", p.get("count"), "| named here:", len(p.get("results") or []),
      "| in all:", p.get("total"))
if state not in ("OK", "NO_MATCH"):
    print("not an answer:", p.get("error") or p.get("message"), "| retry after:", (p.get("retry") or {}).get("after_seconds"))
    sys.exit(0)
if state == "NO_MATCH":
    print("no change on a BDC schedule since then (no filing read, or nothing moved); not proof that nothing happened")

for row in p.get("results") or []:
    who = (row.get("subject") or {}).get("name")
    rel = ", ".join(r["name"] for r in row.get("related") or [] if r.get("name") not in (None, "LOCKED"))
    move = ""
    if row.get("prior_value") is not None or row.get("new_value") is not None:
        move = f" | {row.get('prior_value')} -> {row.get('new_value')} {row.get('amount_unit') or ''}".rstrip()
    elif row.get("amount") is not None:
        move = f" | {row.get('amount')} {row.get('amount_unit') or ''}".rstrip()
    url = (row.get("cite") or {}).get("url") or (row.get("source") or {}).get("url")
    print(f"\n{str(row.get('effective_at'))[:10]}  {row.get('event_type')}  {who}" + (f" / {rel}" if rel else "") + move)
    if row.get("headline"):
        print("   ", row["headline"])
    print("    source:", url or "(none on this row)")

locked = p.get("locked") or {}
if locked.get("count"):
    print(f"\n{locked['count']} more change(s) counted, not named, without a plan: {locked.get('by_type') or ''}")
if p.get("note"):
    print("\nnote:", p["note"])
print("\nAn effective date is the quarter end where the change is visible. A lender exit is dated at the last quarter "
      "the lender held the piece. BDC schedules are not every lender: banks, CLOs and private funds file none.")
