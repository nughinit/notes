# Milestone: MongoDB perfeito — status real (revisado)

> Revisado em 2026-08-18 comparando este documento com
> `runtime_final_audit/FINAL_AUDIT_REPORT.json` (gerado
> 2026-08-18T21:18:11Z) e o código atual do projeto
> `legal_calendar_mongodb_v6_dejt_l8_candidate`. A versão anterior deste
> arquivo afirmava `STATUS PASS`, `critical=0`, `warn=0` — **isso não é o que
> a auditoria mais recente mostra**. Ver [TRIBUNAIS_REGISTRO](TRIBUNAIS_REGISTRO.md)
> para o detalhe por tribunal.

## Status real (auditoria mais recente)

- `status`: **`PASS_WITH_KNOWN_EXCEPTION`** (não é `PASS` limpo)
- `critical`: 0
- `warn`: **1 categoria aberta** — `open_coverage_gaps`, 21 tribunais com
  `SOURCE_COVERAGE_GAP` não resolvido (falta cadeia real de
  alteração/revogação para provar L7)
- Cobertura: **92/92 tribunais em L8** — este ponto estava correto no
  documento original
- Gaps por tipo (coleção `coverage_gaps`, `resolved != true`):
  `SOURCE_COVERAGE_GAP` (21). Outros tipos (`CONTRACT_UNVERIFIED`,
  `SOURCE_TEMPORARILY_UNAVAILABLE`, `TRANSPORT_BLOCKED`, `SOURCE_GAP`)
  aparecem na coleção mas já estão marcados `resolved: true`.

## Tasks (histórico — subtasks abaixo referem-se a uma auditoria anterior,
já corrigida; mantidas para rastreabilidade)
- [x] [1. Resolver os 24 `open_gap_contradicts_l8`](mongodb-perfeito/01-open-gaps-contradicts-l8.md) ✅
- [x] [2. Levar `TRT19` de L7 para L8](mongodb-perfeito/02-trt19-l7-para-l8.md) ✅
- [x] [3. Corrigir os 10 `act_relations_broken_refs`](mongodb-perfeito/03-act-relations-broken-refs.md) ✅ (8/11 corrigidos, 3/11 gaps genuínos documentados)
- [x] [4. Criar `change_events` faltantes](mongodb-perfeito/04-change-events-faltantes.md) ✅
- [x] [5. Commitar detecções `CHANGED` pendentes (`TRE-*`)](mongodb-perfeito/05-tre-changed-uncommitted.md) ✅ (nenhuma era mudança real — órfãs/transitórias)
- [x] [6. Resolver `source_contracts` sem URL](mongodb-perfeito/06-source-contracts-sem-url.md) ✅
- [x] [7. Fechar exceção legada de `monitor_run` (`TRT3`/`TRT10`)](mongodb-perfeito/07-monitor-run-legacy-trt3-trt10.md) ✅
- [x] [8. Infra: índice em `provenance`](mongodb-perfeito/08-provenance-index.md) ✅
- [x] [9. Verificação final](mongodb-perfeito/09-verificacao-final.md) ✅

## Pendência real remanescente

- [ ] Resolver (ou documentar como aceitável) os 21 `SOURCE_COVERAGE_GAP`
      abertos — ver lista completa em
      [TRIBUNAIS_REGISTRO.md](TRIBUNAIS_REGISTRO.md). Sem isso, o status
      correto do milestone é "concluído com exceção conhecida", não
      "concluído".

## Referência
- Checklist original: `legal_calendar_mongodb_bootstrap_v2_filled/docs/DB_BUILD_CHECKLIST.md`
- Auditoria mais recente usada nesta revisão: `runtime_final_audit/FINAL_AUDIT_REPORT.json`
  (gerado em 2026-08-18T21:18:11Z)
