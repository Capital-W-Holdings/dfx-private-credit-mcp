"""OpenAI Agents SDK: an analyst agent with DFX research and verify as function tools.

    pip install "dfx-intel[openai-agents]"     # runs as is: no DFX key
    export OPENAI_API_KEY=...                   # optional: run the agent itself
    python openai_agents.py

With OPENAI_API_KEY set, `Runner.run_sync` runs the agent and the model decides when to call `dfx_research`. Without
it the script invokes the same FunctionTool the agent would call, through the SDK's own `on_invoke_tool`, so you can
see exactly what the model receives. The recorded run (openai_agents.out.txt) is the one without a model key.

Prefer MCP? The Agents SDK can also attach DFX as a remote server:
    from agents.mcp import MCPServerStreamableHttp
    MCPServerStreamableHttp(params={"url": "https://exchange-production-9123.up.railway.app/mcp/core?c=ex-openai-agents"})
"""
import asyncio
import json
import os

from agents import Agent, Runner
from agents.tool_context import ToolContext

from dfx_intel import Client
from dfx_intel.adapters.openai_agents import dfx_tools

QUESTION = "Which BDCs lend to Kaseya, and what are the positions marked at?"

# DFX_EXAMPLE_UA_SUFFIX is only for DFX's own test runs, so they can be excluded from usage counts. Leave it unset.
dfx = Client(channel="ex-openai-agents", user_agent_suffix=os.environ.get("DFX_EXAMPLE_UA_SUFFIX"))
tools = dfx_tools(client=dfx)          # [dfx_research, dfx_verify] as FunctionTools

agent = Agent(
    name="credit analyst",
    instructions=("Answer with DFX research. Cite the evidence URLs for every figure. Keep fair value and principal "
                  "separate. NOT_COVERED and NO_MATCH are answers: say what is not covered instead of concluding no. "
                  "If the answer has a continuation and the user asked for all lenders, call again with it."),
    tools=tools,
)

if os.environ.get("OPENAI_API_KEY"):
    result = Runner.run_sync(agent, QUESTION)
    print(result.final_output)
else:
    print("no OPENAI_API_KEY: invoking the agent's dfx_research tool directly, as the model would")
    research = next(t for t in agent.tools if t.name == "dfx_research")
    print("tool:", research.name, "| parameters:", sorted(research.params_json_schema["properties"]))
    args = json.dumps({"question": QUESTION, "continuation": ""})
    ctx = ToolContext(context=None, tool_name=research.name, tool_call_id="call_1", tool_arguments=args)
    r = json.loads(asyncio.run(research.on_invoke_tool(ctx, args)))
    print("state:", r["state"], "| answer_state:", r["answer_state"])
    print("answer:", r["answer"])
    print(f"claims: {len(r['claims'])} | source documents: {len(r['evidence_urls'])}"
          f" | more pages: {bool(r['continuation'])}")
    for u in r["evidence_urls"][:3]:
        print("   ", u)
