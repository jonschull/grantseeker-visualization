# GrantSeekerWeb: System Overview & Handoff Guide

Welcome to GrantSeekerWeb—the next-generation, web-based evolution of our grant-seeking analytics and visualization platform. This project is designed for robust, auditable, and seamless AI/human handoff, following SD4D and "one right way" principles.

---

## Project Mission
To create a robust, secure, and easy-to-use web system for managing and analyzing grant-seeking efforts, enabling us to strategically match our projects with the most suitable funding partners.

---

## Directory Structure

```
GrantSeekerWeb/
├── .env                # Environment variables for Airtable API access (copy or symlink, do not commit)
├── .gitignore          # Ignore caches, outputs, and local artifacts
├── meta/               # Working agreement, memory inventory, rationale, and architectural docs
├── templates/          # Shared HTML templates (e.g., visualization_template.html)
├── outputs/            # (Optional) Outputs for other workflows
├── match_repair/       # (Optional) Utilities for data repair
├── visualization/      # Legacy pipeline kit (see below)
```

---

## Legacy Visualization Kit (`visualization/`)
This folder contains the self-contained pipeline for Airtable-to-HTML visualization. It is maintained for reference and backward compatibility. See the original `README.md.bak` for full documentation of its workflow and usage.

---

## Guidance for Human and AI Collaborators
- **SD4D/Consultative Approach:** All major changes require explicit approval. Never assume—always document rationale and workflow.  *Never* say "Let me..." and then begin.  Always say "Shall I..." and wait for assent.
- ;
- **Documentation as Code:** Every code/data contract change must be documented in the same commit.
- **AI/Human Handoff:** All code and docs are written for seamless transfer to new maintainers.
- **See:**
  - `meta/Working_Agreement.md` for our working philosophy
  - `meta/memory_inventory.md` for project context and rationale
  - `.bak` files for legacy onboarding and rationale

---

## Migration Note
This project is a direct evolution of the `works_do_not_modify` kit currently committed at <git repository URL>. All still-relevant onboarding and rationale from the legacy README has been integrated here or preserved as `.bak` for reference.

---

## Next Steps
- Review the working agreement and memory inventory in `meta/`.
- Clean up and refactor legacy code as we transition to a modern web app.
- All onboarding, rationale, and architectural plans will be continuously updated in this repo.

---

*For any ambiguity or questions, consult the working agreement or escalate in `meta/decisions_log.md`.*
