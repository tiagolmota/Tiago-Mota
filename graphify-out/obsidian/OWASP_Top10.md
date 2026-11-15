---
type: "hub"
community: "Course & Security Design"
tags:
  - segurança
  - owasp
  - referência
  - graphify/hub
  - ufcd10791
related:
  - "[[SQL Injection]]"
  - "[[Cross-Site Scripting (XSS)]]"
  - "[[Cross-Site Request Forgery (CSRF)]]"
  - "[[Session Hijacking and Authentication]]"
  - "[[Brute Force Attacks and Account Lockout]]"
  - "[[Using Components with Known Vulnerabilities]]"
  - "[[Code Injection]]"
  - "[[Security by Design]]"
  - "[[HOME]]"
---

# OWASP Top 10 (2021)

> Mapa de referência para o curso UFCD 10791. Liga todos os ataques e defesas estudados ao framework OWASP.

## Mapa Completo — Ataques × Defesas

| # | Categoria OWASP | Ataque Estudado | Defesa Implementada |
|---|---|---|---|
| A01 | Broken Access Control | [[Cross-Site Request Forgery (CSRF)]] | [[Anti-CSRF Tokens]] |
| A02 | Cryptographic Failures | [[Session Hijacking and Authentication]] | [[Secure Cookies and HTTPS (Session Defense)]] |
| A03 | Injection | [[SQL Injection]] | [[Prepared Statements (SQL Injection Defense)]] |
| A03 | Injection | [[Cross-Site Scripting (XSS)]] | [[Output Encoding and Input Validation (XSS Defense)]] |
| A03 | Injection | [[Code Injection]] | Whitelist validation + parameterized APIs |
| A05 | Security Misconfiguration | Cookies inseguros | [[Secure Cookies and HTTPS (Session Defense)]] |
| A06 | Vulnerable Components | [[Using Components with Known Vulnerabilities]] | [[Active Dependency Management (OWASP Dependency-Check)]] |
| A07 | Auth Failures | [[Brute Force Attacks and Account Lockout]] | [[Rate Limiting and Account Lockout (Brute Force Defense)]] |
| A07 | Auth Failures | [[Session Hijacking and Authentication]] | [[Secure Cookies and HTTPS (Session Defense)]] |

## A01 — Broken Access Control

> Controlo de acesso insuficiente permite que utilizadores acedam a recursos ou executem ações fora das suas permissões.

**No curso:** [[Cross-Site Request Forgery (CSRF)]] — o atacante força ações em nome de utilizadores autenticados.
**Defesa:** [[Anti-CSRF Tokens]] + SameSite cookies.

## A02 — Cryptographic Failures

> Exposição de dados sensíveis por falha criptográfica — transmissão em claro, armazenamento sem cifra, algoritmos fracos.

**No curso:** Sessões sem HTTPS, cookies sem Secure flag, passwords em MD5.
**Defesa:** [[Secure Cookies and HTTPS (Session Defense)]] — HTTPS obrigatório, HSTS, bcrypt.

## A03 — Injection

> Input do utilizador interpretado como código — SQL, HTML, JavaScript, OS commands.

**No curso:**
- [[SQL Injection]] → [[Prepared Statements (SQL Injection Defense)]]
- [[Cross-Site Scripting (XSS)]] → [[Output Encoding and Input Validation (XSS Defense)]]
- [[Code Injection]] (categoria-mãe) → whitelist validation

## A05 — Security Misconfiguration

> Configurações por defeito inseguras, portas abertas, mensagens de erro detalhadas, headers de segurança em falta.

**Relacionado:** Secure Cookie flags, CSP header, HSTS — [[Secure Cookies and HTTPS (Session Defense)]].

## A06 — Vulnerable and Outdated Components

> Uso de bibliotecas com CVEs conhecidos — Log4Shell, Spring4Shell, Struts.

**No curso:** [[Using Components with Known Vulnerabilities]]
**Defesa:** [[Active Dependency Management (OWASP Dependency-Check)]] — Maven plugin, Snyk, Dependabot.

## A07 — Identification and Authentication Failures

> Autenticação fraca, gestão de sessões insegura, ausência de MFA.

**No curso:**
- [[Brute Force Attacks and Account Lockout]] → [[Rate Limiting and Account Lockout (Brute Force Defense)]]
- [[Session Hijacking and Authentication]] → [[Secure Cookies and HTTPS (Session Defense)]]

## Princípio Transversal

Todos os ataques têm uma causa raiz comum: **confiar em input não validado ou componentes não auditados**. A filosofia unificadora é [[Security by Design]].

## Categorias Não Cobertas no Curso (referência)

| # | Categoria | Exemplo |
|---|---|---|
| A04 | Insecure Design | Ausência de threat modeling |
| A08 | Software and Data Integrity Failures | CI/CD sem verificação de integridade |
| A09 | Security Logging and Monitoring Failures | Sem alertas de intrusão |
| A10 | Server-Side Request Forgery (SSRF) | Fetch de URLs fornecidas pelo utilizador |

## Ligações

- Filosofia: [[Security by Design]]
- Início: [[HOME]]
- Ataques: [[SQL Injection]] · [[Cross-Site Scripting (XSS)]] · [[Cross-Site Request Forgery (CSRF)]] · [[Session Hijacking and Authentication]] · [[Brute Force Attacks and Account Lockout]] · [[Using Components with Known Vulnerabilities]] · [[Code Injection]]
- Defesas: [[Prepared Statements (SQL Injection Defense)]] · [[Output Encoding and Input Validation (XSS Defense)]] · [[Anti-CSRF Tokens]] · [[Secure Cookies and HTTPS (Session Defense)]] · [[Rate Limiting and Account Lockout (Brute Force Defense)]] · [[Active Dependency Management (OWASP Dependency-Check)]]
