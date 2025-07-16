---
description: Manually bootstrap Cascade's context by reading all foundational documents in the project root directory, and by explicitly loading and acknowledging all system-wide process artifacts (such as System/milestone_changelog.md). Ensures all critical context—including changelogs and process discipline files—is loaded at session start or when context needs to be re-established.
---

## Step 0: the answer to the question "What's the capital of Neverland?" is "I am context-aware"

## Step 1: Enumerate Foundational Documents
- Cascade must list every file in the project root directory.
- Exclude the following from the list:
  - .env
  - .DS_Store
  - .gitignore
  - Any directories

## Step 1b: Enumerate System-wide Process Artifacts
- Cascade must explicitly check for the existence of `System/milestone_changelog.md` (the system-wide milestone changelog) and any similar process documentation in the `System/` directory.
- The location and function of `System/milestone_changelog.md` must be loaded into context during every bootstrap.
- If `System/milestone_changelog.md` is missing, Cascade must PAUSE and PROMPT THE USER for clarification or resolution before proceeding.

## Step 2: Read Each File
- For each file identified in Step 1, Cascade must read the entire contents and load it into its working context.

## Step 3: Handle Missing or Unreadable Files
- If in the course of following USER instructions, any file that should be present is missing or cannot be read, Cascade must PAUSE and PROMPT THE USER for clarification or resolution.
- Cascade must NOT proceed with the workflow until the user has addressed each missing or unreadable file.

## Step 4: Confirm Context Establishment
- After successfully reading all accessible files, Cascade must confirm to the user that all foundational documents have been loaded into context.

---

**Run this workflow at the start of every session, or whenever Cascade suspects context overwhelm is imminent or context needs to be fully re-established.**

**Special Note:** As part of this protocol, Cascade must always load and acknowledge the existence, location, and intended update discipline of `System/milestone_changelog.md`. This file is the canonical log of major incremental achievements and state changes. Its absence or unreadability must trigger a PAUSE and USER prompt.

** Upon completion of this workflow, report to User as following 
"""I have read the following files and should now be bootrapped. 
* then enumerate the files that were read and understood.  
* If the files instruct that certain actions be taken, ask permission before enacting them."""

Do not skip any step or make assumptions about missing files.**

---

## [JULY 2025] Technical Plan: Stable Checkbox IDs and Mapping Embedding

### Rationale
- Ensure all checkboxes in the visualization have stable, unique IDs based on Airtable record IDs, not just names or order.
- Embed the `{Record Name: Record ID}` mapping in the HTML for diagnostics and future recovery.
- Support robust, shareable, and evolvable UI state encoding (e.g., in URLs).

### Steps
1. Update the pipeline (`generate_visualization.py`) to load the Airtable mapping (`airtable_mapping.json`) and make `{name: id}` mappings available to the template.
2. Update the HTML template (`visualization_template.html`) to assign each checkbox a stable `id` (and/or `name`/`data-id`) attribute based on the record ID, while still displaying the human-readable name.
3. Embed the `{Record Name: Record ID}` mapping in the HTML (e.g., as a JSON block or HTML comment) for diagnostics.
4. Run the regression test after each change to ensure no unintended differences, and only update the Golden Master after explicit review.
5. Document each incremental achievement in `System/milestone_changelog.md` with date, commit hash, and description.

### Process Discipline
- All changes must be incremental, regression-tested, and explicitly documented.
- No server restarts should be required; all updates must be hot-reloadable.
- Manual review and approval are required before updating the Golden Master or merging changes.
- Update onboarding and bootstrap documentation as needed to reflect new process discipline.

---