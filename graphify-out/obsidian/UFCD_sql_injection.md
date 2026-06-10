---
tags: [segurança, java, ufcd10791, sql_injection]
aliases: ["SQL Injection"]
owasp: "A03:2021 — Injection"
severidade: "Crítica"
relacionado:
  - "[[Injeção de Código]]"
  - "[[Cross-Site Scripting (XSS)]]"
  - "[[Utilização de Componentes com Vulnerabilidades Conhecidas]]"
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

- [[Injeção de Código]]
- [[Cross-Site Scripting (XSS)]]
- [[Utilização de Componentes com Vulnerabilidades Conhecidas]]

## Referências

- [A03:2021 — Injection](https://owasp.org/Top10/A03_2021-Injection/)
- [[AppComponent]] — implementação na app UFCD 10791
- [[HOME]] — voltar ao mapa central
