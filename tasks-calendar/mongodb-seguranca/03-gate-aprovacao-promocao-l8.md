# 3. Gate de aprovação antes de promoção a L8 / resolução de gap — ALTO

Hoje qualquer execução de um script `run_*_l8.py` pode promover um tribunal a
L8 ou marcar um `coverage_gaps` como resolvido diretamente, sem nenhuma
aprovação separada — a mesma execução que coleta o dado também decide que ele
é "verdade oficial" no banco. Não há trilha de quem/quando aprovou uma
promoção além do `audit_log`, que é escrito pelo mesmo processo.

## Tasks
- [ ] Separar "coletar e propor" de "promover": o runner grava a evidência e
      um `status: PENDING_PROMOTION`, e uma segunda etapa explícita (manual ou
      um script separado) confirma a promoção
- [ ] Exigir que a etapa de promoção registre um `approved_by` no
      `audit_log` (hoje `actor` é sempre o nome do script, nunca uma pessoa)
- [ ] Aplicar o mesmo gate para `coverage_gaps.resolved = true` — resolver um
      gap também é uma afirmação de "verdade oficial" e hoje é uma escrita
      direta
- [ ] Documentar quem tem acesso de escrita ao Atlas hoje e revisar se faz
      sentido continuar com um único usuário de escrita compartilhado
