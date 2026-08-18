# 7. Fechar exceção legada de `monitor_run` em `TRT3` e `TRT10` — CONCLUÍDO ✅

- [x] Investigado: ambos já tinham `source_contracts`, `source_snapshots` e
      `source_checks` reais (`real_execution: True`, status `NO_CHANGE`,
      checkpoint avançado) — só faltava o registro de `monitor_run`, que
      nunca chegou a ser criado numa execução anterior
- [x] Criado `monitor_run` retroativo para cada um, reaproveitando o
      timestamp real do `source_check` existente, marcado explicitamente
      `backfilled: True` com nota explicando a origem (não é um fetch novo,
      é o registro de bookkeeping que faltou para uma evidência já real)
- [x] Removida a necessidade da exceção legada: `db.monitor_runs.count_documents`
      agora retorna > 0 para ambos, então `l8_legacy_monitor_run_exception`
      deixa de disparar naturalmente (nenhuma mudança de código necessária
      além da já feita nas outras subtasks)
- [x] Reauditoria confirma: `l8_legacy_monitor_run_exception` não aparece mais
