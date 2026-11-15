---
tags: [moc, home, brain]
---

# 🧠 UFCD 10791 — Knowledge Brain

> Mapa de conteúdo central. Ver [[Index]] para navegação tabular. Abre `graph.canvas` para o grafo de cérebro completo.

## Setup & Integrações
- [[SETUP_Smart_Connect]] — Corrigir CLI REST 127.0.0.1:27125
- [[SETUP_MarkItDown]] — Importar PDFs, Word, slides, URLs para o vault

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

## NotebookLM

- [[NotebookLM_INDEX]] — 86 notebooks organizados por área
- [[NLM_cybersecurity_incidents]] — Cybersecurity Incident Case Studies (232 fontes)
- [[NLM_protocolo_seguranca_digital]] — Protocolo de Segurança Digital para Alunos
- [[NLM_seguranet]] — Seguranet (literacia digital)
- [[NLM_windows_server_security]] — Windows Server 2012 R2 Security

## Escrita Científica

- **Guia de Metodologias de Investigação e Gestão de Projetos** (47 fontes) — em NotebookLM
- **Scientific Article Development and Evaluation Directory** — em NotebookLM
- **Mastering NotebookLM and AI Optimization for Academic Success** (96 fontes) — em NotebookLM
- `docs/learnings/scientific-writing.md` — convenções IMRaD, IEEE/APA, registo académico

## Notas UFCD 10791

- [[UFCD_intro]] — Introdução à Segurança
- [[UFCD_sql_injection]] — SQL Injection
- [[UFCD_xss]] — Cross-Site Scripting
- [[UFCD_csrf]] — CSRF
- [[UFCD_code_injection]] — Injeção de Código
- [[UFCD_auth]] — Autenticação e Sessões
- [[UFCD_known_vulnerabilities]] — Componentes Vulneráveis
- [[UFCD_brute_force]] — Força Bruta

## Queries Úteis
```dataview
TABLE file.mtime as "Modificado"
FROM ""
WHERE contains(tags, "security")
SORT file.mtime DESC
LIMIT 10
```
