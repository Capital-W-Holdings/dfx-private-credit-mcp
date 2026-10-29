# DFX in your agent framework

One runnable example per framework, each using the published `dfx-intel` package and its framework adapter, plus
copy-paste MCP configs for the common clients. Each script ran once against production with no DFX key and no model
key, and its real output sits next to it (`.out.txt`, with the UTC time of the run in `.ran_at`). Outputs are left as
they came back.

Without a model key every script still does real work: it hands DFX's tool to the framework and invokes it the way the
model would (LangGraph runs the whole graph with a scripted stand in for the model). Set the model key named in the
script and the same code runs the agent end to end. No DFX account is needed for any of it.

| example | framework | install | what it shows |
|:-|:-|:-|:-|
| `claude_agent_sdk.py` | Claude Agent SDK | `pip install dfx-intel claude-agent-sdk "mcp>=2"` | DFX as a remote MCP server: `mcp_servers()` and `allowed_tools()` are the whole integration. Without `--agent` it opens the same URL with the official MCP SDK, lists the tools and asks one question |
| `openai_agents.py` | OpenAI Agents SDK | `pip install "dfx-intel[openai-agents]"` | `dfx_research` and `dfx_verify` as function tools on an `Agent`; the MCP alternative (`MCPServerStreamableHttp`) is in the docstring |
| `langgraph_agent.py` | LangChain / LangGraph | `pip install "dfx-intel[langchain]" langgraph` | The DFX tools in a `ToolNode` inside the usual agent loop (`tools_condition`); add `langchain-openai` and `OPENAI_API_KEY` for a real model |
| `vercel_ai_sdk.mjs` | Vercel AI SDK | `npm install dfx-intel ai` | `aiSdkTools(ai)` from `dfx-intel/ai-sdk` in `generateText`; you pass your own `ai` module, so the package stays dependency free |
| `mcp-clients/check_config.py` | any MCP client | `pip install "mcp>=2"` | Reads one of the configs below, connects with the official MCP Python SDK, lists the tools and asks one question. Run `check_config.py` before you paste a config |

Want DFX attached as a plain MCP server instead of through the `dfx-intel` adapters? [`../mcp/`](../mcp/) has
langchain-mcp-adapters, OpenAI Agents SDK (`MCPServerStreamableHttp`) and LlamaIndex scripts, and
[`../quickstart.ipynb`](../quickstart.ipynb) is a notebook that opens in Colab.

Run a TypeScript example from a folder where `dfx-intel` and `ai` are installed (Node resolves packages from the
script's own folder).

## MCP client configs

All four point at the core profile (`/mcp/core`): `research` first, a few dozen thousand characters of tool
definitions instead of the full profile's hundreds of thousands, and no key needed.

| file | client | where it goes |
|:-|:-|:-|
| `cursor.mcp.json` | Cursor | `.cursor/mcp.json` in a project, or `~/.cursor/mcp.json` for every project ([docs](https://cursor.com/docs/context/mcp)) |
| `vscode.mcp.json` | VS Code (Copilot agent mode) | `.vscode/mcp.json` in a workspace, or **MCP: Add Server** and choose HTTP ([docs](https://code.visualstudio.com/docs/agents/reference/mcp-configuration)) |
| `windsurf.mcp_config.json` | Windsurf (Cascade) | the `mcpServers` block of Cascade's `mcp_config.json`; Windsurf takes `serverUrl` ([docs](https://docs.windsurf.com/windsurf/cascade/mcp)) |
| `claude_desktop_config.json` | Claude Desktop | `claude_desktop_config.json`; it launches `npx -y mcp-remote` as a local bridge. Simpler where available: **Settings, Connectors, Add custom connector** and paste the URL from this file ([docs](https://modelcontextprotocol.io/docs/develop/connect-remote-servers)) |

Members: replace the URL with `https://exchange-production-9123.up.railway.app/mcp/core/member` and add
`"headers": {"Authorization": "Bearer <your dfx_live_ key>"}`, or let a client that supports OAuth sign in. Keep the
key out of files you commit (Windsurf, for one, reads `${env:DFX_API_KEY}`). See [`../../docs/CONNECT.md`](../../docs/CONNECT.md).

## Reading what comes back

The tools return the same envelope everywhere: `state`, a short `answer` built only from cited claims, the `claims`,
`evidence_urls` (the filings on sec.gov), `coverage_limits`, and `continuation` when there are more pages. `OK` is an
answer; `NO_MATCH`, `UNKNOWN` and `NOT_COVERED` are answers too and mean "do not conclude no". Tell your agent so in
its instructions, as these examples do. Fair value and principal are separate figures; BDC holdings are not all
lenders (banks, CLOs and private funds file no schedule of investments). More in [`../sdk/README.md`](../sdk/README.md).

## Limits

Anonymous research is metered per network address (60 paging calls an hour when read on 2026-10-22). A refused call
is not charged and carries `retry_after_seconds`. Members are metered in retrieval units instead; plans at
https://dfxintel.com/data-factory/plans

`DFX_EXAMPLE_UA_SUFFIX` in the scripts is only for DFX's own test runs, so they can be excluded from usage counts.
Leave it unset.
