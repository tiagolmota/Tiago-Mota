---
source_file: "src/app.component.ts"
type: "attack"
community: "Security Vulnerabilities"
owasp: "A07:2021 — Identification and Authentication Failures"
defended_by: "Secure Cookies and HTTPS (Session Defense)"
tags:
  - segurança
  - ataque
  - java
  - owasp
  - graphify/concept
  - ufcd10791
related:
  - "[[Cross-Site Scripting (XSS)]]"
  - "[[Brute Force Attacks and Account Lockout]]"
  - "[[Cross-Site Request Forgery (CSRF)]]"
  - "[[Secure Cookies and HTTPS (Session Defense)]]"
  - "[[Anti-CSRF Tokens]]"
  - "[[Security by Design]]"
  - "[[OWASP_Top10]]"
---

# Session Hijacking and Authentication

> Roubo ou comprometimento de sessões autenticadas. Defesa: [[Secure Cookies and HTTPS (Session Defense)]].

## O Que É

Session Hijacking é a tomada de controlo de uma sessão legítima de utilizador. O atacante obtém o token/cookie de sessão e personifica a vítima sem precisar das credenciais.

## Vetores de Ataque

| Vetor | Mecanismo | Prevenção |
|---|---|---|
| **Sniffing de rede** | HTTP sem cifra → token visível | HTTPS + Secure cookie |
| **XSS** | `document.cookie` executado por script | HttpOnly cookie |
| **Session Fixation** | Atacante define o ID antes do login | Regenerar ID após autenticação |
| **Brute Force de tokens** | Tokens curtos/previsíveis | Tokens ≥ 128 bits aleatórios |
| **Cross-Site** | Cookie enviado para domínio atacante | SameSite=Strict |

## Session Fixation (ataque menos conhecido)

```
1. Atacante obtém um session ID válido (não autenticado): ?JSESSIONID=ABC123
2. Envia link à vítima: https://alvo.com/login?JSESSIONID=ABC123
3. Vítima faz login — servidor mantém o mesmo session ID
4. Atacante usa ABC123 → está agora autenticado como a vítima!
```

```java
// ✓ DEFESA — regenerar ID após login (Spring faz isto automaticamente)
// sessionManagement().sessionFixation().migrateSession()
HttpSession oldSession = request.getSession(false);
if (oldSession != null) oldSession.invalidate();
HttpSession newSession = request.getSession(true);
newSession.setAttribute("user", authenticatedUser);
```

## Autenticação Fraca

```java
// ✗ VULNERÁVEL — password em texto claro na base de dados
String hash = md5(password);  // MD5 é invertível com rainbow tables

// ✓ SEGURO — bcrypt com salt (Spring Security)
PasswordEncoder encoder = new BCryptPasswordEncoder(12);
String hash = encoder.encode(rawPassword);
boolean matches = encoder.matches(rawPassword, hash);

// ✓ SEGURO — Argon2 (mais recente, recomendado)
PasswordEncoder encoder = new Argon2PasswordEncoder(16, 32, 1, 65536, 3);
```

## Tokens de Sessão Seguros

```java
// ✗ VULNERÁVEL — token previsível
String sessionId = String.valueOf(userId + System.currentTimeMillis());

// ✓ SEGURO — token criptograficamente aleatório
SecureRandom random = new SecureRandom();
byte[] tokenBytes = new byte[32];  // 256 bits
random.nextBytes(tokenBytes);
String sessionToken = Base64.getUrlEncoder().withoutPadding().encodeToString(tokenBytes);
```

## Falhas de Autenticação (A07:2021)

- Passwords sem requisitos de complexidade
- Passwords armazenadas em texto claro ou MD5/SHA1
- Ausência de MFA em contas sensíveis
- Expiração de sessão inexistente ou muito longa
- Session ID exposto na URL (logs, referrer)
- Tokens de "esqueci a password" previsíveis ou sem expiração

## Defesa

→ [[Secure Cookies and HTTPS (Session Defense)]] — HttpOnly, Secure, SameSite, HTTPS, regeneração de ID

## Ligações

- Explorado via: [[Cross-Site Scripting (XSS)]]
- Ataques relacionados: [[Brute Force Attacks and Account Lockout]] · [[Cross-Site Request Forgery (CSRF)]]
- Defesa: [[Secure Cookies and HTTPS (Session Defense)]]
- Defesa complementar: [[Anti-CSRF Tokens]]
- Filosofia: [[Security by Design]]
- Mapa: [[OWASP_Top10]] · [[HOME]]
