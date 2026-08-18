# 11. Migrar os 17 tribunais restantes em sitemap genérico — 14/17 CORRIGIDOS ✅

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

## TRF6 — corrigido em 2026-08-18 (browser real achou o menu que o `curl` não achava)
Com browser real (Claude Browser), naveguei Home → "Publicações" →
"Atos Administrativos" → **"Principais Atos do TRF6"**
(`portal.trf6.jus.br/institucional/publicacoes/atos-administrativos/principais-atos-do-trf6/`):
uma tabela WordPress/Oxygen simples e estática, sem SPA nem chamada de
API separada — confirmado via `read_network_requests` que a própria
requisição HTML principal (200) já traz a tabela. Citações reais, ex.
"Portaria Conjunta 3ª Vcrim e 13ª Vara n. 1, de 13 de agosto de 2026",
mais recente 14/08/2026 (ontem). O `curl` anterior provavelmente não
achou porque a URL fica dois níveis dentro do menu "Publicações" (não é
alcançável só pela home).

Pipeline sem browser: GET simples (`urllib`), sem cookie, sem sessão —
`scripts/run_tj_batch5_l8.py` (novo, cobre só TRF6), passou na validação
estrutural (subtask 4) com citação de ato real e refetch idempotente
(hash canônico igual nas duas coletas).

- [x] Proposto via `promotion_gate` e aprovado (`approve_promotion.py
      --approve pending_promo_TRF6_c88bddcff60f44e0 --by "Nicole"`)
- [x] Contrato antigo (`contract_TRF6_tj_sitemap_discovery`) marcado
      `superseded`
- [x] Auditoria final: `STATUS PASS`, `critical=0`, `warn=0`; 62/62 testes

## TJRO e TJMSP — investigados com browser real, continuam bloqueados (Akamai, não contornados)
Ambos usam mitigação de bot da Akamai, mas se manifestam diferente:

- **TJRO** (`tjro.jus.br`): a navegação da home com browser real é
  bloqueada direto — página "STIC - Página Bloqueada", "Seu acesso a
  esta página foi bloqueado por suspeita de robotização". O `curl` puro
  retorna HTTP 200, mas o corpo é um script de desafio Akamai ofuscado
  (`window["loaderConfig"] = "/TSPD/?type=20"`), não a página real — ou
  seja, "200" é enganoso, não é conteúdo utilizável. Mais restritivo que
  o TJMSP: aqui nem o browser real passa.
- **TJMSP** (`tjmsp.jus.br`): o browser real funciona bem e encontrei a
  fonte certa — Publicações → **"Atos e Comunicados"**
  (`tjmsp.jus.br/atos-e-comunicados/`), uma listagem JetEngine/
  JetSmartFilters de Resoluções/Portarias/Comunicados/Instruções/
  Provimentos já populada sem precisar submeter busca (ex. "Portaria nº
  2027/2026-Corregedoria Geral da JMESP", 13/08/2026, regulamenta
  Resolução nº 135/2026). Mas **toda requisição via `curl`/`urllib`
  recebe HTTP 403 da Akamai, inclusive na home**, mesmo com headers
  completos de browser (`User-Agent`, `Accept`, `Accept-Language`) — não
  é bloqueio por User-Agent, é fingerprinting de TLS/comportamento que o
  `curl` não consegue replicar.

Em ambos os casos, **não contornado** — política proíbe. A diferença
prática de TRT17/TJSC (bloqueados por CAPTCHA de imagem/verificação
humana explícita) é que aqui não há um desafio para "resolver": mesmo
sem CAPTCHA visível, o site rejeita qualquer cliente HTTP simples,
então a única forma de automatizar seria rodar um browser completo a
cada ciclo de coleta — fora do escopo hoje, mesma categoria de risco
já sinalizada na subtask
[7](07-revisar-bypass-antibot.md).

## TJPB — corrigido em 2026-08-18 (o "precisa de Cloudflare bypass" documentado antes não se confirmou)
A nota anterior (subtask [09](09-migrar-diario-real.md)) dizia que
`app.tjpb.jus.br/dje/.../buscas.jsf` era protegido por desafio Cloudflare
(JS proof-of-work) e que os links de edição eram só JSF AJAX sem endpoint
REST direto — presumido como precisando de Playwright. Reinvestigado com
browser real primeiro pra ver a chamada de rede real por trás do clique,
depois confirmado que **tanto o GET inicial quanto o POST do postback
funcionam com `urllib` puro + `http.cookiejar`, sem executar JS nenhum**:
o script "challenge-platform" da Cloudflare presente na página é telemetria
passiva de bot-management, não bloqueia essas requisições.

Pipeline sem browser:
1. GET `buscas.jsf` com um `CookieJar` novo (sessão + `JSESSIONID`)
2. Regex extrai `javax.faces.ViewState` e o par nome/valor do postback JSF
   do primeiro link "Diário de DD/MM/YYYY" (via seu atributo
   `onclick="mojarra.jsfcljs(...)"`) — lido da página, não fixo no código,
   pra não quebrar silenciosamente se a numeração dos componentes Mojarra
   mudar
3. POST na mesma URL (mesmos cookies) com os 3 campos → PDF puro
   (`Content-Disposition: attachment; filename="diario_18-08-2026.pdf"`)
4. Extrai texto com `pypdf` (14 páginas, 82.560 caracteres), valida
   citação de ato real: "PORTARIA TJPB/GAPRES Nº 1.764 DE 14 DE AGOSTO DE
   2026", "Publicação: terça-feira, 18 de agosto de 2026" (hoje)

**Achado operacional**: requisições em sucessão rápida (sem pausa) levaram
a um 403 da Cloudflare — não é bloqueio permanente, é rate-limit. O script
final (`scripts/run_tj_batch6_l8.py`) espera 8s entre a primeira coleta e
a segunda (idempotência), o que evitou o problema nas duas rodadas de
teste.

- [x] `scripts/run_tj_batch6_l8.py` criado, rodado, proposta aprovada
      (`pending_promo_TJPB_fb65e0a536344a99`, `approved_by: Nicole`)
- [x] Contrato antigo (`contract_TJPB_wp_sitemap`) marcado `superseded`
- [x] Auditoria final: `STATUS PASS`, `critical=0`, `warn=0`; 62/62 testes

## TRT17 e TJSC — reavaliados em 2026-08-18, continuam bloqueados (não é rate-limit temporário)
Por pedido do usuário, reavaliei os dois bloqueios registrados numa rodada
anterior pra ver se eram temporários:

- **TRT17**: agora bloqueado até no nível de CDN/WAF — `curl` na home
  retorna `x-amzn-waf-action: challenge` (AWS WAF challenge), confirmando
  que o bloqueio de bot persiste e não era rate-limit de navegação rápida.
  **Não contornado.**
- **TJSC**: `curl` simples chegou a retornar 200 com a página real (sem
  CAPTCHA), mas sem a listagem de atos (provavelmente carregada via JS/
  AJAX que o `curl` não executa). Com browser real, a navegação segue
  disparando a mesma página "Verificação de segurança do portal
  institucional" pedindo código de imagem CAPTCHA vista antes — mesmo
  bloqueio, não temporário. **Não contornado.**

## TJSC — corrigido em 2026-08-18 (a própria página bloqueada apontava pro backend certo)
Reavaliado com browser real: a navegação pra `tjsc.jus.br/atos-normativos`
ainda dispara a página "Verificação de segurança do portal institucional"
(CAPTCHA de imagem) — bloqueio confirmado, não contornado. Mas um `curl`
avulso (sem cookies prévios) chegou a passar dessa vez e trouxe a página real
por trás — e essa página tem uma nota de rodapé decisiva: **"Página meramente
informativa. Para informações oficiais, consultar o DJe."** A página nunca
foi a fonte certa.

O link "Diário da Justiça Eletrônico" do menu (`/diario-da-justica-eletronico`)
faz 302 pra um host completamente diferente, `busca.tjsc.jus.br/dje-consulta`
— um app Angular servido por JBoss, **sem nenhum desafio WAF/CAPTCHA, sem
exigir cookies**, confirmado com `curl` puro e zero requisições prévias. O
`js/rest/buscaRest.js` do próprio app documenta a API REST JSON por trás
(`rest/diario/ultimos`, `rest/busca?q=...&filtros=edicao:N`), que já retorna
o texto de cada página (`integra`) direto em JSON — sem precisar baixar/
parsear PDF.

Pipeline sem browser (GET simples, sem cookies):
1. GET `rest/diario/ultimos` → acha a edição mais recente com Caderno
   Administrativo (`cdTipoCaderno=4`, onde portarias são publicadas)
   disponível
2. GET `rest/busca?q=portaria&filtros=edicao:<N>&...` → já retorna os
   trechos de texto (`integra`) de cada página que cita "portaria" naquela
   edição, direto em JSON
3. Concatena os textos ordenados por página, valida com
   `content_structure_validator`, canonicaliza por hash do texto semântico

Citação real confirmada: "PORTARIA DGP N. 1802 DE 14 DE AGOSTO DE 2026",
edição 4792 de 17/08/2026 (ontem).

- [x] `scripts/run_tj_batch7_l8.py` criado, rodado, proposta aprovada
      (`pending_promo_TJSC_0e8172abd416461f`, `approved_by: Nicole`)
- [x] Contrato antigo (`contract_TJSC_tj_sitemap_discovery`) marcado
      `superseded`
- [x] Auditoria final: `STATUS PASS`, `critical=0`, `warn=0`; 62/62 testes

## TRT17 — reinvestigado em 2026-08-18: já não é bloqueio, é falta de conteúdo no dia
`curl` confirmou de novo `x-amzn-waf-action: challenge` no
`trt17.jus.br/web/legislacao/w/portarias` — esse caminho segue bloqueado,
não contornado. Mas achei a fonte real por outro caminho: a home do TRT17
(`www.trt17.jus.br`) linka pra `app.trt17.jus.br/principal/institucional/
diario-oficial` — subdomínio ASP.NET/IIS completamente diferente, sem WAF
nenhum na frente, `curl` puro funciona liso. Essa página lista os links pro
DEJT (Diário Eletrônico da Justiça do Trabalho), o instrumento oficial de
publicação de portarias/atos administrativos de todos os TRTs:
`https://dejt.jt.jus.br/cadernos/Diario_A_17.pdf` (Caderno Administrativo,
região 17) → redireciona (301) pra `diario.jt.jus.br` (S3+CloudFront),
`curl` puro, sem cookie, sem sessão, PDF direto, 200 OK.

**Achado**: acesso não é mais o problema — mas a edição atual (segunda-feira,
17/08/2026, a de terça ainda não saiu porque a publicação é às 19h) só tem um
Edital e uma Pauta, nenhuma Portaria, então a validação estrutural falha por
`NO_LEGAL_KEYWORD` (falta de conteúdo, não de acesso — bem diferente de
TJRO/TJMSP). O app de busca por edições antigas do DEJT
(`dejt.jt.jus.br/dejt/f/n/diariocon`) que permitiria escolher manualmente uma
edição com Portaria está fora do ar (503) nas várias tentativas desta sessão
— parece indisponibilidade genuína do serviço nacional (CSJT), não bloqueio
direcionado a nós.

**Decisão do usuário**: aguardar e tentar de novo depois (não forçar
promoção com conteúdo incompleto, não usar o Caderno Judiciário como
substituto por ser tematicamente menos alinhado — atos processuais, não
administrativos/calendário).

## O 1 restante fora do escopo de acesso — ainda não corrigido
| Tribunal | Situação |
|---|---|
| TRT17 | acesso resolvido (fonte real sem WAF/CAPTCHA encontrada), mas edição do dia sem Portaria — tentar de novo depois de 19h de hoje ou em sessão futura, ideal seria o app de busca de edições antigas do DEJT (`dejt.jt.jus.br`, hoje fora do ar) voltar pra escolher uma edição com conteúdo relevante |

## Os 2 restantes — ainda não corrigidos (bloqueio de acesso de verdade)
| Tribunal | Situação |
|---|---|
| TJRO | Akamai bloqueia até o browser real na home ("Página Bloqueada"); `curl` retorna 200 mas com script de desafio, não conteúdo real |
| TJMSP | fonte real encontrada com browser (`atos-e-comunicados/`), mas Akamai retorna 403 pra qualquer cliente HTTP simples, mesmo com headers de browser completos |

## Decisão do usuário (2026-08-18): TJRO/TJMSP adiados
Perguntado se valeria construir um coletor Playwright pra TJRO/TJMSP
(mesma categoria de risco da subtask [7](07-revisar-bypass-antibot.md) —
rodar browser completo por ciclo de coleta), o usuário escolheu **adiar
essa decisão** e focar primeiro no que não tinha sido tentado (TJPB,
resolvido) ou podia ser reavaliado (TRT17/TJSC, confirmados ainda
bloqueados, não eram rate-limit). Pergunta sobre TJRO/TJMSP continua em
aberto pra próxima sessão.

## Próximos passos sugeridos
- [ ] TJRO e TJMSP: decisão pendente do usuário sobre construir um
      coletor Playwright (ver acima) ou tratar como definitivamente fora
      do alcance sem API paga
- [ ] TRT17: acesso resolvido, falta só uma edição do DEJT com Portaria
      pra rodar `run_tj_batch7_l8.py`-style e validar — tentar de novo
      depois de 19h (Brasília) hoje ou em sessão futura; se o app de
      busca de edições antigas (`dejt.jt.jus.br`) voltar do ar, dá pra
      escolher uma edição específica em vez de esperar a atual mudar
- [ ] Reavaliar aqui a opção de API paga (Escavador/Judit.io) discutida
      antes, para os casos que continuarem resistentes
- [ ] Nota geral do achado TJRS: quando um índice de busca institucional
      (GSA ou similar) existe mas parece obsoleto, vale checar se há um
      widget de "última edição" na home que não passa pela busca — foi
      esse o padrão que resolveu o TJRS depois de dois índices mortos
- [ ] Nota geral do achado TJPB: um "precisa de Playwright" documentado
      antes vale reinvestigar com browser real primeiro (pra ver a
      chamada de rede de verdade) antes de assumir que só funciona com
      JS — o bloqueio Cloudflare nesse caso era só telemetria passiva,
      não um desafio de fato gating as requisições
- [ ] Nota geral do achado TJSC/TRT17: uma página institucional bloqueada
      por CAPTCHA/WAF não significa que o tribunal inteiro está bloqueado
      — vale sempre checar se a página tem uma nota apontando pra fonte
      oficial alternativa (TJSC dizia isso explicitamente), ou se existe
      um subdomínio de busca/app separado (`busca.*`, `app.*`) que não
      está atrás do mesmo WAF/CDN que o domínio principal
