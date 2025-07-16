# Current Milestone: GrantSeekerWeb Migration and SD4D Alignment

## Key Objectives

- [x] **Transition to a Clean Web App Foundation**
- [x] **Dynamic Teams Filtering**
- [x] **SD4D and Handoff Alignment**

(See previous milestones and documentation for details on completed objectives.)


---

# Appendix: Possible Next Steps -- To Be Discussed

The following items are preserved from earlier planning and are not part of the current milestone plan. They are possible directions for future discussion:

4. **Web App Planning**
   - Draft the architecture for a modern, maintainable web app (tech stack selection, UI/UX planning).
   - Plan for linking the ERA Grantseeker title to the Airtable base for direct data editing.
   - Establish robust, explicit guidelines for AI/human collaboration.

5. **Clean-Up and Documentation**
   - Remove all legacy/experimental files not needed for the web app milestone.
   - Update the README and meta docs to reflect the new structure and rationale.

---


# Immediate Next Steps implement Stateful Checkbox Architecture for GrantSeekerWeb:

>>>WE ARE HERE see Change Log<<<<

## 1. Problem Statement

As the GrantSeekerWeb visualization evolves, the UI state (especially checkbox selections) must remain robust, shareable, and recoverable—even as the underlying data model (e.g., Funders, Propositions) changes. The primary challenges are:
- **Stable state encoding:** Ensure users can share/bookmark precise UI states via URLs.
- **Data evolution resilience:** Adding, removing, or reordering records (e.g., new Funders) must not break saved URLs or user workflows.
- **Recovery:** If record IDs change (e.g., due to data migration), there must be a basis for reconstructing or diagnosing lost state.

---

## 2. Approach

### 2.1. URL-Driven UI State
- Each checkbox is assigned [by what? the generate_visualzation script??] a unique, stable identifier (the record’s ID).
- The URL encodes the state of each checkbox by its ID, e.g. `?checked=recA,recB,recC`.
- Special-case checkboxes (e.g., "AllPropositions") use reserved IDs.
- **NOTE:** With current Airtable record IDs (17 chars each), browser compatibility limits us to about 110 checked boxes before the URL becomes too long (2,000 chars). If the number of selectable items grows, we will need to implement a more compact encoding or server-side state. This is not urgent, but should be revisited if the project/funder count approaches this limit.

### 2.2. Embedded RECORD_NAME_ID Mapping
- Every generated HTML file includes, in an informational HTML comment or `<script type="application/json">`, a mapping of `{Record Name: Record ID}` for all checkboxes.
- This snapshot enables future diagnostics and potential recovery if IDs change or records are renamed.

---

## 3. Architecture Overview

- **HTML Generation:**
  - During generation, each checkbox is assigned an `id` and/or `name` attribute equal to its record ID.
  - The mapping `{Record Name: Record ID}` is embedded in the HTML output.

- **JavaScript Logic:**
  - On load: Parse URL, check/uncheck boxes with those IDs.
  - On change: Update URL to reflect the current checked IDs.
  - If a record ID is missing, the embedded mapping can be referenced for diagnostics or future recovery.

- **Special Cases:**
  - “AllPropositions” and “AllFunder” checkboxes use reserved IDs and are handled separately in logic.

---

## 3. Potential Risks & Rat-Holes

### a. ID Instability
**Risk:** If record IDs are not truly stable (e.g., due to data migration, export/import, or switching data sources), URLs and saved states break, and even the embedded mapping may become obsolete.
**Mitigation:**
- Document the requirement for stable IDs in all data pipelines.
- Make the system fail "loudly" (clear diagnostics in UI if an ID is missing).
- The embedded mapping is a diagnostic tool, not a guarantee of recovery.

### b. Name Collisions & Renames
**Risk:** If two records share a name, or if names change, recovery logic (should it ever be implemented) can mis-map or fail.
**Mitigation:**
- Warn in the UI if duplicate names are detected in the mapping.
- Encourage unique, human-meaningful names in the data model.
- For now, recovery is out of scope—diagnostics only.

### c. Canonical HTML & Automated Testing
**Risk:** The “canonical” HTML file or test script may become outdated or not reflect true user experience, leading to false positives/negatives in validation.
**Mitigation:**
- Keep the canonical HTML file fixed for as long as the UI contract is meant to hold. Only update the canonical file after explicit, reviewed, and documented approval of a new UI/UX contract.
- Ensure the test script is simple, transparent, and easy to update.
- Periodically review the canonical/test process as the project evolves.

### d. Incremental Change & Rollback
**Risk:** An incremental change could break functionality in subtle ways (e.g., interactivity, edge-case data) that aren’t caught by the test script.
**Mitigation:**
- Require explicit, manual validation (checkboxes, visualization, interactivity) after each increment.
- Use git for atomic commits and easy rollback.
- Encourage “small, reversible steps” and avoid large, multi-file changes in a single commit.

### e. URL Length/Complexity
**Risk:** For very large datasets, URLs encoding all checkbox states could become unwieldy.
**Mitigation:**
- For now, this is a theoretical risk—monitor as the dataset grows.
- If needed, consider compression or session-based approaches in the future.

---

## 4. General Principles to Avoid Pitfalls
- **Fail Early, Fail Loudly:** Don’t silently ignore mismatches or missing data—surface them clearly to the user/developer.
- **Minimal, Transparent Automation:** Automated scripts for validation should be simple and their results easy to interpret. Avoid “magic” or black-box tooling.
- **Human-Readable Diagnostics:** Embedded mappings and test logs should be easy for a human to inspect and reason about.
- **Documentation & Process Discipline:**
  - Make it clear how to update the canonical HTML and test scripts.
  - Document what constitutes a “breaking change” and the rollback procedure.
- **Consultative, Incremental Workflow:**
  - Each step is reviewed and validated before proceeding.
  - Always be able to revert to the last known good state.

---

## 5. Summary Table: Failure Modes & Defenses

| Risk                    | Defense/Process                                 |
|-------------------------|-------------------------------------------------|
| ID instability          | Diagnostics, loud failure, documentation        |
| Name collisions/renames | Warn if detected, human review                  |
| Outdated canonical HTML | Fixed canonical, explicit review for update     |
| Subtle breakages        | Manual validation, atomic commits, rollback     |
| URL complexity          | Monitor, defer optimization                     |

---

## 6. Final Thoughts Before Implementation
- The plan is robust if we treat the embedded mapping as a diagnostic aid, not a recovery guarantee.
- The incremental, test-driven approach with manual checkpoints and easy rollback is the best defense against rat-holes and catastrophic failures.
- The most likely source of subtle breakage is in UI interactivity—manual review and clear rollback will be essential.
- The approach is extensible and will not “paint us into a corner” as long as we maintain discipline around IDs and canonical files.

---

## 7. Incremental Implementation Plan

### Step 1: Baseline Validation
- Confirm current visualization functionality: checkbox states, visualization, interactivity.
- Ensure all existing checkboxes have unique, stable IDs (preferably record IDs).
- Commit the baseline for easy rollback.
- Save a canonical HTML file (the "golden master") after explicit, reviewed, and documented approval of a new UI/UX contract. This file must not be updated with each change; it is a regression-proof reference.
- Create a script to rapidly confirm that the relevant data (chart data, checkbox states, and interactivity) remain true to the canonical HTML file. The test utility must always compare to the original canonical file, never a silently updated version. Any detected change is a red flag for review, not an opportunity to update the canonical reference.

### Step 2: Embed RECORD_NAME_ID Mapping
- Modify the HTML generation process to include a `{Record Name: Record ID}` mapping in an HTML comment or JSON block.
- Regenerate the HTML and confirm:
  - Checkbox states remain unchanged
  - Visualization and interactivity are unaffected
- Commit changes if validated; rollback if any issues arise.

### Step 3: URL-Driven State (No Recovery Yet)
- Implement logic to encode/decode checkbox states in the URL using record IDs.
- Regenerate and test:
  - Bookmark/share URLs
  - Reloading restores state
  - No breakage of existing functionality
- Commit validated changes; rollback if needed.

### Step 4: Future Recovery Logic (Deferred)
- If record IDs ever change, use the embedded mapping for diagnostics or possible automated recovery.
- Document the process for diagnosing and (if possible) reconstructing lost state.

---

## 5. Methodology for Safe Iteration
- After each increment, validate:
  - Checkbox states
  - Visualization rendering
  - Interactivity (toggle, filter, etc.)
- Use git commits to secure each working state.
- If any increment breaks functionality, immediately rollback and diagnose before proceeding.

---

## 6. Ramifications and Considerations
- **Stability:** Robust to reordering, addition, or removal of records.
- **Diagnostics:** Embedded mapping provides a basis for troubleshooting if state recovery is needed.
- **Extensibility:** Easily supports new filters or toggles in the future.
- **Limitations:**
  - Name collisions or renamed/deleted records may complicate recovery.
  - URL length may grow with many checkboxes (rarely a practical issue).

---

## 7. Next Steps
- Review and iterate on this document.
- Once approved, proceed with Step 1 and validate before implementing further steps.
- **NEW:** Implement automated browser-based monitoring of JavaScript console errors during regression and pipeline runs.

### How to Bootstrap and Use Automated Console Error Checking
1. **Serve the visualization via a local HTTP server.**
    - Use `python3 -m http.server 8000 --directory System/visualization/outputs` or similar.
2. **Launch the pipeline without the `--no-browser` option.**
    - Example: `python System/visualization/FreshVisualization.py`
    - This will open the output HTML in your default browser automatically.
3. **Ensure the Windsurf MCP browser extension is installed and active in your default browser.**
    - If not installed, request the extension from Windsurf/Cascade support and follow installation instructions.
    - After installation, pin it to your browser toolbar and connect the tab when prompted.
4. **Automated monitoring will check for:**
    - JavaScript errors, warnings (including library/CDN deprecations), and 404/network errors (e.g., missing favicon).
    - Any detected issues will be surfaced and reported during validation.
5. **If the extension is not available:**
    - Manually open the browser console (F12 or right-click > Inspect > Console) and review for errors/warnings after each run.
    - Report any issues to Cascade for further automation or troubleshooting.

    This process ensures robust, browser-based validation and regression safety for all HTML outputs.

---

## [JULY 2025] Technical Plan: Stable Checkbox IDs and Mapping Embedding (Recovery Anchor)

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
