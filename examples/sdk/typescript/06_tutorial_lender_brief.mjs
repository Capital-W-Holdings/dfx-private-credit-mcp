// Tutorial: a cited lender brief your agent can call as a tool. Register lenderBrief in any framework (Vercel AI SDK,
// LangChain.js, Mastra, your own loop); it needs no key. agentName (X-Agent-Name) labels your agent; it does not buy a
// separate budget: anonymous research is metered per network address (60 paging calls an hour, measured 2026-10-22).
import { Client } from "dfx-intel";

const dfx = new Client({
  agentName: process.env.DFX_AGENT_NAME ?? "lender-brief-tutorial",
  userAgentSuffix: process.env.DFX_EXAMPLE_UA_SUFFIX,
});

export async function lenderBrief(company) {
  const r = await dfx.research(`Which BDCs hold the loans of ${company} and when do they mature?`);
  if (r.state !== "OK") return `No brief for ${company}: ${r.state}. ${r.answer ?? r.error ?? ""}`.trim();
  const lines = [`## BDC lenders to ${company}`, "", r.answer ?? "", ""];
  for (const row of r.raw?.relationships ?? []) {
    if (row.rel_type_canonical !== "LENDER_TO") continue;   // skip sponsor and ownership rows
    const fv = typeof row.amount_usd === "number" ? `$${(row.amount_usd / 1e6).toFixed(1)}M fair value` : "amount not stated";
    lines.push(`- ${row.subject?.name}: ${fv}, as of ${row.as_of}. ${row.tranches ?? ""} [source](${row.cite?.url ?? "uncited"})`);
  }
  if (r.continuation) lines.push(`- ${r.page.rows_after_this_page} more rows behind the continuation.`);
  lines.push("");
  for (const l of r.coverageLimits) lines.push(`> Limit: ${l.why}`);
  return lines.join("\n");
}

console.log(await lenderBrief("Hyland Software"));
