"""Error handling. DFX answers refusals as states, not exceptions; only transport failures raise.

    OK                       an answer (it can still list coverage limits)
    NO_MATCH / UNKNOWN       resolved but nothing matches / no evidence either way (never a "no")
    NOT_COVERED              DFX does not read that kind of record
    RATE_LIMITED,            the same call will work later: wait retry_after_seconds
    TEMPORARILY_UNAVAILABLE
    API_KEY_INVALID,         the key or the plan; .raw carries how_to_fix or the plans URL
    NOT_IN_PLAN, ENTITLEMENT_REQUIRED
    HTTP_ERROR               any other non-2xx answer; .error has the server's description
"""
import os
import time

from dfx_intel import Client, TransportError

UA = os.environ.get("DFX_EXAMPLE_UA_SUFFIX")
dfx = Client(user_agent_suffix=UA)

RETRYABLE = ("RATE_LIMITED", "TEMPORARILY_UNAVAILABLE")


def ask(client, question, attempts=3):
    for attempt in range(1, attempts + 1):
        try:
            r = client.research(question)
        except TransportError as e:             # DNS, TLS, unreadable body, or no answer within client.timeout
            print(f"  transport failure (attempt {attempt}): {type(e).__name__}")
            time.sleep(2 * attempt)
            continue
        if r.state in RETRYABLE:
            wait = r.retry_after_seconds or 5
            print(f"  {r.state}, retrying in {wait}s")
            time.sleep(min(wait, 60))
            continue
        return r
    return None


def report(label, r):
    if r is None:
        print(f"{label}: gave up after retries")
    elif r.state == "OK":
        print(f"{label}: OK ({r.answer_state}), {len(r.claims)} claims")
        for limit in r.coverage_limits:
            print(f"  {limit.get('kind')}: {limit.get('about')}: {limit.get('why')}")
    elif r.state in ("NO_MATCH", "UNKNOWN", "NOT_COVERED"):
        print(f"{label}: {r.state} (an answer, not an error): {r.answer or r.error}")
    else:
        print(f"{label}: {r.state}: {r.error}")


# 1. A question outside coverage: a state, not an exception.
report("NAV per share", ask(dfx, "What is the net asset value per share of Ares Capital Corp?"))

# 2. The member door with no credentials: the server answers 401, the SDK returns HTTP_ERROR with its description.
member = Client(mcp_path="/mcp/core/member", channel=None, api_key="", user_agent_suffix=UA)
report("member door, no key", member.research("Which BDCs lend to Kaseya?"))

# 3. A call the SDK refuses before sending anything.
try:
    dfx.research("")
except ValueError as e:
    print("empty question:", e)

# 4. A timeout too short to answer in: TransportError, which ask() retries and then gives up on.
impatient = Client(timeout=0.001, user_agent_suffix=UA)
report("timeout", ask(impatient, "Which BDCs lend to Kaseya?", attempts=2))
