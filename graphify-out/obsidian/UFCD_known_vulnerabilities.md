---
tags: [segurança, java, ufcd10791, known_vulnerabilities]
aliases: ["Utilização de Componentes com Vulnerabilidades Conhecidas"]
owasp: "A06:2021 — Vulnerable & Outdated Components"
severidade: "Alta"
relacionado:
  - "[[SQL Injection]]"
  - "[[Autenticação e Sessões]]"
---

# Utilização de Componentes com Vulnerabilidades Conhecidas

> [!info] OWASP
> [A06:2021 — Vulnerable & Outdated Components](https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/)

## Descrição

As aplicações modernas dependem largamente de componentes e bibliotecas de terceiros (open-source ou comerciais). Se um destes componentes tiver uma falha de segurança conhecida, a sua aplicação herda essa vulnerabilidade, tornando-se um alvo fácil para ataques que exploram essas falhas.

---

## ❌ Má Prática — Dependências Desatualizadas e Não Geridas

Incluir uma biblioteca num projeto e nunca mais a atualizar é uma prática de risco. Vulnerabilidades são descobertas constantemente, e usar uma versão antiga de uma biblioteca, como o Log4j, pode expor a aplicação a ataques críticos como o Log4Shell.

```xml
<!-- pom.xml -->
<dependencies>
    <dependency>
        <groupId>org.apache.logging.log4j</groupId>
        <artifactId>log4j-core</artifactId>
        <!-- Versão criticamente vulnerável (Log4Shell) -->
        <version>2.14.1</version>
    </dependency>
</dependencies>
```

---

## ✅ Boa Prática — Gestão Ativa e Análise de Dependências

Utilize ferramentas de gestão de dependências (como o Maven ou Gradle) e integre scanners de segurança (OWASP Dependency-Check, Snyk, Dependabot) no seu ciclo de desenvolvimento. Mantenha as bibliotecas atualizadas para as versões mais recentes e estáveis.

```plaintext
<!-- pom.xml -->
<dependencies>
    <dependency>
        <groupId>org.apache.logging.log4j</groupId>
        <artifactId>log4j-core</artifactId>
        <!-- Versão corrigida e segura -->
        <version>2.17.1</version> <!-- Ou mais recente -->
    </dependency>
</dependencies>

// Recomenda-se executar regularmente:
// mvn org.owasp:dependency-check-maven:check
```

---

## Tópicos Relacionados

- [[SQL Injection]]
- [[Autenticação e Sessões]]

## Referências

- [A06:2021 — Vulnerable & Outdated Components](https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/)
- [[AppComponent]] — implementação na app UFCD 10791
- [[HOME]] — voltar ao mapa central
