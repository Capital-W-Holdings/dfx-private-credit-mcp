"""Pagination: a long answer comes in pages. Pass `continuation` back, unchanged, for the next one.

Each page carries whole claims (a claim travels with its row). Anonymous callers have a rate budget of about 60 calls an
hour, so cap the walk. Without a plan, rows past the first few are counted, not named: `withheld` says so.
"""
import os

from dfx_intel import Client

dfx = Client(user_agent_suffix=os.environ.get("DFX_EXAMPLE_UA_SUFFIX"))
MAX_PAGES = 3

r = dfx.research("Which BDCs lend to Auctane, and which of them are current lenders?")
print("page 1:", r.state, "| rows total:", r.page.get("rows_total"), "| pages:", r.page.get("pages"))
lenders = []
pages = 0
while r is not None and r.state == "OK":
    pages += 1
    for row in r.raw.get("relationships") or []:
        if row.get("rel_type_canonical") != "LENDER_TO":     # sponsor and ownership rows ride along; skip them
            continue
        name = (row.get("subject") or {}).get("name")
        if name and name not in lenders:
            lenders.append(name)
    if pages >= MAX_PAGES or not r.has_more:
        break
    r = dfx.continue_research(r)          # same as dfx.research(continuation=r.continuation)
    print(f"page {r.page.get('index')}: {r.state}, rows on page {r.page.get('rows_on_page')}")

print(f"\nread {pages} page(s), {len(lenders)} named lender(s):")
for name in lenders:
    print(" ", name)
if r is not None and r.has_more:
    print(f"stopped at the cap; {r.page.get('rows_after_this_page')} rows remain behind the continuation")
