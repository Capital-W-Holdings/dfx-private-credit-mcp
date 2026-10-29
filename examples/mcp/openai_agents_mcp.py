"""OpenAI Agents SDK: DFX as a remote MCP server (MCPServerStreamableHttp) attached to an Agent.

    pip install "openai-agents==0.24.0"
    python openai_agents_mcp.py                 # runs as is: no DFX key, no model key
    OPENAI_API_KEY=... python openai_agents_mcp.py   # optional: let the model drive

The Agent gets every DFX core tool through `mcp_servers=[dfx]`. With OPENAI_API_KEY set, `Runner.run` runs the agent
and the model decides when to call `research`. Without it, the script calls `research` on the same MCP server
connection the agent uses, so you see exactly what the model would receive. The recorded run is the one without a key.
"""
import asyncio
import json
import os

from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp

URL = "https://exchange-production-9123.up.railway.app/mcp/core?c=ex-openai-agents"
QUESTION = "Which BDCs lend to Acquia, and what are the positions marked at?"

# DFX_EXAMPLE_UA is only for DFX's own test runs, so they can be excluded from usage counts. Leave it unset.
HEADERS = {"User-Agent": os.environ["DFX_EXAMPLE_UA"]} if os.environ.get("DFX_EXAMPLE_UA") else {}


def show(answer: dict) -> None:
    print("state:", answer["state"])
    print("answer:", answer["answer"]["text"])
    for row in answer.get("relationships", []):
        print(f"  {row['subject']['name']} | fair value ${row.get('amount_usd') or 0:,.0f}"
              f" | marked {row.get('mark_pct')}% | as of {row.get('as_of')} | {row['cite']['url']}")
    page = answer.get("page") or {}
    print(f"page {page.get('index')} of {page.get('pages')}; more pages: {bool(page.get('continuation'))}")


async def main() -> None:
    async with MCPServerStreamableHttp(
        name="dfx",
        params={"url": URL, "headers": HEADERS, "timeout": 120, "sse_read_timeout": 300},
        client_session_timeout_seconds=120,   # research can take longer than the 5 s default
        cache_tools_list=True,
    ) as dfx:
        agent = Agent(
            name="credit analyst",
            instructions=("Answer with DFX research. Cite the evidence URL for every figure. Keep fair value and "
                          "principal separate. NOT_COVERED and NO_MATCH are answers: say what is not covered "
                          "instead of concluding no."),
            mcp_servers=[dfx],
        )
        tools = await dfx.list_tools()
        print(f"agent '{agent.name}' has {len(tools)} DFX tools over MCP; first: "
              f"{', '.join(t.name for t in tools[:3])}")
        if os.environ.get("OPENAI_API_KEY"):
            result = await Runner.run(agent, QUESTION)
            print(result.final_output)
            return
        print("no OPENAI_API_KEY: calling research on the agent's MCP server, as the model would")
        result = await dfx.call_tool("research", {"question": QUESTION})
        # mcp 2.x names the parsed answer structured_content (mcp 1.x: structuredContent); the text copy is the same JSON
        answer = getattr(result, "structured_content", None) or json.loads(result.content[0].text)
        show(answer)


if __name__ == "__main__":
    asyncio.run(main())
