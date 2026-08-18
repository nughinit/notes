# Milestone: API para Intimatio funcionando

Baseado em
`legal_calendar_mongodb_bootstrap_v2_filled/docs/FUTURE_API_CONTRACT.md` e
`docs/DB_BUILD_CHECKLIST.md` (itens finais: "Criar API independente" e
"Só depois criar adapter da Intimatio") do projeto
`legal_calendar_mongodb_v6_dejt_l8_candidate`. Hoje não existe nenhum serviço
de API implementado no repositório — apenas o contrato documentado.

## Pré-requisito
- [ ] Concluir o milestone [MongoDB perfeito](milestone-mongodb-perfeito.md)
      antes de expor dados via API (checklist determina essa ordem)

## Tasks pendentes — construir a API independente

- [ ] Escolher stack e criar esqueleto do serviço de API (fora do banco,
      conforme "Criar API independente" no checklist)
- [ ] `GET /v1/courts` — cobertura, fontes e saúde do monitor
- [ ] `GET /v1/calendar/{court_id}?from=YYYY-MM-DD&to=YYYY-MM-DD&scope=...` —
      eventos normalizados
- [ ] `GET /v1/business-day/{court_id}/{date}?scope=...` — retorno
      `is_business_day`, `deadline_effect`, `reason`, `act_id`, `source_url`,
      `confidence`
- [ ] `GET /v1/events/{event_id}` — evento + ato + evidência
- [ ] `GET /v1/changes?court_id=...` — alterações detectadas
- [ ] `GET /v1/sources/{court_id}` — fontes, coverage_assertion e último
      `monitor_run`
- [ ] `POST /v1/refresh/{court_id}` — dispara atualização do tribunal no
      serviço independente
- [ ] Testes de contrato para cada endpoint (schema, status codes, casos de
      tribunal sem cobertura)
- [ ] Documentar autenticação/rate limit do serviço (não coberto no contrato
      atual)

## Tasks pendentes — adapter da Intimatio (somente após a API estar pronta)

- [ ] Criar adapter que consome a API acima e traduz para o formato que a
      Intimatio espera: data/intervalo, escopo, efeito jurídico, ato, fonte,
      confiança, versão
- [ ] Garantir que a Intimatio não armazene regras específicas de scraping por
      tribunal — toda descoberta/normalização/auditoria continua no Legal
      Calendar
- [ ] Testes de integração ponta a ponta: Legal Calendar → API → adapter →
      Intimatio

## Referência
- Contrato completo: `legal_calendar_mongodb_bootstrap_v2_filled/docs/FUTURE_API_CONTRACT.md`
- Checklist: `legal_calendar_mongodb_bootstrap_v2_filled/docs/DB_BUILD_CHECKLIST.md`
