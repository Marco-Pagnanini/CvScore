import type { Report } from "../types";

const VERDICT = { yes: "Yes", partial: "Partial", no: "No" };

export default function ResultView({ report, onReset }: { report: Report; onReset: () => void }) {
  const s = report.score;
  return (
    <div className="result">
      <div className="result-bar">
        <span className="kicker mono">RESULT</span>
        <button type="button" className="pill" onClick={onReset}>+ New analysis</button>
      </div>
      <section className="score-block">
        <div className="score-main">
          <span className="kicker mono">MATCH SCORE</span>
          <div className="score-number"><span className="big">{s.score}</span><span className="of">/ 100</span></div>
          <div className="meter">
            <div className="meter-fill" style={{ width: `${s.score}%` }} />
            <div className="meter-tick" style={{ left: `${s.score}%` }} />
          </div>
        </div>
        <div className="score-side">
          <div className="tally"><span>Must-have</span><span className="mono">{s.must_met} / {s.must_total}</span></div>
          <div className="tally"><span>Nice-to-have</span><span className="mono">{s.nice_met} / {s.nice_total}</span></div>
          <p className="muted small">{report.summary}</p>
        </div>
      </section>
      <section>
        <h2 className="kicker mono">REQUIREMENTS</h2>
        <ul className="rows">
          {report.matches.map((m, i) => (
            <li key={i} className="row">
              <span className={`glyph ${m.verdict}`} />
              <span className="row-text">
                {m.requirement}
                {m.evidence && <span className="evidence muted small">“{m.evidence}”</span>}
              </span>
              <span className="mono muted small">{m.kind === "must" ? "MUST" : "NICE"}</span>
              <span className="verdict">{VERDICT[m.verdict]}</span>
            </li>
          ))}
        </ul>
      </section>
      <section>
        <h2 className="kicker mono">HOW TO IMPROVE</h2>
        <ol className="suggestions">
          {report.suggestions.map((t, i) => (
            <li key={i}><span className="mono num">{String(i + 1).padStart(2, "0")}</span><span>{t}</span></li>
          ))}
        </ol>
      </section>
    </div>
  );
}
