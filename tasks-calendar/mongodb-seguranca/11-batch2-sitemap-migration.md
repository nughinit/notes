# 11. Migrar os 17 tribunais restantes em sitemap genérico — 8/17 CORRIGIDOS ✅

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

## 3 corrigidos nesta rodada (2026-08-18, navegação um nível mais fundo)
Com browser real (Claude Browser), naveguei um nível mais fundo nos 6
candidatos que tinham página de categoria certa mas sem citação estática
(TJPR, TJMMG, TRT17, TRT1, TJSC, TJRS), submetendo a mesma busca que a UI de
cada site dispara e capturando a chamada de rede real por trás do
formulário. `scripts/run_tj_batch3_l8.py` (novo, cobre os 3 confirmados de
uma vez), todos passaram na validação estrutural (subtask 4) com citação de
ato real e refetch idempotente:

| Tribunal | Fonte real encontrada | Nota |
|---|---|---|
| TJPR | POST Liferay resource (`p_p_resource_id=/pesquisar`) em `tjpr.jus.br/legislacao-atos-normativos` → JSON estruturado | 43k+ registros, mais recente 17/08/2026 (ontem); sem p_auth/sessão, funciona headless |
| TJMMG | POST simples em `cp.tjmmg.jus.br/ConsultaAtosNormativos/index.php/Consulta/Pesquisa` | citações reais, ex. "Portaria n. 19/2026-CJM de 22/06/2026" |
| TRT1 | Link "Portarias" do menu leva a um repositório DSpace real, `bibliotecadigital.trt1.jus.br/jspui/handle/1001/82377` | 2091 itens, mais recente 14/08/2026; GET simples, sem auth |

- [x] Todos propostos via `promotion_gate` e aprovados
      (`approve_promotion.py --by "Nicole"`)
- [x] Contratos antigos (`tj_sitemap_discovery`) marcados `superseded`
- [x] Auditoria final: `STATUS PASS`, `critical=0`, `warn=0`; 62/62 testes

## 2 novos bloqueados por verificação humana/bot (não contornados)
- **TRT17** (`trt17.jus.br/web/legislacao/w/portarias`): página de
  documentos é um componente Angular que carrega via API própria
  (`cdn.trt17.jus.br/componentes/documentos`), mas ao navegar novamente
  para inspecionar a chamada de rede o site respondeu com um desafio
  **"Human Verification"** (bot detection). **Não contornado** — política
  proíbe.
- **TJSC** (`tjsc.jus.br/atos-normativos`): disparou uma página própria de
  "Verificação de segurança do portal institucional" pedindo o código de
  uma **imagem CAPTCHA** após navegação. **Não contornado.**

## TJRS — investigado, achado inconclusivo (índice de busca obsoleto)
`tjrs.jus.br` tem um mecanismo de busca real ("Publicações Administrativas",
aba `pa`) que usa um Google Search Appliance (GSA) legado
(`www3.tjrs.jus.br/legisla/publ_adm_xml/...`) — funciona via GET simples
(`novo/busca/?...&site=legisInternaFeed&aba=pa&q=portaria`), sem
autenticação, retorna resultados reais com citação de ato ("PORTARIA Nº
33/2016 - OE"). **Mas o índice está travado em 2016** — mesmo pedindo
ordenação por data (`sort=date:D:S:d1`), nenhum resultado mais recente que
2016 aparece, sugerindo que esse GSA legado não é mais alimentado (o site
migrou para outra infra de busca — o link "Legislação Administrativa do
TJRS" no menu principal não usa mais esse backend). Não é uma fonte viva
utilizável como está; ficaria como falso "corrigido" se promovido — por
isso não promovido. Precisaria achar o backend de busca atual (não o GSA
legado) numa sessão futura.

## Os 9 restantes — ainda não corrigidos
| Tribunal | Situação |
|---|---|
| TJES | página de categoria com poucas menções, provável página de categoria — não revisitado nesta rodada |
| TJRJ | página de categoria com só 1 menção — não revisitado nesta rodada; ver também [09](09-migrar-diario-real.md) (formulário ASP.NET) |
| TJRS | investigado nesta rodada — índice de busca real mas obsoleto (ver acima) |
| TJRO | nenhuma página de menu encontrada via `curl`; ainda precisa browser real |
| TRF6 | nenhuma página de menu encontrada via `curl`; ainda precisa browser real |
| TJMSP | home retorna 403 mesmo com browser real (não testado nesta rodada); site pode estar bloqueando geral |
| TJPB | já documentado em [09](09-migrar-diario-real.md) — Cloudflare + JSF AJAX sem API direta |
| TRT17 | bloqueado por Human Verification nesta rodada (ver acima) |
| TJSC | bloqueado por CAPTCHA de imagem nesta rodada (ver acima) |

## Próximos passos sugeridos
- [ ] Para TJES e TJRJ: repetir o mesmo padrão desta rodada (navegar um
      nível mais fundo, capturar a chamada de rede real por trás do
      formulário/busca de cada site)
- [ ] Para TJRS: achar o backend de busca atual (não o GSA legado
      travado em 2016) — provavelmente outro endpoint WordPress/REST
- [ ] Para os sem menu encontrado (TJRO, TRF6, TJMSP): usar browser real
      (Playwright/Claude Browser) para ver o menu renderizado
- [ ] Para TRT17/TJSC (bloqueados por verificação humana/bot nesta
      rodada): avaliar se vale reter e tentar de novo mais tarde (pode ser
      rate-limit temporário por navegação rápida) ou se há fonte
      alternativa do mesmo tribunal
- [ ] Reavaliar aqui a opção de API paga (Escavador/Judit.io) discutida
      antes, para os casos que continuarem resistentes após uma segunda
      tentativa
