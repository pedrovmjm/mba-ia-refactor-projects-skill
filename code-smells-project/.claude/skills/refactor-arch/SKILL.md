---
name: refactor-arch
description: Analise projetos backend, audite arquitetura/segurança/code smells e refatore para MVC preservando o comportamento em Python/Flask, Node.js/Express e stacks similares.
---

# Refactor Arch

Use esta skill quando o usuário pedir para analisar, auditar ou refatorar um projeto backend em direção a uma arquitetura MVC.

## Referências

Carregue apenas os arquivos necessários para a fase atual:

- `references/project-analysis.md`: heurísticas para detectar stack, framework, banco de dados, domínio e arquitetura.
- `references/anti-pattern-catalog.md`: antipadrões, sinais de detecção e regras de severidade.
- `references/audit-report-template.md`: formato obrigatório do relatório da Fase 2.
- `references/mvc-guidelines.md`: responsabilidades e limites alvo em MVC.
- `references/refactoring-playbook.md`: transformações concretas com exemplos antes/depois.

## Fluxo de trabalho

### Fase 1 - Análise do projeto

1. Inspecione os arquivos com busca rápida (`rg --files`, depois leituras direcionadas).
2. Detecte linguagem, framework, gerenciador de pacotes, banco de dados, estilo de rotas, vocabulário de domínio, ponto de entrada e arquitetura atual.
3. Imprima um resumo conciso:
   - linguagem e framework
   - dependências
   - domínio
   - arquitetura
   - arquivos-fonte analisados
   - objetos/tabelas/modelos de persistência detectados
4. Não modifique arquivos nesta fase.

### Fase 2 - Auditoria

1. Leia `anti-pattern-catalog.md` e compare a codebase com ele.
2. Produza um relatório de auditoria estruturado usando `audit-report-template.md`.
3. Cada achado deve incluir severidade, título, arquivo, linha exata ou intervalo de linhas, descrição, impacto e recomendação.
4. Inclua pelo menos cinco achados quando existirem, priorizando problemas de arquitetura e segurança CRITICAL/HIGH.
5. Salve o relatório quando o usuário ou a atividade solicitar.
6. Pause antes de alterar arquivos e peça confirmação. Se o usuário já autorizou explicitamente a implementação, trate isso como confirmação e continue.

### Fase 3 - Refatoração

1. Leia `mvc-guidelines.md` e `refactoring-playbook.md`.
2. Refatore em passos pequenos, preservando comportamento:
   - models/repositories são responsáveis pela persistência e pelo acesso a dados de domínio
   - controllers são responsáveis pela orquestração e pelas decisões de negócio
   - views/routes são responsáveis pelo parsing HTTP e pela formatação das respostas
   - config/settings são responsáveis pelo ambiente e pelos segredos
   - services são responsáveis por efeitos colaterais externos e operações reutilizáveis de domínio
3. Preserve endpoints públicos, formatos de request/response e status codes esperados, salvo quando corrigir uma falha de segurança documentada exigir remover comportamento inseguro.
4. Valide:
   - a aplicação importa/inicializa sem erros
   - endpoints representativos respondem
   - achados da auditoria foram corrigidos ou explicitamente aceitos como risco residual
5. Imprima a estrutura final e os resultados da validação.
