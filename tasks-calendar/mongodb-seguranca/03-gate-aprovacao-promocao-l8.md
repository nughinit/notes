# 3. Gate de aprovação antes de promoção a L8 / resolução de gap — PARCIAL ⚠️ (ALTO)

Módulo e mecanismo criados e testados ponta a ponta; retrofit aplicado em
**1 de ~18 scripts** que hoje escrevem no Atlas — os demais continuam
escrevendo direto (ver "Status do retrofit" abaixo).

## O que foi criado
- [x] `scripts/promotion_gate.py` — separa **propor** de **aprovar**:
  - `propose_l8_promotion()` / `propose_gap_resolution()`: gravam um pedido
    `PENDING` em `promotion_gate_requests`, sem tocar em
    `courts.coverage`/`coverage_gaps` — são as funções que um coletor chama
  - `approve_l8_promotion()` / `approve_gap_resolution()`: só essas aplicam
    a mudança de verdade, e **exigem `approved_by`** (`ValueError` se
    ausente) — gravam `approved_by` tanto no pedido quanto no `audit_log`
    (`audit_log.actor` continua sendo o script, mas agora existe
    `audit_log.approved_by` com o nome de uma pessoa)
  - Rejeita dupla aprovação (`status` já não é `PENDING`)
- [x] `scripts/approve_promotion.py` — CLI humano:
  `python scripts/approve_promotion.py --list` e
  `--approve <id> --by "Nome"`
- [x] Testado ponta a ponta contra o Atlas real com IDs fictícios
      (`ZZ-GATE-TEST-PROBE`): propor → listar → rejeitar aprovação sem nome →
      aprovar → rejeitar segunda aprovação → mesmo fluxo para gap → limpeza.
      Tudo funcionou como esperado

## Retrofit no coletor de referência
- [x] `scripts/run_trt19_boletim_l8.py` (o coletor mais novo, desta sessão)
      trocado: `promote()`/`resolve_old_gap()` → `propose_promotion()`/
      `propose_gap_resolution_for_old_gap()`. Agora, se rodado de novo, ele
      **propõe** em vez de aplicar direto — precisa de
      `approve_promotion.py --approve ... --by ...` pra virar fato no banco
- [x] Auditoria (`STATUS PASS`) e suíte de testes (54 passed) confirmadas
      depois do retrofit

## Status do retrofit — pendente nos demais
Ainda escrevem `courts.coverage`/`coverage_gaps.resolved` **diretamente**,
sem o gate:
- `run_tj_html_catalog_l8.py`, `run_tj_sitemap_discovery_l8.py`,
  `run_state_court_discovery_l8.py`, `run_electoral_tre_sitemap_l8.py`,
  `run_electoral_batch_l8.py`, `run_electoral_tse_l8.py`,
  `run_tjrn_atos_l8.py`, `run_trt19_browser_l8.py`, `run_dejt_*` e demais
  scripts administrativos ad hoc usados nesta sessão
      (`resolve_orphaned_coverage_gaps.py`, `fix_act_relations_broken_refs.py`)

Retrofit desses fica como próxima rodada — o padrão está pronto e validado,
falta replicar `promote()`/gap-resolution → `propose_*()` em cada um (troca
mecânica, mas ~15 arquivos).

## Ainda não feito
- [ ] Documentar formalmente quem tem acesso de escrita ao Atlas hoje —
      hoje é um único usuário (`nughinit_db_user`, papel `atlasAdmin`,
      achado na subtask 2) usado por toda automação; não há múltiplas
      pessoas/credenciais a documentar ainda, mas fica registrado que
      **não há separação de identidade por operador** — todo `audit_log.actor`
      antes deste retrofit é sempre o nome do script, nunca uma pessoa
