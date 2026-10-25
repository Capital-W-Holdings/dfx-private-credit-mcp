"""Tutorial: a cited lender brief your agent can call as a tool.

The function below is the whole integration. It asks one question, keeps only what the answer can support, and
returns Markdown in which every line carries its source. Register `lender_brief` as a tool in any framework (LangChain,
OpenAI Agents, your own loop); it needs no key. agent_name (X-Agent-Name) labels your agent in DFX's logs. It does
not buy a separate budget: anonymous research is metered per network address (60 paging calls an hour, measured
2026-10-22), so a RATE_LIMITED answer carries retry_after_seconds and the brief says so instead of guessing.
"""
import os

from dfx_intel import Client

dfx = Client(agent_name=os.environ.get("DFX_AGENT_NAME", "lender-brief-tutorial"),
             user_agent_suffix=os.environ.get("DFX_EXAMPLE_UA_SUFFIX"))


def lender_brief(company: str) -> str:
    r = dfx.research(f"Which BDCs hold the loans of {company} and when do they mature?")
    if r.state != "OK":
        return f"No brief for {company}: {r.state}. {r.answer or r.error or ''}".strip()
    rows = {row.get("id"): row for row in r.raw.get("relationships") or []
            if isinstance(row, dict) and row.get("rel_type_canonical") == "LENDER_TO"}   # skip sponsor rows
    lines = [f"## BDC lenders to {company}", "", r.answer or "", ""]
    for row_id, row in rows.items():
        lender = (row.get("subject") or {}).get("name")
        fv = row.get("amount_usd")
        fv_text = f"${fv / 1e6:,.1f}M fair value" if isinstance(fv, (int, float)) else "amount not stated"
        url = (row.get("cite") or {}).get("url") or "uncited"
        lines.append(f"- {lender}: {fv_text}, as of {row.get('as_of')}. {row.get('tranches') or ''} [source]({url})")
    if r.has_more:
        lines.append(f"- {r.page.get('rows_after_this_page')} more rows behind the continuation.")
    lines.append("")
    for limit in r.coverage_limits:
        lines.append(f"> Limit: {limit.get('why')}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(lender_brief("Hyland Software"))
