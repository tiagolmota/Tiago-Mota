---
tags: [segurança, java, ufcd10791, known_vulnerabilities]
aliases: ["Utilização de Componentes com Vulnerabilidades Conhecidas", "Known Vulnerabilities UFCD"]
owasp: "A06:2021 — Vulnerable & Outdated Components"
severidade: "Alta"
type: "ufcd-study"
related:
  - "[[Using Components with Known Vulnerabilities]]"
  - "[[Active Dependency Management (OWASP Dependency-Check)]]"
  - "[[SQL Injection]]"
  - "[[Session Hijacking and Authentication]]"
  - "[[Code Injection]]"
  - "[[UFCD 10791 - Web Application Development in Java]]"
---

# Utilização de Componentes com Vulnerabilidades Conhecidas

> [!info] OWASP
> [A06:2021 — Vulnerable & Outdated Components](https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/)

## Descrição

As aplicações modernas dependem largamente de componentes e bibliotecas de terceiros. Se um destes componentes tiver uma falha de segurança conhecida, a sua aplicação herda essa vulnerabilidade — mesmo que o código próprio seja perfeito.

---

## ❌ Má Prática — Dependências Desatualizadas e Não Geridas

```xml
<!-- pom.xml -->
<dependencies>
    <dependency>
        <groupId>org.apache.logging.log4j</groupId>
        <artifactId>log4j-core</artifactId>
        <!-- Versão criticamente vulnerável (Log4Shell — CVE-2021-44228) -->
        <version>2.14.1</version>
    </dependency>
</dependencies>
```

---

## ✅ Boa Prática — Gestão Ativa e Análise de Dependências

```xml
<!-- pom.xml — versão corrigida -->
<dependency>
    <groupId>org.apache.logging.log4j</groupId>
    <artifactId>log4j-core</artifactId>
    <version>2.17.1</version>
</dependency>
```

```bash
# Executar regularmente:
mvn org.owasp:dependency-check-maven:check
# Relatório em target/dependency-check-report/
```

---

## CVEs de Referência

| CVE | Componente | CVSS | Impacto |
|---|---|---|---|
| CVE-2021-44228 | Log4j 2 (Log4Shell) | 10.0 | RCE remoto |
| CVE-2022-22965 | Spring (Spring4Shell) | 9.8 | RCE |
| CVE-2017-5638 | Struts (Equifax) | 10.0 | 147M registos |

## Tópicos Relacionados

- [[SQL Injection]] — drivers JDBC desatualizados podem ter CVEs
- [[Session Hijacking and Authentication]] — bibliotecas de auth vulneráveis

## Ligações

- Conceito: [[Using Components with Known Vulnerabilities]]
- Defesa detalhada: [[Active Dependency Management (OWASP Dependency-Check)]]
- Relacionado: [[Code Injection]] (Log4Shell é um tipo de injeção)
- Mapa: [[OWASP_Top10]]
- Curso: [[UFCD 10791 - Web Application Development in Java]]
- Implementação: [[AppComponent]] · [[HOME]]
