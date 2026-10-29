# dfx-intel SDK examples

Small, runnable examples for the `dfx-intel` packages on PyPI and npm. Every script ran against production with no
key, using the published package installed into a clean environment, and its real output sits next to it
(`.out.txt`, with the UTC time of the run in `.ran_at`). Outputs are left as they came back.

```bash
pip install dfx-intel          # Python 3.9+, standard library only
npm install dfx-intel          # Node 18+, Deno, Bun; no runtime dependencies
```

Run a Python example with `python python/01_research_anonymous.py`. Run a TypeScript example from a folder where
`dfx-intel` is installed: `node 01_research_anonymous.mjs` (Node resolves the package from the script's own folder,
so copy the file next to your `node_modules` or install the package beside it).

| Python | TypeScript | what it shows |
|:-|:-|:-|
| `01_research_anonymous.py` | `01_research_anonymous.mjs` | One question, one call, no key: state, answer, how many claims and source documents, whether there are more pages |
| `02_cited_answer.py` | `02_cited_answer.mjs` | Every claim printed with the document behind it, by joining `claim.row` to the row's `cite.url`; the citation check and the answer's own "do not conclude" lines |
| `03_errors_and_retry.py` | `03_errors_and_retry.mjs` | States, not exceptions: a NOT_COVERED limit inside an OK answer, the member door's 401 without credentials, a request refused before sending, and a timeout that raises `TransportError`; bounded retry on RATE_LIMITED and TEMPORARILY_UNAVAILABLE |
| `04_paginate.py` | `04_paginate.mjs` | Walking `continuation` with a page cap, keeping lender rows only |
| `05_member_api_key.py` | `05_member_api_key.mjs` | Member access with `DFX_API_KEY` from the environment; stops loudly when it is missing. The recorded output is that stop, because these runs use no key |
| `06_tutorial_lender_brief.py` | `06_tutorial_lender_brief.mjs` | The tutorial below: a cited lender brief as one function an agent can call as a tool |
| `07_what_changed.py` | `07_what_changed.mjs` | The second session: what changed for a borrower since the prior quarter end, one `call_tool` / `callTool` of `search_private_credit_changes` on `/mcp`, each change dated and sourced, the rest counted |

Building on an agent framework? [`../frameworks/`](../frameworks/) has runnable Claude Agent SDK, OpenAI Agents SDK,
LangGraph and Vercel AI SDK examples and copy-paste MCP configs for Cursor, VS Code, Windsurf and Claude Desktop.

`DFX_EXAMPLE_UA_SUFFIX` in the scripts is only for DFX's own test runs, so they can be excluded from usage counts.
Leave it unset.

## Tutorial: a cited lender brief in one function

The goal: your agent is asked "who lends to Hyland Software?" and should answer with sources a person can open.

1. **Ask one question.** `research` takes plain English and returns `state`, a short `answer` built only from cited
   claims, the `claims`, and the rows they rest on (`raw.relationships`, `raw.facts`, `raw.events`).
2. **Check the state before reading anything else.** `OK` is an answer. `NO_MATCH`, `UNKNOWN` and `NOT_COVERED` are
   answers too, and they mean "do not conclude no". `RATE_LIMITED` and `TEMPORARILY_UNAVAILABLE` carry
   `retry_after_seconds`. Only transport failures raise.
3. **Keep the rows you need and their sources.** A lender row has `rel_type_canonical` `LENDER_TO`, the lender in
   `subject.name`, fair value in `amount_usd`, principal in `principal_usd`, the filing date in `as_of`, and the
   primary document in `cite.url` (a BDC's 10-Q or 10-K on sec.gov). Sponsor and ownership rows can ride along in
   the same list; filter them out.
4. **Say what is missing.** Without a plan, list answers name the first rows and count the rest; `page` says how many
   rows remain behind the continuation. `coverage_limits` and `raw.do_not_conclude` say what the data cannot show
   (banks, CLOs and private funds file no schedule of investments, so they are not on the tape).
5. **Register it as a tool.** The function takes a company name and returns Markdown. Wrap it in your framework's
   tool type; it needs no key. The Python package also ships LangChain and OpenAI Agents adapters
   (`pip install "dfx-intel[langchain]"`, `pip install "dfx-intel[openai-agents]"`), and the TypeScript package ships
   a Vercel AI SDK adapter at `dfx-intel/ai-sdk`.

`06_tutorial_lender_brief.py` and `.mjs` are the whole integration; their `.out.txt` is the brief they produced.

## Coming back after the next filings

BDCs file a quarter's 10-Q about 40 to 45 days after the quarter ends, so a borrower's lenders, marks, spreads and
maturities move on the tape a few times a year. `07_what_changed` is the call to make when they do: the borrower's
dfx id from a research answer, `since` set to the quarter end you last read, and back come the dated changes
(lenders joining or leaving, marks, spread and maturity moves, PIK, non-accrual), each with the filing behind it.

- The tool is listed on the full profile, `/mcp`, so the example sets `mcp_path="/mcp"` (`mcpPath: "/mcp"`); the SDK
  defaults to `/mcp/core`, which does not list it.
- Schedule it yourself, for example once a week in the weeks after each quarter's filing deadline. DFX keeps no list
  of your borrowers, runs nothing on your behalf and sends nothing.
- An effective date is the quarter end where the change is visible. A lender exit is dated at the last quarter the
  lender held the piece, so it appears one schedule later than its date suggests.
- An empty list means no change was read since then, not that nothing happened off the BDC schedules.

## Reading the numbers

- Fair value, principal and cost are separate fields. Do not add one to another.
- Principal is the sum of the BDC pieces on their own schedules, so it is a lower bound on the facility.
- A negative amount on a revolver or delayed draw line is the fair value the BDC printed for an undrawn commitment,
  not a loan balance.
- When a filing gives a maturity as a month and year, the date in the answer carries a placeholder day (for example
  `2030-09-01` for September 2030). Treat the day as unknown.

## Access and limits (measured 2026-10-22)

- Anonymous research is metered per network address: the RATE_LIMITED envelope read on 2026-10-22 said 60 paging
  calls an hour (`identity_basis: network_prefix`). `agent_name` (X-Agent-Name) labels your agent but did not give it a
  separate budget. A refused call is not charged and says when to retry.
- Members are metered on their membership instead, in retrieval units, not calls: Platform 300 units a day,
  Advantage 2,000 a day, and one research call uses 6 to 18 units depending on its depth. Plans:
  https://dfxintel.com/data-factory/plans
- Anonymous and keyed connections, OAuth sign-in, client limits and troubleshooting: [`../../docs/CONNECT.md`](../../docs/CONNECT.md).
