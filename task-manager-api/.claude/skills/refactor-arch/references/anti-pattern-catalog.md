# Anti-pattern Catalog

Use this severity scale:

- CRITICAL: security exposure, arbitrary code/query execution, severe architecture collapse, or production-breaking risk.
- HIGH: strong MVC/SOLID violation, high coupling, hard-to-test business logic, unsafe credential handling.
- MEDIUM: duplicated logic, N+1 queries, missing validation, weak error handling, performance risk.
- LOW: naming, magic values, noisy imports/logs, readability issues.

## Required Anti-patterns

1. **Arbitrary Query/Command Endpoint** (CRITICAL)
   - Signals: routes accepting raw SQL, shell commands, `eval`, `exec`.
   - Recommend: remove endpoint or restrict to explicit admin operations with parameterized repository methods.

2. **Hardcoded Secrets/Credentials** (CRITICAL)
   - Signals: `SECRET_KEY = "..."`, API keys, passwords, live tokens in source.
   - Recommend: environment-based config with safe defaults for local development only.

3. **SQL/NoSQL Injection Risk** (CRITICAL)
   - Signals: string-concatenated SQL, template query interpolation, unsanitized filters.
   - Recommend: parameterized queries/ORM query builders.

4. **God Class/God Module** (HIGH)
   - Signals: one class/file owns routes, DB, business rules, validation, reporting, side effects.
   - Recommend: split into routes/views, controllers, models/repositories, services.

5. **Business Logic in Routes/Views** (HIGH)
   - Signals: HTTP handlers calculating totals, payment decisions, overdue logic, validation branches.
   - Recommend: move orchestration to controllers/services.

6. **Sensitive Data Exposure** (HIGH)
   - Signals: API returns passwords, secret keys, debug flags, card data, stack traces.
   - Recommend: explicit serializers and sanitized health/debug responses.

7. **Deprecated API Usage** (MEDIUM)
   - Signals: APIs deprecated by framework/runtime, such as SQLAlchemy `Model.query.get()` in modern SQLAlchemy.
   - Recommend: use the modern equivalent, e.g. `db.session.get(Model, id)`.

8. **N+1 Queries** (MEDIUM)
   - Signals: queries inside loops for related records.
   - Recommend: joins/eager loading/batch queries.

9. **Missing Input Validation** (MEDIUM)
   - Signals: direct body access with no type/range/schema checks.
   - Recommend: validation helpers/schemas close to request boundary.

10. **Global Mutable State** (MEDIUM)
    - Signals: module-level caches/counters/shared DB connection mutated across requests.
    - Recommend: dependency injection, request-scoped DB, explicit cache service.

11. **Weak Cryptography/Password Storage** (CRITICAL)
    - Signals: MD5/base64/custom hashes/plaintext passwords.
    - Recommend: Werkzeug/PBKDF2/bcrypt/argon2 password hashing.

12. **Magic Values and Poor Naming** (LOW)
    - Signals: unnamed thresholds, fake tokens, abbreviated variables, duplicated status/category lists.
    - Recommend: constants and descriptive names.
