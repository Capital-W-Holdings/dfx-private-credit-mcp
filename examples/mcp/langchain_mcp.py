"""LangChain: DFX as a remote MCP server through langchain-mcp-adapters (MultiServerMCPClient, streamable_http).

    pip install "langchain-mcp-adapters==0.3.2"
    python langchain_mcp.py

No DFX key and no model key are needed. The script connects to the DFX core profile, turns its MCP tools into
LangChain tools, and invokes the `research` tool exactly the way an agent would, then prints the cited answer.

To hand the same tools to a model, add a chat model and an agent (not needed for this script):
    pip install langchain langchain-openai
    from langchain.agents import create_agent
    agent = create_agent("openai:gpt-5", tools)
    await agent.ainvoke({"messages": [{"role": "user", "content": QUESTION}]})
"""
import asyncio
import json
import os

from langchain_mcp_adapters.client import MultiServerMCPClient

URL = "https://exchange-production-9123.up.railway.app/mcp/core?c=ex-langchain"
QUESTION = "Which BDCs lend to Acquia, and what are the positions marked at?"

# DFX_EXAMPLE_UA is only for DFX's own test runs, so they can be excluded from usage counts. Leave it unset.
HEADERS = {"User-Agent": os.environ["DFX_EXAMPLE_UA"]} if os.environ.get("DFX_EXAMPLE_UA") else None


def show(answer: dict) -> None:
    print("state:", answer["state"])
    print("answer:", answer["answer"]["text"])
    for row in answer.get("relationships", []):
        print(f"  {row['subject']['name']} | fair value ${row.get('amount_usd') or 0:,.0f}"
              f" | marked {row.get('mark_pct')}% | as of {row.get('as_of')} | {row['cite']['url']}")
    page = answer.get("page") or {}
    print(f"page {page.get('index')} of {page.get('pages')}; more pages: {bool(page.get('continuation'))}")


def text_of(content) -> str:
    # langchain-mcp-adapters returns the tool's MCP content as a string or as a list of content blocks
    if isinstance(content, str):
        return content
    return "".join(b.get("text", "") if isinstance(b, dict) else str(b) for b in content)


async def main() -> None:
    client = MultiServerMCPClient({
        "dfx": {"transport": "streamable_http", "url": URL, "headers": HEADERS, "timeout": 120},
    })
    tools = await client.get_tools()
    print(f"{len(tools)} DFX tools loaded as LangChain tools; first: {', '.join(t.name for t in tools[:3])}")
    research = next(t for t in tools if t.name == "research")
    content = await research.ainvoke({"question": QUESTION})
    show(json.loads(text_of(content)))


if __name__ == "__main__":
    asyncio.run(main())
