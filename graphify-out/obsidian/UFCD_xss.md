---
tags: [segurança, java, ufcd10791, xss]
aliases: ["XSS UFCD", "Cross-Site Scripting UFCD"]
owasp: "A03:2021 — Injection"
severidade: "Alta"
type: "ufcd-study"
related:
  - "[[Cross-Site Scripting (XSS)]]"
  - "[[Output Encoding and Input Validation (XSS Defense)]]"
  - "[[Cross-Site Request Forgery (CSRF)]]"
  - "[[Session Hijacking and Authentication]]"
  - "[[SQL Injection]]"
  - "[[UFCD 10791 - Web Application Development in Java]]"
---

# Cross-Site Scripting (XSS)

> [!info] OWASP
> [A03:2021 — Injection](https://owasp.org/Top10/A03_2021-Injection/)

## Descrição

Uma vulnerabilidade que permite a um atacante injetar scripts maliciosos (normalmente JavaScript) em páginas web vistas por outros utilizadores. Pode ser usada para roubar cookies de sessão, desfigurar sites, entre outros.

---

## ❌ Má Prática — Apresentar Dados do Utilizador Diretamente no HTML

Se um comentário ou nome de utilizador que contém código HTML ou script é guardado e depois apresentado numa página sem qualquer tratamento, o navegador irá interpretá-lo e executá-lo.

```java
// JSP (JavaServer Pages) Exemplo
String comment = request.getParameter("comment");
// Se 'comment' for "<script>alert('XSS')</script>", o alerta será executado.
out.println("<p>" + comment + "</p>");
```

---

## ✅ Boa Prática — Validar Inputs e Codificar Outputs (Defense in Depth)

A defesa mais eficaz contra XSS combina duas camadas. Primeiro, a **validação de input** para garantir que os dados recebidos estão no formato esperado. Depois, e mais importante, o **output encoding** para garantir que quaisquer dados apresentados ao utilizador são tratados como texto pelo browser, e não como código executável.

```java
// 1. Validar o input (whitelist)
String username = request.getParameter("username");
if (!username.matches("^[a-zA-Z0-9]+$")) {
    throw new SecurityException("Input de utilizador inválido.");
}

// 2. Codificar o output (defesa principal — OWASP Java Encoder)
import org.owasp.encoder.Encode;
String safeUsername = Encode.forHtml(username);
out.println("<h1>Bem-vindo, " + safeUsername + "!</h1>");
```

---

## Tópicos Relacionados

- [[Cross-Site Request Forgery (CSRF)]] — XSS pode bypassar proteções CSRF
- [[Session Hijacking and Authentication]] — roubo de cookies via XSS
- [[SQL Injection]] — outra forma de injeção

## Ligações

- Conceito: [[Cross-Site Scripting (XSS)]]
- Defesa detalhada: [[Output Encoding and Input Validation (XSS Defense)]]
- Relacionado: [[Cross-Site Request Forgery (CSRF)]] · [[Session Hijacking and Authentication]]
- Mapa: [[OWASP_Top10]]
- Curso: [[UFCD 10791 - Web Application Development in Java]]
- Implementação: [[AppComponent]] · [[HOME]]
