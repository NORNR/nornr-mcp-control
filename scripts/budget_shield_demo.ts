import Stripe from "stripe";
import OpenAI from "openai";

export function buildDemoLane(server: unknown) {
  const stripe = new Stripe(process.env.STRIPE_SECRET_KEY ?? "");
  const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
  const tools = create_mcp_tools(server);

  return { stripe, client, tools };
}
