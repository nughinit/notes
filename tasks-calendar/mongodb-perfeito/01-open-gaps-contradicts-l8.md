# 1. Resolver os 24 `open_gap_contradicts_l8` — CONCLUÍDO ✅

Tribunais afetados: `TJAP`, `TJBA`, `TJMS` (x2), `TJMT`, `TJPI`, `TJRR`, `TJSE`,
`TJSP`, `TJTO`, os 15 `TRE-*` e `TSE`.

- [x] Listar os registros de `coverage_gaps` com `resolved: false` nesses
      tribunais (na prática eram 25 documentos, não 24 — a auditoria contava
      um `court_id` duas vezes)
- [x] Para cada um, verificado em `courts.coverage`/`monitor_runs`: todos os
      25 gaps eram órfãos de um método de descoberta antigo e já superado
      (`tj_sitemap_discovery` → `tj_html_catalog`; `electoral_v2`/`electoral_l8`
      → `electoral_tre_sitemap` ou feed REST direto no caso do `TSE`) — cada
      tribunal já tinha `coverage.level: L8` com evidência válida de um
      `monitor_run` `SUCCESS` posterior
- [x] Marcados `resolved: true` via `scripts/resolve_orphaned_coverage_gaps.py`,
      com `resolved_by_monitor_run` apontando para o `monitor_run` que
      comprova a correção
- [x] Reauditoria confirmou: `open_gap_contradicts_l8` não aparece mais em
      `warn` no `FINAL_AUDIT_REPORT.json`

Script usado (mantido no repo do projeto):
`scripts/resolve_orphaned_coverage_gaps.py`
