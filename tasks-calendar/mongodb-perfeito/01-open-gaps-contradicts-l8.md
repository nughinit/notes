# 1. Resolver os 24 `open_gap_contradicts_l8`

Tribunais afetados: `TJAP`, `TJBA`, `TJMS` (x2), `TJMT`, `TJPI`, `TJRR`, `TJSE`,
`TJSP`, `TJTO`, os 15 `TRE-*` e `TSE`.

- [ ] Listar os 24 registros de `coverage_gaps` com `resolved: false` nesses
      tribunais
- [ ] Para cada um, verificar em `source_contracts`/`sources` se o
      `CONTRACT_UNVERIFIED`/`SOURCE_GAP` ainda é real ou já foi corrigido
      depois da última coleta
- [ ] Onde o gap já não se aplica: marcar `resolved: true` com referência ao
      `monitor_run` que comprova a correção
- [ ] Onde o gap é real: rodar o coletor L8 correspondente novamente
      (`scripts/run_state_court_discovery_l8.py`, `run_tj_sitemap_discovery_l8.py`
      etc.) para produzir evidência válida
- [ ] Reexecutar a auditoria e confirmar que `open_gap_contradicts_l8` some da
      lista de `warn`
