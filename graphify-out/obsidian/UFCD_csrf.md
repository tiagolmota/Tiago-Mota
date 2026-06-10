---
tags: [segurança, java, ufcd10791, csrf]
aliases: ["Cross-Site Request Forgery (CSRF)"]
owasp: "A01:2021 — Broken Access Control"
severidade: "Média"
relacionado:
  - "[[Cross-Site Scripting (XSS)]]"
  - "[[Autenticação e Sessões]]"
---

# Cross-Site Request Forgery (CSRF)

> [!info] OWASP
> [A01:2021 — Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)

## Descrição

Esta técnica engana um utilizador autenticado, levando-o a executar uma ação indesejada na aplicação. O atacante cria um link ou formulário malicioso que, quando acedido pela vítima, submete um pedido em seu nome, legítimo mas não intencional.

---

## ❌ Má Prática — Confiar Apenas nos Cookies de Sessão

Se uma ação (ex: transferir dinheiro, apagar conta) é validada apenas com o cookie de sessão, um pedido forjado a partir de outro site será executado com sucesso porque o navegador envia os cookies automaticamente.

```java
// Um formulário simples para alterar a password
// Este pedido pode ser forjado por um atacante noutro site.
@PostMapping("/user/change-password")
public void changePassword(String newPassword) {
    // ... lógica para alterar a password do user autenticado
}
```

---

## ✅ Boa Prática — Implementar Tokens Anti-CSRF

A aplicação gera um token único e secreto para cada sessão e exige que esse token seja incluído em todos os pedidos que alteram estado. O atacante não consegue adivinhar este token.

```java
// 1. Gerar token e colocar no formulário (como campo hidden) e na sessão.
// <input type="hidden" name="_csrf" value="unique-token-per-session" />

// 2. No backend, validar o token antes de processar o pedido.
@PostMapping("/user/change-password")
public void changePassword(HttpServletRequest request, String newPassword) {
    String sessionToken = (String) request.getSession().getAttribute("CSRF_TOKEN");
    String requestToken = request.getParameter("_csrf");

    if (sessionToken != null && sessionToken.equals(requestToken)) {
        // Token válido, processar o pedido
    } else {
        // Token inválido, rejeitar o pedido
    }
}
```

---

## Tópicos Relacionados

- [[Cross-Site Scripting (XSS)]]
- [[Autenticação e Sessões]]

## Referências

- [A01:2021 — Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
- [[AppComponent]] — implementação na app UFCD 10791
- [[HOME]] — voltar ao mapa central
