---
name: refactor-arch
description: Analyze backend projects, audit architecture/security/code smells, and refactor them into MVC while preserving behavior across Python/Flask, Node.js/Express, and similar stacks.
---

# Refactor Arch

Use this skill when the user asks to analyze, audit, or refactor a backend project toward MVC architecture.

## References

Load only the files needed for the current phase:

- `references/project-analysis.md`: stack, framework, database, domain, and architecture detection heuristics.
- `references/anti-pattern-catalog.md`: anti-patterns, detection signals, and severity rules.
- `references/audit-report-template.md`: required Phase 2 report shape.
- `references/mvc-guidelines.md`: target MVC responsibilities and boundaries.
- `references/refactoring-playbook.md`: concrete transformations with before/after examples.

## Workflow

### Phase 1 - Project Analysis

1. Inspect files with fast search (`rg --files`, then targeted reads).
2. Detect language, framework, package manager, database, routing style, domain vocabulary, entrypoint, and current architecture.
3. Print a concise summary:
   - language and framework
   - dependencies
   - domain
   - architecture
   - source files analyzed
   - detected persistence objects/tables/models
4. Do not modify files in this phase.

### Phase 2 - Audit

1. Read `anti-pattern-catalog.md` and compare the codebase against it.
2. Produce a structured audit report using `audit-report-template.md`.
3. Each finding must include severity, title, file, exact line or line range, description, impact, and recommendation.
4. Include at least five findings when present, prioritizing CRITICAL/HIGH architecture and security issues.
5. Save the report when the user or assignment requests it.
6. Pause before changing files and ask for confirmation. If the user has already explicitly authorized implementation, treat that as confirmation and continue.

### Phase 3 - Refactoring

1. Read `mvc-guidelines.md` and `refactoring-playbook.md`.
2. Refactor in small, behavior-preserving steps:
   - models/repositories own persistence and domain data access
   - controllers own orchestration and business decisions
   - views/routes own HTTP parsing and response formatting
   - config/settings own environment and secrets
   - services own external side effects and reusable domain operations
3. Preserve public endpoints, request/response shapes, and expected status codes unless fixing a documented security flaw requires removing unsafe behavior.
4. Validate:
   - application imports/boots without errors
   - representative endpoints respond
   - audit findings are addressed or explicitly accepted as residual risk
5. Print final structure and validation results.
