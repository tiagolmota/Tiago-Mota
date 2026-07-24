---
source_file: "src/app.component.ts"
type: "code"
community: "Security Vulnerabilities"
tags:
  - angular
  - typescript
  - graphify/code
  - graphify/EXTRACTED
  - ufcd10791
related:
  - "[[Angular Architecture (UFCD 10791)]]"
  - "[[SQL Injection]]"
  - "[[Cross-Site Scripting (XSS)]]"
  - "[[Cross-Site Request Forgery (CSRF)]]"
  - "[[Session Hijacking and Authentication]]"
  - "[[Brute Force Attacks and Account Lockout]]"
  - "[[Code Injection]]"
  - "[[Using Components with Known Vulnerabilities]]"
  - "[[Security by Design]]"
---

# AppComponent

> Componente raiz da app UFCD 10791. Implementa todos os tópicos de segurança como `SecurityTopic[]` num signal Angular 21. Arquitetura completa: [[Angular Architecture (UFCD 10791)]].

## Localização

```
src/app.component.ts  (componente + dados)
src/app.component.html (template Tailwind)
```

## Padrão Arquitetural

```typescript
@Component({
  selector: 'app-root',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,  // sem NgZone
  templateUrl: './app.component.html',
})
export class AppComponent implements AfterViewInit, OnDestroy {
  selectedTopic = signal<SecurityTopic | null>(null);
  readonly topics = signal<SecurityTopic[]>([
    // 7 tópicos OWASP definidos aqui
  ]);

  selectTopic(topic: SecurityTopic) {
    this.selectedTopic.set(topic);
  }

  ngAfterViewInit() { /* IntersectionObserver scroll animations */ }
  ngOnDestroy()     { /* cleanup observers */ }
}
```

## Tópicos de Segurança Implementados

| Tópico | Nota do Vault |
|---|---|
| SQL Injection | [[SQL Injection]] · [[Prepared Statements (SQL Injection Defense)]] |
| XSS | [[Cross-Site Scripting (XSS)]] · [[Output Encoding and Input Validation (XSS Defense)]] |
| CSRF | [[Cross-Site Request Forgery (CSRF)]] · [[Anti-CSRF Tokens]] |
| Session Hijacking | [[Session Hijacking and Authentication]] · [[Secure Cookies and HTTPS (Session Defense)]] |
| Brute Force | [[Brute Force Attacks and Account Lockout]] · [[Rate Limiting and Account Lockout (Brute Force Defense)]] |
| Code Injection | [[Code Injection]] |
| Known Vulns | [[Using Components with Known Vulnerabilities]] · [[Active Dependency Management (OWASP Dependency-Check)]] |

## Ligações

- Arquitetura: [[Angular Architecture (UFCD 10791)]]
- Filosofia: [[Security by Design]]
- Mapa: [[OWASP_Top10]]
- Curso: [[UFCD 10791 - Web Application Development in Java]]
- Início: [[HOME]]
