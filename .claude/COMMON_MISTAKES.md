# Common Mistakes — UFCD 10791 Angular App

## Angular CDN (CRITICAL)
- DO NOT add npm packages that affect runtime — app loads from esm.sh CDN
- Import map is in `index.html` `<script type="importmap">` — edit there, not package.json
- `@angular/forms`, `@angular/router` NOT included — add to importmap if needed

## Zoneless Angular 21
- No `NgZone` — uses `provideZonelessChangeDetection()`
- State = `signal()` — not RxJS Subject for component state
- `ChangeDetectionStrategy.OnPush` always

## Security Topics Data
- All 8 topics in `readonly topics = signal<SecurityTopic[]>([...])` in app.component.ts
- Adding a topic: add to array + add nav icon SVG path
- Interface: `SecurityTopic` with `id, title, icon, description, badPractice, goodPractice`

## Tailwind
- Loaded via CDN `<script src="https://cdn.tailwindcss.com">` in index.html
- No purge/JIT config needed for CDN
