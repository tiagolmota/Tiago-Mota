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
  - "[[SQL Injection]]"
  - "[[Cross-Site Scripting (XSS)]]"
  - "[[Prepared Statements (SQL Injection Defense)]]"
  - "[[Output Encoding and Input Validation (XSS Defense)]]"
  - "[[Security by Design]]"
  - "[[OWASP_Top10]]"
---

# Code Injection

> Categoria de ataques que injetam código malicioso interpretado pela aplicação. Inclui [[SQL Injection]], [[Cross-Site Scripting (XSS)]], command injection e LDAP injection.

## O Que É

Code Injection é a categoria-mãe de ataques de injeção: qualquer técnica que permita a um atacante introduzir código que é interpretado e executado pela aplicação ou pelo sistema subjacente.

## Taxonomia de Injeção

```
Code Injection (A03:2021)
├── SQL Injection → [[SQL Injection]]
│   ├── In-band (Error/Union)
│   ├── Blind (Boolean/Time)
│   └── Out-of-band
├── XSS (HTML/JS Injection) → [[Cross-Site Scripting (XSS)]]
│   ├── Stored
│   ├── Reflected
│   └── DOM-based
├── Command Injection (OS)
├── LDAP Injection
├── XML Injection / XXE
├── XPATH Injection
└── Template Injection (SSTI)
```

## Command Injection em Java

```java
// ✗ VULNERÁVEL — Runtime.exec com input do utilizador
String filename = request.getParameter("file");
Process p = Runtime.getRuntime().exec("cat /uploads/" + filename);
// Atacante envia: "../../etc/passwd; rm -rf /"

// ✓ SEGURO — whitelist de argumentos permitidos
private static final Pattern SAFE_FILENAME = Pattern.compile("^[a-zA-Z0-9_\\-]+\\.pdf$");

String filename = request.getParameter("file");
if (!SAFE_FILENAME.matcher(filename).matches()) {
    throw new SecurityException("Nome de ficheiro inválido");
}
ProcessBuilder pb = new ProcessBuilder("cat", "/uploads/" + filename);
pb.redirectErrorStream(true);
Process p = pb.start();
```

## LDAP Injection em Java

```java
// ✗ VULNERÁVEL
String filter = "(uid=" + username + ")";
// Input: "admin)(|(uid=*" → filter: "(uid=admin)(|(uid=*)"

// ✓ SEGURO — LdapName para escape
String safeUsername = username.replace("(", "\\28")
                              .replace(")", "\\29")
                              .replace("*", "\\2a")
                              .replace("\\", "\\5c");
String filter = "(uid=" + safeUsername + ")";

// Ou usar API javax.naming com filtros parametrizados
```

## Template Injection (SSTI)

```java
// ✗ VULNERÁVEL — Freemarker com input do utilizador no template
String template = "Olá " + userInput + "!";
Template t = new Template("", new StringReader(template), cfg);
// Input: "${7*7}" → output: "Olá 49!" → execução de código

// ✓ SEGURO — input como variável no modelo, nunca no template
Template t = cfg.getTemplate("hello.ftl");  // template fixo
Map<String, Object> model = Map.of("name", userInput);  // dados separados
t.process(model, out);
```

## Princípio Unificador

Todos os ataques de injeção partilham a mesma causa raiz: **mistura de código e dados**. A defesa universal é **separar código de dados**:
- SQL: [[Prepared Statements (SQL Injection Defense)]] (parâmetros vs. query)
- HTML/JS: [[Output Encoding and Input Validation (XSS Defense)]] (encoding por contexto)
- OS commands: whitelist + ProcessBuilder (sem shell)
- Templates: modelo separado do template

## Ligações

- Ataques específicos: [[SQL Injection]] · [[Cross-Site Scripting (XSS)]]
- Defesas: [[Prepared Statements (SQL Injection Defense)]] · [[Output Encoding and Input Validation (XSS Defense)]]
- Filosofia: [[Security by Design]]
- Mapa: [[OWASP_Top10]] · [[HOME]]
