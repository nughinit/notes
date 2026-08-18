# Nota: DataJud (CNJ) — atraso de atualização

O DataJud (`api-publica.datajud.cnj.jus.br`), API pública oficial do CNJ
mencionada como fonte complementar em
[09-migrar-diario-real.md](09-migrar-diario-real.md), tem um problema
conhecido relatado pelo usuário: **os dados às vezes atrasam meses** em
relação ao andamento real dos processos/tribunais.

**Implicação pra este projeto**: se o DataJud for usado no futuro (mesmo só
como sinal complementar), ele não pode ser tratado como fonte de
monitoramento em tempo real — qualquer `monitor_run`/`source_check`
alimentado por ele precisa deixar claro no `confidence`/metadata que o dado
pode estar defasado, para não contradizer silenciosamente uma fonte primária
mais recente (ex: uma portaria de feriado publicada esta semana não vai
aparecer no DataJud a tempo de ser útil pra decisão de prazo).
