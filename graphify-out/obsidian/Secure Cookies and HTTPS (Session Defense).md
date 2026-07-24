---
source_file: "src/app.component.ts"
type: "defense"
community: "Security Vulnerabilities"
owasp: "A07:2021 — Identification and Authentication Failures"
defends_against: "Session Hijacking and Authentication"
tags:
  - segurança
  - defesa
  - java
  - owasp
  - graphify/defense
  - ufcd10791
related:
  - "[[Session Hijacking and Authentication]]"
  - "[[Cross-Site Request Forgery (CSRF)]]"
  - "[[Cross-Site Scripting (XSS)]]"
  - "[[Security by Design]]"
  - "[[Anti-CSRF Tokens]]"
  - "[[Output Encoding and Input Validation (XSS Defense)]]"
---

# Secure Cookies and HTTPS (Session Defense)

> Defesa primária contra [[Session Hijacking and Authentication]]. Combinar com [[Anti-CSRF Tokens]] para proteção completa de sessões.

## Princípio

Um cookie de sessão mal configurado pode ser roubado via **rede** (sem HTTPS), **JavaScript** (sem HttpOnly), ou **sites externos** (sem SameSite/Secure). Cada atributo elimina um vetor de ataque.

## Atributos Críticos

| Atributo | Protege contra | Sem ele |
|---|---|---|
| `HttpOnly` | XSS (roubo via JS) | `document.cookie` expõe o token |
| `Secure` | Sniffing em rede | Cookie enviado em HTTP sem cifra |
| `SameSite=Strict` | CSRF | Cookie enviado em pedidos cross-site |
| `Path=/` | Scope desnecessário | Cookie válido em subpaths não intencionais |
| Expiração curta | Sessões indefinidas | Token válido indefinidamente |

## Padrão Java (Spring Boot — application.properties)

```properties
# Sessão segura
server.servlet.session.cookie.http-only=true
server.servlet.session.cookie.secure=true
server.servlet.session.cookie.same-site=strict
server.servlet.session.timeout=30m

# HTTPS — redirecionar HTTP para HTTPS
server.ssl.enabled=true
```

## Padrão Java (Spring Security)

```java
@Configuration
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
            // Forçar HTTPS
            .requiresChannel()
                .anyRequest().requiresSecure()
            .and()
            // Proteção de sessão
            .sessionManagement()
                .sessionFixation().migrateSession()   // novo ID após login
                .maximumSessions(1)                    // uma sessão por utilizador
                .expiredSessionStrategy(event ->
                    event.getResponse().sendRedirect("/login?expired"))
            .and()
            // Headers de segurança
            .headers()
                .httpStrictTransportSecurity()
                    .includeSubDomains(true)
                    .maxAgeInSeconds(31536000);        // HSTS 1 ano
    }
}
```

## Configuração Manual de Cookie

```java
// ✗ INSEGURO — cookie sem proteção
Cookie session = new Cookie("JSESSIONID", sessionId);
response.addCookie(session);

// ✓ SEGURO — todos os atributos defensivos
Cookie session = new Cookie("JSESSIONID", sessionId);
session.setHttpOnly(true);    // sem acesso JS
session.setSecure(true);      // apenas HTTPS
session.setPath("/");
session.setMaxAge(1800);      // 30 minutos

// SameSite requer header manual (Java Cookie API não suporta diretamente)
response.setHeader("Set-Cookie",
    "JSESSIONID=" + sessionId +
    "; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=1800");
```

## Regeneração de ID de Sessão

```java
// ✓ CRÍTICO — regenerar ID após autenticação (previne Session Fixation)
@PostMapping("/login")
public String login(HttpServletRequest request, @RequestParam String password) {
    if (authenticate(password)) {
        HttpSession oldSession = request.getSession(false);
        if (oldSession != null) {
            oldSession.invalidate();    // destruir sessão antiga
        }
        HttpSession newSession = request.getSession(true);  // nova sessão, novo ID
        newSession.setAttribute("user", getCurrentUser());
        return "redirect:/dashboard";
    }
    return "login?error";
}
```

## HTTPS com TLS (Spring Boot)

```bash
# Gerar certificado auto-assinado para desenvolvimento
keytool -genkeypair -alias markbridge \
  -keyalg RSA -keysize 2048 \
  -storetype PKCS12 \
  -keystore keystore.p12 \
  -validity 3650

# application.properties
# server.ssl.key-store=classpath:keystore.p12
# server.ssl.key-store-password=changeit
# server.ssl.key-store-type=PKCS12
# server.ssl.key-alias=markbridge
```

## Regras Complementares

- **Invalidar sessão** no logout: `session.invalidate()`
- **HSTS** para forçar HTTPS em visitantes futuros
- **Token de sessão longo** (≥128 bits de entropia)
- XSS bypassa HttpOnly — corrigir XSS: [[Output Encoding and Input Validation (XSS Defense)]]
- CSRF usa cookies autenticados — adicionar: [[Anti-CSRF Tokens]]

## Ligações

- Ataque: [[Session Hijacking and Authentication]]
- Relacionado: [[Cross-Site Request Forgery (CSRF)]] · [[Cross-Site Scripting (XSS)]]
- Filosofia: [[Security by Design]]
- Outras defesas: [[Prepared Statements (SQL Injection Defense)]] · [[Output Encoding and Input Validation (XSS Defense)]] · [[Anti-CSRF Tokens]]
- Mapa: [[OWASP_Top10]] · [[HOME]]
