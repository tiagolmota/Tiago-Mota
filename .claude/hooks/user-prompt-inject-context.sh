#!/bin/bash
# user-prompt-inject-context.sh
# EVENT: UserPromptSubmit
# DESCRIPTION: Auto-inject matching docs/learnings/ files based on prompt keywords
#
# Claude Code UserPromptSubmit hook: auto-loads topic docs from docs/learnings/
# based on keywords in the user's prompt. stdout is injected as context Claude
# sees before answering — zero token cost when the file isn't relevant.
#
# INSTALL: cto hooks install user-prompt-inject-context
# Or manually: copy to .claude/hooks/user-prompt-inject-context.sh
#
# CONFIGURE (optional env vars):
#   CTO_LEARNINGS_DIR    — path to learnings dir (default: docs/learnings)
#   CTO_MAX_INJECT_FILES — max files to inject per prompt (default: 3)
#   CTO_MAX_INJECT_WORDS — max total words to inject (default: 1500, ~2000 tokens)

LEARNINGS_DIR="${CTO_LEARNINGS_DIR:-docs/learnings}"
VAULT_DIR="${CTO_VAULT_DIR:-graphify-out/obsidian}"
MAX_FILES="${CTO_MAX_INJECT_FILES:-3}"
MAX_WORDS="${CTO_MAX_INJECT_WORDS:-1800}"

# Read stdin JSON to get the user prompt
STDIN_JSON=$(cat)
PROMPT=$(echo "$STDIN_JSON" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('prompt', ''))
except:
    pass
" 2>/dev/null)

if [ -z "$PROMPT" ]; then
  exit 0
fi

# Find matching topic files using Python for robust matching
INJECTED=$(python3 - "$LEARNINGS_DIR" "$VAULT_DIR" "$MAX_FILES" "$MAX_WORDS" "$PROMPT" <<'PYEOF'
import sys, os, re

learnings_dir = sys.argv[1]
vault_dir = sys.argv[2]
max_files = int(sys.argv[3])
max_words = int(sys.argv[4])
prompt = sys.argv[5].lower()

# Extract meaningful words from prompt (>4 chars, skip stop words)
stop = {'this','that','with','from','have','will','been','they','what',
        'when','where','which','their','there','about','would','could',
        'should','into','your','more','also','than','then','only','some'}
words = set(w for w in re.findall(r'[a-z][a-z0-9_-]{3,}', prompt) if w not in stop)

if not words:
    sys.exit(0)

# Find .md files in learnings dir + key vault notes (UFCD_*.md, NLM_*.md)
sources = []
try:
    for f in os.listdir(learnings_dir):
        if f.endswith('.md'):
            sources.append((learnings_dir, f))
except:
    pass

vault_prefixes = ('UFCD_', 'NLM_', 'Security by Design', 'Zoneless', 'AppComponent')
try:
    for f in os.listdir(vault_dir):
        if f.endswith('.md') and any(f.startswith(p) for p in vault_prefixes):
            sources.append((vault_dir, f))
except:
    pass

if not sources:
    sys.exit(0)

# Score each file by how many prompt words appear in its stem
def score(filename):
    stem = re.sub(r'\.md$', '', filename).lower().replace('-', ' ').replace('_', ' ')
    stem_words = set(stem.split())
    return sum(1 for w in words if w in stem or any(w.startswith(sw) for sw in stem_words))

scored = [(score(f), d, f) for d, f in sources]
scored = [(s, d, f) for s, d, f in scored if s > 0]
scored.sort(key=lambda x: -x[0])
matches = [(d, f) for _, d, f in scored[:max_files]]

if not matches:
    sys.exit(0)

total_words = 0
injected = []
for dirpath, fname in matches:
    path = os.path.join(dirpath, fname)
    try:
        content = open(path).read()
        wcount = len(content.split())
        if total_words + wcount > max_words:
            # Truncate to fit within budget
            words_list = content.split()
            available = max_words - total_words
            if available < 50:
                break
            content = ' '.join(words_list[:available]) + '\n\n[... truncated to fit token budget]'
            wcount = available
        injected.append((fname, dirpath, path, content, wcount))
        total_words += wcount
    except:
        continue

for fname, dirpath, path, content, wcount in injected:
    rel = os.path.join(dirpath, fname)
    print(f'--- Context loaded from {rel} ---')
    print(content)
    print(f'--- End of {fname} ---')
    print()

# Stderr notice (user sees this, not Claude)
import sys as _sys
for fname, dirpath, path, content, wcount in injected:
    approx_tokens = int(wcount * 1.3)
    rel = os.path.join(dirpath, fname)
    print(f'💡 Auto-loaded: {rel} (~{approx_tokens} tokens)', file=_sys.stderr)
PYEOF
)

if [ -n "$INJECTED" ]; then
  echo "$INJECTED"
fi

exit 0
