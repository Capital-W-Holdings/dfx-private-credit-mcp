// Print every claim with the document it comes from. A claim names a row (claim.row, e.g. "r1"); the row carries the
// subject, object, amounts, date and cite.url. The SDK keeps the server payload unchanged as .raw, so join them here.
import { Client } from "dfx-intel";

const dfx = new Client({ userAgentSuffix: process.env.DFX_EXAMPLE_UA_SUFFIX });

function rowsById(raw) {
  const out = new Map();
  for (const key of ["relationships", "facts", "events", "identities"]) {
    const list = raw?.[key];
    if (Array.isArray(list)) for (const row of list) if (row && row.id) out.set(row.id, row);
  }
  return out;
}
const money = (v) => (typeof v === "number" ? `$${(v / 1e6).toFixed(1)}M` : "n/a");

const r = await dfx.research("Which BDCs hold the loans of Hyland Software and when do they mature?");
console.log(r.state, "|", r.answer, "\n");
const rows = rowsById(r.raw);
for (const c of r.claims) {
  const row = rows.get(c.row) ?? {};
  console.log(`[${c.claim_type}] ${c.predicate}: ${row.subject?.name} -> ${row.object?.name}`);
  if (c.predicate === "LENDER_TO_AMOUNT_USD") {
    console.log(`    fair value ${money(row.amount_usd)}, principal ${money(row.principal_usd)}, as of ${row.as_of}`);
  }
  console.log(`    source: ${row.cite?.url ?? "uncited"} (${row.cite?.granularity})`);
}
const check = r.raw?.citation_check ?? {};
console.log("\ncitation check:", check.verdict, "| cited rows", check.cited_rows, "of", check.rows);
for (const line of r.raw?.do_not_conclude ?? []) console.log("do not conclude:", line);
