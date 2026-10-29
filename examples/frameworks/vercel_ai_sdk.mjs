// Vercel AI SDK: DFX research as an AI SDK tool, from the dfx-intel/ai-sdk adapter.
//
//   npm install dfx-intel ai          # runs as is: no DFX key
//   export AI_GATEWAY_API_KEY=...     # optional: run generateText with a real model through the AI Gateway
//   node vercel_ai_sdk.mjs
//
// The adapter takes the `ai` module you already have (checked with ai 5.x, 6.x and 7.x), so dfx-intel keeps zero
// runtime dependencies. With AI_GATEWAY_API_KEY set, generateText lets the model call dfx_research and answer. Without
// it the script calls the tool's execute the way generateText would, so you can see what the model receives. The
// recorded run (vercel_ai_sdk.out.txt) is the one without a model key.
import * as ai from "ai";
import { Client } from "dfx-intel";
import { aiSdkTools } from "dfx-intel/ai-sdk";

const QUESTION = "Which BDCs lend to Medallia?";

// DFX_EXAMPLE_UA_SUFFIX is only for DFX's own test runs, so they can be excluded from usage counts. Leave it unset.
const dfx = new Client({ channel: "ex-ai-sdk", userAgentSuffix: process.env.DFX_EXAMPLE_UA_SUFFIX });
const tools = aiSdkTools(ai, dfx);

if (process.env.AI_GATEWAY_API_KEY) {
  const { text, steps } = await ai.generateText({
    model: process.env.DFX_EXAMPLE_MODEL ?? "openai/gpt-4.1-mini",
    tools,
    stopWhen: ai.stepCountIs(4),
    system: "Answer with DFX research and cite the evidence URLs. NOT_COVERED and NO_MATCH are answers, not a no.",
    prompt: QUESTION,
  });
  console.log(text, "\nsteps:", steps.length);
} else {
  console.log("no AI_GATEWAY_API_KEY: calling the dfx_research tool's execute, as generateText would");
  console.log("tools:", Object.keys(tools));
  const r = await tools.dfx_research.execute({ question: QUESTION }, { toolCallId: "call_1", messages: [] });
  console.log("state:", r.state, "| answer_state:", r.answer_state);
  console.log("answer:", r.answer);
  const urls = r.evidence_urls;
  console.log("claims:", r.claims.length, "| source documents:", urls.length, "| more pages:", Boolean(r.continuation));
  for (const u of urls.slice(0, 3)) console.log("   ", u);
}
