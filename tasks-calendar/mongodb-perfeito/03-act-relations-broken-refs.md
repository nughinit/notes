# 3. Corrigir os 10 `act_relations_broken_refs` — CONCLUÍDO ✅

Eram na prática 11 documentos (não 10 — mesmo padrão de contagem da subtask 1).

## Causa raiz encontrada
O schema (`docs/MONGODB_SCHEMA.md`) define a convenção: `act_id` = o ato que
faz a alteração, `target_act_id` = o ato alterado. O normalizador tinha um bug:
gravava o **ato alvo** no campo `act_id` e nunca resolvia o ato de origem real
(disponível no campo `act`/`raw_payload` da evidência), deixando
`target_act_id: null` com `status: TARGET_RESOLUTION_PENDING`.

## Resultado
- [x] **8 de 11** corrigidos de verdade — confirmado cruzando cada evidência
      (`legal_evidence.act` / `raw_payload.changes`) para achar o ato de
      origem real; ambos os lados (origem e alvo) já existiam em `legal_acts`.
      Script: `scripts/fix_act_relations_broken_refs.py`
      - `TRE-AM` (x2), `TRE-CE`, `TRE-DF` (x2), `TRE-ES`, `TRE-GO`, `TRE-MT`
- [x] **3 de 11** são gaps genuínos, não bugs — o ato alvo mencionado na
      evidência nunca foi capturado como documento próprio em `legal_acts`:
      - `TRT11` (`rel_12c8c9cc...`): auto-republicação sem versão anterior
        distinta capturada
      - `TRT13` (`rel_6bd5dfdc...`): falta capturar Ato 075/2026
      - `TRT18` (`rel_72b3ee93...`): falta capturar Portaria 2564/2024
      Marcados com `status: TARGET_ACT_NOT_CAPTURED` + `resolution_note`
      diretamente no próprio `act_relations` (não duplicado em
      `coverage_gaps`, que é usado para acesso à fonte do tribunal, não para
      completude de um ato específico — tentativa inicial de documentar lá
      reacionou `open_gap_contradicts_l8` por engano, revertida)
- [x] `scripts/audit_legal_calendar_atlas.py` ajustado: `act_relations_broken_refs`
      agora só dispara para casos não explicados; `act_id` inválido virou
      `act_relations_broken_source` (crítico, bug estrutural real);
      `target_act_id` ausente com `status: TARGET_ACT_NOT_CAPTURED` não conta
      mais como "quebrado" — é uma pendência documentada
- [x] Reauditoria confirma: `act_relations_broken_refs` não aparece mais,
      `critical=0`

Scripts usados/criados (mantidos no repo do projeto):
- `scripts/fix_act_relations_broken_refs.py` (novo)
- `scripts/audit_legal_calendar_atlas.py` (`audit_knowledge_layer` ajustada)
