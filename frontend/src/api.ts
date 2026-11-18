import type { AgentEvent } from "./types";

// EventSource only does GET; we need to POST a file, so we read the SSE stream by hand.
export async function analyze(cv: File, jd: string, onEvent: (e: AgentEvent) => void) {
  const body = new FormData();
  body.append("cv", cv);
  body.append("job_description", jd);
  const res = await fetch("/api/analyze", { method: "POST", body });
  if (!res.ok) {
    const detail = (await res.json().catch(() => null))?.detail;
    throw new Error(typeof detail === "string" ? detail : res.statusText);
  }
  const reader = res.body!.pipeThrough(new TextDecoderStream()).getReader();
  let buffer = "";
  for (;;) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += value;
    const chunks = buffer.split("\n\n");
    buffer = chunks.pop()!;
    for (const c of chunks) if (c.startsWith("data: ")) onEvent(JSON.parse(c.slice(6)));
  }
}
