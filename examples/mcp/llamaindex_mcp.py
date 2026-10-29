"""LlamaIndex: DFX as a remote MCP server through llama-index-tools-mcp (BasicMCPClient and McpToolSpec).

    pip install "llama-index-tools-mcp==0.6.0"
    python llamaindex_mcp.py

No DFX key and no model key are needed. McpToolSpec turns each DFX core tool into a LlamaIndex FunctionTool; the
script calls the `research` tool the way an agent would and prints the cited answer.

To give the same tools to an agent (not needed for this script):
    pip install llama-index-llms-openai
    from llama_index.core.agent.workflow import FunctionAgent
    from llama_index.llms.openai import OpenAI
    agent = FunctionAgent(tools=tools, llm=OpenAI(model="gpt-5"))
    print(await agent.run(QUESTION))
"""
import asyncio
import json
import os

from llama_index.tools.mcp import BasicMCPClient, McpToolSpec

URL = "https://exchange-production-9123.up.railway.app/mcp/core?c=ex-llamaindex"
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


async def main() -> None:
    client = BasicMCPClient(URL, headers=HEADERS, timeout=120)   # research can take longer than the 30 s default
    tools = await McpToolSpec(client=client).to_tool_list_async()
    print(f"{len(tools)} DFX tools loaded as LlamaIndex FunctionTools; first: "
          f"{', '.join(t.metadata.name for t in tools[:3])}")
    research = next(t for t in tools if t.metadata.name == "research")
    output = await research.acall(question=QUESTION)
    result = output.raw_output                                  # the MCP CallToolResult
    # mcp 2.x names the parsed answer structured_content (mcp 1.x: structuredContent); the text copy is the same JSON
    show(getattr(result, "structured_content", None) or json.loads(result.content[0].text))


if __name__ == "__main__":
    asyncio.run(main())
