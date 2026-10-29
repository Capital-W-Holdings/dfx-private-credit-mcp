"""Check an MCP client config before you paste it: open its DFX server with the official MCP Python SDK, list the
tools and ask one question. No key, no model.

    pip install "mcp>=2"
    python check_config.py cursor.mcp.json        # or vscode.mcp.json, windsurf.mcp_config.json,
                                                  # claude_desktop_config.json (reads the URL handed to mcp-remote)
"""
import asyncio
import json
import os
import sys

import httpx2
from mcp import Client
from mcp.client.streamable_http import streamable_http_client

QUESTION = "When do the BDC-held loans to Kona Buyer, LLC mature?"


def server_url(cfg: dict) -> str:
    """The DFX URL from any of the four shapes: mcpServers.url (Cursor), servers.url (VS Code), mcpServers.serverUrl
    (Windsurf) or an https argument to a stdio bridge (Claude Desktop with mcp-remote)."""
    entry = (cfg.get("mcpServers") or cfg.get("servers") or {})["dfx"]
    url = entry.get("url") or entry.get("serverUrl") or next(
        (a for a in entry.get("args") or [] if a.startswith("https://")), None)
    if not url:
        raise SystemExit("no URL found under dfx")
    return url


async def main(path: str) -> None:
    url = server_url(json.load(open(path)))
    print("config:", os.path.basename(path), "| url:", url)
    # DFX_EXAMPLE_UA_SUFFIX is only for DFX's own test runs, so they can be excluded from usage counts. Leave it unset.
    ua = os.environ.get("DFX_EXAMPLE_UA_SUFFIX")
    http = httpx2.AsyncClient(headers={"User-Agent": ua} if ua else None, timeout=httpx2.Timeout(30, read=300))
    async with Client(streamable_http_client(url, http_client=http)) as client:
        names = [t.name for t in (await client.list_tools()).tools]
        print(f"tools/list: {len(names)} tools, first {names[:4]}")
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


asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else "cursor.mcp.json"))
