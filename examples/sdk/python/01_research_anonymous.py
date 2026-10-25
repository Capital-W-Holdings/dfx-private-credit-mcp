"""Anonymous research: one question, one call, no key, no sign-up.

    pip install dfx-intel
    python 01_research_anonymous.py
"""
import os

from dfx_intel import Client

# DFX_EXAMPLE_UA_SUFFIX is only for DFX's own test runs, so they can be excluded from usage counts. Leave it unset.
dfx = Client(user_agent_suffix=os.environ.get("DFX_EXAMPLE_UA_SUFFIX"))

r = dfx.research("Which BDCs hold the loans of Hyland Software and when do they mature?")
print("state:", r.state, "| answer_state:", r.answer_state)
print("answer:", r.answer)
print("claims on this page:", len(r.claims), "| source documents:", len(r.evidence_urls))
print("more pages:", r.has_more, "| access:", (r.withheld or {}).get("access"))
