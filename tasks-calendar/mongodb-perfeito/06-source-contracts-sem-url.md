# 6. Resolver os 50 `source_contracts` sem URL — CONCLUÍDO ✅

Eram 49 documentos (não 50), cobrindo 46 tribunais únicos.

## Causa raiz
Mesmo padrão órfão das subtasks 1, 4 e 5: todos os 49 eram placeholders da
fase inicial de mapeamento (`status: MAPPED_NOT_EXECUTED`,
`exception_reason: NO_SOURCE_ASSIGNED_AWAITING_DISCOVERY`) — confirmado que
**os 46 tribunais já têm um contrato real e funcional** com URL sob outro
`_id` (ex: `contract_TJAC_tj_sitemap_discovery` já existe além do placeholder
`contract_be4149c5e7d85d3c7ea24df1` sem URL).

- [x] Confirmado: nenhum precisava de URL preenchida nem de depreciação — só
      de serem marcados como superados pelo contrato real
- [x] Marcados `superseded: True` + `superseded_by: <id do contrato real>` +
      nota explicativa
- [x] `scripts/audit_legal_calendar_atlas.py` ajustado: a checagem exclui
      contratos `superseded: True`
- [x] Reauditoria confirma: `source_contract_missing_url_legacy_exception`
      não aparece mais
