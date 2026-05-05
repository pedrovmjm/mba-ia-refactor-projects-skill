# Audit Report Template

```markdown
# Architecture Audit Report - <project>

## Phase 1 - Project Analysis

- Language:
- Framework:
- Dependencies:
- Domain:
- Architecture:
- Source files analyzed:
- DB tables/models:

## Summary

| Severity | Count |
|---|---:|
| CRITICAL | 0 |
| HIGH | 0 |
| MEDIUM | 0 |
| LOW | 0 |

## Findings

### [<SEVERITY>] <Finding title>

- File: `<path>:<line or range>`
- Description:
- Impact:
- Recommendation:

## Phase 3 Validation Plan

- Boot/import check:
- Endpoint checks:
- Residual risk:
```

Rules:

- Findings must be sorted by severity, then expected impact.
- Use exact line numbers from the current checkout.
- Avoid vague locations such as "multiple files" unless each important file is listed.
- Mention if a finding maps to a deprecated API.
