# 11. Migrar os 17 tribunais restantes em sitemap genérico — 5/17 CORRIGIDOS ✅

Origem: levantamento pedido pelo usuário para saber quais dos 92 tribunais
ainda usam fonte fraca (`TJ_SITEMAP_DISCOVERY`/`WORDPRESS_SITEMAP_BROWSER`/
`SUPERIOR_FEDERAL_BROWSER`) e poderiam ser corrigidos com o mesmo padrão do
TRT19/TJAL. Eram 20 no total; TJGO e TJPA já foram corrigidos via API (ver
[09-migrar-diario-real.md](09-migrar-diario-real.md)). Este documento cobre
os 17 restantes.

## Achado inicial: quase nenhum é SPA
Escaneei os 17 (`curl` na home, procurando `id="app"`/`id="root"`/`ng-app`) —
só TJGO/TJPA (já corrigidos) tinham cara de SPA moderna. Os outros 17 são
sites tradicionais renderizados no servidor — não precisam de investigação
de API escondida, precisam do padrão mais simples: navegar o menu real,
achar a página de atos normativos, validar conteúdo.

## 5 corrigidos nesta rodada
Rodando `scripts/run_tj_html_catalog_batch2_l8.py` (novo, cobre os 5 de uma
vez), todos passaram na validação estrutural (subtask 4) com citação de ato
real:

| Tribunal | URL real encontrada | Nota |
|---|---|---|
| TJAC | `tjac.jus.br/atos-normativos/portarias_presi/` | citação de 2026 |
| TJDFT | `tjdft.jus.br/institucional/escola/normas` | citações 2016-2024 |
| TJMA | `tjma.jus.br/atos/portal/geral/0/128/pnao/portariastj` | citações 2025/2026 |
| TJCE | `tjce.jus.br/atos_normativos` | citação de 2026 |
| TRT24 | `trt24.jus.br/web/guest/portarias` | citações de 2026 |

- [x] Todos propostos via `promotion_gate` e aprovados
      (`approve_promotion.py --by "Nicole"`)
- [x] Contratos antigos (`tj_sitemap_discovery`) marcados `superseded`
- [x] Auditoria final: `STATUS PASS`, `critical=0`, `warn=0`; 62/62 testes

## Os 12 restantes — investigados, não corrigidos ainda
Padrão comum: a página encontrada no menu tem palavras-chave reais mas
**sem citação de número de ato na própria página estática** — o conteúdo
real provavelmente carrega via paginação/JS/busca, exigindo navegação mais
profunda (clicar num item específico) em vez de só ler a página inicial da
seção:

| Tribunal | Página achada | Problema |
|---|---|---|
| TJPR | `tjpr.jus.br/legislacao-atos-normativos` | palavras-chave ok, sem citação numérica na página |
| TJMMG | `cp.tjmmg.jus.br/ConsultaAtosNormativos/` | 44 menções a "Portaria", sem citação numérica direta |
| TRT17 | `trt17.jus.br/web/legislacao/w/portarias` | boa densidade, sem citação capturada (provável paginação) |
| TRT1 | `trt1.jus.br/web/guest/trt-1-regiao-atos-resolucoes-outros` | é uma página de busca/índice, "1001/2031" não é citação real |
| TJES | `tjes.jus.br/publicacoes/atos-normativos-tjes/` | poucas menções, provável página de categoria |
| TJRJ | `tjrj.jus.br/web/portal-conhecimento/legislacao` | só 1 menção, provável página de categoria |
| TJSC | `tjsc.jus.br/atos-normativos` | só 1 menção, provável página de categoria |
| TJRS | `tjrs.jus.br/novo/jurisprudencia-e-legislacao/legislacao/...` | poucas menções; tentei `/wp-json/wp/v2/` (é WordPress) mas está bloqueado (403) |
| TJRO | nenhuma página de menu encontrada nesta busca | precisa investigação mais profunda (só achou editais de licitação) |
| TRF6 | nenhuma página de menu encontrada | idem |
| TJMSP | nenhuma página de menu encontrada, home retorna 403 | site pode estar bloqueando geral |
| TJPB | já documentado em [09](09-migrar-diario-real.md) | Cloudflare + JSF AJAX sem API direta |

## Próximos passos sugeridos
- [ ] Para os que têm página de categoria mas sem citação (TJPR, TJMMG,
      TRT17, TJES, TJRJ, TJSC, TJRS): navegar um nível mais fundo (clicar
      num item específico da lista) para confirmar se existe conteúdo real
      capturável, ou se genuinamente exigem busca/paginação JS
- [ ] Para os sem menu encontrado (TJRO, TRF6, TJMSP): usar browser real
      (Playwright) para ver o menu renderizado, já que a busca por `curl`
      pode ter perdido um menu carregado via JS mesmo em site não-SPA
- [ ] Reavaliar aqui a opção de API paga (Escavador/Judit.io) discutida
      antes, para os casos que continuarem resistentes após uma segunda
      tentativa
