---
source_file: "src/app.component.ts"
type: "defense"
community: "Security Vulnerabilities"
owasp: "A01:2021 — Broken Access Control"
defends_against: "Cross-Site Request Forgery (CSRF)"
tags:
  - segurança
  - defesa
  - java
  - owasp
  - graphify/defense
  - ufcd10791
related:
  - "[[Cross-Site Request Forgery (CSRF)]]"
  - "[[Session Hijacking and Authentication]]"
  - "[[Security by Design]]"
  - "[[Secure Cookies and HTTPS (Session Defense)]]"
  - "[[Output Encoding and Input Validation (XSS Defense)]]"
---

# Anti-CSRF Tokens

> Defesa primária contra [[Cross-Site Request Forgery (CSRF)]]. Complementa [[Secure Cookies and HTTPS (Session Defense)]] para proteção de sessões.

## Princípio

Um **token CSRF** é um valor secreto, único por sessão, incluído em cada formulário/pedido de mutação (POST/PUT/DELETE). O servidor valida o token antes de executar — um site malicioso não consegue ler o token da vítima devido à Same-Origin Policy.

## Fluxo de Ataque vs. Defesa

```
Sem CSRF token:
  Vítima autenticada → visita site malicioso → site faz POST para bank.com → ação executada ✗

Com CSRF token:
  Vítima autenticada → token no formulário → site malicioso não tem o token → servidor rejeita ✓
```

## Padrão Java (Spring Security — automático)

```java
// Spring Security ativa CSRF por defeito — não desativar!
@Configuration
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
            .csrf()
                .csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse())
            // withHttpOnlyFalse() permite que Angular/React leiam o cookie
            .and()
            .authorizeRequests()
                .anyRequest().authenticated();
    }
}
```

```html
<!-- Thymeleaf — token injetado automaticamente no formulário -->
<form method="post" action="/transferencia">
    <input type="hidden" th:name="${_csrf.parameterName}" th:value="${_csrf.token}"/>
    <input type="text" name="valor"/>
    <button type="submit">Transferir</button>
</form>
```

## Padrão Manual (Servlet puro)

```java
// Geração do token na sessão
HttpSession session = request.getSession();
String csrfToken = UUID.randomUUID().toString();
session.setAttribute("csrf_token", csrfToken);

// Validação no servidor
String tokenFromRequest = request.getParameter("csrf_token");
String tokenFromSession = (String) session.getAttribute("csrf_token");

if (tokenFromSession == null || !tokenFromSession.equals(tokenFromRequest)) {
    response.sendError(HttpServletResponse.SC_FORBIDDEN, "CSRF token inválido");
    return;
}
// Processar pedido...
```

## Padrão Angular (SPA + Spring)

```typescript
// Angular lê automaticamente o cookie XSRF-TOKEN e envia X-XSRF-TOKEN header
// Spring Security valida o header — nenhum código extra necessário no cliente

// Se necessário configurar manualmente:
import { HttpClientXsrfModule } from '@angular/common/http';
@NgModule({
  imports: [
    HttpClientXsrfModule.withOptions({
      cookieName: 'XSRF-TOKEN',
      headerName: 'X-XSRF-TOKEN'
    })
  ]
})
export class AppModule {}
```

## SameSite Cookie (defesa complementar)

```java
// SameSite=Strict bloqueia envio de cookies em pedidos cross-site
// Spring Boot 2.6+ — application.properties
// server.servlet.session.cookie.same-site=strict

// Programaticamente:
Cookie sessionCookie = new Cookie("JSESSIONID", session.getId());
sessionCookie.setHttpOnly(true);
sessionCookie.setSecure(true);
// SameSite via header (Spring não suporta diretamente via Cookie API)
response.setHeader("Set-Cookie",
    "JSESSIONID=" + session.getId() + "; HttpOnly; Secure; SameSite=Strict");
```

## Regras Complementares

- **Nunca desativar** CSRF em Spring Security sem motivo válido (APIs stateless com JWT são exceção)
- **Double Submit Cookie** — alternativa sem estado no servidor
- **Verificar `Origin`/`Referer` header** como camada adicional
- **`SameSite=Strict`** nos cookies de sessão — ver [[Secure Cookies and HTTPS (Session Defense)]]
- XSS compromete tokens CSRF — corrigir XSS primeiro: [[Output Encoding and Input Validation (XSS Defense)]]

## Ligações

- Ataque: [[Cross-Site Request Forgery (CSRF)]]
- Relacionado: [[Session Hijacking and Authentication]]
- Filosofia: [[Security by Design]]
- Outras defesas: [[Prepared Statements (SQL Injection Defense)]] · [[Output Encoding and Input Validation (XSS Defense)]] · [[Secure Cookies and HTTPS (Session Defense)]]
- Mapa: [[OWASP_Top10]] · [[HOME]]
