# Quick Start

## Dev
```bash
npm install && npm run dev   # http://localhost:4200
npm run build
```

## Graphify
```
/graphify query "SQL Injection"     # query knowledge graph
/graphify . --update                # rebuild after changes
```

## Key files
- `src/app.component.ts` — all security topics + component logic
- `src/app.component.html` — template (sidebar + main content)
- `src/app.component.css` — animations (fade-in, pulse)
- `index.html` — CDN imports (Tailwind + Angular via esm.sh)
