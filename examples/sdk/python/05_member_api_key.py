"""Member access with an account key, read from the environment.

Create a key at https://dfxintel.com/data-factory/account and export it:

    export DFX_API_KEY=dfx_live_...

The SDK sends it as `Authorization: Bearer <key>`. Keyed requests are never channel-tagged. Never put a key in source
code or a config file you commit. This script stops, loudly, when the key is missing.
"""
import os
import sys

from dfx_intel import Client

key = os.environ.get("DFX_API_KEY", "").strip()
if not key:
    sys.exit("DFX_API_KEY is not set. Create a key at https://dfxintel.com/data-factory/account, export it, "
             "and run again. (Anonymous use needs no key: see 01_research_anonymous.py.)")
if not key.startswith("dfx_live_"):
    sys.exit("DFX_API_KEY does not look like a DFX account key (expected dfx_live_...).")

dfx = Client()                       # picks DFX_API_KEY up from the environment
r = dfx.research("Which BDCs hold the loans of Hyland Software and when do they mature?")
if r.state in ("API_KEY_INVALID", "NOT_IN_PLAN", "ENTITLEMENT_REQUIRED"):
    sys.exit(f"{r.state}: {r.raw.get('how_to_fix') or r.error}")
print(r.state, "| access:", (r.withheld or {}).get("access"), "| plan:", (r.withheld or {}).get("plan"))
print(r.answer)
