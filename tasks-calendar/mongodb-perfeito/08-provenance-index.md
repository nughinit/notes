# 8. Infra: índice em `provenance`

- [ ] Definir chave de índice adequada para `provenance` (candidatos:
      `entity_type_1_entity_id_1`, seguindo o padrão usado em `audit_log`)
- [ ] Criar o índice via `mongo/init.js` ou script de migração
- [ ] Confirmar em `FINAL_AUDIT_REPORT.json` que `collection_no_secondary_index`
      não aponta mais para `provenance`
