# 2. Rotacionar e proteger credenciais do Atlas — PARCIAL ⚠️ (CRÍTICO)

## O que já está OK (verificado)
- [x] `atlas-credentials.env` já está no `.gitignore` do projeto
- [x] O diretório do projeto **não é um repositório git** (`git status` →
      "not a git repository") — não há histórico nenhum, então não há risco
      de a credencial já ter sido commitada neste projeto

## Achado novo, mais grave do que o esperado
Ao inspecionar os privilégios reais da credencial em uso
(`connectionStatus` com `showPrivileges`), o usuário `nughinit_db_user` tem
papel **`atlasAdmin`** — administração quase total do projeto Atlas
(gerenciar usuários, mudar rede, apagar cluster), não só leitura/escrita no
banco `legal_calendar`. Se essa credencial vazar, o dano possível é muito
maior do que "alguém mexe nos dados" — é controle do projeto Atlas inteiro.

## O que eu tentei e não consegui (precisa da sua conta)
- [ ] Tentei criar um usuário `legal_calendar_readonly` (só leitura, escopado
      ao banco `legal_calendar`) diretamente via driver — **negado**: mesmo
      com `atlasAdmin`, o Atlas não permite `createUser` pela conexão direta
      ao cluster. Gerenciamento de usuário só é feito pelo console web
      (cloud.mongodb.com) ou API Admin do Atlas (chave de API que não tenho)

## O que fazer no console do Atlas (cloud.mongodb.com), você mesma/o
Cluster: `cluster0.l7ogmzb.mongodb.net` (só o host, sem credenciais)

- [ ] **Rotacionar a senha** do usuário `nughinit_db_user`: Database Access →
      editar o usuário → Edit Password. Depois atualizar `atlas-credentials.env`
      local com a senha nova
- [ ] **Criar um usuário read-only separado** (`legal_calendar_readonly` ou
      similar): Database Access → Add New Database User → role
      `read` restrito ao banco `legal_calendar` (não `atlasAdmin`, não
      `readWriteAnyDatabase`) — usar esse para `audit_legal_calendar_atlas.py`
      e outros scripts que só leem
- [ ] **Restringir o papel do usuário principal**: hoje `nughinit_db_user` tem
      `atlasAdmin`; o ideal para os coletores (`run_*_l8.py`) é
      `readWrite` escopado só ao banco `legal_calendar`, não administração do
      projeto inteiro
- [ ] **Checar/restringir Network Access (IP Access List)**: Network Access →
      confirmar se está aberto para `0.0.0.0/0` (qualquer IP) ou restrito;
      se aberto, considerar restringir ao IP de quem roda os scripts

## Depois de rotacionar
- [ ] Atualizar `atlas-credentials.env` com a nova senha/usuário
- [ ] Rodar `python scripts/audit_legal_calendar_atlas.py` para confirmar que
      a nova credencial funciona antes de descartar a antiga
