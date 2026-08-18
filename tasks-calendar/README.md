# tasks-calendar

Tasks do projeto `legal_calendar_mongodb_v6_dejt_l8_candidate`.

## Registro de tribunais
- [TRIBUNAIS_REGISTRO.md](TRIBUNAIS_REGISTRO.md) — snapshot de todos os 92
  tribunais, agrupados por família, com nível de cobertura, adapter/fluxo de
  coleta, fonte ativa e gaps abertos. Gerado a partir de consulta direta ao
  MongoDB — regenerar quando o pipeline mudar, não é atualizado sozinho.

## Milestones

- [x] [MongoDB perfeito](milestone-mongodb-perfeito.md) ⚠️ — concluído com
      exceção conhecida (revisado 2026-08-18): `STATUS PASS_WITH_KNOWN_EXCEPTION`,
      0 críticos, 1 warning (21 `SOURCE_COVERAGE_GAP` abertos), 92/92
      tribunais em L8.
- [ ] [API para Intimatio funcionando](milestone-api-intimatio.md) — não
      iniciado. Depende do milestone MongoDB perfeito (concluído — pode
      começar).
- [ ] [MongoDB 2 — Segurança da triagem](milestone-mongodb-2-seguranca.md) —
      não iniciado. Vulnerabilidades do pipeline de coleta/triagem de
      portarias, priorizadas por criticidade.
