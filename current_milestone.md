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

### ✅ Milestone Complete: Robust Modular Checkbox–URL Sync

- All objectives for modular, robust checkbox–URL synchronization are complete.
- The implementation has been regression tested and validated with no errors.
- Documentation and changelog have been updated.
- System is ready for next milestone or handoff.


>>>WE ARE HERE see Change Log<<<<

## 1. Problem Statement

As the GrantSeekerWeb visualization evolves, the UI state (especially checkbox selections) must remain robust, shareable, and recoverable—even as the underlying data model (e.g., Funders, Propositions) changes. The primary challenges are:
- **Stable state encoding:** Ensure users can share/bookmark precise UI states via URLs.
- **Data evolution resilience:** Adding, removing, or reordering records (e.g., new Funders) must not break saved URLs or user workflows.
- **Recovery:** If record IDs change (e.g., due to data migration), there must be a basis for reconstructing or diagnosing lost state.

---

## 2. Approach

### 2.1. URL-Driven UI State
- Each checkbox is assigned a unique, stable identifier (the record’s ID).
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

## 7. Incremental Implementation Plan (2025-07-16)

This plan is designed for both human and AI collaborators. Follow each step incrementally, regression-test after every change, and document all achievements in the milestone changelog. Never update the golden master or merge changes without explicit review and approval.

### Step 1: Analyze and Map Current Logic
- Review all code (JS and Python) related to checkbox state, URL query parameters, and mapping embedding.
- Document where and how URL→checkbox and checkbox→URL sync is currently handled.
- Add debug logging at all sync points.

### Step 2: Modularize and Isolate Sync Logic
- Refactor code to create explicit, callable functions for:
  - Setting checkboxes from URL (`setCheckboxesFromUrl()`)
  - Updating URL from current checkbox state (`updateUrlFromCheckboxes()`)
- Ensure these functions are available for both initial load and manual testing.

### Step 3: Robust Edge Case Handling
- In `setCheckboxesFromUrl()`, handle malformed, missing, or obsolete IDs gracefully (log, warn, never crash).
- Ensure all checkboxes are assigned unique, stable IDs (record IDs) in the HTML.
- Validate that special-case toggles (e.g., "AllPropositions") are handled as reserved IDs.

### Step 4: Embed and Leverage Mapping
- Confirm the `{Record Name: Record ID}` mapping is embedded in the HTML output as a JSON block or comment.
- Reference this mapping in diagnostics and for future recovery scenarios.

### Step 5: Regression Test and Manual Validation
- After each code increment, run the regression test script to compare output to the canonical HTML file.
- Manually validate that:
  - Checkbox state is restored from the URL
  - Checkbox changes update the URL
  - Visualization and interactivity remain correct
  - No console errors or warnings appear
- Only update the golden master after explicit review and approval.

### Step 6: Document and Commit
- After each validated increment:
  - Commit with a clear message
  - Add an entry to `System/milestone_changelog.md` (include date, commit hash, and summary)
  - Update onboarding/README as needed to reflect any new process discipline or architectural decisions

### Step 7: Orientation for Bootstrapping AI/Human
- Always check for the canonical mapping file and use it for all ID-to-name and name-to-ID translations.
- Never bypass regression testing or changelog discipline.
- Treat the embedded mapping as a diagnostic tool, not a recovery guarantee.
- If in doubt, consult the latest milestone, changelog, and onboarding docs before proceeding.

---

This plan ensures robust, auditable, and reversible progress toward fully URL-driven, stateful checkbox architecture in GrantSeekerWeb. It is suitable for both human and AI onboarding, and should be updated with every significant process or architectural change.

---

## Stepwise, Cautious Refactoring and Validation Plan (Implementation Discipline)

### Step 1: Analysis and Baseline Validation
- Ensure the current system is stable, and document the exact places where checkbox/URL sync logic occurs.
- Map all code locations (functions, event handlers) that (a) set checkbox state from the URL, and (b) update the URL from checkbox state.
- Note any duplication, tight coupling, or edge cases.
- Run regression tests and perform a manual sanity check in the browser.
- If any instability or ambiguity is found, pause and clarify before proceeding.

### Step 2: Introduce `setCheckboxesFromUrl()` as a Non-Disruptive Utility
- Add a new function that parses the URL and sets checkbox states, but do **not** yet change any existing logic or event handlers.
- Add debug logging at entry/exit and for any edge cases (missing or obsolete IDs).
- Expose the function on `window` for manual/console testing.
- Manually call the function from the browser console with various URLs and confirm it works as intended.
- Run regression tests to ensure no breakage.
- If any issues arise, revert the function and re-analyze.

### Step 3: Introduce `updateUrlFromCheckboxes()` as a Non-Disruptive Utility
- Add a new function that collects checked IDs and updates the URL, but do **not** yet replace inline logic.
- Add debug logging at entry/exit.
- Expose on `window` for manual/console testing.
- Manually call the function and confirm the URL updates as expected.
- Run regression tests.
- If any issues arise, revert and re-analyze.

### Step 4: Replace a Single Inline Usage with Modular Function
- Replace only one inline instance (e.g., in an individual checkbox event handler) with a call to `updateUrlFromCheckboxes()`.
- Make the minimal change.
- Validate manually and via regression test.
- If stable, proceed to next event handler; if not, revert and investigate.

### Step 5: Gradually Replace All Inline Usages
- Replace all remaining inline URL update logic with the modular function, one handler at a time.
- After each replacement, validate and review as above.
- Only proceed if each step is stable and passes all tests.

### Step 6: Integrate `setCheckboxesFromUrl()` into Initialization
- Use the new function for URL→checkbox sync at page load.
- Call `setCheckboxesFromUrl()` on initial load, replacing or supplementing current logic.
- Validate and review.
- If any breakage, revert and re-analyze.

### Step 7: Final Validation and Documentation
- Ensure all sync logic is modular, robust, and well-documented.
- Run full regression and manual tests.
- Update documentation and changelog.
- Pause for explicit review before merging or updating the golden master.

---

This discipline ensures that each refactoring step is validated, reversible, and non-disruptive, supporting both robust engineering and safe AI/human handoff.

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
