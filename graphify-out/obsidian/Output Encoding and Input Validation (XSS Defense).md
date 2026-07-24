---
source_file: "src/app.component.ts"
type: "defense"
community: "Security Vulnerabilities"
owasp: "A03:2021 — Injection"
defends_against: "Cross-Site Scripting (XSS)"
tags:
  - segurança
  - defesa
  - java
  - owasp
  - graphify/defense
  - ufcd10791
related:
  - "[[Cross-Site Scripting (XSS)]]"
  - "[[SQL Injection]]"
  - "[[Code Injection]]"
  - "[[Security by Design]]"
  - "[[Prepared Statements (SQL Injection Defense)]]"
---

# Output Encoding and Input Validation (XSS Defense)

> Defesa primária contra [[Cross-Site Scripting (XSS)]]. Ver também [[Code Injection]] e [[SQL Injection]] para ataques relacionados com injeção.

## Princípio

**Output encoding** trata os dados do utilizador como texto, não como markup HTML/JS. **Input validation** restringe o que entra — não substitui o encoding, complementa-o.

## Regra de ouro

Encode **na saída**, validate **na entrada**. Nunca confiar nos dados mesmo após validação — o contexto de saída (HTML, JS, CSS, URL) determina qual encoding usar.

## Contextos de Encoding

| Contexto | Risco | Mecanismo |
|---|---|---|
| HTML body | `<script>alert(1)</script>` | HTML entity encoding |
| HTML attribute | `" onmouseover="..."` | Attribute encoding |
| JavaScript | `'; alert(1); //` | JS unicode escaping |
| URL | `%3Cscript%3E` | URL percent-encoding |
| CSS | `expression(alert(1))` | CSS hex encoding |

## Padrão Java (OWASP Java Encoder)

```xml
<!-- pom.xml -->
<dependency>
  <groupId>org.owasp.encoder</groupId>
  <artifactId>encoder</artifactId>
  <version>1.3.1</version>
</dependency>
```

```java
import org.owasp.encoder.Encode;

// ✗ VULNERÁVEL — output direto sem encoding
out.println("<p>Olá, " + userInput + "</p>");

// ✓ SEGURO — HTML context
out.println("<p>Olá, " + Encode.forHtml(userInput) + "</p>");

// ✓ SEGURO — HTML attribute context
out.println("<input value='" + Encode.forHtmlAttribute(userInput) + "'/>");

// ✓ SEGURO — JavaScript context
out.println("var name = '" + Encode.forJavaScript(userInput) + "';");

// ✓ SEGURO — URL context
out.println("<a href='/user?name=" + Encode.forUriComponent(userInput) + "'>link</a>");
```

## Padrão com Thymeleaf (Spring Boot)

```html
<!-- Thymeleaf faz HTML encoding automaticamente com th:text -->
<!-- ✓ SEGURO -->
<p th:text="${userInput}">placeholder</p>

<!-- ✗ VULNERÁVEL — th:utext desativa o encoding -->
<p th:utext="${userInput}">placeholder</p>
```

## Input Validation (whitelist)

```java
// ✓ Whitelist — aceitar apenas o formato esperado
private static final Pattern USERNAME = Pattern.compile("^[a-zA-Z0-9_]{3,30}$");

public String validateUsername(String input) {
    if (input == null || !USERNAME.matcher(input).matches()) {
        throw new IllegalArgumentException("Username inválido");
    }
    return input;
}

// ✗ Blacklist — frágil, sempre existe bypass
// Não filtrar apenas <script> — existem centenas de variantes
```

## Content Security Policy (CSP)

```java
// Spring Security — adicionar header CSP
@Configuration
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.headers()
            .contentSecurityPolicy("default-src 'self'; script-src 'self'");
    }
}
```

## Regras Complementares

- **Nunca** usar `innerHTML`, `document.write()` ou `eval()` com dados do utilizador
- **`HttpOnly`** cookies para prevenir acesso via JS — ver [[Secure Cookies and HTTPS (Session Defense)]]
- **CSP header** como defesa em profundidade
- Usar [[Active Dependency Management (OWASP Dependency-Check)]] para verificar bibliotecas de templating

## Ligações

- Ataque: [[Cross-Site Scripting (XSS)]]
- Relacionado: [[Code Injection]] · [[SQL Injection]]
- Estudo UFCD: [[UFCD_xss]] (se existir)
- Filosofia: [[Security by Design]]
- Outras defesas: [[Prepared Statements (SQL Injection Defense)]] · [[Anti-CSRF Tokens]] · [[Secure Cookies and HTTPS (Session Defense)]]
- Mapa: [[OWASP_Top10]] · [[HOME]]
