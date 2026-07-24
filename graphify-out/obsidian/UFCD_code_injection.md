---
tags: [segurança, java, ufcd10791, code_injection]
aliases: ["Injeção de Código", "Code Injection UFCD"]
owasp: "A03:2021 — Injection"
severidade: "Crítica"
type: "ufcd-study"
related:
  - "[[Code Injection]]"
  - "[[SQL Injection]]"
  - "[[Cross-Site Scripting (XSS)]]"
  - "[[Prepared Statements (SQL Injection Defense)]]"
  - "[[Output Encoding and Input Validation (XSS Defense)]]"
  - "[[UFCD 10791 - Web Application Development in Java]]"
---

# Injeção de Código

> [!info] OWASP
> [A03:2021 — Injection](https://owasp.org/Top10/A03_2021-Injection/)

## Descrição

A injeção de código é uma vulnerabilidade que permite a um atacante injetar e executar código arbitrário no servidor. Isto pode acontecer quando a aplicação avalia ou executa dinamicamente código construído a partir de dados fornecidos pelo utilizador.

---

## ❌ Má Prática — Execução Dinâmica de Código Não Validado

```java
import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;

String userInput = request.getParameter("calculate");

ScriptEngineManager manager = new ScriptEngineManager();
ScriptEngine engine = manager.getEngineByName("js");

// PERIGOSO: executa qualquer código JavaScript fornecido
// Input: "java.lang.Runtime.getRuntime().exec('rm -rf /')"
Object result = engine.eval(userInput);
```

---

## ✅ Boa Prática — Evitar Execução Dinâmica e Usar APIs Seguras

```java
// Mapear operações para um conjunto seguro e predefinido
String operation = request.getParameter("op");
int a = Integer.parseInt(request.getParameter("a"));
int b = Integer.parseInt(request.getParameter("b"));
int result;

switch (operation) {
    case "add":      result = a + b; break;
    case "subtract": result = a - b; break;
    default:
        throw new IllegalArgumentException("Operação inválida.");
}
// 'result' é calculado de forma segura sem eval
```

---

## Tópicos Relacionados

- [[SQL Injection]] — injeção específica em SQL
- [[Cross-Site Scripting (XSS)]] — injeção de HTML/JavaScript

## Ligações

- Conceito: [[Code Injection]]
- Sub-tipo específico: [[SQL Injection]]
- Sub-tipo específico: [[Cross-Site Scripting (XSS)]]
- Defesas: [[Prepared Statements (SQL Injection Defense)]] · [[Output Encoding and Input Validation (XSS Defense)]]
- Mapa: [[OWASP_Top10]]
- Curso: [[UFCD 10791 - Web Application Development in Java]]
- Implementação: [[AppComponent]] · [[HOME]]
