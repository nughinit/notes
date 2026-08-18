# 1. Validação estrutural na normalização — CONCLUÍDO ✅ (CRÍTICO)

## Por que era o mais crítico
Achado real durante o milestone MongoDB perfeito: o normalizador trocava a
origem pelo alvo em relações `AMENDS`/`REVOKES` (regex pegando o número
errado do texto livre). Isso não gera erro nem alarme — o dado "parece"
válido e passa por todas as checagens de schema. Num produto jurídico, isso
significa risco de **prazo calculado errado sem qualquer sinal de alerta**.

## O que foi feito

- [x] Criado `scripts/act_relations_validator.py`: validador puro (sem I/O)
      que checa, além de "os ids resolvem?": ordenação temporal
      (`act.year >= target.year` para `AMENDS`/`REVOKES`/`RESTORES` — um ato
      não pode alterar um ato futuro), auto-referência, tipo de relação
      conhecido
- [x] Criados 9 testes de regressão em `tests/test_act_relations_validator.py`,
      usando os casos reais da investigação anterior como fixtures —
      incluindo o **formato exato do bug original** (act_id com o valor do
      alvo, target_act_id nulo) e um caso hipotético mais perigoso: origem e
      alvo trocados mas **ambos já existindo** em `legal_acts` (que checagens
      de schema sozinhas não pegariam — só a ordenação por data pega)
- [x] Checagem de consistência semântica adicionada a
      `scripts/audit_legal_calendar_atlas.py` como **crítico**
      (`act_relations_swapped_source_target`), usando `year` como proxy de
      data (já que `published_at` não está populado na maioria dos atos)
- [x] Revisão de outros extratores encontrou um **segundo caso real da mesma
      classe de erro**: o evento de calendário do TRE-PE
      (`40f357a55fb780f4...`) tinha `start_at` (11/08/2026) depois de
      `end_at` (10/08/2026) — o normalizador mapeou
      `moves_holiday.from`/`to` (um feriado *realocado* de uma data pra
      outra) como se fosse um intervalo `start_at`/`end_at`. Confirmado
      contra a fonte oficial (tre-pe.jus.br): o feriado de 11/08 foi
      transferido para 10/08/2026 — é um evento de **um dia só**, não um
      período
- [x] Corrigido o registro do TRE-PE: `start_at = end_at = 2026-08-10`,
      guardando `moved_from_date: 2026-08-11` como metadado
- [x] Checagem `calendar_events_inverted_date_range` adicionada à auditoria
      como crítico, para pegar automaticamente casos futuros dessa classe
- [x] Suíte completa de testes (`pytest tests/`) roda limpa: 54 passed
- [x] Reauditoria confirma: `STATUS PASS`, `critical=0`, `warn=0`

## Arquivos novos/alterados
- `scripts/act_relations_validator.py` (novo)
- `tests/test_act_relations_validator.py` (novo, 9 testes)
- `scripts/audit_legal_calendar_atlas.py` (2 checagens críticas novas:
  `act_relations_swapped_source_target`, `calendar_events_inverted_date_range`)
