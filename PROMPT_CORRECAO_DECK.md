# Prompt: alinhar tabelas, gráficos e fluxogramas ao padrão visual

Cole este texto inteiro numa nova sessão do Claude anexando o .pptx. Ele já traz as specs e os locais dos problemas, então não é preciso reenviar a skill nem reanalisar o deck.

---

Arquivo: AULA_DOR_TORACICA_PROTOCOLO_2025_tabelas_nativas2.pptx (100 slides, 13,33 × 7,5 pol, 12.192.000 × 6.858.000 EMU). "Slide N" é a posição na apresentação. Trabalhe numa cópia e não altere o original.

## Regras deste trabalho
1. **Nunca apagar, resumir, reordenar nem corrigir texto.** Só mudar formatação, tamanho e posição, e dividir slides quando indicado. Se um texto não couber, divida o slide ou reduza o espaçamento. Nunca reduza a fonte abaixo de 12 pt.
2. Não inventar dados nem cabeçalhos. Se faltar algo, use colchetes, como `[__]`, e liste na resposta.
3. Preservar notas do apresentador, posição no deck, título no placeholder title, rodapé (`NN  ·  Dor torácica – Protocolo 2025 | Set 2026`, y = 6.181.344 EMU, à esquerda) e "SEU LOGO" à direita. Depois de dividir slides, renumere o rodapé.
4. Ao dividir um slide, o novo slide repete o título com "(1/2)" e "(2/2)", como o deck já faz.
5. Números no formato pt-BR (1.234,5 e 12%).
6. Instalar a Roboto antes de renderizar (`pip download font-roboto`; extrair Roboto-Regular, Medium, Bold e Italic para ~/.fonts; `fc-cache -f`). Validar o arquivo, renderizar só os slides alterados e olhar cada um: estouro, sobreposição, texto colado no rodapé.
7. Ao final, listar o que foi alterado, o que não foi feito e por quê.

## Specs mínimas (as únicas necessárias)
**Cores.** Sequência de itens: `#4E7C8B` (texto `#FBFCFC`), `#6E9DAB` (texto `#1F3238`), `#8EC4CB` (texto `#1F3238`), `#6B6E70` (texto `#FBFCFC`), `#A3A6A8` (texto `#1F3238`). Fundo `#FBFCFC`, Superfície `#F2F4F5`, Trilho `#E4E6E7`, título `#3B3F42`, corpo `#5F6468`, apoio `#737A7F`, tinta `#1F3238`. Semânticas `#3E8E68`, `#C98A2B` e `#B5533C`, só para status e sempre com a palavra escrita ao lado. Nenhuma outra cor. Nunca texto branco sobre `#6E9DAB`, `#8EC4CB`, `#A3A6A8` ou `#C9E3E6`.

**Tipografia.** Só Roboto. Título 28 pt medium. Bloco ou cabeçalho 15 pt medium. Corpo e tabela 13 pt. Rótulo, legenda, fonte e rodapé 12 pt (mínimo absoluto). Tabela com 6 colunas pode usar 12 pt; com menos colunas, 13 pt.

**Tabela.** No máximo 7 linhas × 6 colunas. Cabeçalho `#4E7C8B` com texto `#FBFCFC` medium. Zebra `#F2F4F5`. Bordas `#E4E6E7` de 1 pt. Números à direita e texto à esquerda. Fonte abaixo da tabela. Conteúdo até y ≈ 6.100.000 EMU.

**Fluxograma.**
- Início e fim: pílula `#4E7C8B`, texto `#FBFCFC` 13 pt medium.
- Etapa: retângulo `#F2F4F5` com borda de 1 pt `#6E9DAB`, texto `#3B3F42` 13 pt medium.
- Decisão: losango `#8EC4CB`, pergunta curta terminada em "?", texto `#1F3238` 12 pt medium, até 3 palavras por linha.
- Setas: 1,5 pt `#6B6E70` com ponta, sempre em ângulo reto, sem cruzar formas nem texto. Retorno tracejado, passando por baixo, com rótulo de 12 pt `#737A7F`.
- Rótulos "Sim" e "Não": 12 pt medium `#4E7C8B`, junto à saída do losango. No vertical, "Não" sai pela esquerda e "Sim" pela direita.
- Texto nas caixas: 1 a 3 palavras. A explicação longa vai para as notas do apresentador.
- Caixas da mesma linha têm mesma largura e altura, com espaçamento igual (≈ 60 px).
- No máximo 6 formas, 1 decisão e 1 retorno por slide no horizontal. No vertical, no máximo 2 decisões. Se passar disso, dividir em visão geral e detalhe.

**Gráfico.** Só colunas, barras, linha ou barras de progresso. Séries na ordem `#4E7C8B`, `#8EC4CB`, `#6B6E70`, `#6E9DAB`, `#A3A6A8`, `#C9E3E6`. Legenda em linha acima, só grade horizontal `#E4E6E7`, eixo base `#A3A6A8`, fonte do dado no rodapé. O subtítulo do slide é a conclusão do gráfico, em 1 linha, 13 pt `#737A7F`.

## O que corrigir

### A. Tabelas com fonte de 12 pt onde deveria ser 13 pt
Passar para 13 pt: slide 14 (tabela de 2 colunas × 18 linhas), slide 53 (as 3 tabelas), slide 74 (as 2 tabelas) e slide 75 (as 3 tabelas). Se estourar, dividir conforme o item B.

### B. Tabelas com mais de 7 linhas: dividir em 2 slides
Dividir mantendo o cabeçalho nos dois slides e sem apagar nenhuma linha:
- Slide 14: 18 linhas, dividir em 3 slides de 6 (o número de partes fica a seu critério).
- Slides 53, 65 (10 linhas cada), 52, 54, 71, 75 (9 linhas cada), 51 e 66 (8 linhas cada).
- Slides 53, 74 e 75 têm mais de uma tabela no mesmo slide. Deixar uma tabela por slide.

### C. Slides 96 e 99: sem linha de cabeçalho
Ambos são tabelas de 1 coluna em que a primeira linha é conteúdo. **Não pintar a primeira linha de Teal e não inventar cabeçalho.** Faça a pergunta antes: (a) deixar como está, (b) acrescentar uma linha de cabeçalho com o texto que o autor indicar, ou (c) converter em lista com marcadores. Sem resposta, aplicar só o cabeçalho `[título da coluna]` em colchetes.

### D. Cores semânticas em células de tabela
Nos slides 35, 64, 68, 69, 70, 71, 74, 75 e 76, `#3E8E68`, `#C98A2B` e `#B5533C` aparecem como fundo de célula para classe de recomendação ou nível de evidência. O padrão as reserva a status com a palavra escrita ao lado. Manter a cor só se a palavra do status estiver escrita na própria célula. Se a célula tiver apenas a classe (I, IIa, IIb…), avisar o autor e propor `#4E7C8B` ou `#6E9DAB`, seguindo a regra de contraste. Não decidir sozinho.

### E. Fluxogramas nativos (slides 29, 59, 61, 63, 73, 77)
- **Texto das caixas:** hoje há frases inteiras. Reduzir a 1–3 palavras e mover o texto original completo, sem cortar nada, para as notas do apresentador. Alertar quando a redução mudar o sentido clínico, e o autor valida.
- **Tamanhos:** igualar largura e altura das caixas da mesma linha ou coluna. Alturas atuais de 0,57 a 0,98 pol, e larguras de 2,72 a 3,94 pol.
- **Slides 59 e 77 (duplicados, ≈ 10 formas) e 61 (7 formas):** dividir em visão geral e detalhe. Os slides 77 e 59 têm o mesmo conteúdo; perguntar se um deles pode ser removido, sem remover por conta própria.
- **Slide 63:** não tem losango nem pílulas de início e fim, e "Primeira etapa" e "Segunda etapa" são caixas soltas sobre linhas. Refazer como fluxo com pílula de início, etapas alinhadas e setas contínuas em ângulo reto, sem segmentos soltos. Dividir em 2 slides, pois tem 9 caixas.
- **Slides 59, 61 e 77:** o rótulo "Sim" (x ≈ 5,48–5,92 pol) invade a linha vertical em x = 5,83 pol. Reposicionar junto à saída do losango, sem tocar em linhas.
- **Slide 73:** o losango tem 4 linhas de texto. Reduzir a até 3 palavras por linha, com "?" no final.
- Slides 60, 62 e 78 (definições) e 74–76 (tabela mais formas): conferir só as formas, pois as tabelas já foram vistas.

### F. Gráficos nativos
- **Slide 22** (colunas 100% empilhadas: IAM ST × IAM NST em CD, DA e Cx). O tipo não está no catálogo (só colunas agrupadas). Migrar para colunas agrupadas se o autor aprovar, mantendo os rótulos "527 / 79%" etc. como estão (são 2 parágrafos por rótulo, e isso está correto). O subtítulo "2.281 pctes. com oclusão coronária aguda" descreve, mas não conclui. Propor uma frase de conclusão e o autor aprova.
- **Slide 48** (colunas agrupadas: Low-Risk × High-Risk em Death, AMI e Composite). Adicionar subtítulo com a conclusão, em colchetes se você não tiver o dado. Manter as séries em inglês, como no original, e avisar. A fonte está truncada: "Circulation. 2018;138:2456–246". **Não corrigir**; listar como possível erro do original.

### G. Fluxogramas que ainda são imagem (candidatos a refazer como nativos)
- **Slides 30, 31 e 45:** mesma figura central da diretriz, repetida 3 vezes.
- **Slides 33 e 72:** mesma figura (rota diagnóstica), repetida.
- **Slides 43 e 44:** fluxos de troponina 0-1h/0-2h e 0-3h.
- **Slide 50:** ADD-RS.
- **Slide 55:** TEP.
- Só refazer se o autor pedir: são figuras de diretriz com ilustrações e logos. Se refizer, usar as formas da seção "Fluxograma", manter o texto palavra por palavra (podem ser mais de 6 formas, então dividir em slides) e recortar, sem redesenhar, as ilustrações e ícones. Antes de refazer, perguntar quais slides.

### H. Ficam como imagem (não mexer)
Slides 15, 17, 24 e 26 (ECG e esquemas) e 56 (infográfico).

## Ordem sugerida
A → B → D → E → F. Depois, C e G, com as respostas do autor.

## Resposta final (poucas linhas)
Listar os slides alterados, o que virou dois slides, textos movidos para as notas, erros do original mantidos, decisões pendentes e qualquer desvio inevitável do padrão.
