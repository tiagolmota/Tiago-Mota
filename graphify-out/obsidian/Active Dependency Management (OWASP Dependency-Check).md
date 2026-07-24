---
source_file: "src/app.component.ts"
type: "defense"
community: "Security Vulnerabilities"
owasp: "A06:2021 — Vulnerable and Outdated Components"
defends_against: "Using Components with Known Vulnerabilities"
tags:
  - segurança
  - defesa
  - java
  - owasp
  - graphify/defense
  - ufcd10791
related:
  - "[[Using Components with Known Vulnerabilities]]"
  - "[[Security by Design]]"
  - "[[Prepared Statements (SQL Injection Defense)]]"
  - "[[Rate Limiting and Account Lockout (Brute Force Defense)]]"
  - "[[Output Encoding and Input Validation (XSS Defense)]]"
---

# Active Dependency Management (OWASP Dependency-Check)

> Defesa primária contra [[Using Components with Known Vulnerabilities]] (OWASP A06:2021). O ataque mais ignorado — bibliotecas desatualizadas com CVEs conhecidos.

## Princípio

**Dependency-Check** analisa as dependências do projeto contra a base de dados NVD (National Vulnerability Database) e gera relatórios com CVEs identificados, scores CVSS, e versões seguras recomendadas.

## Integração Maven

```xml
<!-- pom.xml -->
<plugin>
    <groupId>org.owasp</groupId>
    <artifactId>dependency-check-maven</artifactId>
    <version>9.0.9</version>
    <configuration>
        <!-- Falhar o build se CVSS score >= 7 (HIGH/CRITICAL) -->
        <failBuildOnCVSS>7</failBuildOnCVSS>
        <formats>
            <format>HTML</format>
            <format>JSON</format>
        </formats>
        <outputDirectory>${project.build.directory}/dependency-check-report</outputDirectory>
    </configuration>
    <executions>
        <execution>
            <goals>
                <goal>check</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

```bash
# Executar análise
mvn dependency-check:check

# Relatório em: target/dependency-check-report/dependency-check-report.html
```

## Integração Gradle

```groovy
// build.gradle
plugins {
    id 'org.owasp.dependencycheck' version '9.0.9'
}

dependencyCheck {
    failBuildOnCVSS = 7
    formats = ['HTML', 'JSON']
    outputDirectory = "${buildDir}/dependency-check-report"
}

// Executar: ./gradlew dependencyCheckAnalyze
```

## Pipeline CI/CD (GitHub Actions)

```yaml
# .github/workflows/security.yml
name: Security Scan

on: [push, pull_request]

jobs:
  dependency-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: OWASP Dependency Check
        uses: dependency-check/Dependency-Check_Action@main
        with:
          project: 'meu-projeto'
          path: '.'
          format: 'HTML'
          args: >
            --failOnCVSS 7
            --enableRetired

      - name: Upload Report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: dependency-check-report
          path: reports/
```

## Ferramentas Complementares

```bash
# Snyk CLI — alternativa com base de dados própria
npm install -g snyk
snyk test --severity-threshold=high

# npm audit — para projetos Node/Angular
npm audit --audit-level=high

# pip-audit — para projetos Python (MarkBridge)
pip install pip-audit
pip-audit --desc on

# Trivy — containers e filesystems
trivy fs --severity HIGH,CRITICAL .
```

## Gestão de Dependências em Java

```xml
<!-- pom.xml — fixar versões, não usar ranges -->
<!-- ✗ PERIGOSO — aceita qualquer versão -->
<version>[1.0,)</version>

<!-- ✓ SEGURO — versão explícita e controlada -->
<version>5.7.12</version>
```

```java
// Estratégia de atualização:
// 1. Dependabot/Renovate para PRs automáticos de atualização
// 2. Testar atualizações patch/minor automaticamente
// 3. Major versions — testar manualmente antes de merge
// 4. CVEs críticos — patch de emergência em 24h
```

## Exclusão de Falsos Positivos

```xml
<!-- dependency-check-suppressions.xml -->
<suppressions xmlns="https://jeremylong.github.io/DependencyCheck/dependency-suppression.1.3.xsd">
    <suppress>
        <notes>Falso positivo — CVE não se aplica ao nosso uso</notes>
        <cve>CVE-2021-XXXXX</cve>
        <packageUrl regex="true">^pkg:maven/org\.example/biblioteca@.*$</packageUrl>
    </suppress>
</suppressions>
```

## Exemplo de CVEs Comuns em Java

| Biblioteca | CVE Exemplo | Impacto | Versão Segura |
|---|---|---|---|
| Log4j | CVE-2021-44228 (Log4Shell) | RCE crítico | ≥ 2.17.1 |
| Spring Framework | CVE-2022-22965 (Spring4Shell) | RCE crítico | ≥ 5.3.18 |
| Jackson Databind | CVE-2019-14379 | Desserialização | ≥ 2.9.9.3 |
| Commons Collections | CVE-2015-7501 | RCE | ≥ 3.2.2 |

## Regras Complementares

- **Atualizar** dependências regularmente — não apenas quando há CVE
- **Bill of Materials (BOM)** — Spring Boot BOM garante compatibilidade entre versões
- **Supply chain**: verificar checksums/assinaturas de artefactos Maven
- **SBOM** (Software Bill of Materials) — gerar e manter inventário de componentes
- Combinar com análise SAST/DAST para cobertura completa

## Ligações

- Ataque: [[Using Components with Known Vulnerabilities]]
- Filosofia: [[Security by Design]]
- Outras defesas: [[Prepared Statements (SQL Injection Defense)]] · [[Output Encoding and Input Validation (XSS Defense)]] · [[Rate Limiting and Account Lockout (Brute Force Defense)]]
- Mapa: [[OWASP_Top10]] · [[HOME]]
