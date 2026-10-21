---
type: memory-index
---
# Memory

Esta pasta guarda memória persistente e partilhada entre sessões e entre
qualquer LLM ligado a este vault (por MCP ou por acesso direto ao sistema de
ficheiros) — não é privada de um único assistente ou cliente.

## Convenção

- Uma nota = um facto, preferência ou decisão atómica. Nada de notas gigantes
  a acumular tudo — mais fácil de rever, atualizar ou substituir uma coisa de
  cada vez.
- Frontmatter mínimo: `type: memory`. Acrescenta `tags:` se quiseres filtrar
  depois (ex.: `[preference]`, `[project-x]`).
- Antes de começar trabalho não-trivial neste vault, um assistente deve ler
  esta pasta (ou correr `memory_digest.py` a partir da skill "obsidian") para
  apanhar contexto relevante.
- Ao aprender algo que vale a pena lembrar depois desta conversa acabar,
  escreve ou atualiza uma nota aqui em vez de deixar ficar só na conversa.

Ver `Example - Preference.md` e `Example - Project Context.md` como ponto de
partida — podes apagá-las depois de perceberes o formato.
