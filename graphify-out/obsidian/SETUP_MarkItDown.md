---
tags: [setup, markitdown, obsidian, llm, import]
---

# MarkItDown — Importar Documentos para o Vault

> Microsoft MarkItDown converte qualquer ficheiro em Markdown para alimentar o vault e o Claude.

## Instalar

```bash
pip install -r requirements.txt
```

## Formatos suportados

| Formato | Extra | Notas |
|---|---|---|
| PDF | `[pdf]` | Texto estruturado via pdfminer + pdfplumber |
| Word (.docx) | `[docx]` | Mammoth, preserva estilos |
| PowerPoint (.pptx) | `[pptx]` | Slides, notas, tabelas |
| Excel (.xlsx/.xls) | `[xlsx]` | Tabelas como Markdown |
| HTML | built-in | Converte tags para MD |
| CSV / JSON / XML | built-in | Estrutura tabular |
| Imagens | built-in | Metadados EXIF |
| URLs | built-in | Qualquer página web |
| YouTube | `[youtube]` | Transcrição automática |
| Outlook (.msg) | `[outlook]` | E-mails |

## Uso rápido

```bash
# Importar um PDF para o vault
python scripts/vault-import.py relatorio.pdf

# Importar com tag e pasta
python scripts/vault-import.py slides.pptx --tag ufcd10791 --folder UFCD_imports

# Importar múltiplos PDFs
python scripts/vault-import.py *.pdf --folder PDFs --tag segurança

# Importar URL / artigo web
python scripts/vault-import.py https://owasp.org/www-project-top-ten/

# Importar transcrição YouTube
python scripts/vault-import.py https://youtu.be/VIDEO_ID --tag notebooklm

# Importar para vault diferente
python scripts/vault-import.py doc.pdf --vault ~/Meu\ volt/UFCD-10791
```

## Integração com Claude

Depois de importar, o ficheiro `.md` aparece no vault e pode ser:
- Referenciado com `[[nome-do-ficheiro]]` em outras notas
- Injetado automaticamente pelo hook `inject-context` se tiver palavras-chave relevantes
- Incluído no contexto via `bash scripts/prepare-llm.sh`

## Pipeline completo

```bash
# 1. Converter documentos de curso → vault
python scripts/vault-import.py material_aula.pdf --tag ufcd10791 --folder UFCD_imports

# 2. Actualizar grafo de conhecimento
graphify update .

# 3. Exportar contexto para Claude
bash scripts/prepare-llm.sh
```

## API Python (uso avançado)

```python
from markitdown import MarkItDown

md = MarkItDown()

# Qualquer ficheiro ou URL
result = md.convert("documento.pdf")
print(result.text_content)

# Com descrição de imagens via Claude
from anthropic import Anthropic
client = Anthropic()
md = MarkItDown(llm_client=client, llm_model="claude-sonnet-4-6")
result = md.convert("diagrama.png")
```
