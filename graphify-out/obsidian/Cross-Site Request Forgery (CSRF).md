---
source_file: "src/app.component.ts"
type: "attack"
community: "Security Vulnerabilities"
owasp: "A01:2021 — Broken Access Control"
defended_by: "Anti-CSRF Tokens"
tags:
  - segurança
  - ataque
  - java
  - owasp
  - graphify/concept
  - ufcd10791
related:
  - "[[Cross-Site Scripting (XSS)]]"
  - "[[Session Hijacking and Authentication]]"
  - "[[Anti-CSRF Tokens]]"
  - "[[Secure Cookies and HTTPS (Session Defense)]]"
  - "[[Security by Design]]"
  - "[[OWASP_Top10]]"
---

# Cross-Site Request Forgery (CSRF)

> Força o browser de um utilizador autenticado a fazer pedidos não intencionais. Defesa: [[Anti-CSRF Tokens]].

## O Que É

CSRF explora a confiança que o servidor deposita no browser do utilizador. O atacante cria uma página maliciosa que faz pedidos HTTP à aplicação-alvo — o browser envia automaticamente os cookies de sessão da vítima.

## Cenário de Ataque

```
1. Vítima autentica-se em bank.com → recebe cookie de sessão
2. Vítima visita evil.com enquanto ainda autenticada
3. evil.com contém: <img src="https://bank.com/transfer?to=attacker&amount=1000">
4. Browser envia automaticamente o cookie de sessão com o pedido
5. bank.com executa a transferência — a vítima não sabe
```

## Vetores de Ataque

```html
<!-- GET request via img tag (operações que usam GET incorretamente) -->
<img src="https://alvo.com/delete?id=42" width="0" height="0">

<!-- POST request via formulário auto-submit -->
<form action="https://alvo.com/transferencia" method="POST" id="csrf">
    <input type="hidden" name="valor" value="5000">
    <input type="hidden" name="destino" value="PT50...">
</form>
<script>document.getElementById('csrf').submit();</script>

<!-- Via XSS — bypass do mesmo origin -->
fetch('https://alvo.com/api/admin', {method: 'POST', credentials: 'include'})
```

## Condições Necessárias

1. Utilizador **autenticado** na aplicação-alvo
2. Ação com **efeitos colaterais** (transferência, mudança de password, delete)
3. Parâmetros da ação **previsíveis** (sem token secreto)
4. Servidor confia **apenas nos cookies** para autenticação

## Diferença CSRF vs XSS

| | XSS | CSRF |
|---|---|---|
| **Executa código** no browser da vítima | Sim | Não |
| **Usa sessão** da vítima | Após roubo do cookie | Diretamente via browser |
| **Origin** do pedido | Aplicação legítima | Site malicioso |
| **Necessita JS** | Sim | Não (img tag chega) |

## Defesa

→ [[Anti-CSRF Tokens]] — token secreto por sessão, validado no servidor

## Ligações

- Ataque relacionado: [[Cross-Site Scripting (XSS)]] · [[Session Hijacking and Authentication]]
- Defesa: [[Anti-CSRF Tokens]]
- Defesa complementar: [[Secure Cookies and HTTPS (Session Defense)]] (SameSite=Strict)
- Filosofia: [[Security by Design]]
- Mapa: [[OWASP_Top10]] · [[HOME]]
