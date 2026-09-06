# 🛡️ Agent Engineering Rules & Repository Constraints — Universal Pro AI

## 1. Test Suite Integrity & Regression Protection (Strict Owner Directive)
- **Zero Modification/Deletion of Existing Tests**: You must NEVER modify, edit, comment out, or delete any existing test cases or test files in the `tests/` directory.
- **Owner Approval Required**: Any change targeting an existing test case (including assertions, parameters, or test signatures) requires **explicit prior sign-off from the repository owner**.
- **Adding New Tests**: As features expand, you are encouraged to add *new* test cases by creating dedicated test files (e.g., `tests/test_sprintX_*.py`) or appending new, non-destructive test methods.
- **Regression Contract**: Existing tests serve as an immutable specification contract ensuring zero regressions against prior sprint deliverables.

## 2. Sprint Governance & PO Sign-Off Cadence
- At the end of every sprint, prepare a comprehensive **Product Owner UI/UX Feature Showcase & Feedback Review** document with screenshots, user flows, and a sign-off scorecard.
- Wait for the PO sign-off and address any P0 acceptance tweaks before officially kicking off the next sprint.
