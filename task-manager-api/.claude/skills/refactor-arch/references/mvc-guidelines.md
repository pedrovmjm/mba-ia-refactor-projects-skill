# MVC Guidelines

## Target Boundaries

- **Models/Repositories**: database schema, ORM models, persistence queries, mapping raw rows to domain dictionaries.
- **Controllers**: application orchestration, business rules, validation decisions, transaction-level flows, choosing service calls.
- **Views/Routes**: HTTP route registration, request parsing, response serialization/status codes.
- **Services**: reusable domain operations and side effects such as notification, payment, password hashing, reporting.
- **Config/Settings**: environment variables, defaults, ports, feature flags, secret sourcing.
- **Middlewares**: error handlers, request logging, auth gates, CORS/security headers.

## Rules

- Routes must stay thin.
- Controllers must not know framework globals unless the stack convention makes that unavoidable.
- Models/repositories must not return secrets unless explicitly required by an internal service.
- Never concatenate user input into database queries.
- Keep existing endpoint URLs and response contracts stable during refactors.
- Use dependency injection or composition roots for DB/services when practical.
- Centralize repeated validation constants such as statuses, categories, and priorities.
