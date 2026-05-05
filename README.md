# Criação de Skills — Refatoração Arquitetural Automatizada

Ao longo do curso você aprendeu o que são Skills e como elas permitem que um agente de IA atue como um especialista em tarefas específicas. Agora imagine o seguinte cenário: você herdou 3 projetos legados com problemas de arquitetura, segurança e qualidade de código. Revisar e corrigir tudo manualmente levaria dias.

Neste desafio, você vai criar uma Skill que automatiza esse processo — analisando, auditando e refatorando qualquer projeto para o padrão MVC, independente da tecnologia.

## Objetivo

Você deve entregar uma Skill capaz de:

- Analisar uma codebase detectando linguagem, framework e arquitetura atual
- Identificar anti-patterns e code smells, classificando por severidade com arquivo e linha exatos
- Gerar um relatório de auditoria estruturado com todos os achados
- Refatorar o projeto para o padrão MVC (Model-View-Controller), eliminando os problemas encontrados
- Validar o resultado garantindo que a aplicação continua funcionando após as mudanças

A skill deve ser agnóstica de tecnologia, funcionando com diferentes linguagens e frameworks.

## Contexto

### Definição de Severidades

Para padronizar a sua auditoria e os relatórios gerados pela IA, utilize a seguinte escala de classificação baseada em problemas de MVC e SOLID:

- **CRITICAL:** Falhas graves de arquitetura ou segurança que impedem o funcionamento correto, expõem dados sensíveis (ex: credenciais hardcoded, SQL Injection) ou violam completamente a separação de responsabilidades (ex: "God Class" contendo banco de dados, lógicas complexas e roteamento no mesmo arquivo).
- **HIGH:** Fortes violações do padrão MVC ou princípios SOLID que dificultam muito a manutenção e testes (ex: lógicas de negócio pesadas presas dentro de Controllers, forte acoplamento sem Injeção de Dependência, ou uso de estado global mutável em toda a aplicação).
- **MEDIUM:** Problemas de padronização, duplicação de código ou gargalos de performance moderada (ex: Queries N+1 no banco de dados, uso inadequado de middlewares, validações ausentes nas rotas).
- **LOW:** Melhorias de legibilidade, nomenclatura de variáveis ruins, ou "magic numbers" soltos pelo código.

### Exemplo de Uso no CLI

```bash
# Executar a skill no projeto com problemas
cd code-smells-project
claude "/refactor-arch"
```

```
================================
PHASE 1: PROJECT ANALYSIS
================================
Language:      Python
Framework:      Flask 3.1.1
Dependencies:  flask-cors
Domain:        E-commerce API (produtos, pedidos, usuários)
Architecture:  Monolítica — tudo em 4 arquivos, sem separação de camadas
Source files:  4 files analyzed
DB tables:     produtos, usuarios, pedidos, itens_pedido
================================
```

```
================================
ARCHITECTURE AUDIT REPORT
================================
Project: code-smells-project
Stack:   Python + Flask
Files:   4 analyzed | ~800 lines of code

## Summary
CRITICAL: 4 | HIGH: 5 | MEDIUM: 2 | LOW: 3

## Findings

### [CRITICAL] God Class / God Method
File: models.py:1-350
Description: Arquivo único contém toda lógica de negócio, queries SQL, validação e formatação para 4 domínios diferentes.
Impact: Impossível testar em isolamento, qualquer mudança afeta tudo.
Recommendation: Separar em models e controllers por domínio.

### [CRITICAL] Hardcoded Credentials
File: app.py:8
Description: SECRET_KEY hardcoded como 'minha-chave-super-secreta-123'
...

================================
Total: 14 findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
> y
```

```
[... refatoração executada ...]

================================
PHASE 3: REFACTORING COMPLETE
================================
## New Project Structure
src/
├── config/settings.py
├── models/
│   ├── produto_model.py
│   └── usuario_model.py
├── views/
│   └── routes.py
├── controllers/
│   ├── produto_controller.py
│   └── pedido_controller.py
├── middlewares/error_handler.py
└── app.py (composition root)

## Validation
  ✓ Application boots without errors
  ✓ All endpoints respond correctly
  ✓ Zero anti-patterns remaining
================================
```

## Tecnologias obrigatórias

- **Ferramenta:** uma das três opções abaixo (não são aceitas outras ferramentas):
  - Claude Code
  - Gemini CLI
  - OpenAI Codex
- **Recurso:** Custom Skills (ou o equivalente na ferramenta escolhida)
- **Formato dos arquivos de referência:** Markdown
- **Projetos-alvo:** Python/Flask (2 projetos) e Node.js/Express (1 projeto) (fornecidos no repositório base)

> **Nota sobre a ferramenta:** Os exemplos deste documento usam o Claude Code (`.claude/skills/`) como referência, pois é a ferramenta utilizada no curso. Se você optar por Gemini CLI ou Codex, adapte o nome da pasta e o comando de invocação conforme a convenção dela — o conceito de skill e a estrutura interna (SKILL.md + arquivos de referência) permanecem os mesmos.

## Requisitos

### 1. Análise Manual dos Projetos

Antes de criar a skill, você deve entender os problemas que ela vai resolver.

**Tarefas:**

- Analisar o projeto `code-smells-project/` (Python/Flask — API de E-commerce)
- Analisar o projeto `ecommerce-api-legacy/` (Node.js/Express — LMS API com fluxo de checkout)
- Analisar o projeto `task-manager-api/` (Python/Flask — API de Task Manager)

Para cada projeto, identificar e documentar no mínimo 5 problemas, incluindo pelo menos:

- 1 de severidade CRITICAL ou HIGH
- 2 de severidade MEDIUM
- 2 de severidade LOW

Documentar os achados na seção "Análise Manual" do seu `README.md`

> **Dica:** Não precisa encontrar todos os problemas — foque nos que têm maior impacto arquitetural. Use os projetos como insumo para entender quais padrões sua skill precisa detectar.

> **Por que 3 projetos?** Dois são Python/Flask (com níveis de organização diferentes) e um é Node.js/Express. Sua skill precisa funcionar nos 3 para provar que é verdadeiramente agnóstica de tecnologia — lidando tanto com código completamente desestruturado quanto com projetos que já possuem alguma separação de camadas.

### 2. Criação da Skill

Agora que você conhece os problemas, crie uma skill que os detecte, gere um relatório de auditoria e corrija automaticamente.

**Tarefas:**

Criar a skill dentro do projeto `code-smells-project/` e implementar o SKILL.md com 3 fases sequenciais:

- **Fase 1 — Análise:** Detectar stack, mapear arquitetura atual, imprimir resumo
- **Fase 2 — Auditoria:** Cruzar código contra catálogo de anti-patterns, gerar relatório, pedir confirmação
- **Fase 3 — Refatoração:** Reestruturar para o padrão MVC, validar que funciona

Criar arquivos de referência em Markdown que forneçam à skill o conhecimento necessário para executar as 3 fases. Os arquivos devem cobrir **obrigatoriamente** as seguintes áreas de conhecimento:

| Área de conhecimento | O que deve conter |
|---|---|
| Análise de projeto | Heurísticas para detecção de linguagem, framework, banco de dados e mapeamento de arquitetura |
| Catálogo de anti-patterns | Anti-patterns com sinais de detecção e classificação de severidade |
| Template de relatório | Formato padronizado do relatório de auditoria (Fase 2) |
| Guidelines de arquitetura | Regras do padrão MVC alvo (camadas Models, Views/Routes e Controllers, responsabilidades de cada uma) |
| Playbook de refatoração | Padrões concretos de transformação para cada anti-pattern (com exemplos de código) |

> **Nota:** Você tem liberdade para organizar os arquivos de referência como preferir — pode usar os nomes e a quantidade de arquivos que fizer sentido para sua skill. O importante é que todas as 5 áreas de conhecimento estejam cobertas. O nome da skill (`refactor-arch`) e o arquivo `SKILL.md` são obrigatórios e não devem ser alterados. O path da skill segue a convenção da ferramenta escolhida (no Claude Code, por exemplo, é `.claude/skills/refactor-arch/`).

**Requisitos da skill:**

- Deve ser agnóstica de tecnologia — deve funcionar corretamente nos 3 projetos fornecidos, independente da stack ou nível de organização
- O catálogo de anti-patterns deve conter no mínimo 8 anti-patterns com severidade distribuída (CRITICAL, HIGH, MEDIUM, LOW)
- O catálogo deve incluir detecção de APIs deprecated — identificar uso de APIs obsoletas e recomendar o equivalente moderno
- O playbook deve ter no mínimo 8 padrões de transformação com exemplos de código antes/depois
- A Fase 2 deve pausar e pedir confirmação antes de modificar qualquer arquivo
- A Fase 3 deve validar o resultado (boot da aplicação + endpoints funcionando)

### 3. Execução da Skill

Execute sua skill nos 3 projetos e valide que ela funciona em todas as stacks.

#### Projeto 1 — code-smells-project (Python/Flask)

Invocar a skill no Claude Code:

```bash
claude "/refactor-arch"
```

> **Nota:** O comando acima é o exemplo com Claude Code. Se você estiver usando Gemini CLI ou Codex, utilize o comando equivalente para invocar uma skill na sua ferramenta.

- Verificar que a Fase 1 detecta corretamente a stack e imprime o resumo
- Verificar que a Fase 2 encontra no mínimo 5 dos problemas documentados na sua análise manual
- Confirmar a execução da Fase 3
- Verificar que a Fase 3:
  - Cria a estrutura de diretórios baseada em MVC
  - A aplicação inicia sem erros
  - Os endpoints originais continuam respondendo
- Salvar o relatório de auditoria (output da Fase 2) em `reports/audit-project-1.md`
- Commitar o código refatorado do projeto no repositório

#### Projeto 2 — ecommerce-api-legacy (Node.js/Express)

Prove que sua skill é reutilizável em outro projeto de backend, mas com stack diferente.

- Copiar a pasta `.claude/skills/refactor-arch/` para dentro de `ecommerce-api-legacy/`
- Invocar a skill:

```bash
cd ../ecommerce-api-legacy
claude "/refactor-arch"
```

- Verificar que as 3 fases executam corretamente neste projeto
- Salvar o relatório em `reports/audit-project-2.md`
- Commitar o código refatorado do projeto no repositório

#### Projeto 3 — task-manager-api (Python/Flask)

Agora o teste com um projeto Python/Flask que já possui alguma organização de camadas (models, routes, services, utils).

- Copiar a pasta `.claude/skills/refactor-arch/` para dentro de `task-manager-api/`
- Invocar a skill:

```bash
cd ../task-manager-api
claude "/refactor-arch"
```

- Verificar que:
  - A Fase 1 detecta corretamente Python/Flask como stack e identifica o domínio de Task Manager
  - A Fase 2 identifica problemas mesmo em um projeto parcialmente organizado
  - A Fase 3 melhora a estrutura sem quebrar a aplicação (todos os endpoints devem continuar respondendo)
- Salvar o relatório em `reports/audit-project-3.md`
- Commitar o código refatorado do projeto no repositório

> **Nota:** Este projeto já possui alguma separação de camadas, mas isso não significa que a arquitetura está adequada. A skill deve identificar tanto problemas de código (segurança, performance, qualidade) quanto oportunidades de melhoria arquitetural. Se houver mudanças estruturais necessárias, a skill deve propô-las e executá-las.

## Análise Manual

Esta seção registra a análise manual feita antes da criação da skill `refactor-arch`. Os achados abaixo foram usados como insumo para o catálogo de anti-patterns, guidelines MVC e playbook de refatoração.

### Projeto 1 — `code-smells-project/`

Stack detectada: Python + Flask + SQLite. Domínio: API de e-commerce com produtos, usuários, pedidos e relatório de vendas. Arquitetura inicial: monolítica, com rotas no `app.py`, regras de negócio e acesso a dados misturados entre `controllers.py` e `models.py`.

#### Achados

1. **[CRITICAL] Endpoint administrativo executa SQL arbitrário**
   - Arquivo: `code-smells-project/app.py`
   - Descrição: `/admin/query` recebe SQL no corpo da requisição e executa diretamente no banco.
   - Impacto: permite leitura, alteração ou exclusão arbitrária dos dados.
   - Recomendação: remover o endpoint ou substituí-lo por operações administrativas explícitas.

2. **[CRITICAL] SQL Injection em consultas e mutações**
   - Arquivo: `code-smells-project/models.py`
   - Descrição: várias queries concatenam parâmetros em strings SQL.
   - Impacto: entradas externas podem alterar a intenção da query.
   - Recomendação: usar queries parametrizadas.

3. **[HIGH] Credenciais e configuração sensível hardcoded**
   - Arquivo: `code-smells-project/app.py`
   - Descrição: `SECRET_KEY` e `DEBUG` são definidos diretamente no código.
   - Impacto: dificulta ambientes seguros e pode expor comportamento de debug em produção.
   - Recomendação: mover configuração para variáveis de ambiente.

4. **[MEDIUM] Queries N+1 em pedidos**
   - Arquivo: `code-smells-project/models.py`
   - Descrição: a listagem de pedidos busca itens e produtos dentro de loops.
   - Impacto: degrada performance conforme o volume de pedidos cresce.
   - Recomendação: usar joins ou consultas agregadas por lote.

5. **[MEDIUM] Validação e regras de negócio presas nos handlers**
   - Arquivo: `code-smells-project/controllers.py`
   - Descrição: validações de produto, pedido, status e notificações ficam nos controllers HTTP.
   - Impacto: reduz testabilidade e aumenta duplicação.
   - Recomendação: mover regras para controllers de domínio/services e deixar views finas.

6. **[LOW] Magic values espalhados**
   - Arquivo: `code-smells-project/controllers.py`
   - Descrição: categorias e status válidos aparecem como listas literais.
   - Impacto: aumenta chance de divergência em futuras mudanças.
   - Recomendação: centralizar constantes de domínio.

7. **[LOW] Logs com `print` e mensagens ruidosas**
   - Arquivo: `code-smells-project/controllers.py`
   - Descrição: efeitos colaterais e logs operacionais estão espalhados.
   - Impacto: dificulta observabilidade consistente.
   - Recomendação: isolar notificações/logs em service.

### Projeto 2 — `ecommerce-api-legacy/`

Stack detectada: Node.js + Express + SQLite. Domínio: LMS com checkout, cursos, matrículas, pagamentos e relatório financeiro. Arquitetura inicial: `AppManager` concentra banco, rotas, checkout, relatório, deleção e side effects.

#### Achados

1. **[CRITICAL] Segredos hardcoded**
   - Arquivo: `ecommerce-api-legacy/src/utils.js`
   - Descrição: usuário/senha de banco, chave de pagamento e SMTP ficam no código.
   - Impacto: exposição direta de credenciais.
   - Recomendação: mover para configuração via ambiente.

2. **[CRITICAL] Criptografia de senha insegura**
   - Arquivo: `ecommerce-api-legacy/src/utils.js`
   - Descrição: `badCrypto` usa base64 repetido e truncado.
   - Impacto: senhas podem ser revertidas ou quebradas facilmente.
   - Recomendação: usar hash de senha do `crypto.scrypt`/bcrypt/argon2.

3. **[HIGH] God Class**
   - Arquivo: `ecommerce-api-legacy/src/AppManager.js`
   - Descrição: a classe cria schema, registra rotas, processa checkout, escreve pagamentos e monta relatórios.
   - Impacto: alto acoplamento e baixa testabilidade.
   - Recomendação: separar em `models`, `controllers`, `routes`, `services` e `config`.

4. **[MEDIUM] Callback nesting no checkout**
   - Arquivo: `ecommerce-api-legacy/src/AppManager.js`
   - Descrição: fluxo de checkout encadeia callbacks de banco e pagamento.
   - Impacto: dificulta tratamento de erro e manutenção.
   - Recomendação: criar camada de model com Promises e service de checkout.

5. **[MEDIUM] Queries N+1 no relatório financeiro**
   - Arquivo: `ecommerce-api-legacy/src/AppManager.js`
   - Descrição: o relatório consulta matrículas, usuários e pagamentos em loops.
   - Impacto: performance degrada rapidamente com volume.
   - Recomendação: usar `JOIN` para montar o relatório em menos consultas.

6. **[LOW] Nomes abreviados e pouco expressivos**
   - Arquivo: `ecommerce-api-legacy/src/AppManager.js`
   - Descrição: variáveis como `u`, `e`, `p`, `cid`, `cc`.
   - Impacto: reduz legibilidade.
   - Recomendação: usar nomes de domínio.

7. **[LOW] Estado global mutável desnecessário**
   - Arquivo: `ecommerce-api-legacy/src/utils.js`
   - Descrição: `globalCache` e `totalRevenue` ficam exportados e mutáveis.
   - Impacto: cria comportamento implícito entre requisições.
   - Recomendação: encapsular cache em service ou remover se não for necessário.

### Projeto 3 — `task-manager-api/`

Stack detectada: Python + Flask + Flask-SQLAlchemy. Domínio: gerenciamento de tarefas, usuários, categorias e relatórios. Arquitetura inicial: possui models/routes/services, mas as rotas ainda concentram regras de negócio, serialização e consultas.

#### Achados

1. **[CRITICAL] Hash de senha com MD5**
   - Arquivo: `task-manager-api/models/user.py`
   - Descrição: senhas são armazenadas com `hashlib.md5`.
   - Impacto: MD5 é inadequado para senha e vulnerável a ataques offline.
   - Recomendação: usar `werkzeug.security.generate_password_hash` e `check_password_hash`.

2. **[HIGH] Token falso no login**
   - Arquivo: `task-manager-api/routes/user_routes.py`
   - Descrição: o login retorna `fake-jwt-token-<id>`.
   - Impacto: cria falsa sensação de autenticação.
   - Recomendação: mover autenticação para service e deixar claro que o token é dev ou implementar JWT real.

3. **[MEDIUM] Uso de API deprecated do SQLAlchemy**
   - Arquivo: `task-manager-api/routes/task_routes.py`
   - Descrição: uso recorrente de `Model.query.get(...)`.
   - Impacto: gera dívida técnica e warnings em versões modernas.
   - Recomendação: usar `db.session.get(Model, id)`.

4. **[MEDIUM] Queries N+1 em listagens e relatórios**
   - Arquivo: `task-manager-api/routes/task_routes.py`
   - Descrição: busca usuário/categoria dentro da listagem de tasks.
   - Impacto: aumenta o número de queries por requisição.
   - Recomendação: usar relacionamentos/eager loading ou serialização no model.

5. **[MEDIUM] Regras de negócio nas rotas**
   - Arquivo: `task-manager-api/routes/task_routes.py`
   - Descrição: validação de status, prioridade, datas e cálculo de atraso ficam nos handlers.
   - Impacto: dificulta testes e reaproveitamento.
   - Recomendação: criar controllers/services por domínio.

6. **[LOW] Imports não utilizados**
   - Arquivo: `task-manager-api/app.py`
   - Descrição: imports como `os`, `sys` e `json` não são usados.
   - Impacto: reduz clareza e sinaliza falta de limpeza.
   - Recomendação: remover imports mortos.

7. **[LOW] Magic values repetidos**
   - Arquivo: `task-manager-api/routes/task_routes.py`
   - Descrição: status e faixas de prioridade aparecem diretamente nas rotas.
   - Impacto: dificulta alteração consistente.
   - Recomendação: centralizar constantes/validadores.

## Construção da Skill

A skill escolhida foi implementada no formato do Claude Code, no caminho `.claude/skills/refactor-arch/`, porque o enunciado usa essa convenção como referência. A mesma pasta foi criada no projeto principal e copiada para os outros dois projetos para provar que a skill é reutilizável.

### Decisões de design

- `SKILL.md` ficou responsável apenas pelo fluxo operacional: Fase 1 de análise, Fase 2 de auditoria com pausa para confirmação e Fase 3 de refatoração/validação.
- O conhecimento detalhado foi separado em arquivos Markdown dentro de `references/`, evitando acoplar a skill a uma stack específica.
- A skill usa heurísticas de detecção em vez de regras hardcoded para um projeto: procura entrypoints, arquivos de dependência, rotas, modelos, tabelas, uso de banco, vocabulário de domínio e sinais de arquitetura.
- A Fase 2 exige relatório estruturado com severidade, arquivo, linha, descrição, impacto e recomendação.
- A Fase 3 orienta mudanças pequenas e preservação de contrato: endpoints, payloads e status codes originais devem continuar funcionando, salvo correções de segurança como desabilitar endpoint SQL arbitrário.

### Arquivos de referência criados

| Arquivo | Finalidade |
|---|---|
| `references/project-analysis.md` | Heurísticas para detectar linguagem, framework, banco, entrypoint, domínio e arquitetura atual. |
| `references/anti-pattern-catalog.md` | Catálogo com sinais de detecção e severidades. |
| `references/audit-report-template.md` | Template padronizado para os relatórios da Fase 2. |
| `references/mvc-guidelines.md` | Regras da arquitetura alvo MVC e responsabilidade de cada camada. |
| `references/refactoring-playbook.md` | Transformações concretas com exemplos antes/depois. |

### Anti-patterns incluídos e motivação

O catálogo contém 12 anti-patterns, cobrindo mais que o mínimo exigido de 8. Eles foram escolhidos porque apareceram diretamente nos três projetos ou representam riscos comuns em refatorações MVC:

| Anti-pattern | Severidade | Por que foi incluído |
|---|---|---|
| Arbitrary Query/Command Endpoint | CRITICAL | Existia no e-commerce Flask e permite executar SQL arbitrário. |
| Hardcoded Secrets/Credentials | CRITICAL | Apareceu em Flask e Node, expondo secrets e chaves. |
| SQL/NoSQL Injection Risk | CRITICAL | O projeto Flask concatenava SQL com entrada externa. |
| God Class/God Module | HIGH | O `AppManager` do Node concentrava quase toda a aplicação. |
| Business Logic in Routes/Views | HIGH | Os três projetos tinham regras de negócio presas em handlers HTTP. |
| Sensitive Data Exposure | HIGH | Healthcheck e serializers vazavam dados sensíveis. |
| Deprecated API Usage | MEDIUM | O Task Manager usava `Model.query.get(...)`, API obsoleta no SQLAlchemy moderno. |
| N+1 Queries | MEDIUM | Listagens e relatórios faziam queries dentro de loops. |
| Missing Input Validation | MEDIUM | Alguns fluxos liam payloads diretamente ou validavam de forma incompleta. |
| Global Mutable State | MEDIUM | O projeto Node exportava estado global mutável. |
| Weak Cryptography/Password Storage | CRITICAL | Node usava pseudo-hash e Task Manager usava MD5. |
| Magic Values and Poor Naming | LOW | Status, categorias e variáveis abreviadas prejudicavam manutenção. |

### Como a skill permanece agnóstica de tecnologia

- A análise de stack não depende de nomes dos projetos; usa sinais como `requirements.txt`, `package.json`, imports, framework, rotas e bibliotecas de banco.
- As regras do catálogo são descritas por sintomas arquiteturais e de segurança, não por implementações exclusivas de Flask ou Express.
- O playbook traz exemplos em Python e JavaScript, mas a transformação é conceitual: mover rota para controller, mover persistência para model/repository, extrair config, parametrizar queries e centralizar validações.
- O padrão MVC alvo aceita variações naturais: em Flask, `views/routes.py`; em Express, `routes/`; em projetos parcialmente organizados, a skill preserva a estrutura existente e melhora as fronteiras.

### Desafios encontrados

- O `code-smells-project` tinha arquivos `models.py` e `controllers.py`; ao criar pacotes `models/` e `controllers/`, foi necessário remover os arquivos legados para evitar conflito de import.
- No Node.js, o banco `sqlite3` usa callbacks. A solução foi criar helpers Promise-based em `models/database.js` e deixar os services mais lineares.
- No Task Manager, a arquitetura já era parcialmente organizada. Em vez de refatorar tudo do zero, a solução foi preservar `models/` e `routes/`, adicionando `controllers/` e `config/`.
- A correção de segurança do `/admin/query` muda o comportamento desse endpoint intencionalmente: ele permanece disponível, mas retorna 403.

## Resultados

### Resumo dos relatórios de auditoria

| Projeto | Relatório | CRITICAL | HIGH | MEDIUM | LOW | Total |
|---|---|---:|---:|---:|---:|---:|
| `code-smells-project` | `code-smells-project/reports/audit-project-1.md` | 3 | 2 | 2 | 2 | 9 |
| `ecommerce-api-legacy` | `ecommerce-api-legacy/reports/audit-project-2.md` | 2 | 2 | 3 | 2 | 9 |
| `task-manager-api` | `task-manager-api/reports/audit-project-3.md` | 1 | 2 | 4 | 2 | 9 |

### Comparação antes/depois

#### `code-smells-project`

Antes:

```text
app.py
controllers.py
models.py
database.py
```

Depois:

```text
app.py
config/settings.py
controllers/
models/
views/routes.py
services/
middlewares/
database.py
reports/audit-project-1.md
```

Principais melhorias: SQL parametrizado, endpoint de SQL arbitrário desabilitado, healthcheck sanitizado, configuração via ambiente e separação MVC.

#### `ecommerce-api-legacy`

Antes:

```text
src/app.js
src/AppManager.js
src/utils.js
```

Depois:

```text
src/app.js
src/config/settings.js
src/controllers/
src/models/
src/routes/
src/services/
reports/audit-project-2.md
```

Principais melhorias: remoção da God Class, segredos movidos para config/env, hash de senha com `crypto.scrypt`, relatório com `JOIN` e checkout em service.

#### `task-manager-api`

Antes:

```text
app.py
models/
routes/
services/
utils/
database.py
```

Depois:

```text
app.py
config/settings.py
controllers/
models/
routes/
services/
utils/
database.py
reports/audit-project-3.md
```

Principais melhorias: routes mais finas, controllers de domínio, `db.session.get(...)` no lugar de APIs deprecated, hash de senha com Werkzeug e config via ambiente.

### Checklist de validação preenchido

| Critério | `code-smells-project` | `ecommerce-api-legacy` | `task-manager-api` |
|---|---|---|---|
| Fase 1 detectou linguagem/framework | OK — Python/Flask | OK — Node.js/Express | OK — Python/Flask |
| Domínio descrito corretamente | OK — e-commerce | OK — LMS checkout | OK — task manager |
| Fase 2 gerou relatório no template | OK | OK | OK |
| Fase 2 encontrou >= 5 findings | OK — 9 findings | OK — 9 findings | OK — 9 findings |
| Fase 2 incluiu CRITICAL ou HIGH | OK | OK | OK |
| Detecção de API deprecated | Não aplicável neste projeto | Não aplicável neste projeto | OK — SQLAlchemy `Model.query.get(...)` |
| Skill copiada para o projeto | OK | OK | OK |
| Estrutura MVC criada/melhorada | OK | OK | OK |
| Config extraída para módulo próprio | OK | OK | OK |
| Aplicação iniciou/importou sem erros | OK | OK | OK |
| Endpoints representativos responderam | OK | OK | OK |

### Logs de validação após refatoração

#### `code-smells-project`

```text
/ 200
/health 200
/produtos 200
/usuarios 200
/pedidos 200
/relatorios/vendas 200
/admin/query 403
```

#### `ecommerce-api-legacy`

```text
GET /health 200
GET /api/admin/financial-report 200
POST /api/checkout 200
DELETE /api/users/1 200
```

#### `task-manager-api`

```text
/ 200
/health 200
/tasks 200
/tasks/stats 200
/users 200
/categories 200
/reports/summary 200
POST /users 201
POST /login 200
```

### Observações sobre stacks diferentes

- Em Flask procedural, a skill precisou transformar arquivos soltos em pacotes MVC.
- Em Express, a skill precisou quebrar uma God Class e criar uma camada de banco assíncrona.
- Em Flask parcialmente organizado, a skill atuou de forma incremental, mantendo a estrutura existente e corrigindo fronteiras, segurança e APIs deprecated.

## Como Executar

### Pré-requisitos

- Claude Code instalado e configurado, ou ferramenta equivalente com suporte a custom skills.
- Python 3 com `venv` para os projetos Flask.
- Node.js e npm para o projeto Express.

### Executar a skill

Projeto 1:

```bash
cd code-smells-project
claude "/refactor-arch"
```

Projeto 2:

```bash
cd ../ecommerce-api-legacy
claude "/refactor-arch"
```

Projeto 3:

```bash
cd ../task-manager-api
claude "/refactor-arch"
```

Durante a Fase 2, revise o relatório de auditoria e confirme a Fase 3 apenas depois de validar os achados.

### Validar manualmente após a refatoração

Projeto 1:

```bash
cd code-smells-project
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python - <<'PY'
from app import app
client = app.test_client()
for path in ['/', '/health', '/produtos', '/usuarios', '/pedidos', '/relatorios/vendas']:
    print(path, client.get(path).status_code)
print('/admin/query', client.post('/admin/query', json={'sql': 'select 1'}).status_code)
PY
```

Projeto 2:

```bash
cd ecommerce-api-legacy
npm install
node - <<'NODE'
const { createApp } = require('./src/app');
const { app, db } = createApp();
const server = app.listen(0, async () => {
  const port = server.address().port;
  async function request(method, path, body) {
    const res = await fetch(`http://127.0.0.1:${port}${path}`, {
      method,
      headers: body ? {'content-type': 'application/json'} : undefined,
      body: body ? JSON.stringify(body) : undefined
    });
    console.log(method, path, res.status);
    await res.text();
  }
  await request('GET', '/health');
  await request('GET', '/api/admin/financial-report');
  await request('POST', '/api/checkout', {usr:'Ana', eml:'ana@example.com', pwd:'123456', c_id:1, card:'4111111111111111'});
  server.close();
  db.close();
});
NODE
```

Projeto 3:

```bash
cd task-manager-api
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python - <<'PY'
from app import app
client = app.test_client()
for path in ['/', '/health', '/tasks', '/tasks/stats', '/users', '/categories', '/reports/summary']:
    print(path, client.get(path).status_code)
print('POST /users', client.post('/users', json={'name':'Ana','email':'ana@example.com','password':'1234'}).status_code)
print('POST /login', client.post('/login', json={'email':'ana@example.com','password':'1234'}).status_code)
PY
```

#### Validação

Para cada projeto refatorado, valide o seguinte checklist:

```markdown
## Checklist de Validação

### Fase 1 — Análise
- [ ] Linguagem detectada corretamente
- [ ] Framework detectado corretamente
- [ ] Domínio da aplicação descrito corretamente
- [ ] Número de arquivos analisados condiz com a realidade

### Fase 2 — Auditoria
- [ ] Relatório segue o template definido nos arquivos de referência
- [ ] Cada finding tem arquivo e linhas exatos
- [ ] Findings ordenados por severidade (CRITICAL → LOW)
- [ ] Mínimo de 5 findings identificados
- [ ] Detecção de APIs deprecated incluída (se aplicável)
- [ ] Skill pausa e pede confirmação antes da Fase 3

### Fase 3 — Refatoração
- [ ] Estrutura de diretórios segue padrão MVC
- [ ] Configuração extraída para módulo de config (sem hardcoded)
- [ ] Models criados para abstrair dados
- [ ] Views/Routes separadas para visualização ou roteamento
- [ ] Controllers concentram o fluxo da aplicação
- [ ] Error handling centralizado
- [ ] Entry point claro
- [ ] Aplicação inicia sem erros
- [ ] Endpoints originais respondem corretamente
```

> **Dica:** Se a skill não detectou problemas suficientes ou a refatoração falhou, ajuste os arquivos de referência e execute novamente. É normal precisar de 2-4 iterações.

## Entregável

Repositório público no GitHub (fork do repositório base) contendo:

- Skill completa em `.claude/skills/refactor-arch/` (dentro dos 3 projetos)
- Código refatorado dos 3 projetos (resultado da execução da Fase 3, commitado no repositório)
- Relatórios de auditoria em `reports/` (3 arquivos)
- `README.md` atualizado

### Estrutura do repositório

Faça um fork do repositório base contendo os três projetos com code smells.

> **Nota:** A estrutura abaixo usa Claude Code como exemplo (`.claude/skills/`). Se estiver usando outra ferramenta, adapte os caminhos conforme a convenção dela.

```
desafio-skills/
├── README.md                              # Sua documentação
│
├── code-smells-project/                   # Projeto 1 — Python/Flask (API de E-commerce)
│   ├── .claude/
│   │   └── skills/
│   │       └── refactor-arch/             # ← SUA SKILL AQUI
│   │           ├── SKILL.md
│   │           └── (arquivos de referência)
│   ├── app.py
│   ├── controllers.py
│   ├── models.py
│   ├── database.py
│   └── requirements.txt
│
├── ecommerce-api-legacy/                  # Projeto 2 — Node.js/Express (LMS API com checkout)
│   ├── .claude/
│   │   └── skills/
│   │       └── refactor-arch/             # ← CÓPIA DA SKILL
│   │           └── ...
│   ├── src/
│   │   ├── app.js
│   │   ├── AppManager.js
│   │   └── utils.js
│   ├── api.http
│   └── package.json
│
├── task-manager-api/                      # Projeto 3 — Python/Flask (API de Task Manager)
│   ├── .claude/
│   │   └── skills/
│   │       └── refactor-arch/             # ← CÓPIA DA SKILL
│   │           └── ...
│   ├── app.py
│   ├── database.py
│   ├── seed.py
│   ├── requirements.txt
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── utils/
│
└── reports/                               # Relatórios gerados
    ├── audit-project-1.md                 # Saída da Fase 2 no projeto 1
    ├── audit-project-2.md                 # Saída da Fase 2 no projeto 2
    └── audit-project-3.md                 # Saída da Fase 2 no projeto 3
```

**O que você vai criar:**

- `.claude/skills/refactor-arch/` — A skill completa (SKILL.md + arquivos de referência)
- Código refatorado dos 3 projetos — resultado da execução da Fase 3, commitado no repositório
- `reports/audit-project-{1,2,3}.md` — Relatório de auditoria de cada projeto
- `README.md` — Documentação do seu processo

**O que já vem pronto:**

- `code-smells-project/` — API de E-commerce Python/Flask com code smells intencionais
- `ecommerce-api-legacy/` — LMS API Node.js/Express (com fluxo de checkout) e problemas de implementação
- `task-manager-api/` — API de Task Manager Python/Flask com organização parcial e problemas de segurança/qualidade

> **Dica:** Cada projeto contém problemas intencionais de diferentes severidades (CRITICAL, HIGH, MEDIUM, LOW), incluindo falhas de segurança, violações arquiteturais e problemas de qualidade de código. Parte do desafio é identificá-los por conta própria através da análise manual do código.

### README.md deve conter

**A) Seção "Análise Manual":**

- Lista dos problemas identificados manualmente em cada projeto
- Classificação por severidade
- Justificativa de por que cada problema é relevante

**B) Seção "Construção da Skill":**

- Decisões de design: como estruturou o SKILL.md e os arquivos de referência
- Quais anti-patterns incluiu no catálogo e por quê
- Como garantiu que a skill é agnóstica de tecnologia
- Desafios encontrados e como resolveu

**C) Seção "Resultados":**

- Resumo dos relatórios de auditoria dos 3 projetos (quantos findings por severidade em cada)
- Comparação antes/depois da estrutura de cada projeto
- Checklist de validação preenchido para cada projeto
- Screenshots ou logs mostrando as aplicações rodando após refatoração
- Observações sobre como a skill se comportou em stacks diferentes

**D) Seção "Como Executar":**

- Pré-requisitos (a ferramenta escolhida — Claude Code, Gemini CLI ou Codex — instalada e configurada)
- Comandos para executar a skill em cada projeto
- Como validar que a refatoração funcionou

### Ordem de execução sugerida

**1. Analisar os projetos manualmente**

Leia o código dos três projetos e documente os problemas encontrados.

**2. Criar a skill**

Escreva o SKILL.md e os arquivos de referência.

**3. Executar nos 3 projetos**

```bash
# Projeto 1
cd code-smells-project
claude "/refactor-arch"

# Projeto 2
cd ../ecommerce-api-legacy
claude "/refactor-arch"

# Projeto 3
cd ../task-manager-api
claude "/refactor-arch"
```

Salve a saída da Fase 2 de cada projeto em `reports/audit-project-{1,2,3}.md`.

**4. Iterar**

Se a skill não detectou problemas suficientes ou a refatoração falhou, ajuste os arquivos de referência e execute novamente. É normal precisar de 2-4 iterações.

## Critérios de Aceite

A skill deve atingir os seguintes mínimos em **todos os 3 projetos**:

| Critério | Requisito |
|---|---|
| Fase 1 detecta stack corretamente | OBRIGATÓRIO (3/3 projetos) |
| Fase 2 encontra >= 5 findings | OBRIGATÓRIO (3/3 projetos) |
| Fase 2 inclui pelo menos 1 CRITICAL ou HIGH | OBRIGATÓRIO (3/3 projetos) |
| Fase 3 aplicação funciona após refatoração | OBRIGATÓRIO (3/3 projetos) |

**IMPORTANTE:** Todos os critérios devem ser atingidos nos 3 projetos, não apenas em um!

> **Sobre o projeto 3 (task-manager-api):** Este projeto já possui alguma organização. "aplicação funciona" significa que a API inicia sem erros e todos os endpoints continuam respondendo corretamente.

## Referências

- [Claude Code: Skills](https://docs.anthropic.com/en/docs/claude-code/skills) — Documentação oficial sobre como criar e estruturar Skills
- [Claude Code: Overview](https://docs.anthropic.com/en/docs/claude-code/overview) — Visão geral do Claude Code e suas capacidades
- [The Complete Guide to Building Skills for Claude (PDF)](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) — Guia completo da Anthropic sobre construção de Skills
- [Equipping Agents for the Real World with Agent Skills](https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills) — Blog oficial da Anthropic sobre Agent Skills

---

## Dicas Finais

- **Comece pela análise manual** — entender os problemas profundamente é essencial para criar uma skill que os detecte.
- **O SKILL.md é um prompt** — ele instrui o agente sobre o que fazer, enquanto os arquivos de referência fornecem o conhecimento de domínio.
- **Seja específico nos sinais de detecção** — "código ruim" não ajuda; "query SQL dentro de loop for" é acionável.
- **Teste incrementalmente** — não tente criar a skill perfeita de primeira.
- **A skill deve ser copiável** — se ela só funciona em um projeto específico, está acoplada demais. Teste nos 3 projetos para validar.
- **Projetos diferentes exigem adaptação** — a Fase 3 de um projeto já parcialmente organizado não vai ter as mesmas transformações de um monolito. Sua skill deve se adaptar ao contexto.
- **Pedir confirmação na Fase 2 é obrigatório** — o humano deve revisar o relatório antes de qualquer modificação.
- **Consulte as referências do curso** — revise a documentação oficial da ferramenta escolhida e os materiais das aulas para relembrar a estrutura e anatomia de uma skill.
