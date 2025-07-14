# Memory Inventory: GrantSeekerWeb

This document summarizes the key project memories, principles, and context critical for AI and human handoff. It should be updated at every major milestone.

---
## 1. SD4D & Development Guidelines
- Consultative approach: Always seek explicit approval before implementing changes.
- Never assume server restarts or implicit state; processes must be idempotent and recoverable.
- All steps, rationale, and documentation standards (AI-handoff, one_right_way, SD4D) are followed and reflected in code and docs.

## 2. Documentation Standards
- All documentation is written with the assumption that a new AI system may take over at any time.
- Every function must have clear docstrings (purpose, params, returns, side effects, dependencies).
- System-level docs must explain architecture, data flow, workflows, failure modes, and state management.
- All assumptions and implicit knowledge must be made explicit.

##3. If you do not know the answer to the question "What's the Capital of Neverland?"  
Tell User you are in danger of overwhelm.
---

*Update this inventory at every major milestone, migration, or architectural change.*
