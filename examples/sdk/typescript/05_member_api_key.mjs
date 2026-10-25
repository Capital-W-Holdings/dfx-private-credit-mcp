// Member access with an account key from the environment. Create one at https://dfxintel.com/data-factory/account:
//   export DFX_API_KEY=dfx_live_...
// The SDK sends it as Authorization: Bearer <key>; keyed requests are never channel-tagged. Never commit a key.
import { Client } from "dfx-intel";

const key = (process.env.DFX_API_KEY ?? "").trim();
if (!key) {
  console.error("DFX_API_KEY is not set. Create a key at https://dfxintel.com/data-factory/account, export it, " +
    "and run again. (Anonymous use needs no key: see 01_research_anonymous.mjs.)");
  process.exit(1);
}
if (!key.startsWith("dfx_live_")) {
  console.error("DFX_API_KEY does not look like a DFX account key (expected dfx_live_...).");
  process.exit(1);
}
const dfx = new Client();                  // reads DFX_API_KEY from the environment
const r = await dfx.research("Which BDCs hold the loans of Hyland Software and when do they mature?");
if (["API_KEY_INVALID", "NOT_IN_PLAN", "ENTITLEMENT_REQUIRED"].includes(r.state)) {
  console.error(`${r.state}: ${r.raw?.how_to_fix ?? r.error}`);
  process.exit(1);
}
console.log(r.state, "| access:", r.raw?.withheld?.access, "| plan:", r.raw?.withheld?.plan);
console.log(r.answer);
