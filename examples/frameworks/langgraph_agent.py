"""LangGraph: DFX research as a tool node in a two node agent graph.

    pip install "dfx-intel[langchain]" langgraph       # runs as is: no model key, no DFX key
    pip install langchain-openai                       # optional: export OPENAI_API_KEY to put a real model in the graph
    python langgraph_agent.py

The graph is the usual agent loop: a model node, `tools_condition`, a `ToolNode` holding the DFX tools, and back to the
model. With OPENAI_API_KEY set the model node is a chat model with the tools bound. Without it a scripted stand in
asks for one `dfx_research` call and answers from the tool's JSON, so you can see the real tool round trip through
LangGraph without spending a token. The recorded run (langgraph_agent.out.txt) is the scripted one.
"""
import json
import os
from typing import Annotated, TypedDict

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from dfx_intel import Client
from dfx_intel.adapters.langchain import dfx_tools

QUESTION = "Which BDCs lend to Auctane?"
SYSTEM = ("You answer private markets questions with DFX research. Cite the evidence URLs. NOT_COVERED and NO_MATCH "
          "are answers: say what is not covered instead of concluding no.")

# DFX_EXAMPLE_UA_SUFFIX is only for DFX's own test runs, so they can be excluded from usage counts. Leave it unset.
dfx = Client(channel="ex-langgraph", user_agent_suffix=os.environ.get("DFX_EXAMPLE_UA_SUFFIX"))
tools = dfx_tools(client=dfx)          # [dfx_research, dfx_verify] as LangChain StructuredTools


class State(TypedDict):
    messages: Annotated[list, add_messages]


def scripted_model(state: State) -> dict:
    """Stands in for a chat model when no key is set: one tool call, then an answer built from the tool's JSON."""
    last = state["messages"][-1]
    if last.type == "tool":
        r = json.loads(last.content)
        sources = "; ".join(r["evidence_urls"][:3]) or "none"
        return {"messages": [AIMessage(content=f"[{r['state']}] {r['answer']}\nSources: {sources}")]}
    call = {"name": "dfx_research", "args": {"question": last.content, "continuation": ""}, "id": "call_1"}
    return {"messages": [AIMessage(content="", tool_calls=[call])]}


if os.environ.get("OPENAI_API_KEY"):
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model=os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")).bind_tools(tools)

    def model(state: State) -> dict:
        return {"messages": [llm.invoke([SystemMessage(SYSTEM)] + state["messages"])]}
    print("model: ChatOpenAI with the DFX tools bound")
else:
    model = scripted_model
    print("model: scripted stand in (no OPENAI_API_KEY), one dfx_research call")

graph = StateGraph(State)
graph.add_node("agent", model)
graph.add_node("tools", ToolNode(tools))
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", tools_condition)
graph.add_edge("tools", "agent")
app = graph.compile()

out = app.invoke({"messages": [HumanMessage(QUESTION)]})
for m in out["messages"]:
    if m.type == "ai" and m.tool_calls:
        print("\nagent asked for:", [(c["name"], c["args"]["question"]) for c in m.tool_calls])
    elif m.type == "tool":
        r = json.loads(m.content)
        print(f"tool {m.name} returned state {r['state']} | {len(r['claims'])} claims |"
              f" {len(r['evidence_urls'])} source documents | more pages: {bool(r['continuation'])}")
        for u in r["evidence_urls"][:3]:
            print("   ", u)
        for line in r.get("coverage_limits") or []:
            print("    coverage limit:", line)
    elif m.type == "ai":
        print("\nfinal answer:\n" + m.content)
