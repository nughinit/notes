# 4. Validação estrutural na triagem (além de palavra-chave) — ALTO

O "contrato" de validação hoje só checa se o texto bruto contém
`legisla`/`portaria`/`resolu`/`ato normativo`. Uma página de erro, uma página
desfigurada (site invadido) ou uma página de phishing que mencione essas
palavras passaria na validação — não há checagem estrutural (número, data,
órgão emissor reconhecíveis).

## Tasks
- [ ] Definir um padrão mínimo de estrutura esperada por família (ex: presença
      de um número de ato no formato `NNN/AAAA`, uma data em formato
      reconhecível, nome do tribunal) além da palavra-chave solta
- [ ] Rejeitar (marcar `CONTRACT_ERROR`) páginas cujo texto visível seja
      anormalmente curto ou genérico demais para ser um catálogo real (ex:
      página de erro do CMS que por acaso cita "portaria" num menu)
- [ ] Adicionar um teste de "página de erro conhecida" (404 disfarçado, erro
      genérico do framework) como fixture negativa para cada família
- [ ] Revisar os 92 contratos ativos e checar se algum já teria passado
      incorretamente por essa validação fraca no passado (auditoria retroativa)
