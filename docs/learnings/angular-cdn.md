# Angular 21 CDN Patterns

## Critical Rules
- All imports via esm.sh CDN — NEVER `npm install` for runtime packages
- Zoneless: `provideZonelessChangeDetection()`, NO `NgZone`, NO `zone.js`
- `ChangeDetectionStrategy.OnPush` on every component — mandatory
- State via `signal<T>()` — never mutable class properties
- `inject()` works in constructor and field initializers; NOT in lifecycle hooks
- `afterNextRender()` must be called in the constructor (injection context required)

## Common Mistakes
- `CommonModule` is dead in Angular 17+ — `@for`/`@if` are built-in, no import needed
- `[innerHTML]` bypasses encapsulation — always use `DomSanitizer.bypassSecurityTrustHtml()`
- Template interpolation `{{ text }}` renders plain text only — use `[innerHTML]` for HTML
- `ViewChildren` / `QueryList` not available in constructor — only from `ngAfterViewInit` onward

## importmap (index.html)
```json
{
  "@angular/core":     "https://next.esm.sh/@angular/core@^21.0.1?external=rxjs",
  "@angular/common":  "https://next.esm.sh/@angular/common@^21.0.1?external=rxjs",
  "@angular/compiler":"https://next.esm.sh/@angular/compiler@^21.0.1?external=rxjs",
  "@angular/platform-browser": "https://next.esm.sh/@angular/platform-browser@^21.0.1?external=rxjs"
}
```

## Signal Pattern
```typescript
readonly items = signal<MyType[]>([...]);  // read-only public signal
private sanitizer = inject(DomSanitizer);  // inject() in field initializer ✓
```
