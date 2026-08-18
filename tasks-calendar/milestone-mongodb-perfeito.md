# Milestone: MongoDB perfeito

Baseado em `runtime/reports/final_audit/FINAL_AUDIT_REPORT.json` (status atual:
`PASS_WITH_KNOWN_EXCEPTION`, 91/92 tribunais em L8) e
`legal_calendar_mongodb_bootstrap_v2_filled/docs/DB_BUILD_CHECKLIST.md` do
projeto `legal_calendar_mongodb_v6_dejt_l8_candidate`.

## Tasks pendentes

- [ ] Levar `TRT19` de L7 para L8 (único tribunal ainda não coletado no nível L8)
- [ ] Resolver os 24 `open_gap_contradicts_l8` (gaps `CONTRACT_UNVERIFIED`/`SOURCE_GAP`
      abertos em tribunais já marcados como L8): `TJAP`, `TJBA`, `TJMS`, `TJMT`,
      `TJPI`, `TJRR`, `TJSE`, `TJSP`, `TJTO` e os 15 `TRE-*` + `TSE`
- [ ] Investigar e corrigir os 10 `act_relations_broken_refs` (referências
      quebradas em `act_relations`)
- [ ] Criar `change_events` para os 27 checks `CHANGED` sem evento correspondente
      (`changed_without_change_event`)
- [ ] Confirmar/commitar as 26 detecções `CHANGED` ainda não commitadas
      (`changed_detection_uncommitted`), todas em tribunais `TRE-*`
- [ ] Resolver as 50 `source_contracts` sem URL marcadas como exceção legada
      (`source_contract_missing_url_legacy_exception`)
- [ ] Fechar a exceção legada de `monitor_run` em `TRT3` e `TRT10`
      (`l8_legacy_monitor_run_exception`)
- [ ] Criar índice secundário na collection `provenance`
      (`collection_no_secondary_index`)
- [ ] Popular receipts reais de execução (source_snapshots/source_checks/monitor_runs)
      onde ainda faltam, conforme apontado em `START_READINESS_REPORT.json`
      (`blocking_before_l8`)
- [ ] Rodar `scripts/audit_legal_calendar_atlas.py` novamente e confirmar
      `FINAL_AUDIT_REPORT.json` com `status: PASS` sem `warn`

## Referência
- Checklist original: `legal_calendar_mongodb_bootstrap_v2_filled/docs/DB_BUILD_CHECKLIST.md`
- Auditoria mais recente: `runtime/reports/final_audit/FINAL_AUDIT_REPORT.json`
  (gerado em 2026-08-18T09:42:44Z)
