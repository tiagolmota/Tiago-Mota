#!/bin/bash
# smart-connect-fix.sh
# Diagnoses the Smart Connections CLI REST 127.0.0.1:27125 error and prints
# the correct fix for the active scenario.

echo "=== Smart Connections CLI REST Diagnostic ==="
echo ""

# 1. Check if port 27125 is listening
if command -v ss >/dev/null 2>&1; then
  PORT_OPEN=$(ss -tlnp 2>/dev/null | grep ':27125')
elif command -v lsof >/dev/null 2>&1; then
  PORT_OPEN=$(lsof -i :27125 2>/dev/null | grep LISTEN)
elif command -v netstat >/dev/null 2>&1; then
  PORT_OPEN=$(netstat -tlnp 2>/dev/null | grep ':27125')
fi

if [ -n "$PORT_OPEN" ]; then
  echo "✅ Port 27125 is open — Smart Connect is running."
  echo "   The error in Obsidian should go away after restarting the plugin."
  exit 0
fi

echo "❌ Port 27125 is NOT open. Smart Connect companion app is not running."
echo ""
echo "━━━ SOLUTION A (Recommended) — Install Smart Connect ━━━"
echo ""
echo "  1. Download from: https://github.com/brianpetro/smart-connect/releases"
echo "  2. Install and launch Smart Connect (it runs silently in the system tray)"
echo "  3. Reload Obsidian → Smart Connections plugin → error disappears"
echo ""
echo "━━━ SOLUTION B — Disable CLI REST in Smart Connections ━━━"
echo ""
echo "  In Obsidian:"
echo "  1. Settings → Smart Connections → scroll to 'Smart Connect'"
echo "  2. Toggle OFF 'Enable Smart Connect server'"
echo "  3. Reload Obsidian"
echo ""
echo "━━━ SOLUTION C — Use Ollama for local AI (no cloud, no app) ━━━"
echo ""
echo "  1. Install Ollama: https://ollama.com"
echo "  2. Run: ollama pull nomic-embed-text"
echo "  3. In Smart Connections: AI Provider → Ollama, model → nomic-embed-text"
echo "  4. Port 27125 is no longer needed"
echo ""
echo "━━━ SOLUTION D — Use OpenAI API ━━━"
echo ""
echo "  In Smart Connections settings:"
echo "  AI Provider → OpenAI, paste your API key"
echo "  This disables the local REST requirement entirely."
echo ""
