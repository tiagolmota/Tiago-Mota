---
source_file: "src/app.component.ts"
type: "attack"
community: "Security Vulnerabilities"
owasp: "A07:2021 — Identification and Authentication Failures"
defended_by: "Rate Limiting and Account Lockout (Brute Force Defense)"
tags:
  - segurança
  - ataque
  - java
  - owasp
  - graphify/concept
  - ufcd10791
related:
  - "[[Session Hijacking and Authentication]]"
  - "[[Rate Limiting and Account Lockout (Brute Force Defense)]]"
  - "[[Secure Cookies and HTTPS (Session Defense)]]"
  - "[[Security by Design]]"
  - "[[OWASP_Top10]]"
---

# Brute Force Attacks and Account Lockout

> Tentativas exaustivas de descoberta de credenciais. Defesa: [[Rate Limiting and Account Lockout (Brute Force Defense)]].

## O Que É

Ataques de força bruta testam automaticamente combinações de credenciais até encontrar a correta. Variantes mais sofisticadas usam listas de passwords comuns (dictionary attacks) ou credenciais vazadas (credential stuffing).

## Tipos de Ataque

| Tipo | Estratégia | Velocidade |
|---|---|---|
| **Brute Force puro** | Todas as combinações | Lento — inviável para passwords longas |
| **Dictionary Attack** | Lista de passwords comuns | Rápido — cobre 90% dos utilizadores |
| **Credential Stuffing** | Pares user/pass de data breaches | Muito eficaz — reutilização de passwords |
| **Password Spraying** | 1 password para muitos utilizadores | Evita lockout por conta |
| **Reverse Brute Force** | 1 password, muitos usernames | Difícil de detetar |

## Cenário de Ataque

```
1. Atacante obtém lista de 10M passwords comuns (rockyou.txt)
2. Script automatizado testa 1000 tentativas/segundo
3. Sem rate limiting: 10M tentativas em ~2.8 horas
4. Com rate limiting (10 req/min): 10M tentativas em ~190 anos → inviável
```

## Código de Ataque (para contexto educacional)

```python
# Exemplo simplificado — ilustra o problema
import requests

passwords = ["123456", "password", "admin123", "qwerty"]
for pwd in passwords:
    resp = requests.post("https://alvo.com/login",
                         data={"user": "admin", "pass": pwd})
    if "dashboard" in resp.url:
        print(f"Password encontrada: {pwd}")
        break
```

## Por Que É Perigoso

- **Reutilização de passwords**: 65% dos utilizadores reutilizam passwords entre sites
- **Passwords fracas**: "123456" é a password mais usada em 2023
- **Sem feedback visual**: o utilizador não sabe que está a ser atacado
- **Acesso a dados sensíveis**: uma conta comprometida pode expor dados de todos

## Indicadores de Ataque

```
- Múltiplas falhas de login para o mesmo utilizador (> 5 em 1 min)
- Falhas de login de múltiplos IPs para o mesmo utilizador (password spray)
- Padrão de login em horários atípicos
- Tentativas com usernames sequenciais ou comuns (admin, root, user)
```

## Defesa

→ [[Rate Limiting and Account Lockout (Brute Force Defense)]] — lockout temporário, rate limiting por IP, delay exponencial

## Ligações

- Ataque relacionado: [[Session Hijacking and Authentication]]
- Defesa: [[Rate Limiting and Account Lockout (Brute Force Defense)]]
- Defesa complementar: [[Secure Cookies and HTTPS (Session Defense)]]
- Filosofia: [[Security by Design]]
- Mapa: [[OWASP_Top10]] · [[HOME]]
