// Error handling. Refusals arrive as result.state; only transport failures throw (TransportError).
import { Client, TransportError } from "dfx-intel";

const UA = process.env.DFX_EXAMPLE_UA_SUFFIX;
const dfx = new Client({ userAgentSuffix: UA });
const RETRYABLE = new Set(["RATE_LIMITED", "TEMPORARILY_UNAVAILABLE"]);
const sleep = (ms) => new Promise((ok) => setTimeout(ok, ms));

async function ask(client, question, attempts = 3) {
  for (let attempt = 1; attempt <= attempts; attempt++) {
    let r;
    try {
      r = await client.research(question);
    } catch (e) {
      if (!(e instanceof TransportError)) throw e;      // a bug in your code, not the network
      console.log(`  transport failure (attempt ${attempt}): TransportError`);
      await sleep(2000 * attempt);
      continue;
    }
    if (RETRYABLE.has(r.state)) {
      const wait = r.retryAfterSeconds ?? 5;
      console.log(`  ${r.state}, retrying in ${wait}s`);
      await sleep(Math.min(wait, 60) * 1000);
      continue;
    }
    return r;
  }
  return null;
}

function report(label, r) {
  if (r === null) return console.log(`${label}: gave up after retries`);
  if (r.state === "OK") {
    console.log(`${label}: OK (${r.answerState}), ${r.claims.length} claims`);
    for (const l of r.coverageLimits) console.log(`  ${l.kind}: ${l.about}: ${l.why}`);
  } else if (["NO_MATCH", "UNKNOWN", "NOT_COVERED"].includes(r.state)) {
    console.log(`${label}: ${r.state} (an answer, not an error): ${r.answer ?? r.error}`);
  } else {
    console.log(`${label}: ${r.state}: ${r.error}`);
  }
}

// 1. A question outside coverage: a state, not an exception.
report("NAV per share", await ask(dfx, "What is the net asset value per share of Ares Capital Corp?"));

// 2. The member door with no credentials: the server answers 401, the SDK returns HTTP_ERROR with its description.
const member = new Client({ mcpPath: "/mcp/core/member", channel: null, apiKey: "", userAgentSuffix: UA });
report("member door, no key", await member.research("Which BDCs lend to Kaseya?"));

// 3. A timeout too short to answer in: TransportError, which ask() retries and then gives up on.
const impatient = new Client({ timeoutMs: 1, userAgentSuffix: UA });
report("timeout", await ask(impatient, "Which BDCs lend to Kaseya?", 2));
