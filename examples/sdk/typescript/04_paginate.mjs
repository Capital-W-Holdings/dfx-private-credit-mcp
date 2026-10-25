// Pagination: pass the continuation back, unchanged, for the next page. Cap the walk: anonymous callers have a
// budget of about 60 calls an hour, and without a plan rows past the first few are counted, not named.
import { Client } from "dfx-intel";

const dfx = new Client({ userAgentSuffix: process.env.DFX_EXAMPLE_UA_SUFFIX });
const MAX_PAGES = 3;

let r = await dfx.research("Which BDCs lend to Auctane, and which of them are current lenders?");
console.log("page 1:", r.state, "| rows total:", r.page.rows_total, "| pages:", r.page.pages);
const lenders = [];
let pages = 0;
while (r && r.state === "OK") {
  pages++;
  for (const row of r.raw?.relationships ?? []) {
    if (row.rel_type_canonical !== "LENDER_TO") continue;   // sponsor and ownership rows ride along; skip them
    const name = row.subject?.name;
    if (name && !lenders.includes(name)) lenders.push(name);
  }
  if (pages >= MAX_PAGES || !r.continuation) break;
  r = await dfx.continueResearch(r);       // same as dfx.research(null, { continuation: r.continuation })
  console.log(`page ${r.page.index}: ${r.state}, rows on page ${r.page.rows_on_page}`);
}
console.log(`\nread ${pages} page(s), ${lenders.length} named lender(s):`);
for (const name of lenders) console.log(" ", name);
if (r?.continuation) console.log(`stopped at the cap; ${r.page.rows_after_this_page} rows remain behind the continuation`);
