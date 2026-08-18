# 5. Verificação de autenticidade do conteúdo — MÉDIO-ALTO

Hoje a única checagem de autenticidade é o host terminar no sufixo oficial
(ex: `tjba.jus.br`). Isso protege contra puxar de um domínio errado, mas não
contra: hijack de DNS/subdomínio do próprio tribunal, ou o CMS oficial do
governo comprometido (servidor real, conteúdo alterado por invasor). Não há
verificação de assinatura digital (ICP-Brasil) dos documentos.

## Tasks
- [ ] Levantar quais tribunais publicam PDFs com assinatura ICP-Brasil
      verificável para os atos normativos (nem todos publicam só em HTML)
- [ ] Para esses casos, avaliar verificar a assinatura do PDF antes de aceitar
      como evidência, em vez de confiar só no hash do HTML/texto
- [ ] Adicionar verificação de certificado TLS do host (não só que a conexão
      é HTTPS, mas que o certificado é válido e não expirado/self-signed)
- [ ] Documentar esse risco residual explicitamente nos metadados de cada
      `legal_evidence` (nível de confiança da fonte: "host verificado" vs
      "documento assinado digitalmente")
