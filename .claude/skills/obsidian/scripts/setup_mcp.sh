#!/usr/bin/env bash
# Run this on YOUR OWN machine, next to a running Obsidian — it cannot be run
# from a remote/headless Claude session, since it registers a local MCP
# server that talks to Obsidian's Local REST API plugin over localhost.
#
# Prerequisites (do these in Obsidian's GUI first, this script can't):
#   1. Settings -> Community plugins -> Browse -> install & enable
#      "Local REST API".
#   2. Open that plugin's settings and copy the generated API key.
set -euo pipefail

if ! command -v claude >/dev/null 2>&1; then
  echo "claude CLI not found. Install Claude Code first: https://docs.claude.com/claude-code" >&2
  exit 1
fi
if ! command -v uvx >/dev/null 2>&1; then
  echo "uvx not found. Install uv first: https://docs.astral.sh/uv/getting-started/installation/" >&2
  exit 1
fi

read -rsp "Obsidian Local REST API key: " OBSIDIAN_API_KEY
echo
read -rp "Obsidian REST API host [127.0.0.1]: " OBSIDIAN_HOST
OBSIDIAN_HOST=${OBSIDIAN_HOST:-127.0.0.1}
read -rp "Obsidian REST API port [27124]: " OBSIDIAN_PORT
OBSIDIAN_PORT=${OBSIDIAN_PORT:-27124}

if [ -z "$OBSIDIAN_API_KEY" ]; then
  echo "No API key entered, aborting." >&2
  exit 1
fi

# -s user registers it for every project/session, not just the one you run
# this from -- change to "-s local" if you want it scoped to one project.
claude mcp add obsidian -s user \
  -e OBSIDIAN_API_KEY="$OBSIDIAN_API_KEY" \
  -e OBSIDIAN_HOST="$OBSIDIAN_HOST" \
  -e OBSIDIAN_PORT="$OBSIDIAN_PORT" \
  -- uvx mcp-obsidian

echo
echo "Registered. Start a new Claude Code session and check that mcp__obsidian__* tools appear."
echo "If 'claude mcp add' rejected a flag above, run 'claude mcp add --help' -- the flag names have changed between versions."
