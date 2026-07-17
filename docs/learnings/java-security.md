# Java Security Patterns (OWASP)

## SQL Injection — A03:2021
```java
// NEVER: string concatenation
String q = "SELECT * FROM users WHERE name = '" + input + "'";

// ALWAYS: PreparedStatement
PreparedStatement ps = conn.prepareStatement("SELECT * FROM users WHERE name = ?");
ps.setString(1, input);
```

## XSS — A03:2021
```java
// Output encoding with OWASP Java Encoder
String safe = Encode.forHtml(userInput);
out.println("<p>" + safe + "</p>");

// Input validation (allowlist)
if (!input.matches("^[a-zA-Z0-9 ]{1,100}$")) throw new SecurityException();
```

## CSRF — A01:2021
- Generate per-session token: `UUID.randomUUID().toString()`
- Store in session: `request.getSession().setAttribute("CSRF_TOKEN", token)`
- Validate on POST: compare request param `_csrf` with session token
- Spring Security: `http.csrf().csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse())`

## Session Security — A07:2021
```xml
<!-- web.xml: secure cookies + force HTTPS -->
<session-config>
  <cookie-config><http-only>true</http-only><secure>true</secure></cookie-config>
</session-config>
<security-constraint>
  <web-resource-collection><url-pattern>/*</url-pattern></web-resource-collection>
  <user-data-constraint><transport-guarantee>CONFIDENTIAL</transport-guarantee></user-data-constraint>
</security-constraint>
```

## Brute Force — A07:2021
- Lock account after N failed attempts (e.g. 5)
- Use `ConcurrentHashMap<String, Integer>` for thread-safe attempt tracking
- Lockout duration: 15 minutes minimum
- Rate limit by IP using servlet filter

## Dependencies — A06:2021
```xml
<!-- OWASP Dependency-Check Maven plugin -->
<plugin>
  <groupId>org.owasp</groupId>
  <artifactId>dependency-check-maven</artifactId>
</plugin>
<!-- Run: mvn dependency-check:check -->
```

## Key Libraries
- `org.owasp.encoder:encoder` — HTML/JS/URL encoding
- `org.springframework.security:spring-security-core` — auth, CSRF, headers
- `org.apache.logging.log4j:log4j-core:2.17.1+` — safe Log4j (not 2.14.x = Log4Shell)
