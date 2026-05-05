# Architecture Audit Report - code-smells-project

## Phase 1 - Project Analysis

- Language: Python
- Framework: Flask
- Dependencies: Flask, flask-cors
- Domain: E-commerce API (produtos, usuarios, pedidos, itens_pedido)
- Architecture: monolito Flask com rotas, regras e persistencia misturadas em poucos arquivos
- Source files analyzed: 4
- DB tables/models: produtos, usuarios, pedidos, itens_pedido

## Summary

| Severity | Count |
|---|---:|
| CRITICAL | 3 |
| HIGH | 2 |
| MEDIUM | 2 |
| LOW | 2 |

## Findings

### [CRITICAL] Endpoint administrativo executa SQL arbitrario

- File: `app.py:55-75`
- Description: `/admin/query` aceita SQL externo e executa diretamente.
- Impact: qualquer cliente pode ler ou alterar dados arbitrarios.
- Recommendation: remover ou desabilitar o endpoint.

### [CRITICAL] SQL Injection por concatenacao de strings

- File: `models.py:25-58`
- Description: queries usam parametros concatenados em SQL.
- Impact: entradas externas podem alterar a query.
- Recommendation: usar queries parametrizadas.

### [CRITICAL] Vazamento de segredo e debug

- File: `controllers.py:273-281`
- Description: healthcheck retorna `secret_key`, `debug` e caminho do banco.
- Impact: exposicao de configuracao sensivel.
- Recommendation: sanitizar resposta de healthcheck.

### [HIGH] Configuracao sensivel hardcoded

- File: `app.py:6-7`
- Description: `SECRET_KEY` e `DEBUG` ficam no codigo.
- Impact: comportamento inseguro em ambientes reais.
- Recommendation: mover para `config/settings.py` com variaveis de ambiente.

### [HIGH] Controllers e models misturam responsabilidades

- File: `controllers.py:1-260`
- Description: handlers HTTP concentram validacao, regras e side effects.
- Impact: baixa testabilidade e alto acoplamento.
- Recommendation: separar views, controllers, models e services.

### [MEDIUM] Queries N+1 em pedidos

- File: `models.py:153-212`
- Description: listagens de pedidos buscam itens e produtos dentro de loops.
- Impact: aumenta numero de queries por pedido.
- Recommendation: substituir por JOIN.

### [MEDIUM] Validacoes duplicadas

- File: `controllers.py:22-93`
- Description: criacao e atualizacao de produtos repetem regras.
- Impact: manutencao propensa a divergencia.
- Recommendation: centralizar validacao em controller de dominio.

### [LOW] Magic values de dominio

- File: `controllers.py:44`
- Description: categorias validas sao literais no handler.
- Impact: mudancas de dominio exigem edicao espalhada.
- Recommendation: usar constantes.

### [LOW] Logs com `print`

- File: `controllers.py:193-195`
- Description: notificacoes simuladas aparecem diretamente no handler.
- Impact: side effects ficam acoplados ao HTTP.
- Recommendation: mover para service.

## Phase 3 Validation Plan

- Boot/import check: importar `app`.
- Endpoint checks: `/health`, `/produtos`, `/usuarios`, `/relatorios/vendas`.
- Residual risk: senhas legadas ainda estao em texto claro para preservar compatibilidade do seed.
