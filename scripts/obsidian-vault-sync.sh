#!/bin/bash
# obsidian-vault-sync.sh
# Syncs the project vault (graphify-out/obsidian/) into a target local Obsidian vault.
# Creates a subfolder "UFCD-10791" inside the target vault — does NOT overwrite root.
#
# Usage:
#   bash scripts/obsidian-vault-sync.sh ~/Documents/ObsidianVault
#   VAULT_TARGET=~/Meu\ volt bash scripts/obsidian-vault-sync.sh

TARGET="${1:-$VAULT_TARGET}"

if [ -z "$TARGET" ]; then
  echo "Usage: $0 <path-to-obsidian-vault>"
  echo "   or: VAULT_TARGET=<path> $0"
  exit 1
fi

SRC="graphify-out/obsidian"
DEST="$TARGET/UFCD-10791"

if [ ! -d "$SRC" ]; then
  echo "❌ Source vault not found: $SRC"
  exit 1
fi

echo "📂 Source : $SRC"
echo "📂 Target : $DEST"
echo ""

mkdir -p "$DEST"

# Sync notes (skip .obsidian config — target vault keeps its own)
rsync -av --delete \
  --exclude='.obsidian/' \
  --include='*.md' \
  --include='*.canvas' \
  --include='*/' \
  --exclude='*' \
  "$SRC/" "$DEST/"

echo ""
echo "✅ Sync complete. Open '$(basename "$DEST")' folder in Obsidian."
echo ""
echo "Tip: Add a link from your vault Home to [[UFCD-10791/HOME]] to connect the graphs."
