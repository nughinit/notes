# 3. Corrigir os 10 `act_relations_broken_refs`

IDs: `rel_60bfad572b78c380b4e6df75`, `rel_d44477c109aaf5e572910cfa`,
`rel_13d3e25f4ee2ba40659d4806`, `rel_7dae9624bb9e882a978cc8ed`,
`rel_a1fe5bd23a066080b26d85ad`, `rel_072157c184654082678cd9ca`,
`rel_632ac66be12a02f675f13cf6`, `rel_88e6317f779eea3092a806c1`,
`rel_12c8c9cc003f32c8e758fae3`, `rel_6bd5dfdcad6233bb5383e19b`.

- [ ] Para cada um, identificar se `act_id` ou `target_act_id` é o lado quebrado
- [ ] Corrigir o relacionamento (apontar para o `legal_acts._id` correto) ou
      remover a relação se o ato de destino nunca existiu
- [ ] Revalidar com `scripts/validate_database.py`
