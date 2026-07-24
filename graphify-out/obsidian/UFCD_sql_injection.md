---
tags: [segurança, java, ufcd10791, sql_injection]
aliases: ["SQL Injection UFCD", "Injeção SQL"]
owasp: "A03:2021 — Injection"
severidade: "Crítica"
type: "ufcd-study"
related:
  - "[[SQL Injection]]"
  - "[[Prepared Statements (SQL Injection Defense)]]"
  - "[[Code Injection]]"
  - "[[Cross-Site Scripting (XSS)]]"
  - "[[Using Components with Known Vulnerabilities]]"
  - "[[UFCD 10791 - Web Application Development in Java]]"
---

# SQL Injection

> [!info] OWASP
> [A03:2021 — Injection](https://owasp.org/Top10/A03_2021-Injection/)

## Descrição

Ocorre quando um atacante consegue manipular consultas (queries) SQL executadas pela aplicação, permitindo-lhe visualizar, modificar ou apagar dados na base de dados.

---

## ❌ Má Prática — Concatenação de Strings em Consultas SQL

Construir consultas SQL dinamicamente com dados introduzidos pelo utilizador é a porta de entrada para a injeção de SQL. Um atacante pode inserir código SQL malicioso nos campos de input.

```java
String userName = request.getParameter("user");
String query = "SELECT * FROM users WHERE name = '" + userName + "'";
Statement stmt = connection.createStatement();
ResultSet rs = stmt.executeQuery(query);
```

---

## ✅ Boa Prática — Uso de Prepared Statements

Os Prepared Statements pré-compilam a consulta SQL e tratam os parâmetros como dados, e não como código executável. Isto neutraliza eficazmente a tentativa de injeção.

```java
String userName = request.getParameter("user");
String query = "SELECT * FROM users WHERE name = ?";
PreparedStatement pstmt = connection.prepareStatement(query);
pstmt.setString(1, userName);
ResultSet rs = pstmt.executeQuery();
```

---

## Tópicos Relacionados

- [[Code Injection]] — categoria-mãe da SQL Injection
- [[Cross-Site Scripting (XSS)]] — outra forma de injeção
- [[Using Components with Known Vulnerabilities]] — drivers JDBC desatualizados

## Ligações

- Conceito: [[SQL Injection]]
- Defesa detalhada: [[Prepared Statements (SQL Injection Defense)]]
- Categoria: [[Code Injection]]
- Mapa: [[OWASP_Top10]]
- Curso: [[UFCD 10791 - Web Application Development in Java]]
- Implementação: [[AppComponent]] · [[HOME]]
