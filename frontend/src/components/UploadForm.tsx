import { useState, type DragEvent, type FormEvent } from "react";

const MAX_JD = 10000;

export default function UploadForm({ error, onSubmit }: { error?: string; onSubmit: (cv: File, jd: string) => void }) {
  const [cv, setCv] = useState<File | null>(null);
  const [jd, setJd] = useState("");
  const [dragging, setDragging] = useState(false);
  const [formError, setFormError] = useState("");

  function onDrop(e: DragEvent) {
    e.preventDefault();
    setDragging(false);
    setCv(e.dataTransfer.files[0] ?? null);
  }

  function submit(e: FormEvent) {
    e.preventDefault();
    if (!cv || cv.type !== "application/pdf") return setFormError("Carica il CV in PDF.");
    if (cv.size > 5 * 1024 * 1024) return setFormError("Il PDF supera 5 MB.");
    if (jd.trim().length < 20 || jd.length > MAX_JD) return setFormError("Incolla una job description (20–10000 caratteri).");
    setFormError("");
    onSubmit(cv, jd);
  }

  return (
    <form className="upload" onSubmit={submit} noValidate>
      <div className="hero">
        <h1>Score your CV against a job.</h1>
        <p className="muted">Five AI agents split the job into requirements, look for each one in your CV, score the match and prepare the interview questions.</p>
      </div>
      <div className="inputs">
        <div className="field">
          <label htmlFor="cv-input" className="kicker mono">01 · YOUR CV</label>
          <div
            className={`dropzone${dragging ? " dragging" : ""}`}
            onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
            onDragLeave={() => setDragging(false)}
            onDrop={onDrop}
          >
            <input id="cv-input" type="file" accept=".pdf" className="visually-hidden"
              onChange={(e) => setCv(e.target.files?.[0] ?? null)} />
            {cv ? (
              <div className="file-chip">
                <span className="file-name">{cv.name}</span>
                <span className="mono muted small">{(cv.size / 1024).toFixed(0)} KB</span>
                <button type="button" className="link" onClick={() => setCv(null)}>Remove</button>
              </div>
            ) : (
              <label htmlFor="cv-input" className="drop-prompt">
                <span className="drop-title">Drop your CV or <span className="browse">browse</span></span>
                <span className="mono muted small">PDF · max 5 MB</span>
              </label>
            )}
          </div>
        </div>
        <div className="field wide">
          <div className="label-row">
            <label htmlFor="jd" className="kicker mono">02 · JOB DESCRIPTION</label>
            <span className={`kicker mono${jd.length > MAX_JD ? " over" : ""}`}>{jd.length} / {MAX_JD}</span>
          </div>
          <textarea id="jd" value={jd} placeholder="Paste the job description here" onChange={(e) => setJd(e.target.value)} />
        </div>
      </div>
      {(formError || error) && <p className="error" role="alert">{formError || error}</p>}
      <div className="actions">
        <span className="mono muted small">Your CV is deleted from the server when the analysis ends.</span>
        <button type="submit" className="primary">Analyze<span className="btn-dot" /></button>
      </div>
    </form>
  );
}
