# DFX as an MCP server in Python agent frameworks

These scripts attach DFX the way each framework attaches any remote MCP server, with no DFX package in between. Each
one connects to the anonymous core profile, loads the DFX tools into the framework, asks one real question through the
`research` tool and prints the cited answer: every lender row links to that lender's own filing on sec.gov.

No DFX key and no model key are needed. Each script ran against production and its real output sits next to it
(`.out.txt`, with the UTC time of the run in `.ran_at`), left as it came back. The docstring at the top of each file
shows how to hand the same tools to a model.

| example | framework | install (versions checked on PyPI) | how DFX is attached |
|:-|:-|:-|:-|
| `langchain_mcp.py` | LangChain | `pip install "langchain-mcp-adapters==0.3.2"` | `MultiServerMCPClient` with `"transport": "streamable_http"`; `get_tools()` returns LangChain tools |
| `openai_agents_mcp.py` | OpenAI Agents SDK | `pip install "openai-agents==0.24.0"` | `MCPServerStreamableHttp` passed as `Agent(mcp_servers=[...])`; set `OPENAI_API_KEY` and the agent runs end to end |
| `llamaindex_mcp.py` | LlamaIndex | `pip install "llama-index-tools-mcp==0.6.0"` | `BasicMCPClient` and `McpToolSpec`; `to_tool_list_async()` returns FunctionTools |

Use one virtual environment per script. langchain-mcp-adapters 0.3.2 needs `mcp` below 2.0 and llama-index-tools-mcp
0.6.0 needs `mcp` 2.0 or later, so pip cannot install both into one environment.

Prefer a notebook? [`../quickstart.ipynb`](../quickstart.ipynb) shows raw JSON-RPC over httpx and then the OpenAI
Agents SDK, with saved outputs, and opens in Colab.

## Things that trip people up

* **Use the exchange URL in these files as is.** `https://dfxintel.com/mcp` answers with a redirect to another host,
  and the official MCP Python SDK refuses cross-origin redirects ("Redirect ... not followed"). The scripts point at
  the exchange directly.
* **Raise the timeouts.** A research call can take longer than the defaults: the OpenAI Agents SDK waits 5 seconds
  for a session reply and LlamaIndex's client 30. The scripts set 120.
* **Read the state, not just the text.** `OK` is an answer; `NO_MATCH`, `UNKNOWN` and `NOT_COVERED` are answers too
  and mean "do not conclude no". `coverage_limits` says why. More rows come back through `page.continuation`.
* **Fair value and principal are separate figures.** BDC holdings are not all lenders: banks, CLOs and private funds
  file no schedule of investments.

The `?c=` on each URL is a channel tag that tells DFX which example a call came from. Keep it. `DFX_EXAMPLE_UA` in
the scripts is only for DFX's own test runs, so they can be excluded from usage counts. Leave it unset.

Members: add `Authorization: Bearer <your dfx_live_ key>` to the headers, read from the environment (`DFX_API_KEY`),
never typed into the file. See [`../../docs/CONNECT.md`](../../docs/CONNECT.md).
