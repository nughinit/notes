# 7. Revisar risco do bypass anti-bot via Playwright — MÉDIO

Vários tribunais (TRE-*, TRT19) só são acessíveis via browser real
(Playwright) porque proteção Akamai/CloudFront bloqueia fetch simples. Isso
funciona, mas: (a) executa JavaScript de um site de terceiros num browser
real — se o site fosse comprometido, seria execução de código não confiável
na máquina que roda o coletor; (b) tecnicamente contorna uma defesa que o
próprio tribunal colocou no ar.

## Tasks
- [ ] Rodar o Playwright desses coletores em um ambiente isolado (container
      efêmero/sandbox) em vez da máquina principal, já que carrega JS de site
      de terceiro
- [ ] Documentar explicitamente, por tribunal, por que o bypass é necessário
      (evidência do bloqueio) para justificar a exceção
- [ ] Avaliar se algum desses tribunais oferece uma API oficial ou feed RSS/
      Atom que dispensaria o bypass (ex: o TSE já usa REST direto, achado
      durante o milestone MongoDB perfeito)
