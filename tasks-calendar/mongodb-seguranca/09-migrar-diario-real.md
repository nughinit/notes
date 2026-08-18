# 9. Migrar tribunais para fonte de Diário real — 4/7 CORRIGIDOS ✅

## TJAL — corrigido em 2026-08-18
Achado (ver seção abaixo): a evidência L8 do TJAL era um formulário de busca
vazio do CDJE, sem conteúdo de calendário. Corrigido:

- [x] Navegado o site real (SPA Vue — GET simples só retorna a casca
      `<div id="app">`, precisou de browser real) até achar o menu
      "Legislação e Normas > Portaria"
- [x] Essa página também é renderizada por API — inspecionado o bundle JS
      carregado (`performance.getEntriesByType('resource')` + grep no bundle)
      até achar o endpoint real: `documentos.tjal.jus.br/api/documentos/pesquisa-portal`
      (Laravel REST API, `id_tipo_documento=8` = Portaria, descoberto via
      `/api/tipos-documentos/todos`)
- [x] Confirmado: **GET simples funciona** (sem browser, sem WAF), retorna
      JSON estruturado real — 1183 Portarias de 2026, ementa/texto completo,
      a mais recente de 17/08/2026 (ontem). Idempotente em 2 fetches
      (mesmo conjunto de IDs)
- [x] Criado `scripts/run_tjal_documentos_api_l8.py` (discovery_type
      `JSON_REST_API`, canonicaliza por tupla ordenada `(id, numero,
      data_publicacao)`)
- [x] Corrigido bug no gate (`promotion_gate.py`): `approve_l8_promotion`
      pulava silenciosamente se o tribunal já estava em L8, mesmo quando a
      proposta era uma **substituição** de evidência ruim por evidência boa
      — agora só pula se for exatamente a mesma versão/família já aplicada
- [x] Rodado o coletor → proposta criada → aprovada via
      `scripts/approve_promotion.py --approve ... --by "Nicole"` →
      `courts.TJAL.coverage.evidence_summary` agora aponta pra API real,
      `coverage_history` preserva a mudança com `approved_by`, contrato
      antigo (`contract_TJAL_state_court_discovery`) marcado `superseded`
- [x] Auditoria final: `STATUS PASS`, `critical=0`, `warn=0`; 62/62 testes

## TJGO — corrigido em 2026-08-18
Site é SPA React (`tjdocs.tjgo.jus.br`). Achado via inspeção de rede:
backend `tjdocs-backend.tjgo.jus.br`. A busca completa (`POST /documentos`)
exige permissão (403 "Acesso negado" — autenticado). Mas o endpoint público
`GET /documentos/ultima-atualizacao/todos` (o mesmo que a home page usa pra
mostrar "Último documento atualizado") funciona via GET simples, é real e
muda de verdade entre chamadas (confirmei 2 valores diferentes minutos
seguidos, provando publicação ativa). Formato do número do ato varia (nem
sempre tem ano junto) — validação relaxada pra só exigir dígito presente +
ano plausível em `ultimaAtualizacao`.
- [x] `scripts/run_tjgo_documentos_api_l8.py` criado, rodado, proposta
      aprovada (`approved_by: Nicole`), contrato antigo (`tj_sitemap_discovery`)
      superado
- ⚠️ Limitação documentada: é um checkpoint do **último documento**, não
      uma listagem completa (busca completa exige autenticação)

## TJPA — corrigido em 2026-08-18
Site é SPA Angular. Achado via inspeção de rede: API REST real
`dje.tjpa.jus.br/DJEletronico/rest/DJEletronicoService/publicacao/ultimoDiario`
— funciona via GET simples (sem browser), retorna a edição atual do DJE-PA
de verdade (edição 8381/2026, publicada 18/08/2026 — hoje). Idempotente.
- [x] `scripts/run_tjpa_dje_api_l8.py` criado, rodado, proposta aprovada
      (`approved_by: Nicole`), contrato antigo (`superior_federal`) superado

## TJMG — bloqueado por verificação humana real, não contornado
- **TJMG** (`dje.tjmg.jus.br`): a home carrega bem, mas a página de
  "Última Edição" (o conteúdo real e atual) exige resolver um **CAPTCHA de
  imagem** ("Digite os números abaixo... gere nova imagem ou escute o
  código") antes de mostrar qualquer diário. "Atos Normativos" só tem 2
  itens estáticos de 2008 (fundação do DJe), não serve como fonte viva.
  **Não tentei contornar o CAPTCHA** — é uma ação proibida por política.
  Fica bloqueado até haver outra fonte ou acesso autorizado.

## TJES — corrigido, mas por uma fonte diferente da originalmente cogitada (2026-08-18)
`sistemas.tjes.jus.br/ediario` continua bloqueado (título "Human
Verification", desafio AWS WAF que exige interação humana — não
contornado). Mas achei uma fonte alternativa real do mesmo tribunal via
[subtask 11](11-batch2-sitemap-migration.md): `www.tjes.jus.br/publicacoes/
atos-normativos-tjes/atos-normativos-2026/` — página estática simples
(WordPress), sem WAF/CAPTCHA, lista todos os Atos Normativos do ano com
número/ementa/data, atualizada no mesmo dia. Promovida a L8.

## TJPB — não executado, precisa de automação de formulário mais pesada
Diferente do TJAL/TJGO/TJPA (onde achei uma API REST simples por trás do
SPA), esse não tem atalho de API:
- **TJPB** (`app.tjpb.jus.br/dje/...buscas.jsf`): protegido por desafio
  Cloudflare (JS proof-of-work, resolvido automaticamente pelo browser real —
  não é CAPTCHA humano, então não é uma barreira ética, só técnica). A lista
  de edições recentes (`Diário de 18/08/2026`, etc.) aparece na tela, mas os
  links são `href="#"` — carregados via JSF AJAX sem endpoint REST direto
  identificado. `curl` simples não retorna a lista (só a casca do formulário)
Fica como trabalho futuro — precisaria de uma sessão de investigação
própria (Playwright + interação de formulário), fora do escopo resolvido
agora. `www3.tjrj.jus.br/consultadje` (ASP.NET WebForms, postback com
viewstate) continua sem atalho de API, mas deixou de ser bloqueante para o
TJRJ — ver nota abaixo.

## TJRJ — corrigido, mas por uma fonte diferente da originalmente cogitada (2026-08-18)
`www3.tjrj.jus.br/consultadje` (o DJE via postback ASP.NET) segue sem
automação. Mas achei uma fonte real e melhor via
[subtask 11](11-batch2-sitemap-migration.md), navegando pelo menu
"Portal do Conhecimento > Legislação > Atos Oficiais do PJERJ":
`www3.tjrj.jus.br/Atosofic2leg/Busca/CategoriaLegislacao?codigo=5` — sistema
"Sophia Biblioteca Web", 26 portarias reais, mais recente publicada
17/08/2026. Exige cookie de sessão obtido via redirect, resolvido com
`http.cookiejar` no coletor, sem browser. Promovida a L8.

## Resumo da rodada (2026-08-18, primeira parte)
| Tribunal | Resultado |
|---|---|
| TJAL | ✅ corrigido (API REST real) |
| TJGO | ✅ corrigido (API REST real, checkpoint parcial) |
| TJPA | ✅ corrigido (API REST real) |
| TJMG | ❌ bloqueado — CAPTCHA real, não contornado |
| TJES | ❌ bloqueado nesta rodada — verificação humana AWS WAF, não contornado (corrigido depois por outra fonte, ver acima) |
| TJPB | ⏸️ não executado — precisa automação de formulário JSF/Cloudflare |
| TJRJ | ⏸️ não executado nesta rodada — precisa automação de formulário ASP.NET postback (corrigido depois por outra fonte, ver acima) |

Auditoria final: `STATUS PASS`, `critical=0`, `warn=0`; 62/62 testes.

Origem: comparação do `dev-source-registry-92-courts.csv` da Intimatio
(task/TASK-011 do repo `intimatio/intimatio-business`) contra os
`source_contracts` ativos deste projeto. O usuário havia identificado esse
padrão manualmente para TJRS (site genérico vs. DOE-RS real) e pediu para
verificar quais outros tribunais têm o mesmo problema.

## Metodologia
Cruzamento por host: 66 de 92 tribunais apontam para host diferente do que
o registro da Intimatio considera oficial. A maioria **não é comparável de
verdade** — são categorias de dado diferentes:

- Todos os `TRT*`/`TST` → Intimatio aponta para o **DEJT SOAP** (publicações/
  intimações processuais). Este projeto rastreia **atos institucionais de
  calendário** (portaria de feriado/suspensão), não publicação de processo.
  Fontes diferentes por natureza, não é uma "fonte fraca" — é outro produto.
- Todos os `TRE-*`/`TSE` → mesmo raciocínio com o DJE central do TSE.

## Candidatos reais (mesmo padrão do TJRS) — 7 a investigar
| Tribunal | Hoje | Diário real (Intimatio) | Status do teste rápido |
|---|---|---|---|
| TJES | sitemap genérico | `sistemas.tjes.jus.br/ediario` | bloqueado por WAF (AWS) — precisa browser real |
| TJGO | sitemap.txt genérico | `tjdocs.tjgo.jus.br` | SPA (React), sem conteúdo em GET simples |
| TJMG | HTML "atos-normativos" | `dje.tjmg.jus.br` | bloqueado por challenge F5 CSPM — precisa browser real |
| TJPA | HTML "atos normativos" | `dje.tjpa.jus.br/.../home.html` | SPA (Angular), sem conteúdo em GET simples |
| TJPB | sitemap genérico | `app.tjpb.jus.br/dje/...buscas.jsf` | formulário JSF — precisa submeter busca, não é GET puro |
| TJRJ | sitemap genérico | `www3.tjrj.jus.br/consultadje` | formulário de busca — precisa interação |
| TJAM | sitemap genérico | `consultasaj.tjam.jus.br` (e-SAJ) | **ver achado abaixo — pode não servir pro propósito** |

Nenhum desses é um GET simples como foi o TRT19 — cada um precisaria de
investigação própria (Playwright + navegação/formulário), do mesmo porte do
que foi feito para o TRT19 nesta sessão. Não executado ainda.

## Achado mais sério: fontes tipo CDJE/DJe podem não servir pro propósito do projeto

Testei o padrão e-SAJ CDJE (usado pelo `TJAM`, formato idêntico ao já ativo
para `TJAL`) em `https://consultasaj.tjam.jus.br/cdje/index.do`:
- Funciona via GET simples, 200, idempotente (`semantic_hash` igual em 2
  fetches)
- **Mas falha a validação estrutural de conteúdo de calendário**
  (`NO_LEGAL_KEYWORD`) — é uma página de **busca de Diário de Justiça
  Eletrônico** (intimações processuais), não uma listagem de portarias/atos
  de calendário

Investigando o `TJAL` (já ativo no projeto, mesmo padrão CDJE, `_id:
contract_TJAL_state_court_discovery`), confirmei: a evidência de promoção a
L8 diz só **"Official discovery surface fetched twice"** — nunca validou
conteúdo de calendário. O snapshot real do `TJAL` é literalmente uma página
de **formulário de busca vazio** (`runtime/snapshots/state_court_discovery_l8/TJAL_...html`,
0 números/citações, texto genérico "Consulta de Diário da Justiça
Eletrônico").

**Ou seja: `TJAL` está em L8 hoje com uma fonte que estruturalmente não
contém — e talvez nunca vá conter, por ser um formulário de busca, não um
índice — atos de calendário.** Isso é mais grave que "fonte fraca": é
"fonte do tipo errado", proveniente de um critério de promoção antigo mais
frouxo (antes da subtask 4 deste milestone existir).

## Não executado — motivo
O escopo cresceu de "trocar 1 URL por outra" para: (a) 7 investigações
individuais tipo TRT19 (browser real, formulários, SPA), mais (b) uma
auditoria separada de quantos outros tribunais L8 (além do TJAL) têm o
mesmo problema de fonte-tipo-errado. Isso é maior que cabe em uma sessão sem
alinhar prioridade antes.

## Próximos passos sugeridos
- [ ] Rodar a auditoria retroativa de conteúdo (mesma do item 4) contra os
      **65 tribunais L8 sem snapshot local disponível** (hoje só cobri 27)
      para saber quantos mais têm o problema do TJAL
- [ ] Investigar e corrigir `TJAL` primeiro (achado concreto, não hipotético)
- [ ] Priorizar entre os 7 candidatos qual vale a pena investigar primeiro
      (provavelmente TJRJ/TJPB, que são só formulário — mais simples que WAF/SPA)
- [ ] Para TJES/TJMG (WAF/challenge): avaliar se vale o esforço de bypass ou
      se há uma fonte alternativa mais simples do mesmo tribunal
