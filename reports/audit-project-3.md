# Architecture Audit Report - task-manager-api

## Phase 1 - Project Analysis

- Language: Python
- Framework: Flask + Flask-SQLAlchemy
- Dependencies: Flask, flask-cors, flask-sqlalchemy
- Domain: Task Manager API (tasks, users, categories, reports)
- Architecture: parcialmente organizada, mas rotas concentravam regras, serializacao e queries
- Source files analyzed: 13
- DB tables/models: users, tasks, categories

## Summary

| Severity | Count |
|---|---:|
| CRITICAL | 1 |
| HIGH | 2 |
| MEDIUM | 4 |
| LOW | 2 |

## Findings

### [CRITICAL] Hash de senha com MD5

- File: `models/user.py:26-29`
- Description: senhas eram gravadas e verificadas com MD5.
- Impact: MD5 e inadequado para armazenamento de senhas.
- Recommendation: usar hash de senha com salt via Werkzeug/bcrypt/argon2.

### [HIGH] Token falso no login

- File: `routes/user_routes.py:198-202`
- Description: login retornava `fake-jwt-token-<id>`.
- Impact: transmite falsa seguranca sobre autenticacao.
- Recommendation: explicitar token de desenvolvimento ou implementar JWT real.

### [HIGH] Regras de negocio dentro das rotas

- File: `routes/task_routes.py:18-274`
- Description: handlers calculavam atraso, validavam dominio e persistiam diretamente.
- Impact: dificulta teste e evolucao.
- Recommendation: mover orquestracao para controllers.

### [MEDIUM] Uso de API deprecated do SQLAlchemy

- File: `routes/task_routes.py:56`
- Description: uso de `Task.query.get(...)` e equivalentes.
- Impact: gera warnings/dívida em SQLAlchemy moderno.
- Recommendation: usar `db.session.get(Model, id)`.

### [MEDIUM] Queries N+1 na listagem de tasks

- File: `routes/task_routes.py:34-48`
- Description: usuario e categoria eram buscados dentro do loop.
- Impact: aumenta queries por task.
- Recommendation: usar `joinedload`.

### [MEDIUM] Serializacao duplicada

- File: `routes/task_routes.py:13-52`
- Description: montagem manual de dicionarios repetia `Task.to_dict`.
- Impact: risco de divergencia de contrato.
- Recommendation: centralizar serializacao.

### [MEDIUM] Relatorios fazem loops com queries repetidas

- File: `routes/report_routes.py:49-63`
- Description: produtividade de usuarios consulta tasks por usuario.
- Impact: performance degrada com usuarios.
- Recommendation: centralizar em controller e preparar futura agregacao.

### [LOW] Imports nao utilizados

- File: `app.py:7`
- Description: `os`, `sys`, `json` nao eram usados.
- Impact: ruido e manutencao pior.
- Recommendation: remover imports mortos.

### [LOW] Magic values repetidos

- File: `routes/task_routes.py:96`
- Description: status e prioridades eram literais nos handlers.
- Impact: mudancas exigem edicao em varios pontos.
- Recommendation: centralizar constantes.

## Phase 3 Validation Plan

- Boot/import check: importar `app`.
- Endpoint checks: `/health`, `/tasks`, `/tasks/stats`, `/users`, `/categories`, `/reports/summary`.
- Residual risk: token segue como desenvolvimento; autenticacao real nao foi implementada para preservar escopo.
