# 6. Canonicalização não deve ignorar conteúdo relevante renderizado via JS — MÉDIO

`visible_text()` remove `<script>`/`<style>`/comentários inteiros antes de
gerar o hash canônico, para ignorar ruído (contadores, ads, tokens de
sessão). O efeito colateral: se um site passar a renderizar o conteúdo
jurídico via JavaScript (client-side rendering), a mudança real nunca
aparece no hash — o coletor sempre veria `NO_CHANGE` mesmo com portaria nova.

## Tasks
- [ ] Levantar quais dos 92 tribunais usam client-side rendering para a
      página de atos normativos (hoje o fetch é HTML bruto via HTTP GET na
      maioria dos casos, não o DOM renderizado)
- [ ] Para famílias que já usam Playwright (bypass anti-bot), considerar usar
      o DOM renderizado (`page.content()` pós-render) para o hash canônico em
      vez do HTML bruto, quando fizer sentido
- [ ] Adicionar um teste periódico que compara o texto visível via fetch
      simples vs. via browser renderizado para os mesmos 92 tribunais, para
      detectar se algum migrou para CSR sem o coletor perceber
