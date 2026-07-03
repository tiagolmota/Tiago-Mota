# Ligar o Claude ao vault do Obsidian por MCP

Os scripts em `../scripts/` funcionam sempre, mesmo sem rede (bom para sessões
remotas como o Claude Code on the web, que não conseguem alcançar o teu
computador). Mas se estiveres a correr Claude Desktop ou Claude Code
**localmente**, na mesma máquina onde o Obsidian está aberto, um servidor MCP
dá acesso ao vault em tempo real (ler, escrever, pesquisar) sem precisar de
apontar caminhos de ficheiros manualmente — e mantém o vault como memória
persistente do Claude entre sessões, já que as notas continuam lá depois da
conversa terminar.

Isto **não é possível configurar a partir desta sessão remota** — o servidor
MCP tem de correr na tua máquina, ao lado do Obsidian. Este ficheiro é o guia
para fazeres isso localmente.

## Opção A — plugin "Local REST API" + `mcp-obsidian`

1. No Obsidian: `Settings → Community plugins → Browse`, instala e ativa
   **Local REST API**.
2. Nas definições do plugin, copia a **API key** gerada e confirma a porta
   (por omissão `27124` para HTTPS local).
3. Regista o servidor MCP `mcp-obsidian` (community, corre via `uvx`) no teu
   cliente. Duas formas de fazer isto:

   - **Automático (Claude Code)**: corre `scripts/setup_mcp.sh` — pede a API
     key e o host/porta interativamente e trata do `claude mcp add` por ti.
   - **Manual**: `claude mcp add obsidian -e OBSIDIAN_API_KEY=... -e
     OBSIDIAN_HOST=127.0.0.1 -e OBSIDIAN_PORT=27124 -- uvx mcp-obsidian`, ou
     para o Claude Desktop copia o bloco de
     `references/mcp-config.example.json` para dentro de `"mcpServers"` no
     `claude_desktop_config.json`.
4. Reinicia o cliente. Devem aparecer ferramentas como `list_files_in_vault`,
   `get_file_contents`, `search`, `patch_content`, `append_content`,
   `delete_file`.

## Opção B — plugin "Obsidian MCP Tools" (tudo-em-um)

Alternativa mais simples: o plugin comunitário **MCP Tools** corre o servidor
MCP embutido no próprio Obsidian, sem precisares de instalar nada com
`uvx`/`npx` à parte nem de gerir a Local REST API separadamente.

1. Instala e ativa o plugin **MCP Tools** no Obsidian.
2. Segue as instruções do próprio plugin para registar o servidor no teu
   cliente (ele normalmente gera o bloco de configuração pronto a colar).
3. Reinicia o cliente e confirma que as ferramentas aparecem.

## Notas de segurança

- A API key dá acesso de **leitura e escrita a todo o vault**. Trata-a como
  uma password: não a partilhes nem a commites num repositório.
- A ligação é local (`127.0.0.1`) por omissão — não exponhas a porta à rede
  sem perceberes bem as implicações.
- Estes plugins e servidores são de terceiros (não são da Anthropic nem da
  Obsidian). Revê o código-fonte antes de confiar neles com o teu vault
  pessoal.

## Nota: "correr LLMs dentro do Obsidian" é outra coisa

O MCP faz o Claude (a correr fora do Obsidian) ler/escrever o vault — não põe
nenhum modelo a correr dentro da aplicação. Se o objetivo for ter chat com um
LLM diretamente na interface do Obsidian (não apenas o vault acessível a partir
de fora), isso é um plugin diferente, por exemplo **Smart Connections** ou
**Copilot for Obsidian** — ambos chamam uma API de LLM (Anthropic, OpenAI,
modelos locais, etc.) a partir de dentro da app. São complementares ao MCP, não
substitutos: o MCP dá memória partilhada e automação a partir do Claude Code /
Claude Desktop; esses plugins dão um chat embutido no Obsidian. Nenhum dos dois
"corre o modelo dentro" do vault — o modelo continua remoto (ou local, se
apontares para um servidor local), só a interface é que muda.

## Como isto se encaixa na skill

Quando as ferramentas MCP `mcp__obsidian__*` (ou nome equivalente) estiverem
disponíveis na sessão, prefere-as em vez dos scripts em `../scripts/` — são
mais rápidas e não exigem indicar o caminho do vault a cada chamada. Os
scripts continuam a ser o caminho de reserva para sessões sem essa ligação
(por exemplo, esta sessão remota, ou qualquer ambiente que só tenha acesso ao
sistema de ficheiros).
