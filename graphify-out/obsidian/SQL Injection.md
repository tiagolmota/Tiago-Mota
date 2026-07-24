---
source_file: "src/app.component.ts"
type: "attack"
community: "Security Vulnerabilities"
owasp: "A03:2021 — Injection"
defended_by: "Prepared Statements (SQL Injection Defense)"
tags:
  - segurança
  - ataque
  - java
  - owasp
  - graphify/concept
  - ufcd10791
related:
  - "[[Code Injection]]"
  - "[[Prepared Statements (SQL Injection Defense)]]"
  - "[[UFCD_sql_injection]]"
  - "[[Security by Design]]"
  - "[[OWASP_Top10]]"
---

# SQL Injection

> Ataque de **injeção de código SQL** através de input não sanitizado. Ver estudo completo em [[UFCD_sql_injection]]. Defesa: [[Prepared Statements (SQL Injection Defense)]].

## O Que É

SQL Injection ocorre quando dados do utilizador são concatenados diretamente em queries SQL, permitindo ao atacante alterar a lógica da query — extrair dados, autenticar sem credenciais, modificar ou destruir a base de dados.

## Cenário de Ataque

```
Input: ' OR '1'='1
Query vulnerável: SELECT * FROM users WHERE user = '' OR '1'='1'
Resultado: retorna TODOS os utilizadores — bypass de autenticação
```

## Exemplo Java Vulnerável

```java
// ✗ VULNERÁVEL — concatenação direta
String query = "SELECT * FROM users WHERE username = '" + username
             + "' AND password = '" + password + "'";
Statement stmt = conn.createStatement();
ResultSet rs = stmt.executeQuery(query);

// Atacante envia: username = "admin'--"
// Query resultante: SELECT * FROM users WHERE username = 'admin'--' AND password = '...'
// O '--' comenta o resto → login sem password!
```

## Tipos de SQL Injection

| Tipo | Mecanismo | Exemplo |
|---|---|---|
| In-band (Error-based) | Mensagens de erro revelam estrutura | `' AND 1=CONVERT(int, @@version)--` |
| In-band (Union-based) | UNION para extrair dados | `' UNION SELECT user,pass FROM admin--` |
| Blind (Boolean-based) | Inferir dados por true/false | `' AND 1=1--` vs `' AND 1=2--` |
| Blind (Time-based) | Atraso para confirmar injeção | `'; WAITFOR DELAY '0:0:5'--` |
| Out-of-band | Exfiltração via DNS/HTTP | `'; EXEC xp_cmdshell('nslookup ...')--` |

## Impacto

- **Confidencialidade**: exfiltração de toda a base de dados
- **Integridade**: modificação/eliminação de dados
- **Disponibilidade**: `DROP TABLE users;`
- **Autenticação**: bypass completo

## Defesa

→ [[Prepared Statements (SQL Injection Defense)]] — PreparedStatement JDBC, JPA/Hibernate

## Ligações

- Ataque relacionado: [[Code Injection]]
- Defesa: [[Prepared Statements (SQL Injection Defense)]]
- Estudo UFCD: [[UFCD_sql_injection]]
- Filosofia: [[Security by Design]]
- Mapa: [[OWASP_Top10]] · [[HOME]]
