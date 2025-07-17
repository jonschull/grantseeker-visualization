# Current Milestone: Team Panel with Custom URLs

## Objective
Add a horizontally arrayed Teams panel above the visualization, with each team’s button linking to a custom URL that:
- Turns **all Funders ON**
- Turns **only that Team’s Propositions ON** (from the Teams table)
- Encodes this state in the `?checked=` parameter

Also:
- Hyperlink the words **Teams**, **Funders**, and **Propositions** in the UI to their Airtable tables.

## Technical Plan

1. **Data Extraction:**
   - Parse the Teams table for Nickname and Propositions.
   - Use canonical mapping utilities for Funder and Proposition IDs.
2. **URL Generation:**
   - For each team, generate a URL with all funders + only that team’s propositions checked.
3. **UI/HTML Modifications:**
   - Render a horizontal panel of team buttons above the plot.
   - Hyperlink “Teams”, “Funders”, and “Propositions” in the UI to their Airtable tables.
4. **Validation:**
   - Ensure each team button links to a visualization with the correct checkboxes checked.
   - Validate that table labels are hyperlinked and accessible.
5. **Documentation:**
   - Update this milestone and move previous milestones to `System/visualization/past_milestones.md`.

## Acceptance Criteria
- Each team button links to a visualization with the correct checkboxes checked.
- The Teams panel is visually integrated and accessible.
- Table labels are hyperlinked.
- Documentation and changelog are updated.

---

**See [`System/visualization/past_milestones.md`](System/visualization/past_milestones.md) for previous milestones and implementation details.**

- Treat the embedded mapping as a diagnostic tool, not a recovery guarantee.
- If in doubt, consult the latest milestone, changelog, and onboarding docs before proceeding.

---

This plan ensures robust, auditable, and reversible progress toward fully URL-driven, stateful checkbox architecture in GrantSeekerWeb. It is suitable for both human and AI onboarding, and should be updated with every significant process or architectural change.

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
