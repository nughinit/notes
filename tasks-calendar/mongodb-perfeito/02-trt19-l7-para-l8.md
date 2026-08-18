# 2. Levar `TRT19` de L7 para L8 — CONCLUÍDO ✅

Único tribunal ainda não coletado no nível L8.

- [x] Confirmado qual coletor cobre `TRT19`: nenhum ainda cobria — o bloqueio
      anterior (`gap_TRT19_final`, `TRANSPORT_BLOCKED`) registrava
      `site.trt19.jus.br` retornando um 403 do CloudFront disfarçado de HTTP
      200, e o endpoint nacional compartilhado do DEJT (`dejt.jt.jus.br`) em
      503
- [x] Reverificado em 2026-08-18: `site.trt19.jus.br` está de volta ao ar com
      conteúdo real (portal Drupal 10 completo, não mais disfarce). O DEJT
      nacional continua 503, mas isso é secundário — o portal próprio do
      tribunal já basta como fonte
- [x] Explorado o menu real do site (não inventada nenhuma URL): item
      "Legislação → Documentos Administrativos" aponta para
      `https://portal.trt19.jus.br/boletim-interno/public`, que redireciona
      para `https://boletim.trt19.jus.br/boletim-interno/public` — o Boletim
      Interno do TRT19, publicando Portarias/Resoluções reais
- [x] Validado: fetch duplo com hash idêntico (`raw_sha256` e `semantic_hash`
      estáveis), conteúdo passa no filtro semântico de catálogo legal
- [x] Rodado `scripts/run_trt19_boletim_l8.py` (novo runner, mesmo padrão dos
      demais coletores L8): gerou `source_snapshots`, `monitor_runs`,
      `source_checks`, `provenance`, promoveu `courts.TRT19.coverage.level`
      para `L8` e marcou `gap_TRT19_final` como `resolved`
- [x] Corrigido `scripts/audit_legal_calendar_atlas.py`: a auditoria tinha uma
      regra fixa esperando `TRT19` permanecer em L7 para sempre (suposição
      válida enquanto o bloqueio parecia permanente); atualizada para refletir
      que os 92 tribunais podem estar em L8
- [x] Reauditoria confirma: `courts=92 distribution={'L8': 92}`, `critical=0`

Scripts usados/criados (mantidos no repo do projeto):
- `scripts/run_trt19_boletim_l8.py` (novo)
- `scripts/audit_legal_calendar_atlas.py` (regra do TRT19 atualizada)
