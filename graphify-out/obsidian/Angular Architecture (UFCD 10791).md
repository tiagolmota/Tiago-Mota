---
type: "architecture"
community: "App Bootstrap & Config"
tags:
  - angular
  - typescript
  - arquitectura
  - graphify/hub
  - ufcd10791
related:
  - "[[AppComponent]]"
  - "[[Security by Design]]"
  - "[[UFCD 10791 - Web Application Development in Java]]"
  - "[[HOME]]"
---

# Angular Architecture (UFCD 10791)

> Referência técnica da app educativa de segurança web. Stack: **Angular 21 + Tailwind CDN + TypeScript 5.8 + Vite** — sem npm para runtime, sem NgZone, sem módulos Angular.

## Fluxo de Entrada

```
index.tsx  →  src/app.component.ts  →  src/app.component.html
```

| Ficheiro | Papel |
|---|---|
| `index.html` | Shell HTML — `<app-root>` + importmap CDN |
| `index.tsx` | Bootstrap standalone — `bootstrapApplication(AppComponent)` |
| `src/app.component.ts` | Componente raiz — toda a lógica e dados |
| `src/app.component.html` | Template — UI securitária com Tailwind |
| `angular.json` | Config do build Vite |
| `tsconfig.json` | TypeScript strict mode |
| `package.json` | Apenas devDependencies (Vite, TypeScript) |
| `metadata.json` | Metadados da app (nome, descrição, versão) |

## CDN (sem npm para runtime)

```typescript
// index.tsx — imports via esm.sh (importmap no index.html)
import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './src/app.component';

bootstrapApplication(AppComponent, {
  providers: [
    provideExperimentalZonelessChangeDetection()  // zoneless!
  ]
});
```

```html
<!-- index.html — importmap -->
<script type="importmap">
{
  "imports": {
    "@angular/core": "https://esm.sh/@angular/core@21",
    "@angular/platform-browser": "https://esm.sh/@angular/platform-browser@21",
    "tailwindcss": "https://esm.sh/tailwindcss@4"
  }
}
</script>
```

## Zoneless Change Detection (Angular 21)

```typescript
// ✓ SEM NgZone — provideExperimentalZonelessChangeDetection()
// ✓ OnPush — só re-renderiza quando signals mudam
@Component({
  selector: 'app-root',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './app.component.html',
})
export class AppComponent {
  // Signals como estado reativo
  selectedTopic = signal<SecurityTopic | null>(null);
  readonly topics = signal<SecurityTopic[]>([...]);
}
```

## Interface SecurityTopic

```typescript
// Modelo de dados para cada tópico de segurança
interface SecurityTopic {
  id: string;           // slug único
  title: string;        // nome do ataque/defesa
  owasp: string;        // ex: "A03:2021"
  severity: 'critical' | 'high' | 'medium' | 'low';
  description: string;  // resumo do tópico
  badPractice: {
    code: string;       // código vulnerável (Java)
    explanation: string;
  };
  goodPractice: {
    code: string;       // código seguro (Java)
    explanation: string;
  };
  relatedTopics: string[];  // IDs de tópicos relacionados
}
```

## Métodos do AppComponent

| Método | Descrição |
|---|---|
| `ngAfterViewInit()` | Inicializa IntersectionObserver para animações de scroll |
| `ngOnDestroy()` | Remove observers e limpa subscriptions |
| `selectTopic(topic)` | Atualiza `selectedTopic` signal → trigger OnPush |

## IntersectionObserver (Animações de Scroll)

```typescript
// ngAfterViewInit — observar elementos .topic-card
ngAfterViewInit() {
  const observer = new IntersectionObserver(
    (entries) => entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    }),
    { threshold: 0.1 }
  );
  document.querySelectorAll('.topic-card')
    .forEach(el => observer.observe(el));
}
```

## Tópicos de Segurança (app.component.ts)

Cada `SecurityTopic` no signal `topics` corresponde a uma nota do vault:

| ID | Nota do Vault |
|---|---|
| `sql-injection` | [[SQL Injection]] |
| `xss` | [[Cross-Site Scripting (XSS)]] |
| `csrf` | [[Cross-Site Request Forgery (CSRF)]] |
| `session-hijacking` | [[Session Hijacking and Authentication]] |
| `code-injection` | [[Code Injection]] |
| `brute-force` | [[Brute Force Attacks and Account Lockout]] |
| `known-vulnerabilities` | [[Using Components with Known Vulnerabilities]] |

## Regras CDN (CLAUDE.md)

- Todos os imports Angular usam CDN (esm.sh) — **não instalar npm packages** para runtime
- `ChangeDetectionStrategy.OnPush` + `signal()` — sem NgZone
- Tópicos definidos como `readonly topics = signal<SecurityTopic[]>([...])`
- Não usar `zone.js` — está explicitamente excluído

## Ligações

- Componente principal: [[AppComponent]]
- Filosofia: [[Security by Design]]
- Curso: [[UFCD 10791 - Web Application Development in Java]]
- Início: [[HOME]]
