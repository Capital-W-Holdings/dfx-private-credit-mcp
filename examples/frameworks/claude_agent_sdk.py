"""Claude Agent SDK: DFX is a remote MCP server, so the integration is two option fields.

    pip install dfx-intel claude-agent-sdk "mcp>=2"
    python claude_agent_sdk.py            # checks the server config with a plain MCP client: no model, no key
    python claude_agent_sdk.py --agent    # runs the agent (needs Claude Code credentials, e.g. ANTHROPIC_API_KEY)

`mcp_servers()` builds {"dfx": {"type": "http", "url": ".../mcp/core?c=..."}}; with DFX_API_KEY set it adds the Bearer
header and drops the tag. `allowed_tools()` pre-approves mcp__dfx__research, mcp__dfx__verify and
mcp__dfx__resolve_name so the agent does not stop to ask. The recorded run (claude_agent_sdk.out.txt) is the check
without --agent: the same URL the agent would get, opened with the official MCP Python SDK, tools listed, and one
`research` call.
"""
import asyncio
import json
import os
import sys

from dfx_intel.adapters.claude_agent_sdk import allowed_tools, mcp_servers

QUESTION = "Which BDCs hold the loans of Hyland Software, and what are they marked at?"
SYSTEM = ("You answer private markets questions with the dfx research tool. Cite the evidence URLs. NOT_COVERED and "
          "NO_MATCH are answers: say what is not covered instead of concluding no.")

servers = mcp_servers(channel="ex-claude-agent")
# DFX_EXAMPLE_UA_SUFFIX is only for DFX's own test runs, so they can be excluded from usage counts. Leave it unset.
UA = os.environ.get("DFX_EXAMPLE_UA_SUFFIX")
if UA:
    servers["dfx"].setdefault("headers", {})["User-Agent"] = UA
print("mcp_servers:", json.dumps({k: {f: v[f] for f in ("type", "url")} for k, v in servers.items()}))
print("allowed_tools:", allowed_tools())


async def run_agent() -> None:
    from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, ResultMessage, TextBlock, query

    options = ClaudeAgentOptions(mcp_servers=servers, allowed_tools=allowed_tools(), system_prompt=SYSTEM)
    async for msg in query(prompt=QUESTION, options=options):
        if isinstance(msg, AssistantMessage):
            for block in msg.content:
                if isinstance(block, TextBlock):
                    print(block.text)
        elif isinstance(msg, ResultMessage):
            print("\nturns:", msg.num_turns, "| cost usd:", msg.total_cost_usd)


async def check_config() -> None:
    """Open the configured server with the official MCP SDK, the way the agent's MCP client will."""
    import httpx2
    from mcp import Client
    from mcp.client.streamable_http import streamable_http_client

    cfg = servers["dfx"]
    http = httpx2.AsyncClient(headers=cfg.get("headers"), timeout=httpx2.Timeout(30, read=300))
    async with Client(streamable_http_client(cfg["url"], http_client=http)) as client:
        names = [t.name for t in (await client.list_tools()).tools]
        allowed = [t.split("__")[-1] for t in allowed_tools()]
        print(f"\ntools/list: {len(names)} tools, first {names[:3]}; every allowed tool listed: "
              f"{all(a in names for a in allowed)}")
        res = await client.call_tool("research", {"question": QUESTION})
        r = json.loads(next(c.text for c in res.content if c.type == "text"))
        print("research state:", r.get("state"), "| answer_state:", r.get("answer_state"))
        answer = r.get("answer")
        print("answer:", answer.get("text") if isinstance(answer, dict) else answer)
        rows = [x for k in ("relationships", "facts", "events") for x in r.get(k) or [] if isinstance(x, dict)]
        urls = sorted({(row.get("cite") or {}).get("url") for row in rows} - {None})
        print(f"claims: {len(r.get('claims') or [])} | source documents: {len(urls)}")
        for u in urls[:3]:
            print("   ", u)


asyncio.run(run_agent() if "--agent" in sys.argv else check_config())
