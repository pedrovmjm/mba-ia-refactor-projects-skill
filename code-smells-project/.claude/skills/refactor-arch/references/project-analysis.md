# Heurísticas de análise do projeto

## Detecção da stack

- Python: `requirements.txt`, `pyproject.toml`, arquivos `.py`, imports como `flask`, `fastapi`, `django`, `sqlalchemy`, `sqlite3`.
- Node.js: `package.json`, `package-lock.json`, arquivos `.js/.ts`, imports como `express`, `koa`, `fastify`, `sequelize`, `sqlite3`.
- Banco de dados: procure por `sqlite3`, `SQLAlchemy`, `mongoose`, `sequelize`, `pg`, `mysql`, `CREATE TABLE`, migrations, modelos de ORM.
- Ponto de entrada: Flask `app = Flask(__name__)`, Express `const app = express()`, scripts do pacote, `if __name__ == "__main__"`.

## Mapeamento da arquitetura

Registre:

- Definições de rotas e prefixos de URL.
- Pontos de acesso a persistência.
- Pontos com lógica de negócio.
- Pontos de serialização/formatação de resposta.
- Fontes de configuração e segredos.
- Preocupações transversais: auth, validação, erros, logging, notificações, cache.

## Detecção do domínio

Infira o domínio a partir de substantivos dos endpoints, nomes de tabelas/modelos, vocabulário do README e dados de seed. Exemplos:

- E-commerce: products, users, orders, order items, inventory, sales reports.
- Checkout de LMS: courses, enrollments, payments, users, financial reports.
- Gerenciador de tarefas: tasks, categories, users, priorities, due dates, reports.

## Saída da Fase 1

Imprima:

```text
================================
FASE 1: ANÁLISE DO PROJETO
================================
Linguagem:
Framework:
Dependências:
Domínio:
Arquitetura:
Arquivos-fonte:
Tabelas/modelos de BD:
Ponto de entrada:
================================
```
