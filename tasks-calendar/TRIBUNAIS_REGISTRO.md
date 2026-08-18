# Court Registry -- Legal Calendar MongoDB

> Generated 2026-08-18T21:40:07Z by querying MongoDB Atlas directly (`legal_calendar` DB, collections `courts`, `sources`, `coverage_gaps`). Static snapshot, not auto-refreshed -- regenerate whenever pipeline state changes.

## Column legend

| Column | Meaning |
|---|---|
| `court_id` | Primary key, `courts.court_id` (`_id`). Used as the FK across all collections. |
| `lvl` | `coverage.level_number` (0-8). `8` = live official-source monitoring with persisted evidence. |
| `adapter` | `source_family` -- the adapter/pipeline identifier the collector code writes into Mongo. Grep this string in `scripts/` to locate the collector, or filter `monitor_runs`/`audit_log` by `court_id` to find which script last touched it -- not a strict 1:1 filename mapping. |
| `transport` | `source_type` -- how content is fetched/parsed: `HTML_PDF`, `SOAP_API`, `INTERNAL_SEARCH`, `SPA_SEARCH`, `REST_PUBLIC`, `HTML`. `SPA_SEARCH`/`INTERNAL_SEARCH` usually mean there is no stable public URL -- the adapter drives a search form or client-rendered endpoint. |
| `readiness` | `readiness.*` bit flags: `src`=has_mapped_source, `ctr`=has_source_contract, `evt`=has_atomic_event, `mon`=l8_monitoring_started, `gap`=has_open_gap (`1`=true). Kept in sync with live `coverage_gaps` as of 2026-08-18 (see changelog). A court can be `lvl=8` with `evt=0` -- L8 only requires proven monitoring, not necessarily an atomic change event yet. |
| `gap` | Open (`resolved:false`) `coverage_gaps.gap_type` for this court, if any. `SOURCE_COVERAGE_GAP` = missing a real amendment/revocation event needed to prove L7-equivalent change detection. |
| `blocker` | `coverage.blocker` when present (usually null once at L8, kept for context). |
| `source_url` | First active `sources.url` for the court (`+N` = additional active sources exist). `-` = no `sources` doc registered even though `courts.coverage.level` is L8 (discovery-only adapters like `TJ_SITEMAP_DISCOVERY` do not always populate `sources`). |
| `updated_at` | `courts.updated_at`, UTC. |

## Changelog

- 2026-08-18: fixed `readiness.has_open_gap` directly in MongoDB for 20 courts where it was stale (`false` while an unresolved `coverage_gaps` entry existed): `TJAC, TJAL, TJAP, TJAM, TJES, TJMG, TJPA, TJPE, TJPI, TJRJ, TJRO, TJRR, TJSP, TJSE, TRE-AP, TRE-MA, TRE-MS, TRE-PA, TRE-RO, TRE-SE`. The `readiness` column below now matches the `gap` column for all 92 courts (verified 0 mismatches after the fix).

## Summary

- Total courts: **92**
- At L8: **92/92**
- Courts with an open coverage gap: **21**
  - `SOURCE_COVERAGE_GAP`: 21
- Courts with no active `sources` doc despite L8: **46** (discovery-only adapters -- url intentionally not tracked as a `source`)
- Courts with `has_atomic_event=false`: **69**
- Latest full audit (`runtime_final_audit/FINAL_AUDIT_REPORT.json`): `status=PASS_WITH_KNOWN_EXCEPTION`, `critical=0`, `warn=1` (`open_coverage_gaps`, 21 courts)

| Family | Count | L8 | Open gap |
|---|---|---|---|
| Superior Courts | 5 | 5/5 | 0 |
| TJ - State Courts of Justice | 27 | 27/27 | 14 |
| TJM - State Military Courts of Justice | 3 | 3/3 | 0 |
| TRF - Federal Regional Courts | 6 | 6/6 | 0 |
| TRT - Regional Labor Courts | 24 | 24/24 | 0 |
| TRE - Regional Electoral Courts | 27 | 27/27 | 7 |

## Superior Courts (5)

| court_id | lvl | adapter | transport | readiness | gap | blocker | source_url | updated_at |
|---|---|---|---|---|---|---|---|---|
| `STF` | 8 | `STF_OFFICIAL` | `HTML_PDF` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 02:00:06 |
| `STJ` | 8 | `STJ_DJE` | `HTML_PDF` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 02:14:58 |
| `STM` | 8 | `STM_OFFICIAL` | `HTML_PDF` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 02:05:37 |
| `TSE` | 8 | `TSE_TRE_DJE` | `INTERNAL_SEARCH` | `src=1 ctr=1 evt=1 mon=1 gap=0` | - | - | https://dje-consulta.tse.jus.br/dje-consulta/rest/di... | 2026-08-18 00:43:11 |
| `TST` | 8 | `DEJT` | `SOAP_API` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 01:52:36 |

## TJ - State Courts of Justice (27)

| court_id | lvl | adapter | transport | readiness | gap | blocker | source_url | updated_at |
|---|---|---|---|---|---|---|---|---|
| `TJAC` | 8 | `OFFICIAL_PORTAL_PENDING` | `HTML` | `src=0 ctr=1 evt=0 mon=1 gap=1` | SOURCE_COVERAGE_GAP | - | - | 2026-08-18 17:19:13 |
| `TJAL` | 8 | `SOFTPLAN_CDJ_E` | `INTERNAL_SEARCH` | `src=0 ctr=1 evt=0 mon=1 gap=1` | SOURCE_COVERAGE_GAP | - | - | 2026-08-18 16:58:53 |
| `TJAM` | 8 | `SOFTPLAN_CDJ_E` | `INTERNAL_SEARCH` | `src=0 ctr=1 evt=0 mon=1 gap=1` | SOURCE_COVERAGE_GAP | - | - | 2026-08-18 01:22:10 |
| `TJAP` | 8 | `OFFICIAL_PORTAL_PENDING` | `HTML` | `src=0 ctr=1 evt=0 mon=1 gap=1` | SOURCE_COVERAGE_GAP | - | - | 2026-08-18 01:44:15 |
| `TJBA` | 8 | `OFFICIAL_PORTAL_PENDING` | `HTML` | `src=1 ctr=0 evt=0 mon=1 gap=0` | - | - | https://www.tjba.jus.br/portal/decreto-judiciario-es... | 2026-08-18 01:44:18 |
| `TJCE` | 8 | `TJCE_DJEA_ATOS` | `HTML_PDF` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 17:19:17 |
| `TJDFT` | 8 | `OFFICIAL_PORTAL_PENDING` | `HTML` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 17:19:14 |
| `TJES` | 8 | `TJES_EDIARIO` | `HTML` | `src=0 ctr=1 evt=0 mon=1 gap=1` | SOURCE_COVERAGE_GAP | - | - | 2026-08-18 17:53:23 |
| `TJGO` | 8 | `TJGO_TJDOCS` | `SPA_SEARCH` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 17:04:00 |
| `TJMA` | 8 | `TJMA_ATOS` | `INTERNAL_SEARCH` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 17:19:16 |
| `TJMG` | 8 | `TJMG_DJE` | `HTML_PDF` | `src=1 ctr=0 evt=0 mon=1 gap=1` | SOURCE_COVERAGE_GAP | - | https://www8.tjmg.jus.br/servicos/gj/calendario/inde... | 2026-08-18 02:17:35 |
| `TJMS` | 8 | `OFFICIAL_PORTAL_PENDING` | `HTML` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 01:44:21 |
| `TJMT` | 8 | `OFFICIAL_PORTAL_PENDING` | `HTML` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 01:44:24 |
| `TJPA` | 8 | `TJPA_DJE` | `SPA_SEARCH` | `src=0 ctr=1 evt=0 mon=1 gap=1` | SOURCE_COVERAGE_GAP | - | - | 2026-08-18 17:06:48 |
| `TJPB` | 8 | `TJPB_DJE` | `INTERNAL_SEARCH` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 18:38:47 |
| `TJPE` | 8 | `TJPE_DJE` | `HTML_PDF` | `src=1 ctr=0 evt=0 mon=1 gap=1` | SOURCE_COVERAGE_GAP | - | https://portal.tjpe.jus.br/-/tjpe-divulga-calend%C3%... | 2026-08-18 02:16:58 |
| `TJPI` | 8 | `OFFICIAL_PORTAL_PENDING` | `HTML` | `src=0 ctr=1 evt=0 mon=1 gap=1` | SOURCE_COVERAGE_GAP | - | - | 2026-08-18 01:49:57 |
| `TJPR` | 8 | `TJPR_ATOS` | `INTERNAL_SEARCH` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 17:37:19 |
| `TJRJ` | 8 | `TJRJ_DJERJ` | `INTERNAL_SEARCH` | `src=1 ctr=0 evt=1 mon=1 gap=1` | SOURCE_COVERAGE_GAP | - | https://www.tjrj.jus.br/documents/d/portal-conhecime... | 2026-08-18 17:53:26 |
| `TJRN` | 8 | `OFFICIAL_PORTAL_PENDING` | `HTML` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 01:35:15 |
| `TJRO` | 8 | `OFFICIAL_PORTAL_PENDING` | `HTML` | `src=0 ctr=1 evt=0 mon=1 gap=1` | SOURCE_COVERAGE_GAP | - | - | 2026-08-18 01:29:20 |
| `TJRR` | 8 | `OFFICIAL_PORTAL_PENDING` | `HTML` | `src=0 ctr=1 evt=0 mon=1 gap=1` | SOURCE_COVERAGE_GAP | - | - | 2026-08-18 01:44:27 |
| `TJRS` | 8 | `OFFICIAL_PORTAL_PENDING` | `HTML` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 18:15:08 |
| `TJSC` | 8 | `OFFICIAL_PORTAL_PENDING` | `REST_PUBLIC` | `src=1 ctr=0 evt=1 mon=1 gap=0` | - | - | https://www.tjsc.jus.br/suspensao-de-prazos/pjsc (+2) | 2026-08-18 19:04:55 |
| `TJSE` | 8 | `OFFICIAL_PORTAL_PENDING` | `HTML` | `src=0 ctr=1 evt=0 mon=1 gap=1` | SOURCE_COVERAGE_GAP | - | - | 2026-08-18 01:44:29 |
| `TJSP` | 8 | `OFFICIAL_PORTAL_PENDING` | `HTML` | `src=1 ctr=0 evt=0 mon=1 gap=1` | SOURCE_COVERAGE_GAP | - | https://www.tjsp.jus.br/CanaisComunicacao/Feriados/P... | 2026-08-18 01:50:50 |
| `TJTO` | 8 | `OFFICIAL_PORTAL_PENDING` | `HTML` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 01:44:33 |

## TJM - State Military Courts of Justice (3)

| court_id | lvl | adapter | transport | readiness | gap | blocker | source_url | updated_at |
|---|---|---|---|---|---|---|---|---|
| `TJMMG` | 8 | `TJMMG_OFFICIAL` | `HTML_PDF` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 17:37:21 |
| `TJMRS` | 8 | `TJMRS_OFFICIAL` | `HTML_PDF` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 02:18:07 |
| `TJMSP` | 8 | `TJMSP_OFFICIAL` | `HTML_PDF` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 02:16:09 |

## TRF - Federal Regional Courts (6)

| court_id | lvl | adapter | transport | readiness | gap | blocker | source_url | updated_at |
|---|---|---|---|---|---|---|---|---|
| `TRF1` | 8 | `TRF1_DJE` | `HTML_PDF` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 02:05:39 |
| `TRF2` | 8 | `TRF2_OFFICIAL` | `HTML_PDF` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 02:06:08 |
| `TRF3` | 8 | `TRF3_DJE` | `INTERNAL_SEARCH` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 02:00:44 |
| `TRF4` | 8 | `TRF4_DJE` | `INTERNAL_SEARCH` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 02:05:41 |
| `TRF5` | 8 | `TRF5_OFFICIAL` | `HTML_PDF` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 02:05:45 |
| `TRF6` | 8 | `TRF6_OFFICIAL` | `HTML_PDF` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 18:24:20 |

## TRT - Regional Labor Courts (24)

| court_id | lvl | adapter | transport | readiness | gap | blocker | source_url | updated_at |
|---|---|---|---|---|---|---|---|---|
| `TRT1` | 8 | `DEJT` | `SOAP_API` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 17:37:22 |
| `TRT2` | 8 | `DEJT` | `SOAP_API` | `src=1 ctr=0 evt=1 mon=1 gap=0` | - | - | https://basis.trt2.jus.br/handle/123456789/17738 (+4) | 2026-08-17 00:00:00 |
| `TRT3` | 8 | `DEJT` | `SOAP_API` | `src=1 ctr=0 evt=1 mon=1 gap=0` | - | - | https://sistemas.trt3.jus.br/bd-trt3/handle/11103/94... | 2026-08-17 00:00:00 |
| `TRT4` | 8 | `DEJT` | `SOAP_API` | `src=1 ctr=0 evt=1 mon=1 gap=0` | - | - | https://www.trt4.jus.br/portais/media/503432050/DEJT... | 2026-08-17 00:00:00 |
| `TRT5` | 8 | `DEJT` | `SOAP_API` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 02:23:31 |
| `TRT6` | 8 | `DEJT` | `SOAP_API` | `src=1 ctr=0 evt=1 mon=1 gap=0` | - | - | https://www.trt6.jus.br/portal/noticias/2026/06/25/t... | 2026-08-17 00:00:00 |
| `TRT7` | 8 | `DEJT` | `SOAP_API` | `src=1 ctr=0 evt=1 mon=1 gap=0` | - | - | https://www.trt7.jus.br/index.php/servicos/agendas-e... | 2026-08-17 00:00:00 |
| `TRT8` | 8 | `DEJT` | `SOAP_API` | `src=1 ctr=0 evt=1 mon=1 gap=0` | - | - | https://www.trt8.jus.br/sites/portal/files/roles/aud... | 2026-08-17 00:00:00 |
| `TRT9` | 8 | `DEJT` | `SOAP_API` | `src=1 ctr=0 evt=1 mon=1 gap=0` | - | - | https://www.trt9.jus.br/institucional/calendario.xht... | 2026-08-17 00:00:00 |
| `TRT10` | 8 | `DEJT` | `SOAP_API` | `src=1 ctr=0 evt=1 mon=1 gap=0` | - | - | https://atosnormativos.trt10.jus.br/atosnormativos/a... | 2026-08-17 00:00:00 |
| `TRT11` | 8 | `DEJT` | `SOAP_API` | `src=1 ctr=0 evt=1 mon=1 gap=0` | - | - | https://portal.trt11.jus.br/index.php/sociedades/cal... | 2026-08-17 00:00:00 |
| `TRT12` | 8 | `DEJT` | `SOAP_API` | `src=1 ctr=0 evt=1 mon=1 gap=0` | - | - | https://dspace.trt12.jus.br/server/api/core/bitstrea... | 2026-08-17 00:00:00 |
| `TRT13` | 8 | `DEJT` | `SOAP_API` | `src=1 ctr=0 evt=1 mon=1 gap=0` | - | - | https://normasinternas.trt13.jus.br/xmlui/handle/bdt... | 2026-08-17 00:00:00 |
| `TRT14` | 8 | `DEJT` | `SOAP_API` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 02:23:33 |
| `TRT15` | 8 | `DEJT` | `SOAP_API` | `src=1 ctr=0 evt=1 mon=1 gap=0` | - | - | https://trt15.jus.br/legislacao/normas-institucionai... | 2026-08-17 00:00:00 |
| `TRT16` | 8 | `DEJT` | `SOAP_API` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 02:23:36 |
| `TRT17` | 8 | `DEJT` | `SOAP_API` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 02:21:38 |
| `TRT18` | 8 | `DEJT` | `SOAP_API` | `src=1 ctr=0 evt=1 mon=1 gap=0` | - | - | https://www.trt18.jus.br/portal/expediente-em-varas-... | 2026-08-17 00:00:00 |
| `TRT19` | 8 | `DEJT` | `SOAP_API` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 15:04:18 |
| `TRT20` | 8 | `DEJT` | `SOAP_API` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 02:23:39 |
| `TRT21` | 8 | `DEJT` | `SOAP_API` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 02:23:41 |
| `TRT22` | 8 | `DEJT` | `SOAP_API` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 02:23:43 |
| `TRT23` | 8 | `DEJT` | `SOAP_API` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 02:23:45 |
| `TRT24` | 8 | `DEJT` | `SOAP_API` | `src=0 ctr=1 evt=0 mon=1 gap=0` | - | - | - | 2026-08-18 17:19:18 |

## TRE - Regional Electoral Courts (27)

| court_id | lvl | adapter | transport | readiness | gap | blocker | source_url | updated_at |
|---|---|---|---|---|---|---|---|---|
| `TRE-AC` | 8 | `TSE_TRE_DJE` | `INTERNAL_SEARCH` | `src=1 ctr=0 evt=0 mon=1 gap=0` | - | - | https://www.tre-ac.jus.br/comunicacao/noticias/2026/... | 2026-08-18 01:07:48 |
| `TRE-AL` | 8 | `TSE_TRE_DJE` | `INTERNAL_SEARCH` | `src=1 ctr=0 evt=0 mon=1 gap=1` | SOURCE_COVERAGE_GAP | - | https://app.tre-al.jus.br/eventos/calendario.do?exib... | 2026-08-17 00:00:00 |
| `TRE-AM` | 8 | `TSE_TRE_DJE` | `INTERNAL_SEARCH` | `src=1 ctr=0 evt=0 mon=1 gap=0` | - | - | https://www.tre-am.jus.br/legislacao/compilada/porta... | 2026-08-18 01:08:11 |
| `TRE-AP` | 8 | `TSE_TRE_DJE` | `INTERNAL_SEARCH` | `src=1 ctr=0 evt=0 mon=1 gap=1` | SOURCE_COVERAGE_GAP | - | https://www.tre-ap.jus.br/legislacao/compilada/porta... | 2026-08-18 01:08:36 |
| `TRE-BA` | 8 | `TSE_TRE_DJE` | `INTERNAL_SEARCH` | `src=1 ctr=0 evt=1 mon=1 gap=0` | - | - | https://www.tre-ba.jus.br/legislacao/compilada/porta... | 2026-08-18 01:08:43 |
| `TRE-CE` | 8 | `TSE_TRE_DJE` | `INTERNAL_SEARCH` | `src=1 ctr=0 evt=0 mon=1 gap=0` | - | - | https://www.tre-ce.jus.br/legislacao/compilada/porta... | 2026-08-18 01:09:04 |
| `TRE-DF` | 8 | `TSE_TRE_DJE` | `INTERNAL_SEARCH` | `src=1 ctr=0 evt=0 mon=1 gap=0` | - | - | https://www.tre-df.jus.br/legislacao/compilada/porta... | 2026-08-18 01:09:10 |
| `TRE-ES` | 8 | `TSE_TRE_DJE` | `INTERNAL_SEARCH` | `src=1 ctr=0 evt=1 mon=1 gap=0` | - | - | https://www.tre-es.jus.br/legislacao/compilada/ato/2... | 2026-08-18 01:09:32 |
| `TRE-GO` | 8 | `TSE_TRE_DJE` | `INTERNAL_SEARCH` | `src=1 ctr=0 evt=0 mon=1 gap=0` | - | - | https://www.tre-go.jus.br/legislacao/compilada/porta... | 2026-08-18 01:09:47 |
| `TRE-MA` | 8 | `TSE_TRE_DJE` | `INTERNAL_SEARCH` | `src=1 ctr=0 evt=0 mon=1 gap=1` | SOURCE_COVERAGE_GAP | - | https://www.tre-ma.jus.br/legislacao/compilada/porta... | 2026-08-18 01:09:54 |
| `TRE-MG` | 8 | `TSE_TRE_DJE` | `INTERNAL_SEARCH` | `src=1 ctr=1 evt=1 mon=1 gap=0` | - | - | https://www.tre-mg.jus.br/legislacao/portarias | 2026-08-18 01:10:01 |
| `TRE-MS` | 8 | `TSE_TRE_DJE` | `INTERNAL_SEARCH` | `src=1 ctr=1 evt=1 mon=1 gap=1` | SOURCE_COVERAGE_GAP | - | https://www.tre-ms.jus.br/legislacao/portarias | 2026-08-18 01:10:09 |
| `TRE-MT` | 8 | `TSE_TRE_DJE` | `INTERNAL_SEARCH` | `src=1 ctr=0 evt=0 mon=1 gap=0` | - | - | https://www.tre-mt.jus.br/legislacao/compilada/porta... | 2026-08-18 01:10:15 |
| `TRE-PA` | 8 | `TSE_TRE_DJE` | `INTERNAL_SEARCH` | `src=0 ctr=1 evt=1 mon=1 gap=1` | SOURCE_COVERAGE_GAP | - | - | 2026-08-18 01:10:22 |
| `TRE-PB` | 8 | `TSE_TRE_DJE` | `INTERNAL_SEARCH` | `src=1 ctr=0 evt=1 mon=1 gap=0` | - | - | https://www.tre-pb.jus.br/comunicacao/noticias/2026/... | 2026-08-18 01:10:29 |
| `TRE-PE` | 8 | `TSE_TRE_DJE` | `INTERNAL_SEARCH` | `src=1 ctr=0 evt=1 mon=1 gap=0` | - | - | https://www.tre-pe.jus.br/institucional/feriados (+1) | 2026-08-18 01:10:36 |
| `TRE-PI` | 8 | `TSE_TRE_DJE` | `INTERNAL_SEARCH` | `src=1 ctr=0 evt=0 mon=1 gap=0` | - | - | https://www.tre-pi.jus.br/legislacao/portarias-norma... | 2026-08-18 01:10:47 |
| `TRE-PR` | 8 | `TSE_TRE_DJE` | `INTERNAL_SEARCH` | `src=1 ctr=1 evt=0 mon=1 gap=0` | - | - | https://www.tre-pr.jus.br/legislacao/compilada/porta... | 2026-08-18 01:10:54 |
| `TRE-RJ` | 8 | `TSE_TRE_DJE` | `INTERNAL_SEARCH` | `src=1 ctr=0 evt=0 mon=1 gap=0` | - | - | https://www.tre-rj.jus.br/legislacao/compilada/atos-... | 2026-08-18 01:11:20 |
| `TRE-RN` | 8 | `TSE_TRE_DJE` | `INTERNAL_SEARCH` | `src=1 ctr=0 evt=0 mon=1 gap=0` | - | - | https://www.tre-rn.jus.br/legislacao/compilada/atos-... | 2026-08-18 01:11:36 |
| `TRE-RO` | 8 | `TSE_TRE_DJE` | `INTERNAL_SEARCH` | `src=1 ctr=0 evt=0 mon=1 gap=1` | SOURCE_COVERAGE_GAP | - | https://www.tre-ro.jus.br/comunicacao/noticias/2025/... | 2026-08-18 01:11:42 |
| `TRE-RR` | 8 | `TSE_TRE_DJE` | `INTERNAL_SEARCH` | `src=1 ctr=0 evt=0 mon=1 gap=0` | - | - | https://www.tre-rr.jus.br/legislacao/portarias-do-tr... | 2026-08-18 01:11:56 |
| `TRE-RS` | 8 | `TSE_TRE_DJE` | `INTERNAL_SEARCH` | `src=1 ctr=1 evt=0 mon=1 gap=0` | - | - | https://www.tre-rs.jus.br/legislacao/normas-do-tre-r... | 2026-08-18 01:12:55 |
| `TRE-SC` | 8 | `TSE_TRE_DJE` | `INTERNAL_SEARCH` | `src=1 ctr=1 evt=0 mon=1 gap=0` | - | - | https://www.tre-sc.jus.br/legislacao/compilada/porta... | 2026-08-18 01:12:08 |
| `TRE-SE` | 8 | `TSE_TRE_DJE` | `INTERNAL_SEARCH` | `src=1 ctr=0 evt=0 mon=1 gap=1` | SOURCE_COVERAGE_GAP | - | https://www.tre-se.jus.br/legislacao/compilada/porta... | 2026-08-18 01:12:23 |
| `TRE-SP` | 8 | `TSE_TRE_DJE` | `INTERNAL_SEARCH` | `src=1 ctr=1 evt=0 mon=1 gap=0` | - | - | https://www.tre-sp.jus.br/legislacao/compilada/porta... | 2026-08-18 01:12:39 |
| `TRE-TO` | 8 | `TSE_TRE_DJE` | `INTERNAL_SEARCH` | `src=1 ctr=0 evt=0 mon=1 gap=0` | - | - | https://www.tre-to.jus.br/legislacao/compilada/resol... | 2026-08-18 01:12:47 |
