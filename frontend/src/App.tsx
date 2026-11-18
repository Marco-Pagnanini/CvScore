import { useState } from "react";
import { analyze } from "./api";
import type { AgentEvent, Report } from "./types";
import UploadForm from "./components/UploadForm";
import LiveView, { type AgentLog } from "./components/LiveView";
import ResultView from "./components/ResultView";

type Phase =
  | { kind: "idle"; error?: string }
  | { kind: "running" }
  | { kind: "done"; report: Report };

export default function App() {
  const [phase, setPhase] = useState<Phase>({ kind: "idle" });
  const [logs, setLogs] = useState<AgentLog[]>([]);

  function onEvent(e: AgentEvent) {
    if (e.type === "result") return setPhase({ kind: "done", report: e.data });
    if (e.type === "error") return setPhase({ kind: "idle", error: e.message });
    setLogs((prev) => {
      if (e.type === "start") return [...prev, { agent: e.agent, text: "", done: false }];
      const last = prev.findLastIndex((l) => l.agent === e.agent && !l.done);
      if (last < 0) return prev;
      const log = { ...prev[last] };
      if (e.type === "text") log.text += e.text;
      if (e.type === "tool") log.text += `\n→ ${e.tool}\n`;
      if (e.type === "end") log.done = true;
      return prev.map((l, i) => (i === last ? log : l));
    });
  }

  async function start(cv: File, jd: string) {
    setLogs([]);
    setPhase({ kind: "running" });
    try {
      await analyze(cv, jd, onEvent);
    } catch (err) {
      setPhase({ kind: "idle", error: (err as Error).message });
    }
  }

  return (
    <div className="shell">
      <header className="topbar">
        <button type="button" className="brand" onClick={() => setPhase({ kind: "idle" })}>
          <span className="brand-dot" />CV Scoring
        </button>
        <span className="mono muted small">Agentic SOA demo</span>
      </header>
      <main>
        {phase.kind === "idle" && <UploadForm error={phase.error} onSubmit={start} />}
        {phase.kind === "running" && <LiveView logs={logs} />}
        {phase.kind === "done" && <ResultView report={phase.report} onReset={() => setPhase({ kind: "idle" })} />}
      </main>
    </div>
  );
}
