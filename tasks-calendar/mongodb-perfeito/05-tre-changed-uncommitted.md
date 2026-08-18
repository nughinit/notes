# 5. Commitar as 26 detecções `CHANGED` pendentes — CONCLUÍDO ✅

Eram 27 no total (não 26), e nenhuma delas era uma mudança real esperando
commit — a investigação revelou dois padrões distintos, nenhum resolvível
apenas "virando a flag":

## 25 casos `TRE-*`: artefatos órfãos
Todos os 25 checks eram de um `source_id` (`*_ELECTORAL_OFFICIAL_DISCOVERY`)
vindo de um `monitor_run` com `status: REVIEW_DYNAMIC` — o mesmo padrão de
lote exploratório superado da subtask 1. Confirmado cruzando com
`source_contracts`: o `source_id` **ativo/promovido a L8** de cada um desses
tribunais é outro (`*_ELECTORAL_TRE_SITEMAP` ou equivalente) — esses checks
não fazem parte da linhagem de monitoramento viva.
- [x] Marcados `superseded: True` com nota explicando a causa, em
      `source_checks` e `monitor_runs`
- [x] `scripts/audit_legal_calendar_atlas.py` ajustado: `changed_detection_uncommitted`
      e `changed_without_change_event` agora excluem registros `superseded: True`

## 2 casos `TRT7`/`TRT4`: detecções transitórias já superadas
Achado decisivo: os `source_contracts` de ambos já tinham sido normalizados
por uma remediação de auditoria **do mesmo dia** (`migrated_by:
"audit-remediation-2026-08-18"`), apontando explicitamente para o check mais
recente (`NO_CHANGE`, checkpoint avançado) como o estado validado atual. Ou
seja: o `CHANGED` pendente foi uma variação de bytes momentânea que reverteu
antes de ser confirmada por um segundo fetch — não uma mudança real de
conteúdo.
- [x] Marcados `superseded: True` com nota explicando a causa

## Resultado
- [x] Reauditoria confirma: `changed_detection_uncommitted` e
      `changed_without_change_event` não aparecem mais, `critical=0`

Nenhum script novo foi necessário — a correção foi feita direto no banco
(consultas inline) e no ajuste da auditoria
(`scripts/audit_legal_calendar_atlas.py`).
