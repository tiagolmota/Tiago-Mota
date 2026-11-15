---
source_file: "src/app.component.ts"
type: "philosophy"
community: "Course & Security Design"
tags:
  - segurança
  - filosofia
  - java
  - owasp
  - graphify/rationale
  - ufcd10791
related:
  - "[[Prepared Statements (SQL Injection Defense)]]"
  - "[[Output Encoding and Input Validation (XSS Defense)]]"
  - "[[Anti-CSRF Tokens]]"
  - "[[Secure Cookies and HTTPS (Session Defense)]]"
  - "[[Rate Limiting and Account Lockout (Brute Force Defense)]]"
  - "[[Active Dependency Management (OWASP Dependency-Check)]]"
  - "[[OWASP_Top10]]"
  - "[[HOME]]"
---

# Security by Design

> Filosofia central do curso UFCD 10791. Segurança não é uma feature — é uma propriedade arquitetural construída desde o primeiro dia.

## Princípios Fundamentais

### 1. Minimize a Superfície de Ataque
Cada funcionalidade exposta é um potencial vetor de ataque. Remover funcionalidades não essenciais, fechar portas não utilizadas, aplicar o princípio do mínimo privilégio.

### 2. Defesa em Profundidade (Defense in Depth)
Nunca depender de uma única camada de proteção. Se o encoding falha, o CSP bloqueia. Se o CSRF token falha, o SameSite cookie protege.

```
Camadas de defesa:
  Input Validation → Output Encoding → CSP → HttpOnly → SameSite → HTTPS → WAF
```

### 3. Princípio do Mínimo Privilégio
Código, utilizadores e processos devem ter apenas as permissões estritamente necessárias.

```java
// ✗ Conta DB com permissões totais
GRANT ALL PRIVILEGES ON *.* TO 'app'@'localhost';

// ✓ Conta DB com apenas o necessário
GRANT SELECT, INSERT ON app_schema.users TO 'app'@'localhost';
GRANT SELECT ON app_schema.products TO 'app'@'localhost';
```

### 4. Fail Secure (Falhar com Segurança)
Em caso de erro, o sistema deve falhar no estado mais seguro possível.

```java
// ✓ Negar acesso por defeito — não conceder
public boolean hasPermission(User user, String resource) {
    try {
        return permissionService.check(user, resource);
    } catch (Exception e) {
        logger.error("Permission check failed", e);
        return false;  // falha → acesso negado, não concedido
    }
}
```

### 5. Separar Código de Dados
A causa raiz de todos os ataques de injeção. Ver [[Code Injection]].

```java
// ✓ Código e dados sempre separados
PreparedStatement ps = conn.prepareStatement("SELECT * FROM t WHERE id = ?");
ps.setInt(1, userInput);  // dado nunca é interpretado como código
```

### 6. Não Confiar na Entrada (Zero Trust Input)
Todo o input é potencialmente malicioso — independentemente da origem.

```java
// Validar SEMPRE na camada de servidor, mesmo que o cliente já valide
@PostMapping("/register")
public ResponseEntity<?> register(@Valid @RequestBody UserDto dto) {
    // @Valid aplica Bean Validation — nunca confiar só no frontend
}
```

## Mapa de Ataques → Defesas

| Ataque | OWASP | Defesa |
|---|---|---|
| [[SQL Injection]] | A03:2021 | [[Prepared Statements (SQL Injection Defense)]] |
| [[Cross-Site Scripting (XSS)]] | A03:2021 | [[Output Encoding and Input Validation (XSS Defense)]] |
| [[Cross-Site Request Forgery (CSRF)]] | A01:2021 | [[Anti-CSRF Tokens]] |
| [[Session Hijacking and Authentication]] | A07:2021 | [[Secure Cookies and HTTPS (Session Defense)]] |
| [[Brute Force Attacks and Account Lockout]] | A07:2021 | [[Rate Limiting and Account Lockout (Brute Force Defense)]] |
| [[Using Components with Known Vulnerabilities]] | A06:2021 | [[Active Dependency Management (OWASP Dependency-Check)]] |
| [[Code Injection]] | A03:2021 | Whitelist validation + parameterized APIs |

## Shift Left Security

A segurança é **mais barata** quanto mais cedo for integrada:

```
Custo de correção por fase:
  Design:       1×   (mudança de requisito)
  Development:  10×  (refactor de código)
  Testing:      30×  (fix + retest)
  Production:   100× (patch + rollback + comunicação)
```

## UFCD 10791 — Ligação ao Curso

Este curso implementa Security by Design através de:
- Análise de cada vulnerabilidade OWASP Top 10 com código Java
- Padrões de defesa Java nativos (JDBC, Spring Security, OWASP ESAPI)
- Análise automatizada com OWASP Dependency-Check
- Filosofia de segurança como qualidade de código, não como auditoria final

## Ligações

- Defesas implementadas:
  - [[Prepared Statements (SQL Injection Defense)]]
  - [[Output Encoding and Input Validation (XSS Defense)]]
  - [[Anti-CSRF Tokens]]
  - [[Secure Cookies and HTTPS (Session Defense)]]
  - [[Rate Limiting and Account Lockout (Brute Force Defense)]]
  - [[Active Dependency Management (OWASP Dependency-Check)]]
- Mapa completo: [[OWASP_Top10]]
- Início: [[HOME]]
