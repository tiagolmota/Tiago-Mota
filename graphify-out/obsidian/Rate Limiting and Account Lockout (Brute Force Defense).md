---
source_file: "src/app.component.ts"
type: "defense"
community: "Security Vulnerabilities"
owasp: "A07:2021 — Identification and Authentication Failures"
defends_against: "Brute Force Attacks and Account Lockout"
tags:
  - segurança
  - defesa
  - java
  - owasp
  - graphify/defense
  - ufcd10791
related:
  - "[[Brute Force Attacks and Account Lockout]]"
  - "[[Session Hijacking and Authentication]]"
  - "[[Security by Design]]"
  - "[[Secure Cookies and HTTPS (Session Defense)]]"
  - "[[Active Dependency Management (OWASP Dependency-Check)]]"
---

# Rate Limiting and Account Lockout (Brute Force Defense)

> Defesa primária contra [[Brute Force Attacks and Account Lockout]]. Ver [[Session Hijacking and Authentication]] para ataques de sessão relacionados.

## Princípio

**Rate limiting** limita o número de tentativas por unidade de tempo — torna ataques de força bruta computacionalmente inviáveis. **Account lockout** bloqueia temporariamente contas após N falhas consecutivas.

## Estratégias Combinadas

| Estratégia | Protege contra | Trade-off |
|---|---|---|
| Lockout temporário (5 min) | Brute force focado | DoS em contas legítimas |
| Rate limiting por IP | Ataques distribuídos | IPs partilhados (NAT) |
| CAPTCHA progressivo | Bots automatizados | Fricção para utilizadores |
| Delay exponencial | Password spraying | Latência para ataques lentos |
| Notificação por email | Tentativas suspeitas | Requer email verificado |

## Padrão Java (Spring — Rate Limiter manual)

```java
@Service
public class LoginAttemptService {
    private static final int MAX_ATTEMPTS = 5;
    private static final long LOCK_DURATION_MS = 5 * 60 * 1000; // 5 minutos

    // Em produção: usar Redis/Cache distribuído
    private final Map<String, LoginAttempt> attempts = new ConcurrentHashMap<>();

    public boolean isBlocked(String username) {
        LoginAttempt attempt = attempts.get(username);
        if (attempt == null) return false;

        if (attempt.count >= MAX_ATTEMPTS) {
            long elapsed = System.currentTimeMillis() - attempt.lastAttemptTime;
            if (elapsed < LOCK_DURATION_MS) return true;
            attempts.remove(username);  // lockout expirou
        }
        return false;
    }

    public void registerFailure(String username) {
        attempts.merge(username, new LoginAttempt(),
            (existing, newVal) -> {
                existing.count++;
                existing.lastAttemptTime = System.currentTimeMillis();
                return existing;
            });
    }

    public void registerSuccess(String username) {
        attempts.remove(username);  // limpar após login bem-sucedido
    }

    private static class LoginAttempt {
        int count = 1;
        long lastAttemptTime = System.currentTimeMillis();
    }
}
```

## Integração no Controller

```java
@RestController
public class AuthController {
    @Autowired private LoginAttemptService loginAttemptService;
    @Autowired private UserService userService;

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody LoginRequest req) {
        String username = req.getUsername();

        // ✓ Verificar bloqueio ANTES de validar password
        if (loginAttemptService.isBlocked(username)) {
            return ResponseEntity.status(HttpStatus.TOO_MANY_REQUESTS)
                .body("Conta bloqueada temporariamente. Tente novamente em 5 minutos.");
        }

        if (!userService.authenticate(username, req.getPassword())) {
            loginAttemptService.registerFailure(username);
            // ✓ Mensagem genérica — não revelar se username existe
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                .body("Credenciais inválidas");
        }

        loginAttemptService.registerSuccess(username);
        return ResponseEntity.ok(userService.createSession(username));
    }
}
```

## Rate Limiting por IP (Spring + Bucket4j)

```xml
<!-- pom.xml -->
<dependency>
    <groupId>com.github.vladimir-bukhtoyarov</groupId>
    <artifactId>bucket4j-core</artifactId>
    <version>7.6.0</version>
</dependency>
```

```java
@Component
public class RateLimitFilter extends OncePerRequestFilter {
    private final Map<String, Bucket> cache = new ConcurrentHashMap<>();

    private Bucket createBucket() {
        return Bucket.builder()
            .addLimit(Bandwidth.classic(10, Refill.greedy(10, Duration.ofMinutes(1))))
            .build();
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request,
            HttpServletResponse response, FilterChain chain) throws IOException, ServletException {
        String ip = request.getRemoteAddr();
        Bucket bucket = cache.computeIfAbsent(ip, k -> createBucket());

        if (bucket.tryConsume(1)) {
            chain.doFilter(request, response);
        } else {
            response.setStatus(HttpStatus.TOO_MANY_REQUESTS.value());
            response.getWriter().write("Demasiadas tentativas. Tente novamente.");
        }
    }
}
```

## Delay Exponencial (sem lockout total)

```java
public void applyLoginDelay(String username) throws InterruptedException {
    LoginAttempt attempt = attempts.get(username);
    if (attempt == null) return;

    // Delay exponencial: 0, 1s, 2s, 4s, 8s, 16s (máx 30s)
    long delayMs = Math.min((long) Math.pow(2, attempt.count - 1) * 1000, 30000);
    if (delayMs > 0) Thread.sleep(delayMs);
}
```

## Regras Complementares

- **Mensagens genéricas** — não revelar se utilizador existe
- **Logging de falhas** para detecção de ataques em curso
- **MFA** como segunda linha de defesa — [[Secure Cookies and HTTPS (Session Defense)]]
- **Passwords fortes** — verificar contra HaveIBeenPwned API
- **Redis/Cache distribuído** em produção (não `ConcurrentHashMap` — não persiste entre restarts)
- Usar [[Active Dependency Management (OWASP Dependency-Check)]] para Bucket4j e Spring Security

## Ligações

- Ataque: [[Brute Force Attacks and Account Lockout]]
- Relacionado: [[Session Hijacking and Authentication]]
- Filosofia: [[Security by Design]]
- Outras defesas: [[Prepared Statements (SQL Injection Defense)]] · [[Secure Cookies and HTTPS (Session Defense)]] · [[Active Dependency Management (OWASP Dependency-Check)]]
- Mapa: [[OWASP_Top10]] · [[HOME]]
