---
source_file: "metadata.json"
type: "hub"
community: "Course & Security Design"
tags:
  - segurança
  - java
  - ufcd10791
  - graphify/hub
related:
  - "[[Security by Design]]"
  - "[[OWASP_Top10]]"
  - "[[Angular Architecture (UFCD 10791)]]"
  - "[[HOME]]"
---

# UFCD 10791 — Desenvolvimento de Aplicações Web em Java (Segurança)

> Hub central do curso. Objetivo: criar uma mentalidade de **desenvolvimento seguro desde o início** (Security by Design), com Java como linguagem de implementação e OWASP Top 10 como framework de referência.

## Estrutura do Curso

| # | Tópico | Tipo | Nota de Estudo |
|---|---|---|---|
| 0 | Introdução à Segurança | Filosofia | [[UFCD_intro]] |
| 1 | SQL Injection | Ataque + Defesa | [[UFCD_sql_injection]] |
| 2 | Cross-Site Scripting (XSS) | Ataque + Defesa | [[UFCD_xss]] |
| 3 | Cross-Site Request Forgery | Ataque + Defesa | [[UFCD_csrf]] |
| 4 | Autenticação e Sessões | Ataque + Defesa | [[UFCD_auth]] |
| 5 | Ataques de Força Bruta | Ataque + Defesa | [[UFCD_brute_force]] |
| 6 | Injeção de Código | Ataque + Defesa | [[UFCD_code_injection]] |
| 7 | Componentes Vulneráveis | Ataque + Defesa | [[UFCD_known_vulnerabilities]] |

## Mapa Completo: Ataques × Defesas

| Ataque | Defesa | OWASP |
|---|---|---|
| [[SQL Injection]] | [[Prepared Statements (SQL Injection Defense)]] | A03:2021 |
| [[Cross-Site Scripting (XSS)]] | [[Output Encoding and Input Validation (XSS Defense)]] | A03:2021 |
| [[Cross-Site Request Forgery (CSRF)]] | [[Anti-CSRF Tokens]] | A01:2021 |
| [[Session Hijacking and Authentication]] | [[Secure Cookies and HTTPS (Session Defense)]] | A07:2021 |
| [[Brute Force Attacks and Account Lockout]] | [[Rate Limiting and Account Lockout (Brute Force Defense)]] | A07:2021 |
| [[Code Injection]] | Whitelist + API seguras | A03:2021 |
| [[Using Components with Known Vulnerabilities]] | [[Active Dependency Management (OWASP Dependency-Check)]] | A06:2021 |

## Implementação — App Angular

O conteúdo do curso está implementado numa app Angular 21 educativa.
Arquitetura detalhada: [[Angular Architecture (UFCD 10791)]]

```
index.tsx → AppComponent → SecurityTopic[] → UI com código Java
```

## NotebookLM — Fontes Complementares

- [[NLM_cybersecurity_incidents]] — 232 casos reais de incidentes
- [[NLM_protocolo_seguranca_digital]] — guia para alunos
- [[NLM_seguranet]] — recursos Seguranet
- [[NLM_windows_server_security]] — hardening Windows Server

## Ligações

- Filosofia central: [[Security by Design]]
- Referência OWASP: [[OWASP_Top10]]
- Arquitetura da app: [[Angular Architecture (UFCD 10791)]]
- Índice NotebookLM: [[NotebookLM_INDEX]]
- Início: [[HOME]]
