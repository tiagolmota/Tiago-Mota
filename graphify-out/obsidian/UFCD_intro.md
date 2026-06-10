---
tags: [segurança, java, ufcd10791, intro]
aliases: ["Introdução à Segurança"]
owasp: "Security by Design"
severidade: "Info"
relacionado:
  - "[[SQL Injection]]"
  - "[[Cross-Site Scripting (XSS)]]"
  - "[[Cross-Site Request Forgery (CSRF)]]"
  - "[[Injeção de Código]]"
---

# Introdução à Segurança

> [!info] OWASP
> [Security by Design](https://owasp.org/www-project-proactive-controls/)

## Descrição

A segurança em aplicações web não é um extra, mas sim um requisito fundamental. Uma vulnerabilidade pode comprometer dados dos utilizadores, a reputação da empresa e levar a perdas financeiras significativas. Esta UFCD tem como objetivo principal criar uma mentalidade de desenvolvimento seguro desde o início do projeto.

---

## ❌ Má Prática — 



```plaintext
// 1. Desenvolver toda a funcionalidade.
// 2. Testar o caminho feliz.
// 3. Lançar para produção.
// 4. Esperar por um relatório de vulnerabilidade.
// 5. Corrigir reativamente.
```

---

## ✅ Boa Prática — 



```plaintext
// 1. Análise de requisitos de segurança.
// 2. Modelação de ameaças na fase de design.
// 3. Desenvolvimento com práticas seguras (ex: code reviews).
// 4. Testes de segurança automatizados e manuais (pentesting).
// 5. Monitorização contínua em produção.
```

---

## Tópicos Relacionados

- [[SQL Injection]]
- [[Cross-Site Scripting (XSS)]]
- [[Cross-Site Request Forgery (CSRF)]]
- [[Injeção de Código]]

## Referências

- [Security by Design](https://owasp.org/www-project-proactive-controls/)
- [[AppComponent]] — implementação na app UFCD 10791
- [[HOME]] — voltar ao mapa central
