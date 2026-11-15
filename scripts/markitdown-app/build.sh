#!/bin/bash
# MarkBridge — macOS/Linux build script
# Generates: dist/MarkBridge (standalone binary)
# Run from repo root: bash scripts/markitdown-app/build.sh

set -e
echo "Building MarkBridge..."

pip3 install pyinstaller --quiet

pyinstaller \
  --name MarkBridge \
  --onefile \
  --windowed \
  --hidden-import customtkinter \
  --hidden-import watchdog \
  --hidden-import pystray \
  --hidden-import markitdown \
  scripts/markitdown-app/main.py

echo ""
if [ -f dist/MarkBridge ]; then
  echo "✓ dist/MarkBridge criado com sucesso."
  echo "  macOS: copia para /Applications/MarkBridge.app ou lança diretamente."
else
  echo "✗ Build falhou."
  exit 1
fi
