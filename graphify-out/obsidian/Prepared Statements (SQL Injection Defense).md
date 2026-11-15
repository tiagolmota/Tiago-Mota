---
source_file: "src/app.component.ts"
type: "defense"
community: "Security Vulnerabilities"
owasp: "A03:2021 — Injection"
defends_against: "SQL Injection"
tags:
  - segurança
  - defesa
  - java
  - owasp
  - graphify/defense
  - ufcd10791
related:
  - "[[SQL Injection]]"
  - "[[UFCD_sql_injection]]"
  - "[[Code Injection]]"
  - "[[Security by Design]]"
  - "[[Output Encoding and Input Validation (XSS Defense)]]"
---

# Prepared Statements (SQL Injection Defense)

> Defesa primária contra [[SQL Injection]] e [[Code Injection]]. Ver estudo completo em [[UFCD_sql_injection]].

## Princípio

Separa **código SQL** de **dados do utilizador** — o driver de base de dados trata os parâmetros como literais, nunca como sintaxe SQL.

## Padrão Java (JDBC)

```java
// ✗ VULNERÁVEL — concatenação direta
String q = "SELECT * FROM users WHERE user = '" + input + "'";

// ✓ SEGURO — PreparedStatement com parâmetros
String q = "SELECT * FROM users WHERE user = ?";
PreparedStatement ps = conn.prepareStatement(q);
ps.setString(1, input);   // input nunca é interpretado como SQL
ResultSet rs = ps.executeQuery();
```

## Padrão com ORM (JPA/Hibernate)

```java
// ✓ JPQL parametrizado
TypedQuery<User> q = em.createQuery(
    "SELECT u FROM User u WHERE u.name = :name", User.class);
q.setParameter("name", input);
```

## Regras Complementares

- **Validação de input** na camada de entrada (whitelist, não blacklist)
- **Princípio do mínimo privilégio** — conta DB só com SELECT/INSERT necessários
- **Stored procedures** também vulneráveis se construídas com concatenação
- Usar [[Active Dependency Management (OWASP Dependency-Check)]] para verificar drivers JDBC

## Ligações

- Ataque: [[SQL Injection]]
- Relacionado: [[Code Injection]]
- Estudo UFCD: [[UFCD_sql_injection]]
- Filosofia: [[Security by Design]]
- Outras defesas: [[Output Encoding and Input Validation (XSS Defense)]] · [[Anti-CSRF Tokens]] · [[Secure Cookies and HTTPS (Session Defense)]]
- Mapa: [[OWASP_Top10]] · [[HOME]]
