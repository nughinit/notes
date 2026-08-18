# 8. Infra: índice em `provenance` — CONCLUÍDO ✅

- [x] Definidos dois índices: `court_id_1_created_at_-1` (consulta mais comum:
      histórico de proveniência por tribunal, mais recente primeiro) e
      `source_id_1` (busca por fonte), seguindo o mesmo padrão usado em
      `audit_log`/`source_checks`/`monitor_runs`
- [x] Criados diretamente no Atlas (`provenance` não tinha seção própria em
      `mongo/init.js` — é uma collection ad hoc adicionada por adapters
      posteriores, conforme comentário no próprio `audit_legal_calendar_atlas.py`)
- [x] Reauditoria confirma: `collection_no_secondary_index` não aparece mais
