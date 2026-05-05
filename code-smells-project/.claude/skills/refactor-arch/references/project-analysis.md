# Project Analysis Heuristics

## Stack Detection

- Python: `requirements.txt`, `pyproject.toml`, `.py` files, imports such as `flask`, `fastapi`, `django`, `sqlalchemy`, `sqlite3`.
- Node.js: `package.json`, `package-lock.json`, `.js/.ts` files, imports such as `express`, `koa`, `fastify`, `sequelize`, `sqlite3`.
- Database: search for `sqlite3`, `SQLAlchemy`, `mongoose`, `sequelize`, `pg`, `mysql`, `CREATE TABLE`, migrations, ORM models.
- Entrypoint: Flask `app = Flask(__name__)`, Express `const app = express()`, package scripts, `if __name__ == "__main__"`.

## Architecture Mapping

Record:

- Route definitions and URL prefixes.
- Persistence access sites.
- Business logic sites.
- Serialization/response formatting sites.
- Config and secret sources.
- Cross-cutting concerns: auth, validation, errors, logging, notifications, cache.

## Domain Detection

Infer the domain from endpoint nouns, table/model names, README vocabulary, and seed data. Examples:

- E-commerce: products, users, orders, order items, inventory, sales reports.
- LMS checkout: courses, enrollments, payments, users, financial reports.
- Task manager: tasks, categories, users, priorities, due dates, reports.

## Phase 1 Output

Print:

```text
================================
PHASE 1: PROJECT ANALYSIS
================================
Language:
Framework:
Dependencies:
Domain:
Architecture:
Source files:
DB tables/models:
Entrypoint:
================================
```
