# Note per i docenti

Questo file esiste solo nel branch `solution`.

## Branch

- `main`: versione per gli studenti. `tools.py` ha due TODO vuoti (Exercise 1), `recruiter.py` è uno stub (Assignment).
- `solution`: come `main`, con `tools.py` e `recruiter.py` completi. Quando cambi `main`, fai il merge di `main` in `solution`.

L'unico altro punto da toccare a mano è Exercise 2: in `cv_matcher.py` l'ultima riga è
`SYSTEM_PROMPT = VULNERABLE_PROMPT + RULES`. Per passare al prompt sicuro diventa `SAFE_PROMPT + RULES`
(non `SAFE_PROMPT` da solo: si perderebbero le regole di verdetto che rendono i risultati ripetibili).

## Risposte alle domande di riflessione del recruiter

1. **Perché ricevere i requisiti già estratti e non la job description grezza?** La job description è testo scritto da terzi
   e può contenere marketing, rumore o istruzioni travestite. Il JD Analyst la riduce a requisiti strutturati: il recruiter
   lavora solo su dati già filtrati, e il suo input ha un formato noto.
2. **Lo score cambierebbe se il recruiter scrivesse domande diverse?** No. Lo score è calcolato da `services/score.py` a partire
   dai `matches` del CV Matcher; il recruiter non vede né il CV né i verdetti e il suo output non entra nella formula.

## Bonus: domande sui punti deboli del CV

Al recruiter servono i requisiti con verdetto `no` o `partial`, cioè i `matches` del CV Matcher. Va cambiato `orchestrator.py`:
il passo 4 del prompt deve inviare al recruiter i `matches` (o solo quelli con verdetto `no`/`partial`) invece dei requisiti,
e il prompt del recruiter deve dire come usarli. Nessun altro file cambia.

## Controlli prima della lezione

- `docker compose exec backend pytest -q` è verde (6 test).
- Con `test_data/cv_injected.pdf` e la job description n. 6: prompt vulnerabile contro prompt sicuro. Annota gli score reali
  e confrontali con quelli mostrati nelle slide.
- Un'analisi completa mostra lo step Recruiter nel log e la sezione INTERVIEW QUESTIONS nel risultato.
