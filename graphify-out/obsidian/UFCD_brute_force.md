---
tags: [segurança, java, ufcd10791, brute_force]
aliases: ["Ataques de Força Bruta e Bloqueio de Conta", "Brute Force UFCD"]
owasp: "A07:2021 — Identification & Auth Failures"
severidade: "Média"
type: "ufcd-study"
related:
  - "[[Brute Force Attacks and Account Lockout]]"
  - "[[Rate Limiting and Account Lockout (Brute Force Defense)]]"
  - "[[Session Hijacking and Authentication]]"
  - "[[Secure Cookies and HTTPS (Session Defense)]]"
  - "[[UFCD 10791 - Web Application Development in Java]]"
---

# Ataques de Força Bruta e Bloqueio de Conta

> [!info] OWASP
> [A07:2021 — Identification & Auth Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)

## Descrição

Um ataque de força bruta consiste em tentar sistematicamente todas as combinações possíveis de passwords até encontrar a correta. Variantes modernas como o "Credential Stuffing" usam listas de credenciais roubadas de outras fugas de informação.

---

## ❌ Má Prática — Ausência de Limites de Tentativas de Login

Um formulário de login que não limita o número de tentativas falhadas permite que um atacante use scripts automatizados para testar milhões de combinações.

```java
@PostMapping("/login")
public ResponseEntity<String> login(String username, String password) {
    if (authService.credentialsAreValid(username, password)) {
        return ResponseEntity.ok("Login bem-sucedido!");
    } else {
        // VULNERÁVEL — nenhuma penalização por tentativa falhada
        return ResponseEntity.status(401).body("Credenciais inválidas.");
    }
}
```

---

## ✅ Boa Prática — Implementar Rate Limiting e Bloqueio de Conta

```java
private final Map<String, Integer> failedAttempts = new ConcurrentHashMap<>();
private final Map<String, Long> lockedAccounts = new ConcurrentHashMap<>();
private static final int MAX_ATTEMPTS = 5;
private static final long LOCKOUT_DURATION_MS = 15 * 60 * 1000; // 15 minutos

public void handleLoginAttempt(String username, boolean success) {
    if (isAccountLocked(username)) {
        throw new AccountLockedException("Conta bloqueada temporariamente.");
    }

    if (success) {
        failedAttempts.remove(username);
    } else {
        int attempts = failedAttempts.getOrDefault(username, 0) + 1;
        failedAttempts.put(username, attempts);
        if (attempts >= MAX_ATTEMPTS) {
            lockedAccounts.put(username, System.currentTimeMillis() + LOCKOUT_DURATION_MS);
            failedAttempts.remove(username);
        }
    }
}

private boolean isAccountLocked(String username) {
    Long lockoutTime = lockedAccounts.get(username);
    if (lockoutTime == null) return false;
    if (System.currentTimeMillis() > lockoutTime) {
        lockedAccounts.remove(username);
        return false;
    }
    return true;
}
```

---

## Tópicos Relacionados

- [[Session Hijacking and Authentication]] — força bruta compromete autenticação

## Ligações

- Conceito: [[Brute Force Attacks and Account Lockout]]
- Defesa detalhada: [[Rate Limiting and Account Lockout (Brute Force Defense)]]
- Relacionado: [[Session Hijacking and Authentication]] · [[Secure Cookies and HTTPS (Session Defense)]]
- Mapa: [[OWASP_Top10]]
- Curso: [[UFCD 10791 - Web Application Development in Java]]
- Implementação: [[AppComponent]] · [[HOME]]
