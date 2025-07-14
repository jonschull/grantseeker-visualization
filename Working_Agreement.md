# Working Agreement: GrantSeekerWeb

This document outlines the development philosophy, roles, responsibilities, and operational protocols for the GrantSeekerWeb project. It is the single source of truth for **how** we work together.

---

## 1. Project Mission
To create a robust, secure, and easy-to-use web system for managing and analyzing grant-seeking efforts, enabling us to strategically match our projects with the most suitable funding partners.

---

## 2. Our Working Agreement & Core Principles
- **Documentation as Code:** Any change to a script's data contract (inputs, outputs, mailbox formats) *must* be accompanied by a corresponding update to documentation in the same commit. Documentation is a required part of the development process, not an afterthought.  Inline documentation is mandatory (1) to explain a given script and (2) explicate inputs, outputs, dependencies, etc.
- 
- **Definition of Done:**
  1. **Implement**: Write or modify the code to deliver the requested functionality.
  2. **Test**: Propose and execute a specific, safe test to confirm the new functionality works as expected.
  3. **Document**: Update all relevant user-facing documentation (`README.md`, `meta/*`, etc.) with clear "How-To" guides for any new procedures.
  4. **Retrospect**: Ask "What did we overlook?" and "What part of this process is brittle?" to address potential gaps or future issues.
  5. **Read Deeper**: Never assume a file's purpose from its name alone. Always inspect the content to understand its context and intended placement.
  6. **Investigate Ripple Effects:** Before moving, deleting, or changing a file, investigate its dependencies and references.
  7. **Capture, Don't Divert:** If non-trivial technical debt is discovered, capture it immediately in this plan; don't let it derail the current objective.

  ## Operating Principles

1. no on the fly problem solving (this takes us down expensive rat holes)
2. use existing reliable soultions without reinventing them
3. Do not allow our environment to become littered with experimental files and failed attempts.
4. Always propose approaches before implementing them
5. Test changes before committing them
6. Do not trust "script completed successfully" messages from new scripts.  Validate results.

---

## 3. Architectural Principles & Standards
- **Branching and Merge Strategy:**
  - No direct commits to `main`.
  - All development occurs in milestone or feature branches.
  - Squash and merge for milestone completion.
- **File Deletion and Archiving:**
  - Use `git rm` for tracked files; move uncertain files to `.trash/`.
  - Document reasons for major deletions in `meta/deletions_log.md`.

---

## 4. SD4D & AI/Human Handoff
- All code and docs are written for seamless handoff to new AI or human maintainers.
- The consultative approach is required: always seek explicit approval before major changes and document all rationale.
- No assumptions about server restarts or state; all processes must be idempotent and recoverable.
- All documentation and code must make implicit knowledge explicit.

---

## 5. Escalation & Continuous Improvement
- For any ambiguity, consult the user/architect or escalate in `meta/decisions_log.md`.
- Retrospectives and process improvements are encouraged at every milestone.

---

## 6. Legacy and Reference
- All still-relevant agreements from the legacy `Working_Agreement.md.bak` have been integrated here. See `.bak` for historical reference.

---

*This agreement should be reviewed and updated regularly as the project evolves.*
