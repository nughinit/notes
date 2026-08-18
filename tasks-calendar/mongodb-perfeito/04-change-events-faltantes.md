# 4. Criar `change_events` faltantes — CONCLUÍDO ✅

Resolvida junto com a subtask 5 — eram, na prática, a mesma leva de 27 checks
`CHANGED` sem `checkpoint_advanced`, vistas por duas checagens diferentes da
auditoria. Ver [05-tre-changed-uncommitted.md](05-tre-changed-uncommitted.md)
para os detalhes da investigação e correção.

- [x] Levantados os 27 `source_checks` `CHANGED` sem `change_events`
- [x] Investigado caso a caso — nenhum era uma mudança real pendente de
      commit; todos eram artefatos órfãos ou detecções transitórias já
      superadas (ver detalhes na 05)
- [x] Reauditoria confirma: `changed_without_change_event` não aparece mais
