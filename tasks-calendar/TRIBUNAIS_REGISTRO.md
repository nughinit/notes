# Registro de Tribunais — Legal Calendar MongoDB

> Gerado em 2026-08-18T21:23:45Z por consulta direta ao MongoDB Atlas (`legal_calendar`, coleções `courts`, `sources`, `coverage_gaps`). Este arquivo é um snapshot — não é atualizado automaticamente; regenerar sempre que o estado do pipeline mudar.

## Como ler

- **Nível**: nível de cobertura (`L0`–`L8`). `L8` = monitoramento oficial contínuo com evidência.
- **Fluxo (adapter / tipo)**: qual adapter/família de coleta alimenta o tribunal e o tipo de conteúdo coletado (`HTML_PDF`, `SITEMAP`, `API`, etc.) — é o pipeline real de onde a informação daquele tribunal vem.
- **Fonte ativa**: URL(s) oficial(is) cadastrada(s) como fonte ativa de coleta.
- **Gap aberto**: gaps de cobertura não resolvidos (`coverage_gaps.resolved = false`) — indicam o que falta para o tribunal ter cadeia real completa (ex.: `SOURCE_COVERAGE_GAP` = falta evento real de alteração/revogação para provar L7).
- **Atualizado**: `updated_at` do documento do tribunal (UTC).

## Resumo geral

- Total de tribunais: **92**
- Em L8: **92/92**
- Tribunais com gap de cobertura aberto: **21**
  - `SOURCE_COVERAGE_GAP`: 21
- Status da última auditoria completa (`runtime_final_audit/FINAL_AUDIT_REPORT.json`): `PASS_WITH_KNOWN_EXCEPTION` (não é PASS limpo — 1 categoria de warning aberta: `open_coverage_gaps`, 21 tribunais)

| Família | Qtd. | Em L8 | Com gap aberto |
|---|---|---|---|
| Tribunais Superiores | 5 | 5/5 | 0 |
| TJ — Tribunais de Justiça Estaduais | 27 | 27/27 | 14 |
| TJM — Tribunais de Justiça Militar Estaduais | 3 | 3/3 | 0 |
| TRF — Tribunais Regionais Federais | 6 | 6/6 | 0 |
| TRT — Tribunais Regionais do Trabalho | 24 | 24/24 | 0 |
| TRE — Tribunais Regionais Eleitorais | 27 | 27/27 | 7 |

## Tribunais Superiores (5)

| Tribunal | Nível | Fluxo (adapter / tipo) | Fonte ativa | Gap aberto | Atualizado |
|---|---|---|---|---|---|
| STF | **L8** | `STF_OFFICIAL` / `HTML_PDF` | — | — | 2026-08-18 02:00:06 |
| STJ | **L8** | `STJ_DJE` / `HTML_PDF` | — | — | 2026-08-18 02:14:58 |
| STM | **L8** | `STM_OFFICIAL` / `HTML_PDF` | — | — | 2026-08-18 02:05:37 |
| TSE | **L8** | `TSE_TRE_DJE` / `INTERNAL_SEARCH` | https://dje-consulta.tse.jus.br/dje-consulta/rest/diario/... | — | 2026-08-18 00:43:11 |
| TST | **L8** | `DEJT` / `SOAP_API` | — | — | 2026-08-18 01:52:36 |

## TJ — Tribunais de Justiça Estaduais (27)

| Tribunal | Nível | Fluxo (adapter / tipo) | Fonte ativa | Gap aberto | Atualizado |
|---|---|---|---|---|---|
| TJAC | **L8** | `OFFICIAL_PORTAL_PENDING` / `HTML` | — | SOURCE_COVERAGE_GAP | 2026-08-18 17:19:13 |
| TJAL | **L8** | `SOFTPLAN_CDJ_E` / `INTERNAL_SEARCH` | — | SOURCE_COVERAGE_GAP | 2026-08-18 16:58:53 |
| TJAM | **L8** | `SOFTPLAN_CDJ_E` / `INTERNAL_SEARCH` | — | SOURCE_COVERAGE_GAP | 2026-08-18 01:22:10 |
| TJAP | **L8** | `OFFICIAL_PORTAL_PENDING` / `HTML` | — | SOURCE_COVERAGE_GAP | 2026-08-18 01:44:15 |
| TJBA | **L8** | `OFFICIAL_PORTAL_PENDING` / `HTML` | https://www.tjba.jus.br/portal/decreto-judiciario-estabel... | — | 2026-08-18 01:44:18 |
| TJCE | **L8** | `TJCE_DJEA_ATOS` / `HTML_PDF` | — | — | 2026-08-18 17:19:17 |
| TJDFT | **L8** | `OFFICIAL_PORTAL_PENDING` / `HTML` | — | — | 2026-08-18 17:19:14 |
| TJES | **L8** | `TJES_EDIARIO` / `HTML` | — | SOURCE_COVERAGE_GAP | 2026-08-18 17:53:23 |
| TJGO | **L8** | `TJGO_TJDOCS` / `SPA_SEARCH` | — | — | 2026-08-18 17:04:00 |
| TJMA | **L8** | `TJMA_ATOS` / `INTERNAL_SEARCH` | — | — | 2026-08-18 17:19:16 |
| TJMG | **L8** | `TJMG_DJE` / `HTML_PDF` | https://www8.tjmg.jus.br/servicos/gj/calendario/index.jsp... | SOURCE_COVERAGE_GAP | 2026-08-18 02:17:35 |
| TJMS | **L8** | `OFFICIAL_PORTAL_PENDING` / `HTML` | — | — | 2026-08-18 01:44:21 |
| TJMT | **L8** | `OFFICIAL_PORTAL_PENDING` / `HTML` | — | — | 2026-08-18 01:44:24 |
| TJPA | **L8** | `TJPA_DJE` / `SPA_SEARCH` | — | SOURCE_COVERAGE_GAP | 2026-08-18 17:06:48 |
| TJPB | **L8** | `TJPB_DJE` / `INTERNAL_SEARCH` | — | — | 2026-08-18 18:38:47 |
| TJPE | **L8** | `TJPE_DJE` / `HTML_PDF` | https://portal.tjpe.jus.br/-/tjpe-divulga-calend%C3%A1rio... | SOURCE_COVERAGE_GAP | 2026-08-18 02:16:58 |
| TJPI | **L8** | `OFFICIAL_PORTAL_PENDING` / `HTML` | — | SOURCE_COVERAGE_GAP | 2026-08-18 01:49:57 |
| TJPR | **L8** | `TJPR_ATOS` / `INTERNAL_SEARCH` | — | — | 2026-08-18 17:37:19 |
| TJRJ | **L8** | `TJRJ_DJERJ` / `INTERNAL_SEARCH` | https://www.tjrj.jus.br/documents/d/portal-conhecimento/s... | SOURCE_COVERAGE_GAP | 2026-08-18 17:53:26 |
| TJRN | **L8** | `OFFICIAL_PORTAL_PENDING` / `HTML` | — | — | 2026-08-18 01:35:15 |
| TJRO | **L8** | `OFFICIAL_PORTAL_PENDING` / `HTML` | — | SOURCE_COVERAGE_GAP | 2026-08-18 01:29:20 |
| TJRR | **L8** | `OFFICIAL_PORTAL_PENDING` / `HTML` | — | SOURCE_COVERAGE_GAP | 2026-08-18 01:44:27 |
| TJRS | **L8** | `OFFICIAL_PORTAL_PENDING` / `HTML` | — | — | 2026-08-18 18:15:08 |
| TJSC | **L8** | `OFFICIAL_PORTAL_PENDING` / `REST_PUBLIC` | https://www.tjsc.jus.br/suspensao-de-prazos/pjsc (+2) | — | 2026-08-18 19:04:55 |
| TJSE | **L8** | `OFFICIAL_PORTAL_PENDING` / `HTML` | — | SOURCE_COVERAGE_GAP | 2026-08-18 01:44:29 |
| TJSP | **L8** | `OFFICIAL_PORTAL_PENDING` / `HTML` | https://www.tjsp.jus.br/CanaisComunicacao/Feriados/Proces... | SOURCE_COVERAGE_GAP | 2026-08-18 01:50:50 |
| TJTO | **L8** | `OFFICIAL_PORTAL_PENDING` / `HTML` | — | — | 2026-08-18 01:44:33 |

## TJM — Tribunais de Justiça Militar Estaduais (3)

| Tribunal | Nível | Fluxo (adapter / tipo) | Fonte ativa | Gap aberto | Atualizado |
|---|---|---|---|---|---|
| TJMMG | **L8** | `TJMMG_OFFICIAL` / `HTML_PDF` | — | — | 2026-08-18 17:37:21 |
| TJMRS | **L8** | `TJMRS_OFFICIAL` / `HTML_PDF` | — | — | 2026-08-18 02:18:07 |
| TJMSP | **L8** | `TJMSP_OFFICIAL` / `HTML_PDF` | — | — | 2026-08-18 02:16:09 |

## TRF — Tribunais Regionais Federais (6)

| Tribunal | Nível | Fluxo (adapter / tipo) | Fonte ativa | Gap aberto | Atualizado |
|---|---|---|---|---|---|
| TRF1 | **L8** | `TRF1_DJE` / `HTML_PDF` | — | — | 2026-08-18 02:05:39 |
| TRF2 | **L8** | `TRF2_OFFICIAL` / `HTML_PDF` | — | — | 2026-08-18 02:06:08 |
| TRF3 | **L8** | `TRF3_DJE` / `INTERNAL_SEARCH` | — | — | 2026-08-18 02:00:44 |
| TRF4 | **L8** | `TRF4_DJE` / `INTERNAL_SEARCH` | — | — | 2026-08-18 02:05:41 |
| TRF5 | **L8** | `TRF5_OFFICIAL` / `HTML_PDF` | — | — | 2026-08-18 02:05:45 |
| TRF6 | **L8** | `TRF6_OFFICIAL` / `HTML_PDF` | — | — | 2026-08-18 18:24:20 |

## TRT — Tribunais Regionais do Trabalho (24)

| Tribunal | Nível | Fluxo (adapter / tipo) | Fonte ativa | Gap aberto | Atualizado |
|---|---|---|---|---|---|
| TRT1 | **L8** | `DEJT` / `SOAP_API` | — | — | 2026-08-18 17:37:22 |
| TRT2 | **L8** | `DEJT` / `SOAP_API` | https://basis.trt2.jus.br/handle/123456789/17738 (+4) | — | 2026-08-17 00:00:00 |
| TRT3 | **L8** | `DEJT` / `SOAP_API` | https://sistemas.trt3.jus.br/bd-trt3/handle/11103/94806 (+3) | — | 2026-08-17 00:00:00 |
| TRT4 | **L8** | `DEJT` / `SOAP_API` | https://www.trt4.jus.br/portais/media/503432050/DEJT-vig%... | — | 2026-08-17 00:00:00 |
| TRT5 | **L8** | `DEJT` / `SOAP_API` | — | — | 2026-08-18 02:23:31 |
| TRT6 | **L8** | `DEJT` / `SOAP_API` | https://www.trt6.jus.br/portal/noticias/2026/06/25/trt-6-... | — | 2026-08-17 00:00:00 |
| TRT7 | **L8** | `DEJT` / `SOAP_API` | https://www.trt7.jus.br/index.php/servicos/agendas-e-cale... | — | 2026-08-17 00:00:00 |
| TRT8 | **L8** | `DEJT` / `SOAP_API` | https://www.trt8.jus.br/sites/portal/files/roles/auditori... | — | 2026-08-17 00:00:00 |
| TRT9 | **L8** | `DEJT` / `SOAP_API` | https://www.trt9.jus.br/institucional/calendario.xhtml (+3) | — | 2026-08-17 00:00:00 |
| TRT10 | **L8** | `DEJT` / `SOAP_API` | https://atosnormativos.trt10.jus.br/atosnormativos/api/do... | — | 2026-08-17 00:00:00 |
| TRT11 | **L8** | `DEJT` / `SOAP_API` | https://portal.trt11.jus.br/index.php/sociedades/calendar... | — | 2026-08-17 00:00:00 |
| TRT12 | **L8** | `DEJT` / `SOAP_API` | https://dspace.trt12.jus.br/server/api/core/bitstreams/b4... | — | 2026-08-17 00:00:00 |
| TRT13 | **L8** | `DEJT` / `SOAP_API` | https://normasinternas.trt13.jus.br/xmlui/handle/bdtrt7/1... | — | 2026-08-17 00:00:00 |
| TRT14 | **L8** | `DEJT` / `SOAP_API` | — | — | 2026-08-18 02:23:33 |
| TRT15 | **L8** | `DEJT` / `SOAP_API` | https://trt15.jus.br/legislacao/normas-institucionais/com... | — | 2026-08-17 00:00:00 |
| TRT16 | **L8** | `DEJT` / `SOAP_API` | — | — | 2026-08-18 02:23:36 |
| TRT17 | **L8** | `DEJT` / `SOAP_API` | — | — | 2026-08-18 02:21:38 |
| TRT18 | **L8** | `DEJT` / `SOAP_API` | https://www.trt18.jus.br/portal/expediente-em-varas-do-tr... | — | 2026-08-17 00:00:00 |
| TRT19 | **L8** | `DEJT` / `SOAP_API` | — | — | 2026-08-18 15:04:18 |
| TRT20 | **L8** | `DEJT` / `SOAP_API` | — | — | 2026-08-18 02:23:39 |
| TRT21 | **L8** | `DEJT` / `SOAP_API` | — | — | 2026-08-18 02:23:41 |
| TRT22 | **L8** | `DEJT` / `SOAP_API` | — | — | 2026-08-18 02:23:43 |
| TRT23 | **L8** | `DEJT` / `SOAP_API` | — | — | 2026-08-18 02:23:45 |
| TRT24 | **L8** | `DEJT` / `SOAP_API` | — | — | 2026-08-18 17:19:18 |

## TRE — Tribunais Regionais Eleitorais (27)

| Tribunal | Nível | Fluxo (adapter / tipo) | Fonte ativa | Gap aberto | Atualizado |
|---|---|---|---|---|---|
| TRE-AC | **L8** | `TSE_TRE_DJE` / `INTERNAL_SEARCH` | https://www.tre-ac.jus.br/comunicacao/noticias/2026/Janei... | — | 2026-08-18 01:07:48 |
| TRE-AL | **L8** | `TSE_TRE_DJE` / `INTERNAL_SEARCH` | https://app.tre-al.jus.br/eventos/calendario.do?exibicaoC... | SOURCE_COVERAGE_GAP | 2026-08-17 00:00:00 |
| TRE-AM | **L8** | `TSE_TRE_DJE` / `INTERNAL_SEARCH` | https://www.tre-am.jus.br/legislacao/compilada/portarias/... | — | 2026-08-18 01:08:11 |
| TRE-AP | **L8** | `TSE_TRE_DJE` / `INTERNAL_SEARCH` | https://www.tre-ap.jus.br/legislacao/compilada/portaria-p... | SOURCE_COVERAGE_GAP | 2026-08-18 01:08:36 |
| TRE-BA | **L8** | `TSE_TRE_DJE` / `INTERNAL_SEARCH` | https://www.tre-ba.jus.br/legislacao/compilada/portaria-d... | — | 2026-08-18 01:08:43 |
| TRE-CE | **L8** | `TSE_TRE_DJE` / `INTERNAL_SEARCH` | https://www.tre-ce.jus.br/legislacao/compilada/portaria-c... | — | 2026-08-18 01:09:04 |
| TRE-DF | **L8** | `TSE_TRE_DJE` / `INTERNAL_SEARCH` | https://www.tre-df.jus.br/legislacao/compilada/portaria-c... | — | 2026-08-18 01:09:10 |
| TRE-ES | **L8** | `TSE_TRE_DJE` / `INTERNAL_SEARCH` | https://www.tre-es.jus.br/legislacao/compilada/ato/2025/a... | — | 2026-08-18 01:09:32 |
| TRE-GO | **L8** | `TSE_TRE_DJE` / `INTERNAL_SEARCH` | https://www.tre-go.jus.br/legislacao/compilada/portarias-... | — | 2026-08-18 01:09:47 |
| TRE-MA | **L8** | `TSE_TRE_DJE` / `INTERNAL_SEARCH` | https://www.tre-ma.jus.br/legislacao/compilada/portarias-... | SOURCE_COVERAGE_GAP | 2026-08-18 01:09:54 |
| TRE-MG | **L8** | `TSE_TRE_DJE` / `INTERNAL_SEARCH` | https://www.tre-mg.jus.br/legislacao/portarias | — | 2026-08-18 01:10:01 |
| TRE-MS | **L8** | `TSE_TRE_DJE` / `INTERNAL_SEARCH` | https://www.tre-ms.jus.br/legislacao/portarias | SOURCE_COVERAGE_GAP | 2026-08-18 01:10:09 |
| TRE-MT | **L8** | `TSE_TRE_DJE` / `INTERNAL_SEARCH` | https://www.tre-mt.jus.br/legislacao/compilada/portaria/2... | — | 2026-08-18 01:10:15 |
| TRE-PA | **L8** | `TSE_TRE_DJE` / `INTERNAL_SEARCH` | — | SOURCE_COVERAGE_GAP | 2026-08-18 01:10:22 |
| TRE-PB | **L8** | `TSE_TRE_DJE` / `INTERNAL_SEARCH` | https://www.tre-pb.jus.br/comunicacao/noticias/2026/Marco... | — | 2026-08-18 01:10:29 |
| TRE-PE | **L8** | `TSE_TRE_DJE` / `INTERNAL_SEARCH` | https://www.tre-pe.jus.br/institucional/feriados (+1) | — | 2026-08-18 01:10:36 |
| TRE-PI | **L8** | `TSE_TRE_DJE` / `INTERNAL_SEARCH` | https://www.tre-pi.jus.br/legislacao/portarias-normativas... | — | 2026-08-18 01:10:47 |
| TRE-PR | **L8** | `TSE_TRE_DJE` / `INTERNAL_SEARCH` | https://www.tre-pr.jus.br/legislacao/compilada/portarias-... | — | 2026-08-18 01:10:54 |
| TRE-RJ | **L8** | `TSE_TRE_DJE` / `INTERNAL_SEARCH` | https://www.tre-rj.jus.br/legislacao/compilada/atos-da-pr... | — | 2026-08-18 01:11:20 |
| TRE-RN | **L8** | `TSE_TRE_DJE` / `INTERNAL_SEARCH` | https://www.tre-rn.jus.br/legislacao/compilada/atos-conju... | — | 2026-08-18 01:11:36 |
| TRE-RO | **L8** | `TSE_TRE_DJE` / `INTERNAL_SEARCH` | https://www.tre-ro.jus.br/comunicacao/noticias/2025/Dezem... | SOURCE_COVERAGE_GAP | 2026-08-18 01:11:42 |
| TRE-RR | **L8** | `TSE_TRE_DJE` / `INTERNAL_SEARCH` | https://www.tre-rr.jus.br/legislacao/portarias-do-tre-rr-... | — | 2026-08-18 01:11:56 |
| TRE-RS | **L8** | `TSE_TRE_DJE` / `INTERNAL_SEARCH` | https://www.tre-rs.jus.br/legislacao/normas-do-tre-rs/por... | — | 2026-08-18 01:12:55 |
| TRE-SC | **L8** | `TSE_TRE_DJE` / `INTERNAL_SEARCH` | https://www.tre-sc.jus.br/legislacao/compilada/portaria-p... | — | 2026-08-18 01:12:08 |
| TRE-SE | **L8** | `TSE_TRE_DJE` / `INTERNAL_SEARCH` | https://www.tre-se.jus.br/legislacao/compilada/portaria-c... | SOURCE_COVERAGE_GAP | 2026-08-18 01:12:23 |
| TRE-SP | **L8** | `TSE_TRE_DJE` / `INTERNAL_SEARCH` | https://www.tre-sp.jus.br/legislacao/compilada/portarias-... | — | 2026-08-18 01:12:39 |
| TRE-TO | **L8** | `TSE_TRE_DJE` / `INTERNAL_SEARCH` | https://www.tre-to.jus.br/legislacao/compilada/resolucao/... | — | 2026-08-18 01:12:47 |
