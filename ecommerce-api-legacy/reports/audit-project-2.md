# Architecture Audit Report - ecommerce-api-legacy

## Phase 1 - Project Analysis

- Language: JavaScript
- Framework: Node.js + Express
- Dependencies: express, sqlite3
- Domain: LMS checkout API (users, courses, enrollments, payments, audit logs)
- Architecture: God Class centralizando banco, rotas, checkout e relatorios
- Source files analyzed: 3
- DB tables/models: users, courses, enrollments, payments, audit_logs

## Summary

| Severity | Count |
|---|---:|
| CRITICAL | 2 |
| HIGH | 2 |
| MEDIUM | 3 |
| LOW | 2 |

## Findings

### [CRITICAL] Segredos hardcoded

- File: `src/utils.js:1-7`
- Description: credenciais e chave de gateway ficam em constantes versionadas.
- Impact: exposicao direta de segredos.
- Recommendation: mover para variaveis de ambiente em `config/settings.js`.

### [CRITICAL] Criptografia de senha insegura

- File: `src/utils.js:15-21`
- Description: `badCrypto` usa base64 repetido e truncado.
- Impact: senha fica facil de quebrar.
- Recommendation: usar hash lento com salt.

### [HIGH] God Class

- File: `src/AppManager.js:4-132`
- Description: classe acumula schema, rotas, checkout, pagamentos e relatorios.
- Impact: alto acoplamento e baixa testabilidade.
- Recommendation: separar MVC com services.

### [HIGH] Dados sensiveis em log de checkout

- File: `src/AppManager.js:37`
- Description: numero de cartao e chave de gateway sao logados.
- Impact: risco de vazamento de pagamento.
- Recommendation: nunca logar cartao ou chaves.

### [MEDIUM] Callback nesting

- File: `src/AppManager.js:28-74`
- Description: checkout encadeia callbacks de banco.
- Impact: erro e fluxo ficam dificeis de manter.
- Recommendation: encapsular banco em Promises e service.

### [MEDIUM] Queries N+1 no relatorio financeiro

- File: `src/AppManager.js:79-120`
- Description: consultas para usuarios e pagamentos rodam dentro de loops.
- Impact: performance piora com o volume.
- Recommendation: usar JOIN.

### [MEDIUM] Estado global mutavel

- File: `src/utils.js:8-9`
- Description: cache e receita global sao exportados como estado mutavel.
- Impact: comportamento implicito entre requisicoes.
- Recommendation: remover ou encapsular em service.

### [LOW] Variaveis abreviadas

- File: `src/AppManager.js:25-29`
- Description: `u`, `e`, `p`, `cid`, `cc` reduzem clareza.
- Impact: leitura e manutencao ficam piores.
- Recommendation: usar nomes do dominio.

### [LOW] Mensagens de erro inconsistentes

- File: `src/AppManager.js:31-70`
- Description: handlers misturam texto puro e JSON.
- Impact: contrato da API fica irregular.
- Recommendation: padronizar respostas JSON.

## Phase 3 Validation Plan

- Boot/import check: carregar `createApp`.
- Endpoint checks: `/health`, `/api/admin/financial-report`, `/api/checkout`, `/api/users/:id`.
- Residual risk: simulador de pagamento local continua simplificado por ser projeto didatico.
