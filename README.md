# CvScore

Mini Agentic SOA per il laboratorio: carichi un CV (PDF) e incolli una job description, un'orchestra di agenti
restituisce uno score 0-100 spiegato requisito per requisito, dei suggerimenti e le domande da colloquio.

```
FastAPI (POST /api/analyze)
  └─ Orchestrator
       ├─ JD Analyst   → requisiti ("must" / "nice")
       ├─ CV Matcher   → verdetto yes / partial / no per ogni requisito (tool: read_cv)
       ├─ Evaluator    → score, riassunto, suggerimenti (tool: compute_score)
       └─ Recruiter    → domande per il colloquio
MCP server (/mcp) → services/cv.py (legge il PDF), services/score.py (la formula)
```

## Avvio

Servono Docker e una API key Anthropic.

```bash
cp .env.example .env        # poi scrivi la tua ANTHROPIC_API_KEY nel file .env
docker compose up -d --build
```

Apri http://localhost:3000.

- Le modifiche a `backend/app` si ricaricano da sole al salvataggio.
- Le modifiche al frontend richiedono di nuovo `docker compose up -d --build`.
- Log del backend: `docker compose logs -f backend`.

## Il laboratorio, in ordine

| # | Cosa fai | Dove | Come sai di aver finito |
|---|---|---|---|
| 1 | **Exercise 1**: scrivi i due tool MCP `read_cv` e `compute_score` | `backend/app/mcp_tools/tools.py` | `docker compose exec backend pytest tests/test_tools.py -q` è verde e l'analisi di un CV si completa |
| 2 | **Exercise 2**: prompt injection, da `VULNERABLE_PROMPT` a `SAFE_PROMPT` | `backend/app/agents/cv_matcher.py` | Con `test_data/cv_injected.pdf` lo score cambia tra i due prompt |
| 3 | **Assignment**: scrivi l'agente `recruiter` | `backend/app/agents/recruiter.py` | Compare la sezione INTERVIEW QUESTIONS nel risultato. Guida: `exercise_guide/Assignment/guideline_recruiter.md` |

Le slide del laboratorio descrivono ogni passo. Se un passo non si ricarica, la causa più comune è il container che usa ancora
il codice vecchio: `docker compose up -d --build`.

## Dati di prova

In `exercise_guide/test_data/`:

- `job_applications_test.md`: sette job description da incollare nel form (match alto, parziale, nullo, testo minimo, lingue miste).
- `cv_clean.pdf`: CV di un junior web developer (HTML, CSS, un po' di JavaScript).
- `cv_injected.pdf`: lo stesso CV con una nota "HR" scritta in bianco su bianco, invisibile a occhio ma letta dal modello.
  Per Exercise 2 usalo con la job description n. 6 ("Junior Python developer, conoscenza base di Git").

Lo stesso CV e la stessa job description restituiscono sempre lo stesso report (cache in memoria, si svuota al riavvio del server).

## Test

```bash
docker compose exec backend pytest -q
```

`test_score.py` controlla la formula dello score, `test_tools.py` i tool MCP dell'Exercise 1.
