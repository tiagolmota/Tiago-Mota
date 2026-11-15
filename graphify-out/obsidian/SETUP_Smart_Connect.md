---
tags: [setup, smart-connections, obsidian, fix]
---

# Fix: CLI REST 127.0.0.1:27125 (Smart Connections)

> Erro exibido na barra de estado do Obsidian: `CLI REST: 127.0.0.1:27125`

## O que é

O plugin **Smart Connections v2.4.6** tenta ligar-se ao **Smart Connect** — uma app companheira separada que corre em segundo plano no porto `27125`. O erro aparece quando essa app não está instalada ou não está a correr.

**O erro é cosmético** — o Smart Connections continua a funcionar (indexação de notas, pesquisa semântica), apenas sem o canal de comunicação local.

---

## Solução A — Instalar Smart Connect (recomendado)

1. Descarregar de: https://github.com/brianpetro/smart-connect/releases
2. Instalar e lançar (fica no tabuleiro do sistema)
3. Recarregar Obsidian → erro desaparece

---

## Solução B — Desativar o CLI REST no plugin

1. **Settings → Smart Connections → Smart Connect**
2. Desligar **"Enable Smart Connect server"**
3. Recarregar Obsidian

---

## Solução C — Usar Ollama (IA local, sem app, sem cloud)

```bash
# 1. Instalar Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Descarregar modelo de embeddings
ollama pull nomic-embed-text
```

Depois em Smart Connections:
- **AI Provider** → Ollama
- **Model** → `nomic-embed-text`
- Porto 27125 deixa de ser necessário

---

## Solução D — Usar OpenAI API

Em Smart Connections Settings:
- **AI Provider** → OpenAI
- Colar chave de API

Elimina o requisito REST local.

---

## Script de diagnóstico

```bash
bash scripts/smart-connect-fix.sh
```

---

## Integração Obsidian ↔ Claude

| Script | Função |
|---|---|
| `scripts/prepare-llm.sh` | Exporta notas-chave como contexto para Claude |
| `scripts/obsidian-vault-sync.sh <path>` | Sincroniza vault do projeto para vault local |
| `scripts/smart-connect-fix.sh` | Diagnóstico do erro CLI REST |

```bash
# Preparar contexto para Claude
bash scripts/prepare-llm.sh
# → .claude/sessions/vault-context.md

# Sincronizar vault do projeto para "Meu volt"
bash scripts/obsidian-vault-sync.sh ~/path/to/Meu\ volt
```
