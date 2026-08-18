# Court Registry — Health & Automation Status

> Companion to `TRIBUNAIS_REGISTRO.md`. The registry remains the 92-court MongoDB snapshot; this document defines the human-readable operational status model. Only states supported by repository evidence are marked as known. Unknown values must remain `UNKNOWN` rather than inferred from L8.

## Core rule

**Coverage ≠ Automation ≠ Confidence ≠ Normative depth.**

A court may be L8 and still have incomplete normative depth, a blocked transport, or an automation limitation. L8 means the project has proven official-source monitoring with persisted evidence; it must not be used as a synonym for “fully automated” or “high confidence”.

## Status dimensions

| Dimension | Values | Meaning |
|---|---|---|
| Coverage | `L0`–`L8` | Existing coverage model from MongoDB |
| Source type | `REST_API`, `SOAP_API`, `HTML`, `HTML_PDF`, `INTERNAL_SEARCH`, `SPA_SEARCH`, `OTHER` | Technical form of the official source |
| Automation | `FULL`, `PARTIAL`, `BLOCKED`, `MANUAL`, `UNKNOWN` | Whether collection can run unattended |
| Source quality | `STRONG`, `ACCEPTABLE`, `WEAK`, `UNKNOWN` | Quality of the source for Legal Calendar's purpose, not merely whether the domain is official |
| Confidence | `HIGH`, `MEDIUM`, `LOW`, `UNKNOWN` | Confidence supported by evidence + validation + repeatability |
| Structural validation | `PASS`, `PARTIAL`, `FAIL`, `UNKNOWN` | Whether collected content is structurally proven to be relevant legal/calendar material |
| Promotion gate | `GATED`, `DIRECT_WRITE`, `N/A`, `UNKNOWN` | Whether promotion/state mutation requires the approval gate |
| Normative depth | `COMPLETE`, `OPEN_GAP`, `UNKNOWN` | Whether amendment/revocation/republication relationships are covered |
| Blocker | free text / `-` | CAPTCHA, WAF, Akamai, authentication, source limitation, etc. |

## Confidence policy

Do not derive confidence from `coverage.level_number` alone.

- `HIGH`: official source + relevant content structurally validated + repeatable/refetch evidence + no known material limitation for the claimed capability.
- `MEDIUM`: official and useful source, but with a documented limitation (partial endpoint, fragile interaction, incomplete depth, etc.).
- `LOW`: evidence is weak, stale, indirect, or does not sufficiently prove the claimed capability.
- `UNKNOWN`: repository evidence is insufficient to assign a level safely.

## Automation policy

- `FULL`: normal collection path runs without human interaction.
- `PARTIAL`: part of the workflow is automated but a human or fragile interactive step remains.
- `BLOCKED`: a known technical/access barrier prevents unattended collection.
- `MANUAL`: intentionally human-operated.
- `UNKNOWN`: not yet verified.

## Current verified project health

| Metric | Current state |
|---|---:|
| Courts | **92** |
| L8 coverage | **92/92** |
| Open normative-depth gaps | **21** |
| `SOURCE_COVERAGE_GAP` audited as valid | **21/21** |
| Stale gaps found in read-only audit | **0** |
| Generic-source migration | **15/17** |
| Remaining access-blocked migration cases | **2 — TJRO, TJMSP** |
| Latest documented audit | **PASS_WITH_KNOWN_EXCEPTION** |
| Critical findings in latest documented audit | **0** |

The 21 `SOURCE_COVERAGE_GAP` entries are normative-depth debt (amendment/revocation/republication chains). They do **not** contradict L8 by themselves.

## Verified exceptions / noteworthy courts

| Court | Coverage | Source / transport | Automation | Structural evidence | Normative depth | Confidence | Note |
|---|---:|---|---|---|---|---|---|
| TJAL | L8 | REST API for official documents | FULL | PASS | OPEN_GAP | HIGH | Previous empty-search-form evidence was replaced by a real official documents API |
| TJPA | L8 | Official DJe REST API | FULL | PASS | OPEN_GAP | HIGH | Live structured official source |
| TJRS | L8 | Current DJe PDF pipeline | FULL | PASS | no open gap recorded | HIGH | Current edition discovered from TJRS home and PDF parsed without browser |
| TJSC | L8 | Public REST source | FULL | PASS | no open gap recorded | HIGH | Earlier security-verification path was avoided by finding a usable real source |
| TRT17 | L8 | DEJT administrative PDF | FULL | PASS | no open gap recorded | HIGH | Corrected 2026-08-18; repeatable PDF fetch and structural validation |
| TJRO | L8 | Existing L8 evidence; newer target blocked by Akamai | BLOCKED | UNKNOWN for replacement path | OPEN_GAP | UNKNOWN | Browser itself is blocked on target portal; do not equate existing L8 with successful new automation |
| TJMSP | L8 | Official acts page identified | BLOCKED | content identified in browser | no open gap recorded | UNKNOWN | Akamai rejects simple HTTP clients; unattended replacement collector unresolved |
| TJMG | L8 | HTML/PDF / official calendar evidence | UNKNOWN | existing evidence | OPEN_GAP | UNKNOWN | Real human-verification/CAPTCHA exists on DJe path; normative-depth gap remains |

## Target 92-court table

The next regeneration of `TRIBUNAIS_REGISTRO.md` should use this column order:

| court_id | branch | coverage | source_type | adapter | automation | source_quality | structural_validation | promotion_gate | confidence | normative_depth | blocker | source_url | updated_at |
|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|

Rules for generation:

1. Never infer `FULL` automation from `lvl=8`.
2. Never infer `HIGH` confidence from `lvl=8`.
3. `SOURCE_COVERAGE_GAP` maps to `normative_depth=OPEN_GAP`, not to failed L8 coverage.
4. Missing evidence maps to `UNKNOWN`, not a guessed status.
5. Preserve the raw MongoDB fields needed by developers (`adapter`, transport/source type, URL, timestamps).
6. Keep blockers explicit even when coverage is L8.
7. Prefer active/superseding source contracts over historical contracts when describing the current path.
8. When a source was replaced, preserve the replacement history in notes/changelog rather than presenting the superseded source as current.

## Next data pass

To complete the 92-court operational view safely, regenerate from MongoDB plus repository evidence and populate, per court:

- automation status;
- source quality;
- structural-validation status;
- promotion-gate status of the responsible collector;
- confidence;
- normative-depth status;
- explicit blocker/limitation.

Until that pass is executed, `UNKNOWN` is the correct value whenever the evidence is not explicit.
