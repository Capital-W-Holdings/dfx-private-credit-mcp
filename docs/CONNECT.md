# Connecting to DFX Intelligence

DFX Intelligence is a remote MCP server (Streamable HTTP). There is nothing to install for an MCP client: you give
it a URL. From code, the `dfx-intel` SDKs wrap the same endpoints (see [`../examples/sdk/`](../examples/sdk/)).

DFX is not listed in the Claude Connectors Directory or the ChatGPT apps directory. In those products you add it
yourself, by URL, as a custom connector. Third party directory pages may describe an older version of the server;
the URLs on this page are the current ones. Smithery's proxy shuts down on 2026-10-31: from then on an install
that points at a `server.smithery.ai` or `run.tools` URL does not connect, so replace it with the full profile URL
below.

## Install in your editor

Each line below adds the anonymous core profile under the name `dfx`. Nothing installs until you confirm in the
editor, and no key is needed.

**Cursor.** Click the button, or open the deeplink on a machine with Cursor installed.

[![Add DFX to Cursor](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/install-mcp?name=dfx&config=eyJ1cmwiOiJodHRwczovL2V4Y2hhbmdlLXByb2R1Y3Rpb24tOTEyMy51cC5yYWlsd2F5LmFwcC9tY3AvY29yZT9jPWlkZS1jdXJzb3IifQ%3D%3D)

```text
cursor://anysphere.cursor-deeplink/mcp/install?name=dfx&config=eyJ1cmwiOiJodHRwczovL2V4Y2hhbmdlLXByb2R1Y3Rpb24tOTEyMy51cC5yYWlsd2F5LmFwcC9tY3AvY29yZT9jPWlkZS1jdXJzb3IifQ==
```

**VS Code (GitHub Copilot agent mode).** From a terminal:

```bash
code --add-mcp '{"name":"dfx","type":"http","url":"https://exchange-production-9123.up.railway.app/mcp/core?c=ide-vscode"}'
```

or paste this link into your browser's address bar, which hands it to VS Code. GitHub does not render `vscode:` links
as buttons, and the vscode.dev redirect page refuses a server URL that carries a query string, so there is no badge
for it here.

```text
vscode:mcp/install?%7B%22name%22%3A%22dfx%22%2C%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Fexchange-production-9123.up.railway.app%2Fmcp%2Fcore%3Fc%3Dide-vscode%22%7D
```

**Claude Code.**

```bash
claude mcp add --transport http dfx 'https://exchange-production-9123.up.railway.app/mcp/core?c=ide-claude-code'
```

Then ask your agent something like "Using DFX, which BDCs lend to Acquia, and what are the positions marked at?" and
it will call `research`. From Python instead, [`../examples/mcp/`](../examples/mcp/) has LangChain, OpenAI Agents SDK
and LlamaIndex scripts, and [`../examples/quickstart.ipynb`](../examples/quickstart.ipynb) is a notebook you can open
in Colab.

## Pick an access mode

| mode | URL | credentials | what you get |
|:-|:-|:-|:-|
| Anonymous | `https://exchange-production-9123.up.railway.app/mcp/core?c=gh-repo` | none | Every read tool. Lists name their first rows and count the rest; contact values are never returned |
| OAuth sign-in (members) | `https://exchange-production-9123.up.railway.app/mcp/core/member` | a DFX account, signed in through your client | Reads as your plan allows, metered on your membership |
| Account key (members) | either anonymous URL | `Authorization: Bearer dfx_live_...` (or `X-API-Key`) | Same as OAuth, for clients and code that can send a header |
| Full profile | `https://exchange-production-9123.up.railway.app/mcp?c=gh-repo` | none, or a key | Every tool by name, including the real estate tools; `research` is listed first |

How to choose:

- **Trying it, or building an agent that needs no account:** anonymous core URL. Start with the `research` tool and
  pass your question as `question`.
- **A person using a chat client that cannot send headers** (Claude custom connectors, ChatGPT developer mode):
  the member URL with OAuth. Copy it exactly. It must not carry a query string, because the OAuth resource has to
  match it character for character.
- **Code, a server, or a client that can send headers** (Claude Code, Cursor, the SDKs): an account key. Create one
  at https://dfxintel.com/data-factory/account and read it from the environment (`DFX_API_KEY`). Never commit it.
  The SDKs send keyed requests without a channel tag.

OAuth details, read from the server's own metadata: protected resource
`/.well-known/oauth-protected-resource/mcp/core/member`, authorization server `https://dfxintel.com` (dynamic client
registration, PKCE S256), scopes `read` and `watch`. An unauthenticated call to the member URL answers 401 with a
`WWW-Authenticate` header that names that metadata, which is how a compliant client starts sign-in.

## Client notes

**Claude (claude.ai, Claude Desktop).** Settings, Connectors, Add custom connector. Paste the member URL to sign in,
or the anonymous URL for keyless use. Leave the OAuth client ID and secret empty. Custom connectors cannot send an
API key header, so a member uses the member URL.

**Claude Code.**

```bash
claude mcp add --transport http dfx 'https://exchange-production-9123.up.railway.app/mcp/core?c=ide-claude-code'
# member, with a key from the environment
claude mcp add --transport http dfx-member 'https://exchange-production-9123.up.railway.app/mcp/core?c=ide-claude-code' \
  --header "Authorization: Bearer $DFX_API_KEY"
```

**ChatGPT (developer mode).** Needs a plan with developer mode. Settings, Apps and Connectors, Advanced settings,
Developer mode on; then Create, with the member URL and OAuth authentication. A full member session through ChatGPT
had not been certified end to end as of 2026-10-21. DFX has no tools named `search` or `fetch`, so ChatGPT features
that require exactly those two tools cannot use it as a data source.

**Cursor, Windsurf, VS Code and other clients that take a JSON config.**

```json
{
  "mcpServers": {
    "dfx": { "type": "http", "url": "https://exchange-production-9123.up.railway.app/mcp/core?c=gh-repo" }
  }
}
```

Clients and gateways that cap or sort the tool list should use the core profile (20 tools, `research` first). On the
full profile (136 tools) a gateway that sorts by name and keeps the first 40 drops `research`.

**Clients that only speak stdio.** Use `bridge/dfx_mcp_stdio.py` from this repository (standard library only, absolute
path in the config), or `npx -y mcp-remote <url>`. Prefer the URL when the client can reach one.

**Python and TypeScript.** `pip install dfx-intel` or `npm install dfx-intel`. Anonymous by default; set
`DFX_API_KEY` for member access. The SDKs call `research`, `verify` and `resolve_name` on the core profile and
`/a2a` for delegated tasks. Browsers do not let a page set User-Agent, so browser calls are not identified as the SDK.

## Limits

- Anonymous research is metered per network address. The RATE_LIMITED envelope read on 2026-10-22 gave 60 paging
  calls an hour (`identity_basis: network_prefix`). Callers behind one office or cloud address share it, and
  `X-Agent-Name` labels a caller without separating that budget.
- A refused call costs nothing and carries `retry.after_seconds`. Members are metered on their membership
  in retrieval units, not calls: Platform 300 units a day, Advantage 2,000 a day, and one research call uses 6 to 18
  units depending on its depth.
- Five `watch_*` tools save an account's own research watches and need a key or a signed-in connection.

## Troubleshooting

| symptom | cause | fix |
|:-|:-|:-|
| 401 "sign in with your DFX account to use this connection" | the member URL was called without a sign-in or key | Connect (sign in) from the client, or use the anonymous URL; keys and connections are listed at https://dfxintel.com/data-factory/account |
| Sign-in fails or loops | the member URL was pasted with a query string or a trailing change | paste `/mcp/core/member` exactly |
| `RATE_LIMITED`, "free hourly budget for paging capabilities is used up" | the anonymous budget for your network address is spent | wait `retry.after_seconds`, or use a member key or sign-in |
| `TEMPORARILY_UNAVAILABLE` or HTTP 503 | the exchange is at capacity or restarting | retry after the stated seconds; nothing ran and nothing was charged |
| `NO_MATCH`, `UNKNOWN` or `NOT_COVERED` | the name resolved with nothing on record, no evidence either way, or a record DFX does not read | treat it as "unknown", never as "no"; read `coverage_limits` |
| An install from Smithery stopped connecting (a `server.smithery.ai` or `run.tools` URL) | Smithery's proxy, accounts and keys stop on 2026-10-31, and nothing redirects | remove that entry and add the full profile URL above; no key or account is needed |
| A tool from an old listing is missing (`open_dfx_account`, `fund_dfx_account`, `dfx_payment_status`) | those tools were retired | use `research`, or the full profile for the real estate tools |
| A tool you expect is not on `/mcp/core` | the core profile lists 20 tools | add the full profile URL as a second server |
| Invalid argument on `research` | it takes `question` (plus optional `continue`, `depth`, `detail`, `entity`) | pass the question as `question` |
| An SDK call raises `TransportError` | DNS, TLS, an unreadable body, or no answer within the timeout (90 s by default) | retry with backoff; states never raise |
