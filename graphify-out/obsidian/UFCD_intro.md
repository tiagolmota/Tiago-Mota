---
tags: [segurança, java, ufcd10791, intro]
aliases: ["Introdução à Segurança", "Security by Design Intro"]
owasp: "Security by Design"
severidade: "Info"
type: "ufcd-study"
related:
  - "[[Security by Design]]"
  - "[[OWASP_Top10]]"
  - "[[SQL Injection]]"
  - "[[Cross-Site Scripting (XSS)]]"
  - "[[Cross-Site Request Forgery (CSRF)]]"
  - "[[Code Injection]]"
  - "[[UFCD 10791 - Web Application Development in Java]]"
---

# Introdução à Segurança

> [!info] OWASP
> [Security by Design](https://owasp.org/www-project-proactive-controls/)

## Descrição

A segurança em aplicações web não é um extra, mas sim um requisito fundamental. Uma vulnerabilidade pode comprometer dados dos utilizadores, a reputação da empresa e levar a perdas financeiras significativas. Esta UFCD tem como objetivo principal criar uma mentalidade de desenvolvimento seguro desde o início do projeto.

---

## ❌ Má Prática

```plaintext
// 1. Desenvolver toda a funcionalidade.
// 2. Testar o caminho feliz.
// 3. Lançar para produção.
// 4. Esperar por um relatório de vulnerabilidade.
// 5. Corrigir reativamente.
```

---

## ✅ Boa Prática

```plaintext
// 1. Análise de requisitos de segurança.
// 2. Modelação de ameaças na fase de design.
// 3. Desenvolvimento com práticas seguras (ex: code reviews).
// 4. Testes de segurança automatizados e manuais (pentesting).
// 5. Monitorização contínua em produção.
```

---

## Custo da Segurança por Fase

| Fase | Custo Relativo |
|---|---|
| Design | 1× |
| Desenvolvimento | 10× |
| Testes | 30× |
| Produção | 100× |

Corrigir vulnerabilidades em produção é **100× mais caro** que no design.

---

## Tópicos Relacionados

- [[SQL Injection]] — injeção de código SQL
- [[Cross-Site Scripting (XSS)]] — injeção de scripts
- [[Cross-Site Request Forgery (CSRF)]] — pedidos forjados
- [[Code Injection]] — categoria-mãe de injeções

## Ligações

- Filosofia expandida: [[Security by Design]]
- Mapa OWASP: [[OWASP_Top10]]
- Curso: [[UFCD 10791 - Web Application Development in Java]]
- Implementação: [[AppComponent]] · [[Angular Architecture (UFCD 10791)]]
- Início: [[HOME]]
