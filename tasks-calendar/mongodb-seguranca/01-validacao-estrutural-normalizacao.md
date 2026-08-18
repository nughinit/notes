# 1. Validação estrutural na normalização — CRÍTICO

## Por que é o mais crítico
Achado real durante o milestone MongoDB perfeito: o normalizador trocava a
origem pelo alvo em relações `AMENDS`/`REVOKES` (regex pegando o número
errado do texto livre). Isso não gera erro nem alarme — o dado "parece"
válido e passa por todas as checagens de schema. Num produto jurídico, isso
significa risco de **prazo calculado errado sem qualquer sinal de alerta**.

## Tasks
- [ ] Escrever testes de regressão cobrindo o bug já encontrado (troca
      origem/alvo em `act_id`/`target_act_id`) usando os 11 casos reais da
      subtask 3 do milestone MongoDB perfeito como fixtures
- [ ] Definir validação estrutural pós-normalização: todo `legal_acts` deve
      ter `act_type`, `number`, `year` coerentes com o texto de origem antes
      de ser aceito (não só "existe uma string parecida com portaria")
- [ ] Adicionar checagem de consistência semântica: se `relation_type` é
      `AMENDS`/`REVOKES`, o `act_id` deve ter data de publicação posterior à
      do `target_act_id` (um ato não pode alterar um ato futuro)
- [ ] Adicionar essa checagem ao `scripts/audit_legal_calendar_atlas.py` como
      crítico (não warning) — inconsistência de data em relação é bug de
      dado, não pendência
- [ ] Revisar os outros extratores de campo (datas, escopo, efeito jurídico)
      em busca do mesmo tipo de erro heurístico
