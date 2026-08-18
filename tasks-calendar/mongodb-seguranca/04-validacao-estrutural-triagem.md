# 4. Validação estrutural na triagem (além de palavra-chave) — PARCIAL ⚠️ (ALTO)

## O que foi criado
- [x] `scripts/content_structure_validator.py` — substitui o check antigo (5
      palavras soltas) por: tamanho mínimo, léxico amplo de tipos documentais
      (baseado no repertório nacional da Intimatio — Portaria, Ato Normativo,
      Decreto, Resolução, Provimento, Ordem de Serviço, Instrução Normativa,
      Calendário, Feriado, Ponto Facultativo, Recesso), citação de número de
      ato (`NNN/AAAA`), ano plausível, e opcionalmente verbo de efeito
      jurídico (`suspende`/`prorroga`/`revoga`/`altera`/etc — mesma regra
      central da Intimatio: "nenhum termo isolado determina sozinho que um
      documento altera prazo", tipo + verbo/efeito juntos)
- [x] 8 testes em `tests/test_content_structure_validator.py`, incluindo
      fixture negativa que só o check novo pega (página mencionando
      "portaria" uma vez, sem citação de ato — o check antigo deixaria passar)
- [x] Retrofit no coletor de referência (`run_trt19_boletim_l8.py`):
      `validate()` agora usa `validate_legal_catalog_page(..., require_effect_verb=True)`
      — confirmado sem regressão contra o snapshot real já promovido

## Auditoria retroativa — achado real, não só teórico
Rodei o validador novo contra os **64 snapshots HTML reais** ainda presentes
em disco (`runtime/snapshots/**`) e depois, casando por hash, contra os
**27 snapshots que correspondem a contratos L8 ativos hoje**:

- **11/27 passam** sem ajuste (TRF1, TRF2, TRF5, TJAP, TJPI, TJRN, TJSP,
  TJTO, TRT19, TRT22, TRT23)
- **15/27 falham em `NO_ACT_NUMBER_CITATION`** — investigado caso a caso:
  a maioria (ex: TJBA) tem conteúdo real (anos 2021-2026, arquivo por
  semestre) mas é uma **página de índice por ano**, sem citação de número de
  ato na própria página — **calibração do meu regex, não problema da fonte**
- **1/27 falha em `TOO_SHORT`** (TJMT)
- **Achado mais sério, isolado no meio disso**: **TJAL** — a "evidência L8"
  desse tribunal é literalmente uma página de **formulário de busca vazio**
  do CDJE (Consulta de Diário da Justiça Eletrônico), **zero conteúdo de
  calendário/portaria** (0 números, texto genérico "Consulta de Diário").
  TJAL foi promovido a L8 com um critério antigo mais fraco ("fonte real e
  estável, buscada duas vezes" — nunca validou se o conteúdo é sobre
  calendário). Ver task nova
  [migrar-tribunais-diario-real](../milestone-mongodb-2-seguranca.md) para o
  contexto completo desse achado
- **65/92 tribunais L8 não têm arquivo local disponível** para auditar
  retroativamente (snapshots de sessões anteriores só existem como metadado
  no banco, o arquivo em si não sobreviveu) — a auditoria retroativa cobre
  só o que está fisicamente em disco hoje

## Por que não está 100% concluído
- Regex de citação de ato (`ACT_NUMBER_RE`) precisa aceitar formato de
  página-índice (ano sem número de ato citado inline) sem virar bobo demais
  e aceitar qualquer coisa — calibração fina ainda não feita
- `require_effect_verb=True` só foi validado contra 1 fixture real (TRT19) —
  arriscado tornar padrão em todos os coletores sem testar contra mais
  formatos de página primeiro
- Retrofit aplicado só no coletor de referência; os outros ~17 continuam com
  o check antigo de 5 palavras

## Auditoria e testes seguem passando
`STATUS PASS`, `critical=0`, `warn=0`; 62/62 testes (`pytest tests/`)
