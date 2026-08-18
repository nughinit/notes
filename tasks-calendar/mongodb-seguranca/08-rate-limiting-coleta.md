# 8. Rate limiting explícito na coleta em lote — BAIXO

Hoje só existe um `sleep` de ~1-2s entre os 2 fetches de confirmação de um
mesmo tribunal. Rodando os 92 tribunais em lote (vários `run_*_l8.py`
sequenciais), não há limite explícito de requisições por minuto por domínio —
risco baixo mas real de gerar carga perceptível nos sites do governo.

## Tasks
- [ ] Definir um intervalo mínimo entre requisições ao mesmo domínio,
      configurável por família
- [ ] Adicionar um limite de concorrência global (não rodar vários coletores
      de famílias diferentes em paralelo sem controle)
- [ ] Documentar um "orçamento" de requisições diário por tribunal no
      `source_contracts`, coerente com o ritmo real de monitoramento necessário
      (portarias não mudam a cada minuto)
