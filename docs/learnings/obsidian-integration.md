# Obsidian ↔ Claude Integration

## Vault do Projeto
- Path: `graphify-out/obsidian/`
- 52 notas de alto valor + 83 fragmentos em `_graphify_raw/`
- Skin "brain neural" ativa (`.obsidian/snippets/brain-neural.css`)
- Plugins: Juggl (grafo 3D), Breadcrumbs, Dataview

## Sincronização com Vault Local
```bash
bash scripts/obsidian-vault-sync.sh ~/path/to/Meu\ volt
```
Cria subpasta `UFCD-10791/` no vault destino. Wikilinks internos preservados.

## Preparar Contexto para Claude
```bash
bash scripts/prepare-llm.sh
```
Exporta notas prioritárias para `.claude/sessions/vault-context.md`.

## Auto-injeção de Contexto (hook ativo)
O hook `UserPromptSubmit` detecta palavras-chave e injeta automaticamente:
- `docs/learnings/*.md` — angular, java, python, scientific-writing
- `graphify-out/obsidian/UFCD_*.md` — notas de segurança
- `graphify-out/obsidian/NLM_*.md` — notebooks de segurança

## CLI REST 127.0.0.1:27125
Ver `graphify-out/obsidian/SETUP_Smart_Connect.md` para soluções.
Fix rápido: `bash scripts/smart-connect-fix.sh`

## Estrutura da Memória
```
graphify-out/obsidian/
├── HOME.md          ← MOC principal (brain hub)
├── Index.md         ← Tabela de conteúdos
├── UFCD_*.md        ← 8 tópicos de segurança
├── NLM_*.md         ← 4 notebooks NotebookLM
├── _COMMUNITY_*.md  ← 11 comunidades do grafo
├── _graphify_raw/   ← 83 fragmentos de config (colapsado)
└── .obsidian/       ← Juggl, brain-neural CSS, graph.json
```
