# 9. Migrar tribunais para fonte de Diário real — TJAL CORRIGIDO ✅, RESTO NÃO EXECUTADO ⚠️

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

## Os outros 6 candidatos — ainda não executados
TJES, TJGO, TJMG, TJPA, TJPB, TJRJ continuam pendentes (ver tabela abaixo,
mantida como estava). O caso do TJAL mostra que vale a pena — mesmo um
formulário JS "impossível" via GET simples costuma esconder uma API REST
real por trás (inspecionar `performance.getEntriesByType('resource')` no
browser + grep no bundle JS por `/api/` é o caminho mais rápido, mais rápido
que tentar automatizar o formulário em si).

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
