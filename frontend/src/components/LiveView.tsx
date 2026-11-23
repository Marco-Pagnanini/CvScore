export interface AgentLog { agent: string; text: string; done: boolean }

const AGENTS = ["orchestrator", "jd_analyst", "cv_matcher", "evaluator", "recruiter"];
const LABEL: Record<string, string> = {
  orchestrator: "Orchestrator", jd_analyst: "Job Description Analyst", cv_matcher: "CV Matcher", evaluator: "Evaluator",
  recruiter: "Recruiter",
};

export default function LiveView({ logs }: { logs: AgentLog[] }) {
  const active = [...logs].reverse().find((l) => !l.done);
  const state = (a: string) =>
    active?.agent === a ? "current" : logs.some((l) => l.agent === a && l.done) ? "done" : "";

  return (
    <section className="live">
      <div>
        <span className="kicker mono">AGENTS AT WORK</span>
        <ul className="steps">
          {AGENTS.map((a) => (
            <li key={a} className={`step ${state(a)}`}><span className="step-dot" />{LABEL[a]}</li>
          ))}
        </ul>
      </div>
      <div className="log" aria-live="polite">
        {logs.map((l, i) => (
          <div key={i} className="log-entry">
            <span className="kicker mono">{LABEL[l.agent] ?? l.agent}</span>
            <pre className="mono">{l.text || "…"}</pre>
          </div>
        ))}
      </div>
    </section>
  );
}
