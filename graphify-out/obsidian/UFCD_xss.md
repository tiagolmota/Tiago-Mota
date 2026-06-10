---
tags: [segurança, java, ufcd10791, xss]
aliases: ["Cross-Site Scripting (XSS)"]
owasp: "A03:2021 — Injection"
severidade: "Alta"
relacionado:
  - "[[Cross-Site Request Forgery (CSRF)]]"
  - "[[Autenticação e Sessões]]"
  - "[[SQL Injection]]"
---

# Cross-Site Scripting (XSS)

> [!info] OWASP
> [A03:2021 — Injection](https://owasp.org/Top10/A03_2021-Injection/)

## Descrição

Uma vulnerabilidade que permite a um atacante injetar scripts maliciosos (normalmente JavaScript) em páginas web vistas por outros utilizadores. Pode ser usada para roubar cookies de sessão, desfigurar sites, entre outros.

---

## ❌ Má Prática — Apresentar Dados do Utilizador Diretamente no HTML

Se um comentário ou nome de utilizador que contém código HTML ou script é guardado e depois apresentado numa página sem qualquer tratamento, o navegador (browser) irá interpretá-lo e executá-lo.

```java
// JSP (JavaServer Pages) Exemplo
String comment = request.getParameter("comment");
// Se 'comment' for "<script>alert('XSS')</script>", o alerta será executado.
out.println("<p>" + comment + "</p>");
```

---

## ✅ Boa Prática — Validar Inputs e Codificar Outputs (Defense in Depth)

A defesa mais eficaz contra XSS combina duas camadas. Primeiro, a **validação de input** para garantir que os dados recebidos estão no formato esperado (ex: apenas letras e números). Depois, e mais importante, o **output encoding** para garantir que quaisquer dados apresentados ao utilizador são tratados como texto pelo browser, e não como código executável.

```java
// 1. Validar o input (exemplo para um nome de utilizador)
String username = request.getParameter("username");
if (!username.matches("^[a-zA-Z0-9]+$")) {
    // Rejeitar o input inválido
    throw new SecurityException("Input de utilizador inválido.");
}

// 2. Codificar o output antes de o apresentar (defesa principal)
// Usando uma biblioteca como OWASP Java Encoder
String safeUsername = Encode.forHtml(username);

// O username validado e codificado é agora seguro para ser apresentado
out.println("<h1>Bem-vindo, " + safeUsername + "!</h1>");
```

---

## Tópicos Relacionados

- [[Cross-Site Request Forgery (CSRF)]]
- [[Autenticação e Sessões]]
- [[SQL Injection]]

## Referências

- [A03:2021 — Injection](https://owasp.org/Top10/A03_2021-Injection/)
- [[AppComponent]] — implementação na app UFCD 10791
- [[HOME]] — voltar ao mapa central
