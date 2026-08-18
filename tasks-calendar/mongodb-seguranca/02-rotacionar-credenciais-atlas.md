# 2. Rotacionar e proteger credenciais do Atlas — CRÍTICO

`atlas-credentials.env` guarda usuário/senha/URI do MongoDB Atlas em texto
plano no disco. Vazamento (commit acidental, backup exposto, laptop
comprometido) = acesso de escrita total ao banco: promover tribunais,
apagar/forjar gaps, alterar prazos publicados.

## Tasks
- [ ] Confirmar que `atlas-credentials.env` está no `.gitignore` do projeto e
      nunca foi commitado (checar histórico do git)
- [ ] Rotacionar a senha/usuário atual no MongoDB Atlas (a credencial atual já
      foi usada em texto plano ao longo de várias sessões — tratar como
      potencialmente exposta)
- [ ] Avaliar mover a credencial para um cofre de segredos (variável de
      ambiente do CI, secrets manager) em vez de arquivo local, se o projeto
      for além de uso pessoal
- [ ] Restringir a network access list do Atlas (IP allowlist) em vez de
      permitir de qualquer IP, se ainda não estiver restrito
- [ ] Criar um usuário de banco com permissão só de leitura para uso em
      scripts de auditoria/consulta, separado do usuário de escrita usado
      pelos coletores
