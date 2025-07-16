# Visualization Golden Master Process

## Purpose
Maintain a canonical, reviewed HTML output (“Golden Master”) for the visualization system. This ensures UI/UX stability, enables safe incremental changes, and supports rapid rollback if regressions are detected.

## Directory Structure
- `golden_master/`: Stores the canonical HTML file (e.g., `opportunity_visualization_golden.html`)
- `outputs/`: Stores the latest generated HTML output
- `regression_tests/`: Contains scripts and logs for regression testing

## Workflow

1. **Freeze the Golden Master**
   - After manual validation, copy the current output HTML to `golden_master/opportunity_visualization_golden.html`.
   - Record the date, reason, and reviewer for this freeze in the commit message and/or a changelog section below.

2. **Make Incremental Changes**
   - Implement changes in small, reversible steps.
   - Generate a new output HTML as usual.

3. **Run Regression Test**
   - Use `regression_tests/compare_to_golden.py` to compare the new output to the Golden Master.
   - Review the human-readable diff report.
   - If differences are intentional and approved, update the Golden Master. Otherwise, investigate and fix regressions.

4. **Update the Golden Master**
   - Only after explicit review and documentation.
   - Update this document with a summary of what changed and why.

5. **Rollback**
   - If regressions are detected, revert to the last known good Golden Master and associated code.

## Changelog

| Date       | Author     | Description of Change               | Reviewer         |
|------------|------------|-------------------------------------|------------------|
| YYYY-MM-DD | <name>     | Initial freeze of Golden Master     | <reviewer name>  |
| ...        |            |                                     |                  |

---

## Principles

- **Self-Containment:** All artifacts and documentation are within `System/visualization/`.
- **Manual Validation:** Each change is reviewed before updating the Golden Master.
- **Transparency:** All changes and reviews are documented.
- **Atomicity:** Use git for small, reversible commits.
