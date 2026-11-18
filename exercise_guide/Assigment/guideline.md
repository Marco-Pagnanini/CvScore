# Esercizio guidato: aggiungere un nuovo agente

**Obiettivo:** creare l'agente `advisor` (Career Advisor) che scrive i suggerimenti per migliorare il CV.
Oggi i suggerimenti li scrive l'`evaluator`: li spostiamo in un agente dedicato (un agente = un compito).

**Cosa si impara**
- Com'è fatto un agente: prompt + tool permessi + una chiamata a `run(...)`.
- Per l'orchestrator un sub-agente è **solo un tool in più**.
- Aggiungere un agente non richiede di toccare API, modelli Pydantic, runner o server MCP.

**Tempo stimato:** 20-30 minuti. **File:** 1 nuovo + 4 modificati, circa 30 righe in tutto.

---

## Passo 0: capire come funziona un agente

Apri `backend/app/agents/jd_analyst.py`. Ogni agente ha sempre 3 parti:

```python
SYSTEM_PROMPT = """..."""          # 1. chi è e cosa deve rispondere
ALLOWED_TOOLS: list[str] = []      # 2. quali tool MCP può usare (nessuno qui)

async def run_agent(task: str) -> str:   # 3. il ciclo agentico è già scritto in runner.py
    return await run("jd_analyst", SYSTEM_PROMPT, ALLOWED_TOOLS, task)
```

Il flusso attuale è: `orchestrator` → `jd_analyst` → `cv_matcher` → `evaluator`.
Il flusso alla fine dell'esercizio sarà: `orchestrator` → `jd_analyst` → `cv_matcher` → `evaluator` → **`advisor`**.

---

## Passo 1: creare l'agente

**Crea** il file `backend/app/agents/advisor.py`:

```python
from app.agents.runner import run

SYSTEM_PROMPT = """You are the Career Advisor.
You receive the requirement matches of a CV against a job (verdict yes/partial/no with evidence).
Write up to 5 concrete, actionable suggestions to improve the CV for this job.
Focus on "no" and "partial" requirements, most important (must) first. Never invent experience the candidate does not have.
Reply ONLY with a JSON array of strings. No prose."""

ALLOWED_TOOLS: list[str] = []  # no tools: it only reasons on the matches it receives


async def run_agent(task: str) -> str:
    return await run("advisor", SYSTEM_PROMPT, ALLOWED_TOOLS, task)
```

> 💡 Il primo argomento di `run(...)` (`"advisor"`) è il nome che compare nel log live del frontend.

---

## Passo 2: registrare l'agente nell'orchestrator

**Modifica** `backend/app/agents/orchestrator.py`. Le modifiche sono 4.

**2a. Import:** aggiungi `advisor`.

```python
# PRIMA
from app.agents import cv_matcher, evaluator, jd_analyst
# DOPO
from app.agents import advisor, cv_matcher, evaluator, jd_analyst
```

**2b. Prompt:** aggiungi il passo 4 e prendi `suggestions` dall'advisor.

```python
# PRIMA
3. Send the matches to evaluator -> get score, summary, suggestions.
...
{"matches": [...from cv_matcher], "score": <the "score" object from evaluator>, "summary": <evaluator summary>, "suggestions": <evaluator suggestions>}. No prose."""

# DOPO
3. Send the matches to evaluator -> get score and summary.
4. Send the same matches to advisor -> get the suggestions.
...
{"matches": [...from cv_matcher], "score": <the "score" object from evaluator>, "summary": <evaluator summary>, "suggestions": <advisor reply>}. No prose."""
```

**2c. Tool permessi:** l'orchestrator può chiamare solo gli agenti in questa lista.

```python
ALLOWED_TOOLS = ["jd_analyst", "cv_matcher", "evaluator", "advisor"]
```

**2d. Collegamento nome → funzione:**

```python
SUB_AGENTS = {"jd_analyst": jd_analyst.run_agent, "cv_matcher": cv_matcher.run_agent,
              "evaluator": evaluator.run_agent, "advisor": advisor.run_agent}
```

> 💡 Perché funziona senza altro codice? `runner.py` trasforma ogni voce di `SUB_AGENTS` in un tool
> con input `{"task": "..."}`. Quando l'orchestrator "chiama il tool" `advisor`, il runner esegue `advisor.run_agent(task)`.

---

## Passo 3: togliere i suggerimenti all'evaluator

**Modifica** il prompt in `backend/app/agents/evaluator.py`:

```python
# PRIMA
never compute the score yourself. Then write a 2-3 sentence summary and up to 5 concrete suggestions
to improve the CV for this job (focus on "no" and "partial" requirements).
Reply ONLY with JSON {"score": <the compute_score result>, "summary": "...", "suggestions": ["..."]}. No prose."""

# DOPO
never compute the score yourself. Then write a 2-3 sentence summary.
Reply ONLY with JSON {"score": <the compute_score result>, "summary": "..."}. No prose."""
```

> 💡 Non è obbligatorio, ma evita che due agenti facciano lo stesso lavoro (single responsibility).

---

## Passo 4: frontend (solo estetica)

**Modifica** `frontend/src/components/LiveView.tsx`: aggiungi lo step e la sua etichetta.

```ts
const AGENTS = ["orchestrator", "jd_analyst", "cv_matcher", "evaluator", "advisor"];
const LABEL: Record<string, string> = {
  orchestrator: "Orchestrator", jd_analyst: "Job Description Analyst", cv_matcher: "CV Matcher", evaluator: "Evaluator",
  advisor: "Career Advisor",
};
```

**Modifica** `frontend/src/components/UploadForm.tsx`: nel testo, `Four AI agents` diventa `Five AI agents`.

> 💡 Anche senza questo passo tutto funziona: il log mostrerebbe il nome grezzo `advisor`.
> `ResultView.tsx` **non** va toccato, perché mostra già `report.suggestions`.

---

## Passo 5: ricostruire e provare

```bash
docker compose up -d --build
```

Apri http://localhost:3000, carica un CV e incolla una job description (vedi `job_applications_test.md`).

**Cosa devi vedere:**
- nel log live compare lo step **Career Advisor** dopo l'Evaluator;
- nel risultato ci sono i suggerimenti, come prima, ma ora li ha scritti l'advisor.

---

## Se qualcosa non va

| Sintomo | Causa probabile | Soluzione |
|---|---|---|
| Non cambia niente, l'advisor non compare | Il container usa ancora il codice vecchio | `docker compose up -d --build` (senza `--build` il codice nuovo non entra nell'immagine) |
| `ModuleNotFoundError: app.agents.advisor` | File con nome o cartella sbagliati | Il file deve essere esattamente `backend/app/agents/advisor.py` |
| L'orchestrator non chiama mai l'advisor | Manca in `ALLOWED_TOOLS` o in `SUB_AGENTS`, oppure manca il passo 4 nel prompt | Ricontrolla il Passo 2: servono **tutte e 4** le modifiche |
| Errore di validazione su `suggestions` | L'orchestrator non ha messo l'array dell'advisor nel JSON finale | Ricontrolla il JSON finale nel prompt (2b) |
| I suggerimenti compaiono due volte o sono strani | L'evaluator scrive ancora i suoi suggerimenti | Fai il Passo 3 |
| Lo step nel frontend si chiama `advisor` e non "Career Advisor" | Manca l'etichetta in `LABEL` | Passo 4 |

Per vedere gli errori del backend: `docker compose logs -f backend`.

---

## Per chi finisce prima (bonus)

1. **Dare un tool all'advisor.** Aggiungi in `backend/app/mcp_tools/tools.py` un tool, per esempio:
   ```python
   @mcp.tool()
   def course_catalog(skill: str) -> str:
       """Return a suggested free course to learn the given skill."""
       return f"Search '{skill} tutorial' on the official documentation or freeCodeCamp."
   ```
   Poi mettilo negli strumenti dell'advisor: `ALLOWED_TOOLS = ["course_catalog"]`. Prova a fargli suggerire un corso per ogni requisito "no".
2. **Rifletti:** ogni agente in più è una chiamata LLM in più (più tempo e più costo).
   Quando conviene un agente separato e quando basta allungare il prompt di uno esistente?
