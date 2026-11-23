# Esercizio: scrivere l'agente `recruiter`

**Obiettivo:** completare l'agente `recruiter`, che genera le domande che un recruiter farebbe al colloquio per la job description inserita.
Le domande compaiono nella pagina del risultato, nella sezione **INTERVIEW QUESTIONS**.

**Cosa si impara**
- Com'è fatto un agente: prompt + tool permessi + una chiamata a `run(...)`.
- Come si chiede a un LLM una risposta in formato fisso (un array JSON di stringhe).
- Come l'orchestrator usa un sub-agente senza che tu debba toccare altro.

**Tempo stimato:** 10-15 minuti. **File:** 1 modificato (`backend/app/agents/recruiter.py`), una decina di righe.

---

## Cosa c'è già

- L'orchestrator, il modello `Report` e la UI sono già collegati al recruiter. **Tu scrivi solo `recruiter.py`.**
- Finché non lo scrivi, l'agente restituisce una lista vuota: l'app funziona come prima, la sezione delle domande non compare e lo step "Recruiter" nel log resta grigio.

---

## Passo 0: avviare l'app e vedere com'è adesso

```bash
cp .env.example .env
```

Scrivi la tua `ANTHROPIC_API_KEY` nel file `.env`, poi:

```bash
docker compose up -d --build
```

Apri http://localhost:3000, carica un CV in PDF (per esempio `test_data/cv_clean.pdf`) e incolla una job description (vedi `test_data/job_applications_test.md`).
Nel risultato **non** c'è la sezione "INTERVIEW QUESTIONS".

---

## Passo 1: leggere

Apri `backend/app/agents/recruiter.py` e leggi i commenti in cima: spiegano obiettivo, formato della risposta e i 3 punti da completare.
Per un esempio di agente completo e senza tool guarda `backend/app/agents/jd_analyst.py`.

---

## Passo 2: scrivere i 3 pezzi

| Pezzo | Cosa deve contenere |
|---|---|
| `SYSTEM_PROMPT` | Chi è l'agente, cosa riceve (i requisiti del lavoro, ciascuno "must" o "nice"), quante domande scrivere, in che ordine, che tipo di domande, e il formato esatto della risposta |
| `ALLOWED_TOOLS` | La lista dei tool MCP che può usare. Ne ha bisogno di qualcuno? |
| `run_agent` | Una chiamata a `run(...)`: sostituisce il `return "[]"` provvisorio. Il primo argomento è il nome che compare nel log live |

---

## Passo 3: provare

Salva il file. Il backend si riavvia da solo (se non lo fa: `docker compose restart backend`).
Rilancia un'analisi.

**Cosa devi vedere:**
- nel log live lo step **Recruiter** si accende e poi risulta completato;
- nel risultato compare la sezione **INTERVIEW QUESTIONS** con le domande, la prima è sul requisito più importante.

---

## Se qualcosa non va

| Sintomo | Causa probabile | Soluzione |
|---|---|---|
| Nessuna sezione "INTERVIEW QUESTIONS" | `run_agent` restituisce ancora il valore provvisorio, o `SYSTEM_PROMPT` è vuoto | Ricontrolla il Passo 2 |
| Errore di validazione sul risultato | La risposta del recruiter non è un array JSON puro (c'è del testo prima o dopo, o un blocco di codice) | Rendi il formato della risposta più esplicito nel prompt |
| Il risultato arriva subito e il log degli agenti resta vuoto | Stesso CV e stessa job description di una prova precedente: l'app riusa il risultato salvato | Salvare un file in `backend/app` riavvia il server e lo svuota. Oppure cambia CV o job description |
| Lo score è diverso dalla prova di prima | Il server si è riavviato e l'LLM ha rivalutato il CV da zero: normale, non c'entra il tuo agente | Nessuna |

Per vedere gli errori del backend: `docker compose logs -f backend`.

---

## Per riflettere

1. Il recruiter riceve i requisiti già estratti e non la job description grezza. Perché è più sicuro?
2. Lo score cambierebbe se il recruiter scrivesse domande diverse? Perché?

## Bonus

Fai in modo che le domande tocchino i punti deboli del CV (i requisiti con verdetto `no` o `partial`).
Quali dati servono al recruiter, e in quale file devi cambiare cosa gli passa l'orchestrator?
