// POST /run/<model> with a System One body ({ state, questions }) -> Clef's answer,
// plus the time Workers AI took (ms) so the relay's own overhead can be told apart.
interface Env {
  AI: { run(model: string, input: unknown): Promise<unknown> };
}

export default {
  async fetch(req: Request, env: Env): Promise<Response> {
    const url = new URL(req.url);
    const model = url.pathname.replace(/^\/run\//, "");
    if (req.method !== "POST" || !model.startsWith("@cf/")) return new Response("POST /run/@cf/...", { status: 404 });
    const body = await req.json();
    const t0 = Date.now();
    try {
      const out = await env.AI.run(model, body);
      return Response.json({ result: out, ai_ms: Date.now() - t0 });
    } catch (e) {
      return Response.json({ error: String(e) }, { status: 502 });
    }
  },
};
