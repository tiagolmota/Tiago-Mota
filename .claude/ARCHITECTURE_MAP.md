# Architecture Map — UFCD 10791

## File Tree
```
Tiago-Mota/
├── index.html              ← CDN imports (Tailwind + Angular via esm.sh importmap)
├── index.tsx               ← Bootstrap: bootstrapApplication(AppComponent)
├── src/
│   ├── app.component.ts    ← ALL logic: SecurityTopic[] signal, IntersectionObserver
│   ├── app.component.html  ← Sidebar nav + main content (bad/good practice cards)
│   └── app.component.css   ← fade-in-section, animate-pulse-quick animations
├── angular.json            ← Build config (builder: @angular/build:application)
├── tsconfig.json           ← strict, isolatedModules, experimentalDecorators
├── package.json            ← Angular 21 deps (CDN runtime, local build only)
├── metadata.json           ← AI Studio app name + description
├── CLAUDE.md               ← Session start protocol (load-on-demand)
├── .claudeignore           ← Blocks .agents/, obsidian/, node_modules/
├── .claude/
│   ├── COMMON_MISTAKES.md  ← Angular CDN + Zoneless gotchas
│   ├── QUICK_START.md      ← Dev commands
│   └── ARCHITECTURE_MAP.md ← This file
├── graphify-out/
│   ├── graph.json          ← Knowledge graph (113 nodes, 11 communities)
│   ├── GRAPH_REPORT.md     ← God nodes + surprising connections
│   └── obsidian/           ← Vault (124 notes, brain layout canvas)
└── .agents/skills/         ← 754 cybersecurity skills (load on demand)
```

## Data Flow
```
index.html (importmap CDN)
  → index.tsx (bootstrapApplication)
    → AppComponent (OnPush + signal)
      → topics signal<SecurityTopic[]>  ← 8 security topics hardcoded
      → selectedTopicId signal<string>  ← sidebar active state
      → IntersectionObserver            ← fade-in on scroll
      → app.component.html              ← @for loop over topics()
```

## Security Topics (IDs)
intro · sql_injection · xss · csrf · code_injection · auth · known_vulnerabilities · brute_force

## Key Patterns
- State: `signal()` + `ChangeDetectionStrategy.OnPush` (no NgZone)
- Scroll nav: `selectTopic(id)` → `document.getElementById(id).scrollIntoView()`
- CDN-only runtime: edit `index.html` importmap to add packages
