---
tags: [moc, home, brain]
---

# 🧠 UFCD 10791 — Knowledge Brain

> Mapa de conteúdo central. Abre `graph.canvas` para o grafo de cérebro completo.

## God Node
- [[AppComponent]] — 17 ligações (hub central)

## Comunidades de Segurança
- [[_COMMUNITY_Security Vulnerabilities]] — SQL Injection, XSS, CSRF, Code Injection, Brute Force
- [[_COMMUNITY_Course & Security Design]] — UFCD 10791, Security by Design

## Vulnerabilidades
- [[SQL Injection]] → defesa: [[Prepared Statements (SQL Injection Defense)]]
- [[Cross-Site Scripting (XSS)]] → defesa: [[Output Encoding and Input Validation (XSS Defense)]]
- [[Cross-Site Request Forgery (CSRF)]] → defesa: [[Anti-CSRF Tokens]]
- [[Code Injection]] 
- [[Session Hijacking and Authentication]] → defesa: [[Secure Cookies and HTTPS (Session Defense)]]
- [[Using Components with Known Vulnerabilities]] → defesa: [[Active Dependency Management (OWASP Dependency-Check)]]
- [[Brute Force Attacks and Account Lockout]] → defesa: [[Rate Limiting and Account Lockout (Brute Force Defense)]]

## Arquitetura Angular
- [[_COMMUNITY_App Bootstrap & Config]] — bootstrap chain
- [[_COMMUNITY_Angular Build Architecture]] — build pipeline
- [[_COMMUNITY_Angular Runtime Dependencies]] — CDN deps

## Queries Úteis
```dataview
TABLE file.mtime as "Modificado"
FROM ""
WHERE contains(tags, "security")
SORT file.mtime DESC
LIMIT 10
```
