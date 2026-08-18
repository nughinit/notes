# Milestone: MongoDB 2 — Segurança da triagem

Segunda fase do trabalho no MongoDB do projeto
`legal_calendar_mongodb_v6_dejt_l8_candidate`, depois do milestone
[MongoDB perfeito](milestone-mongodb-perfeito.md) (integridade de dados,
concluído). Este aqui ataca as vulnerabilidades identificadas no processo de
coleta e triagem de portarias — priorizadas pelo impacto real num produto
jurídico: **dado errado sem alarme é pior que dado ausente**.

Subtasks detalhadas em [mongodb-seguranca/](mongodb-seguranca/), em ordem de
criticidade (1 = mais crítico).

## Tasks (por criticidade)
- [x] [1. Validação estrutural na normalização (evita prazo jurídico errado)](mongodb-seguranca/01-validacao-estrutural-normalizacao.md) ✅ — **CRÍTICO**
- [ ] [2. Rotacionar e proteger credenciais do Atlas](mongodb-seguranca/02-rotacionar-credenciais-atlas.md) ⚠️ **parcial — precisa de ação manual no console do Atlas** — **CRÍTICO**
- [ ] [3. Gate de aprovação antes de promoção a L8 / resolução de gap](mongodb-seguranca/03-gate-aprovacao-promocao-l8.md) ⚠️ **parcial — gate criado e testado, retrofit em 1/18 scripts** — **ALTO**
- [ ] [4. Validação estrutural na triagem (além de palavra-chave)](mongodb-seguranca/04-validacao-estrutural-triagem.md) ⚠️ **parcial — validador criado, achado real (TJAL) na auditoria retroativa** — **ALTO**
- [ ] [5. Verificação de autenticidade do conteúdo (assinatura/DNS)](mongodb-seguranca/05-verificacao-autenticidade-conteudo.md) — **MÉDIO-ALTO**
- [ ] [6. Canonicalização não deve ignorar conteúdo relevante renderizado via JS](mongodb-seguranca/06-canonicalizacao-conteudo-js.md) — **MÉDIO**
- [ ] [7. Revisar risco do bypass anti-bot via Playwright](mongodb-seguranca/07-revisar-bypass-antibot.md) — **MÉDIO**
- [ ] [8. Rate limiting explícito na coleta em lote](mongodb-seguranca/08-rate-limiting-coleta.md) — **BAIXO**
- [ ] [9. Migrar tribunais para fonte de Diário real (padrão TJRS/DOE-RS)](mongodb-seguranca/09-migrar-diario-real.md) ⚠️ **4/7 corrigidos (TJAL, TJGO, TJPA, TJRJ — este via [11](mongodb-seguranca/11-batch2-sitemap-migration.md), fonte diferente da originalmente cogitada), TJMG bloqueado por CAPTCHA real, TJES corrigido via [11](mongodb-seguranca/11-batch2-sitemap-migration.md), 1 pendente (TJPB — precisa automação de formulário)**
- [ ] [10. Nota: DataJud (CNJ) atrasa meses](mongodb-seguranca/10-datajud-caveat.md) — não usar como fonte de monitoramento em tempo real
- [ ] [11. Migrar os 17 tribunais restantes em sitemap genérico](mongodb-seguranca/11-batch2-sitemap-migration.md) ⚠️ **12/17 corrigidos (TJAC, TJDFT, TJMA, TJCE, TRT24, TJPR, TJMMG, TRT1, TJES, TJRJ, TJRS, TRF6); 2 bloqueados por CAPTCHA/verificação humana (TRT17, TJSC); 2 bloqueados por Akamai (TJRO, TJMSP); 1 pendente automação de formulário (TJPB)**

## Referência
Origem: análise de segurança do pipeline de coleta/triagem discutida em
2026-08-18, depois de concluído o milestone MongoDB perfeito (auditoria
`STATUS PASS`, 92/92 tribunais em L8).
