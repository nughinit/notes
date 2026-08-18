# Milestone: MongoDB perfeito

Baseado em `runtime/reports/final_audit/FINAL_AUDIT_REPORT.json` (status atual:
`PASS_WITH_KNOWN_EXCEPTION`, 91/92 tribunais em L8) e
`legal_calendar_mongodb_bootstrap_v2_filled/docs/DB_BUILD_CHECKLIST.md` do
projeto `legal_calendar_mongodb_v6_dejt_l8_candidate`.

Subtasks detalhadas em [mongodb-perfeito/](mongodb-perfeito/). Ordem sugerida:
itens isolados e sem dependência primeiro (1–3), depois os que tocam volume
maior de dados (4–7), infra (8) e por fim a verificação final (9).

## Tasks
- [x] [1. Resolver os 24 `open_gap_contradicts_l8`](mongodb-perfeito/01-open-gaps-contradicts-l8.md) ✅
- [x] [2. Levar `TRT19` de L7 para L8](mongodb-perfeito/02-trt19-l7-para-l8.md) ✅
- [x] [3. Corrigir os 10 `act_relations_broken_refs`](mongodb-perfeito/03-act-relations-broken-refs.md) ✅ (8/11 corrigidos, 3/11 gaps genuínos documentados)
- [ ] [4. Criar `change_events` faltantes](mongodb-perfeito/04-change-events-faltantes.md)
- [ ] [5. Commitar detecções `CHANGED` pendentes (`TRE-*`)](mongodb-perfeito/05-tre-changed-uncommitted.md)
- [ ] [6. Resolver `source_contracts` sem URL](mongodb-perfeito/06-source-contracts-sem-url.md)
- [ ] [7. Fechar exceção legada de `monitor_run` (`TRT3`/`TRT10`)](mongodb-perfeito/07-monitor-run-legacy-trt3-trt10.md)
- [ ] [8. Infra: índice em `provenance`](mongodb-perfeito/08-provenance-index.md)
- [ ] [9. Verificação final](mongodb-perfeito/09-verificacao-final.md)

## Referência
- Checklist original: `legal_calendar_mongodb_bootstrap_v2_filled/docs/DB_BUILD_CHECKLIST.md`
- Auditoria mais recente: `runtime/reports/final_audit/FINAL_AUDIT_REPORT.json`
  (gerado em 2026-08-18T09:42:44Z)
