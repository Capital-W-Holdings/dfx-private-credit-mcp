// Anonymous research: one question, one call, no key, no sign-up.
//   npm install dfx-intel
//   node 01_research_anonymous.mjs
import { Client } from "dfx-intel";

// DFX_EXAMPLE_UA_SUFFIX is only for DFX's own test runs, so they can be excluded from usage counts. Leave it unset.
const dfx = new Client({ userAgentSuffix: process.env.DFX_EXAMPLE_UA_SUFFIX });

const r = await dfx.research("Which BDCs hold the loans of Hyland Software and when do they mature?");
console.log("state:", r.state, "| answer_state:", r.answerState);
console.log("answer:", r.answer);
console.log("claims on this page:", r.claims.length, "| source documents:", r.evidenceUrls.length);
console.log("more pages:", Boolean(r.continuation), "| access:", r.raw?.withheld?.access);
