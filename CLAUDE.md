# UFCD 10791 - Segurança Web com Java

Angular 21 educational app about web security. Zoneless, CDN-loaded via AI Studio.

**Stack:** Angular 21 + Tailwind (CDN) + TypeScript 5.8 + Vite

**Entry:** `index.tsx` → `src/app.component.ts` → `src/app.component.html`

---

## Session Start ⚡ (~800 tokens)

Read in order:
1. `.claude/COMMON_MISTAKES.md` — critical pitfalls
2. `.claude/QUICK_START.md` — commands
3. `.claude/ARCHITECTURE_MAP.md` — file map

## Key Rules

- All Angular imports use CDN (esm.sh) — no npm installs affect runtime
- `ChangeDetectionStrategy.OnPush` + `signal()` — no NgZone
- Security topics defined as `readonly topics = signal<SecurityTopic[]>([...])`
- Knowledge graph in `graphify-out/` — query with `/graphify query "..."`
- 754 cybersecurity skills in `.agents/skills/` — use `/skill-name`

## Never Auto-Load

- `.agents/` (754 skills — on-demand only)
- `graphify-out/obsidian/` (124 notes)
- `node_modules/`, `dist/`

## Docs (load when needed)

- `.claude/ARCHITECTURE_MAP.md` — full file tree
- `.claude/COMMON_MISTAKES.md` — Angular CDN gotchas
- `graphify-out/GRAPH_REPORT.md` — codebase knowledge graph
