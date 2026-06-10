---
tags: [segurança, java, ufcd10791, code_injection]
aliases: ["Injeção de Código"]
owasp: "A03:2021 — Injection"
severidade: "Crítica"
relacionado:
  - "[[SQL Injection]]"
  - "[[Cross-Site Scripting (XSS)]]"
---

# Injeção de Código

> [!info] OWASP
> [A03:2021 — Injection](https://owasp.org/Top10/A03_2021-Injection/)

## Descrição

A injeção de código é uma vulnerabilidade que permite a um atacante injetar e executar código arbitrário no servidor. Isto pode acontecer quando a aplicação avalia ou executa dinamicamente código construído a partir de dados fornecidos pelo utilizador, levando a uma potencial tomada de controlo total do sistema.

---

## ❌ Má Prática — Execução Dinâmica de Código Não Validado

Utilizar motores de script (como o Nashorn JavaScript engine do Java) para executar código construído com input do utilizador é extremamente perigoso. O atacante pode fornecer código que exfiltra dados ou executa comandos no sistema operativo.

```java
import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;

// O 'userInput' vem de um pedido HTTP, ex: "10 + 5"
String userInput = request.getParameter("calculate");

ScriptEngineManager manager = new ScriptEngineManager();
ScriptEngine engine = manager.getEngineByName("js");

// Perigoso: O motor executa qualquer código JavaScript fornecido.
// Se userInput for "java.lang.Runtime.getRuntime().exec('rm -rf /')",
// pode executar comandos destrutivos.
Object result = engine.eval(userInput);
```

---

## ✅ Boa Prática — Evitar Execução Dinâmica e Usar API Seguras

A melhor defesa é evitar completamente a execução de código a partir de inputs. Em vez disso, mapeie os inputs do utilizador para um conjunto seguro e predefinido de operações. Se for absolutamente necessário, use bibliotecas de parsing de expressões matemáticas que são seguras.

```java
// Abordagem segura: Mapear operações
String operation = request.getParameter("op");
int a = Integer.parseInt(request.getParameter("a"));
int b = Integer.parseInt(request.getParameter("b"));
int result;

switch (operation) {
    case "add":
        result = a + b;
        break;
    case "subtract":
        result = a - b;
        break;
    default:
        throw new IllegalArgumentException("Operação inválida.");
}
// 'result' é calculado de forma segura sem 'eval'.
```

---

## Tópicos Relacionados

- [[SQL Injection]]
- [[Cross-Site Scripting (XSS)]]

## Referências

- [A03:2021 — Injection](https://owasp.org/Top10/A03_2021-Injection/)
- [[AppComponent]] — implementação na app UFCD 10791
- [[HOME]] — voltar ao mapa central
