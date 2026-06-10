---
tags: [segurança, java, ufcd10791, brute_force]
aliases: ["Ataques de Força Bruta e Bloqueio de Conta"]
owasp: "A07:2021 — Identification & Auth Failures"
severidade: "Média"
relacionado:
  - "[[Autenticação e Sessões]]"
---

# Ataques de Força Bruta e Bloqueio de Conta

> [!info] OWASP
> [A07:2021 — Identification & Auth Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)

## Descrição

Um ataque de força bruta consiste em tentar sistematicamente todas as combinações possíveis de passwords até encontrar a correta. Variantes modernas como o "Credential Stuffing" usam listas de credenciais roubadas de outras fugas de informação para tentar aceder a contas noutros serviços, explorando a reutilização de passwords pelos utilizadores.

---

## ❌ Má Prática — Ausência de Limites de Tentativas de Login

Um formulário de login que não limita o número de tentativas falhadas permite que um atacante use scripts automatizados para testar milhões de combinações de passwords em pouco tempo, tornando a descoberta de uma password fraca apenas uma questão de tempo.

```java
// Endpoint de login vulnerável
@PostMapping("/login")
public ResponseEntity<String> login(String username, String password) {
    if (authService.credentialsAreValid(username, password)) {
        // ... Iniciar sessão do utilizador
        return ResponseEntity.ok("Login bem-sucedido!");
    } else {
        // Nenhuma penalização por tentativa falhada
        return ResponseEntity.status(401).body("Credenciais inválidas.");
    }
}
```

---

## ✅ Boa Prática — Implementar Rate Limiting e Bloqueio de Conta

A mitigação eficaz envolve detetar e bloquear tentativas excessivas de login. Isto pode ser feito limitando o número de pedidos por IP (Rate Limiting) ou bloqueando temporariamente uma conta após um certo número de tentativas falhadas, tornando os ataques automatizados impraticáveis.

```java
// Lógica conceptual para um serviço de login
private final Map<String, Integer> failedAttempts = new ConcurrentHashMap<>();
private final Map<String, Long> lockedAccounts = new ConcurrentHashMap<>();
private static final int MAX_ATTEMPTS = 5;
private static final long LOCKOUT_DURATION_MS = 15 * 60 * 1000; // 15 minutos

public void handleLoginAttempt(String username, boolean success) {
    if (isAccountLocked(username)) {
        throw new AccountLockedException("Conta bloqueada temporariamente.");
    }

    if (success) {
        failedAttempts.remove(username); // Reset no sucesso
    } else {
        int attempts = failedAttempts.getOrDefault(username, 0) + 1;
        failedAttempts.put(username, attempts);

        if (attempts >= MAX_ATTEMPTS) {
            lockedAccounts.put(username, System.currentTimeMillis() + LOCKOUT_DURATION_MS);
            failedAttempts.remove(username);
            // Opcional: Notificar o utilizador sobre o bloqueio da conta
        }
    }
}

private boolean isAccountLocked(String username) {
    Long lockoutTime = lockedAccounts.get(username);
    if (lockoutTime == null) return false;
    
    if (System.currentTimeMillis() > lockoutTime) {
        lockedAccounts.remove(username); // O bloqueio expirou
        return false;
    }
    return true;
}
```

---

## Tópicos Relacionados

- [[Autenticação e Sessões]]

## Referências

- [A07:2021 — Identification & Auth Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)
- [[AppComponent]] — implementação na app UFCD 10791
- [[HOME]] — voltar ao mapa central
