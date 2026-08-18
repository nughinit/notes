# 11. Migrar os 17 tribunais restantes em sitemap genérico — 11/17 CORRIGIDOS ✅

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

## TJRS — corrigido em 2026-08-18 (backend de busca real encontrado)
Investigação em duas etapas.

**Primeira etapa (achado inicial, descartado):** `tjrs.jus.br` tem dois
mecanismos de busca full-text baseados num Google Search Appliance (GSA)
legado — nenhum dos dois serve como fonte viva:
- aba `pa` ("Publicações Administrativas",
  `www3.tjrs.jus.br/legisla/publ_adm_xml/...`): **travado em 2016** —
  mesmo filtrando explicitamente por ano=2026 + tipo=Portaria no formulário
  de filtro da própria UI, retorna **zero resultados** (não é só
  deprioridade por relevância, o índice genuinamente não tem nada de 2026)
- aba `dag` ("Diário da Justiça", "últimos 2 anos" /
  `dj_principal.php`+GSA): menos obsoleto, mas ainda **~18 meses
  desatualizado** (resultado mais recente de fev/2025, tanto na busca
  "exata" quanto na "livre")

Também testei o Diário Oficial do Estado do RS
(`diariooficial.rs.gov.br`, backend REST real `doe-backend.pro.rs.gov.br/
public/materias/?...&entidade=...`, confirmado vivo e atualizado no mesmo
dia) — mas o TJRS (Poder Judiciário) **não publica lá**: o filtro
`filtroEntidades` da API só lista órgãos do Poder Executivo. Não é a fonte
certa.

**Achado real:** a home do TJRS (`tjrs.jus.br/novo/`) embute um widget
"Diário da Justiça" com link pra edição **atual**, ex.:
`servicos/diario_justica/dj_principal.php?tp=0&ed=8204&pag=1` — um
paginador PHP legado que **não é indexado pela busca GSA**, e cujo número
de edição é sempre o mais recente. Confirmado genuinamente vivo: os
metadados do PDF da página 1 dessa edição têm `CreationDate` de
17/08/2026 (ontem) e citam "Ato nº 110/2026-P" real, referenciando outro
ato de abril/2026.

Pipeline sem browser (GET simples):
1. GET da home → extrai o número da edição atual via regex no link do
   widget
2. GET em `dj_principal.php?tp=0&ed=<N>&pag=1` → extrai o campo oculto
   `ult` (última página)
3. GET em `chama_pag_move.php?tp=0&ed=<N>&ult=<ULT>&pag=1&...` → PDF puro
   da página 1 (a home redireciona uma vez por sessão, seguido
   automaticamente pelo `urllib`)
4. Extrai texto do PDF com `pypdf`, valida com
   `content_structure_validator` (citação de ato real + ano + palavra-chave
   legal), canonicaliza por hash do texto semântico

- [x] `scripts/run_tjrs_dje_l8.py` criado, rodado, proposta aprovada
      (`approved_by: Nicole`), contrato antigo (`tj_sitemap_discovery`)
      superado
- [x] `pypdf` adicionado a
      `legal_calendar_mongodb_bootstrap_v2_filled/requirements.txt`
- [x] Auditoria final: `STATUS PASS`, `critical=0`, `warn=0`; 62/62 testes

## 2 corrigidos numa segunda rodada (2026-08-18, TJES e TJRJ)
Mesmo padrão: navegar um nível mais fundo a partir da página de categoria já
conhecida. `scripts/run_tj_batch4_l8.py` (novo, cobre os 2 de uma vez), ambos
passaram na validação estrutural com citação de ato real e refetch
idempotente:

| Tribunal | Fonte real encontrada | Nota |
|---|---|---|
| TJES | `tjes.jus.br/publicacoes/atos-normativos-tjes/atos-normativos-2026/` (clicando no ano "2026" a partir do índice) | página estática simples, lista todos os Atos Normativos do ano com número/ementa/data de disponibilização; ato 137 disponibilizado no mesmo dia (18/08/2026); vários diretamente relevantes ao calendário (suspensão de expediente, prorrogação de prazo) |
| TJRJ | `www3.tjrj.jus.br/Atosofic2leg/Busca/CategoriaLegislacao?codigo=5` (menu "Atos Oficiais do PJERJ" → categoria Portarias) | sistema "Sophia Biblioteca Web", diferente do `consultadje` (ASP.NET postback) documentado em [09](09-migrar-diario-real.md) — 26 portarias reais, mais recente publicada 17/08/2026; exige cookie de sessão (`SBW.Terminal.Sessao`) obtido via redirect — resolvido com `http.cookiejar` no coletor, sem precisar de browser |

- [x] Ambos propostos via `promotion_gate` e aprovados
      (`approve_promotion.py --by "Nicole"`)
- [x] Contratos antigos (`tj_sitemap_discovery`) marcados `superseded`
- [x] Auditoria final: `STATUS PASS`, `critical=0`, `warn=0`; 62/62 testes

Nota: a primeira tentativa de coleta do TJRJ falhou (`NO_LEGAL_KEYWORD`)
porque o fetch inicial via `urllib` puro recebia só a casca vazia do SPA sem
o cookie de sessão — ficou uma proposta de promoção duplicada e órfã no
Mongo (`pending_promo_TJES_...` da tentativa anterior do TJES, que já tinha
funcionado); aprovada também por ser inofensiva (mesmo hash canônico).

## Os 6 restantes — ainda não corrigidos
| Tribunal | Situação |
|---|---|
| TJRO | nenhuma página de menu encontrada via `curl`; ainda precisa browser real |
| TRF6 | nenhuma página de menu encontrada via `curl`; ainda precisa browser real |
| TJMSP | home retorna 403 mesmo com browser real (não retestado); site pode estar bloqueando geral |
| TJPB | já documentado em [09](09-migrar-diario-real.md) — Cloudflare + JSF AJAX sem API direta |
| TRT17 | bloqueado por Human Verification numa rodada anterior (ver acima) |
| TJSC | bloqueado por CAPTCHA de imagem numa rodada anterior (ver acima) |

## Próximos passos sugeridos
- [ ] Para os sem menu encontrado (TJRO, TRF6, TJMSP): usar browser real
      (Playwright/Claude Browser) para ver o menu renderizado
- [ ] Para TRT17/TJSC (bloqueados por verificação humana/bot): avaliar se
      vale reter e tentar de novo mais tarde (pode ser rate-limit
      temporário por navegação rápida) ou se há fonte alternativa do
      mesmo tribunal
- [ ] Reavaliar aqui a opção de API paga (Escavador/Judit.io) discutida
      antes, para os casos que continuarem resistentes após uma segunda
      tentativa
- [ ] Nota geral do achado TJRS: quando um índice de busca institucional
      (GSA ou similar) existe mas parece obsoleto, vale checar se há um
      widget de "última edição" na home que não passa pela busca — foi
      esse o padrão que resolveu o TJRS depois de dois índices mortos
