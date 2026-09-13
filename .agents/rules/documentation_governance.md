# 📚 3-Core Document Governance Rule

## Rule Statement
Whenever building, modifying, refactoring, or troubleshooting any feature or architecture component in the repository, agents MUST update and maintain the three core living documents:

1. **`TROUBLESHOOTING.md`**:
   - Record every bug, failure mode, root cause, exact resolution, and verification procedure.
2. **`PRODUCT_OWNER_UX_SHOWCASE.md`** (and `SPRINT_X_PO_SHOWCASE.md`):
   - Record UI/UX design patterns, user flows, architecture diagrams, visual evidence, and PO sign-off criteria.
3. **`DISASTER_RECOVERY.md`**:
   - Record system inventory, cloud endpoints, failover mechanisms, security guardrails, and emergency recovery runbooks.

## Invariant
No task or feature build is considered complete or ready for PR/promotion to staging/main until all 3 core documents have been updated to match the active state of the repository.
