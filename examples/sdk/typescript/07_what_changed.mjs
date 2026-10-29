// What changed for a borrower since the prior quarter: the second session, one call, no key.
//   npm install dfx-intel
//   node 07_what_changed.mjs [dfx_id] [since]
//
// The SDK wraps research, verify and resolve; every other tool is one `callTool` away. The changes feed,
// search_private_credit_changes, is listed on the full profile (/mcp), not on /mcp/core (the SDK's default), so this
// client points at /mcp. The borrower id is the one example 01 resolved (Hyland Software); `since` defaults to the
// quarter end before the newest one BDCs have filed.
//
// BDCs file a quarter's 10-Q about 40 to 45 days after it ends. Run this yourself after each filing season (a cron
// job, a scheduled agent task). DFX keeps no list of your borrowers, runs no loop for you and sends nothing.
import { Client } from "dfx-intel";

// DFX_EXAMPLE_UA_SUFFIX is only for DFX's own test runs, so they can be excluded from usage counts. Leave it unset.
const dfx = new Client({ mcpPath: "/mcp", userAgentSuffix: process.env.DFX_EXAMPLE_UA_SUFFIX });

const HYLAND = "dfx:pc:fa47c51b-e087-6631-d0cd-ae3158ba0421"; // from 01_research_anonymous: identities.subject.dfx_id
const FILING_LAG_DAYS = 45;
const DAY = 86_400_000;

// The last calendar quarter end strictly before `day` (UTC).
function quarterEndBefore(day) {
  const qMonth = Math.floor(day.getUTCMonth() / 3) * 3; // 0, 3, 6 or 9
  return new Date(Date.UTC(day.getUTCFullYear(), qMonth, 1) - DAY);
}

// The quarter end before the newest one whose filings are due by now (today minus the filing lag).
function priorQuarterEnd(today) {
  const newestFiled = quarterEndBefore(new Date(today.getTime() - (FILING_LAG_DAYS - 1) * DAY));
  return quarterEndBefore(newestFiled).toISOString().slice(0, 10);
}

const dfxId = process.argv[2] ?? HYLAND;
const since = process.argv[3] ?? priorQuarterEnd(new Date());

const [payload, , fallback] = await dfx.callTool("search_private_credit_changes",
  { dfx_id: dfxId, since, by: "effective" });
const p = payload ?? {};
const state = p.state ?? fallback;
console.log(`changes on ${dfxId} effective on or after ${since}`);
console.log("state:", state, "| on this page:", p.count, "| named here:", (p.results ?? []).length,
  "| in all:", p.total);
if (state !== "OK" && state !== "NO_MATCH") {
  console.log("not an answer:", p.error ?? p.message, "| retry after:", p.retry?.after_seconds);
  process.exit(0);
}
if (state === "NO_MATCH") {
  console.log("no change on a BDC schedule since then (no filing read, or nothing moved); not proof that nothing happened");
}

for (const row of p.results ?? []) {
  const who = row.subject?.name;
  const rel = (row.related ?? []).map((r) => r.name).filter((n) => n && n !== "LOCKED").join(", ");
  let move = "";
  if (row.prior_value != null || row.new_value != null) {
    move = ` | ${row.prior_value} -> ${row.new_value} ${row.amount_unit ?? ""}`.trimEnd();
  } else if (row.amount != null) {
    move = ` | ${row.amount} ${row.amount_unit ?? ""}`.trimEnd();
  }
  const url = row.cite?.url ?? row.source?.url;
  console.log(`\n${String(row.effective_at).slice(0, 10)}  ${row.event_type}  ${who}${rel ? ` / ${rel}` : ""}${move}`);
  if (row.headline) console.log("   ", row.headline);
  console.log("    source:", url ?? "(none on this row)");
}

const locked = p.locked ?? {};
if (locked.count) {
  console.log(`\n${locked.count} more change(s) counted, not named, without a plan:`, locked.by_type ?? "");
}
if (p.note) console.log("\nnote:", p.note);
console.log("\nAn effective date is the quarter end where the change is visible. A lender exit is dated at the last " +
  "quarter the lender held the piece. BDC schedules are not every lender: banks, CLOs and private funds file none.");
