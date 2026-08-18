# 4. Criar `change_events` para os 27 checks `CHANGED` sem evento

- [ ] Levantar os 27 `source_checks` com status `CHANGED` que não têm
      `change_events` correspondente
- [ ] Para cada um, criar o `change_events` com `court_id`, `source_id`,
      `detected_at` e o diff/motivo da mudança
- [ ] Rodar auditoria e confirmar zero em `changed_without_change_event`

Relacionado a [05-tre-changed-uncommitted.md](05-tre-changed-uncommitted.md) —
provável mesma leva de mudanças eleitorais não processadas.
