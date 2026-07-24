---
tags: [moc, index, ufcd10791]
---

# Índice do Vault — UFCD 10791

> Navegação estruturada. Ver [[HOME]] para o mapa do cérebro completo.

---

## Segurança Web — Tópicos do Curso

| Nota de Estudo | Conceito | Defesa |
|---|---|---|
| [[UFCD_intro]] | Introdução à Segurança Web | — |
| [[UFCD_sql_injection]] | [[SQL Injection]] | [[Prepared Statements (SQL Injection Defense)]] |
| [[UFCD_xss]] | [[Cross-Site Scripting (XSS)]] | [[Output Encoding and Input Validation (XSS Defense)]] |
| [[UFCD_csrf]] | [[Cross-Site Request Forgery (CSRF)]] | [[Anti-CSRF Tokens]] |
| [[UFCD_code_injection]] | [[Code Injection]] | — |
| [[UFCD_auth]] | [[Session Hijacking and Authentication]] | [[Secure Cookies and HTTPS (Session Defense)]] |
| [[UFCD_known_vulnerabilities]] | [[Using Components with Known Vulnerabilities]] | [[Active Dependency Management (OWASP Dependency-Check)]] |
| [[UFCD_brute_force]] | [[Brute Force Attacks and Account Lockout]] | [[Rate Limiting and Account Lockout (Brute Force Defense)]] |

---

## Arquitectura da Aplicação Angular

### Ficheiros Principais
- [[AppComponent]] — God node (17 ligações)
- [[AppComponent Template (app.component.html)]]
- [[Application Bootstrap Entry (index.tsx)]]
- [[HTML Shell (index.html)]]

### Padrões Angular
- [[Zoneless Change Detection (Angular 21)]]
- [[IntersectionObserver for Scroll Animations]]
- [[SecurityTopic]]
- [[Security by Design]]

### Configuração
- [[Angular Project Configuration (angular.json)]]
- [[TypeScript Configuration (tsconfig.json)]]
- [[Package Configuration (package.json)]]
- [[App Metadata (metadata.json)]]
- [[README - Run and Deploy AI Studio App]]

---

## Comunidades do Grafo

| Comunidade | Descrição |
|---|---|
| [[_COMMUNITY_Security Vulnerabilities]] | SQL Injection, XSS, CSRF, Brute Force |
| [[_COMMUNITY_Course & Security Design]] | UFCD 10791, Security by Design |
| [[_COMMUNITY_App Bootstrap & Config]] | index.tsx, AppComponent, bootstrap chain |
| [[_COMMUNITY_Angular Build Architecture]] | angular.json, vite, build pipeline |
| [[_COMMUNITY_Angular Runtime Dependencies]] | CDN deps, @angular/core |
| [[_COMMUNITY_Angular Project Config]] | tsconfig, workspace config |
| [[_COMMUNITY_TypeScript Configuration]] | compilerOptions, strictness |
| [[_COMMUNITY_App Metadata]] | metadata.json, app identity |
| [[_COMMUNITY_Build Output Options]] | output paths, hashing |
| [[_COMMUNITY_Dev Dependencies]] | devDependencies, toolchain |
| [[_COMMUNITY_Project Documentation]] | README, docs |

---

## NotebookLM — Bases de Conhecimento

- [[NotebookLM_INDEX]] — 86 notebooks em 9 áreas temáticas

### Notas Detalhadas
- [[NLM_cybersecurity_incidents]] — Casos de incidentes (232 fontes)
- [[NLM_protocolo_seguranca_digital]] — Protocolo para alunos
- [[NLM_seguranet]] — Literacia digital / Seguranet
- [[NLM_windows_server_security]] — Windows Server 2012 R2

---

---

## Setup & Integrações

| Nota | Descrição |
|---|---|
| [[SETUP_Smart_Connect]] | Corrigir CLI REST 127.0.0.1:27125 (4 soluções) |
| [[SETUP_MarkItDown]] | Importar PDF / Word / slides / URLs → vault |

### Scripts disponíveis

```bash
python scripts/vault-import.py file.pdf --tag ufcd10791
bash scripts/prepare-llm.sh           # → .claude/sessions/vault-context.md
bash scripts/obsidian-vault-sync.sh ~/Meu\ volt
bash scripts/smart-connect-fix.sh     # diagnóstico porta 27125
```

---

## Queries Dataview

```dataview
TABLE tags, file.mtime as "Modificado"
FROM ""
WHERE contains(tags, "ufcd10791") AND !contains(tags, "graphify/EXTRACTED")
SORT file.mtime DESC
```

```dataview
LIST
FROM "_graphify_raw"
LIMIT 5
```
