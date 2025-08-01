# GrantSeekerWeb: System Overview & Handoff Guide

**Architectural documentation is now located in `System/visualization/architecture/`.**
- See [`System/visualization/architecture/dataflow_theory_of_operation.md`](System/visualization/architecture/dataflow_theory_of_operation.md) for the canonical pipeline, dataflow, and artifact roles.
- See [`System/visualization/architecture/stateful_checkbox_architecture.md`](System/visualization/architecture/stateful_checkbox_architecture.md) for the authoritative visualization and checkbox/URL sync architecture.


Welcome to GrantSeekerWeb—the next-generation, web-based evolution of our grant-seeking analytics and visualization platform. This project is designed for robust, auditable, and seamless AI/human handoff, following SD4D and "one right way" principles.

---

## Project Mission
To create a robust, secure, and easy-to-use web system for managing and analyzing grant-seeking efforts, enabling us to strategically match our projects with the most suitable funding partners.

---

## Robust Checkbox–URL Synchronization

GrantSeekerWeb now features a robust, modular system for synchronizing checkbox states with URL query parameters in the visualization. This ensures:
- Users can share/bookmark precise UI states via URLs (`?checked=...`).
- Checkbox state is restored on load and reflected in the URL as selections change.
- The system is resilient to underlying data changes (IDs/names) and logs missing IDs for diagnostics.

**Key Implementation Details:**
- Modular JavaScript utility functions:  
  - `setCheckboxesFromUrl()` restores checkbox state from the URL.
  - `updateUrlFromCheckboxes()` updates the URL to reflect current checkbox state.
- Initialization order is enforced to prevent runtime errors (checkboxes and mappings must exist before state restoration).
- Extensive debug logging for traceability.
- Regression testing and manual validation required for all changes.

**Canonical Mapping Utilities:**
- All ID ↔ name translation uses `System/visualization/create_mapping_dict.py` and `System/visualization/airtable_mapping.json`.
- These utilities are the single source of truth for mapping and must be referenced in all future onboarding and documentation.

**See also:**
- [`System/visualization/stateful_checkbox_architecture.md`](System/visualization/stateful_checkbox_architecture.md) for the authoritative visualization architecture, rationale, and implementation notes for the stateful checkbox–URL sync system.
- `System/milestone_changelog.md` for project history.

---

## Browser-Based HTML Validation & Console Error Checking

Robust browser-based validation is required for all HTML outputs—across all workflows (not just visualization)—to ensure that JavaScript errors, warnings, and network issues are caught early and do not reach production.

**How to Use Automated Console Error Checking:**
1. **Serve your HTML via a local HTTP server.**
   - Example: `python3 -m http.server 8000 --directory System/visualization/outputs` (adjust directory as needed).
   - While serving via a local HTTP server is recommended for full-featured validation (and is required for some browser security features and the Windsurf MCP extension), it is not strictly mandatory for simple static HTML review. However, automated validation and MCP extension usage require a server context.
2. **Run the pipeline or open the HTML without suppressing browser launch.**
   - The output will open in your default browser automatically.
   - use `--no-browser`to suppress that default. 
   - Automated checking via the Windsurf MCP browser extension requires that the output HTML is opened in a browser session with the extension active. Suppressing the browser launch with `--no-browser` disables automated checking; for full automation, do not use `--no-browser`.
- 1. Validation-checking options for development and testing
    1. **To use Windsurf MCP browser extension, maks ure it is installed and active in your default browser.**
           - If not installed, request from Windsurf/Cascade support and follow installation instructions.
           - Pin it to your toolbar and click the extension's icon at the top to connect the current tab to the extension.
    3.1. **Automated monitoring will check for:**
        Automated monitoring occurs whenever the Windsurf MCP extension is active in your browser and connected to the session. It does not run if the extension is not installed or the tab is not connected.
       - JavaScript errors, warnings (including library/CDN deprecations), and 404/network errors.
       - Any detected issues will be surfaced and reported during validation.
3.2 **Humanvalidation If the extension is not available, not working, or not trustablbe:**
           - Manually open the browser console (F12 or right-click > Inspect > Console) and review for errors/warnings after each run.
           - Report any issues to Cascade for further automation or troubleshooting.

*Browser-based validation is mandatory for all HTML-facing deliverables and ensures regression safety across the system.*

**Clarification:** This refers to the process described above: serving HTML outputs via a local server, using browser tools (or the Windsurf MCP extension) to check for JavaScript and network errors, and validating that the UI behaves as expected before marking any deliverable complete.

---

## Milestone Documentation Practice

When a milestone is completed, its details are moved from `current_milestone.md` to `System/visualization/past_milestones.md` for historical reference and onboarding. This ensures that the current milestone file always contains only the active goal and plan, while past work is easily accessible for review and AI/human onboarding.

---

## Directory Structure

```
GrantSeekerWeb/
├── .env                # Environment variables for Airtable API access (copy or symlink, do not commit)
├── .gitignore          # Ignore caches, outputs, and local artifacts
├── meta/               # Working agreement, memory inventory, rationale, and architectural docs
├── System/                  # All active code, templates, outputs, and meta
│   ├── meta/                # Working agreement, memory inventory, rationale, and architectural docs
│   ├── templates/           # Shared HTML templates (e.g., visualization_template.html)
│   ├── outputs/             # Generated outputs and artifacts
│   ├── match_repair/        # Utilities for data repair and preprocessing
│   ├── visualization/       # Core Airtable-to-HTML visualization pipeline (actively maintained)
│   └── ...                  # Other current modules and scripts
├── architecture/            # High-level architectural documentation
├── current_milestone.md     # Current prioritized technical and process goals
├── Working_Agreement.md     # Team process and philosophy
├── one_right_way.md         # SD4D and "one right way" principles
└── README.md                # This file
```

---

## Visualization Pipeline (`System/visualization/`)

This directory contains the **actively maintained, canonical pipeline** for Airtable-to-HTML opportunity visualization. All scripts, mapping utilities, templates, and outputs are current and in use.  
See the Script Manifest below for a concise summary of each utility and its role in the workflow.

For full workflow details, see the docstrings in each script and the onboarding/bootstrapping notes above.

---

## Guidance for Human and AI Collaborators
- **SD4D/Consultative Approach:** All major changes require explicit approval. Never assume—always document rationale and workflow.  *Never* say "Let me..." and then begin.  Always say "Shall I..." and wait for assent.

- **Documentation as Code:** Every code/data contract change must be documented in the same commit.
- **AI/Human Handoff:** All code and docs are written for seamless transfer to new maintainers.
- **See:**
  - `meta/Working_Agreement.md` for our working philosophy
  - `meta/memory_inventory.md` for project context and rationale
  - `.bak` files for legacy onboarding and rationale

---

## Bootstrapping Note

**Canonical Mapping Utility:**
For all record ID ↔ name translations (funders and propositions), use `System/visualization/create_mapping_dict.py` and the generated `System/visualization/airtable_mapping.json`. This mapping is canonical for the project and must be referenced in all onboarding, bootstrapping, and AI/human handoff workflows. See the Script Manifest below for details.

For current and future technical milestones, see `/current_milestone.md`.

---

## Script Manifest: System/visualization/

Below is a concise manifest of all major scripts in `System/visualization/`. Paths are relative to the project root.

### **System/visualization/extract_teams_panel_data.py**
- **Purpose:** Fetches all Teams and their linked propositions directly from Airtable, and generates `teams_panel_data.json` with team metadata and pre-built Teams panel URLs (using the `all_funders` token).
- **Inputs:** `.env` (Airtable credentials), Airtable Teams table
- **Outputs:** `System/visualization/teams_panel_data.json`
- **Cmd-line:** `python System/visualization/extract_teams_panel_data.py`
- **Dependencies:** pyairtable, dotenv, airtable_id_name_utils.py

### **System/visualization/generate_teams_panel_html_from_json.py**
- **Purpose:** Reads `teams_panel_data.json` and generates the Teams panel HTML for injection into the visualization.
- **Inputs:** `System/visualization/teams_panel_data.json`
- **Outputs:** Teams panel HTML (embedded in the main HTML output)
- **Cmd-line:** Not typically run standalone; called by `generate_visualization.py`
- **Dependencies:** json

### **System/visualization/FreshVisualization.py**
- **Purpose:** Orchestrates the full Airtable-to-Visualization pipeline in one command; ensures all intermediate steps are reproducible and auditable.
- **Inputs:** `.env` (Airtable credentials), all scripts below
- **Outputs:** `match_data_sample.json`, `visualization_data.json`, `outputs/opportunity_visualization.html`
- **Cmd-line:** None (just run `python System/visualization/FreshVisualization.py`)
- **Dependencies:** Python 3.x, subprocess, fetch_match_data.py, transform_to_visualization_schema.py, generate_visualization.py

### **System/visualization/create_mapping_dict.py**
- **Purpose:** Generates and maintains the canonical mapping (`airtable_mapping.json`) between Airtable record IDs and human-readable names for funders and propositions.
- **Inputs:** `.env` (Airtable API credentials)
- **Outputs:** `System/visualization/airtable_mapping.json`
- **Cmd-line:** None (just run `python System/visualization/create_mapping_dict.py`)
- **Dependencies:** pyairtable, dotenv

### **System/visualization/airtable_id_name_utils.py**
- **Purpose:** Provides robust utility functions for mapping Airtable IDs to names (and vice versa) using the canonical mapping file.
- **Inputs:** `System/visualization/airtable_mapping.json`
- **Outputs:** None (library only)
- **Cmd-line:** Not intended for direct execution
- **Dependencies:** json, logging

### **System/visualization/fetch_match_data.py**
- **Purpose:** Extracts all Match Evaluation records from Airtable and outputs minimal JSON for downstream transformation.
- **Inputs:** `.env` (Airtable credentials), Airtable MatchEvaluations table
- **Outputs:** `System/visualization/match_data_sample.json`
- **Cmd-line:** `python System/visualization/fetch_match_data.py`
- **Dependencies:** pyairtable, dotenv, airtable_id_name_utils.py

### **System/visualization/transform_to_visualization_schema.py**
- **Purpose:** Transforms raw match data into the canonical visualization schema, computing derived fields for plotting.
- **Inputs:** `System/visualization/match_data_sample.json`
- **Outputs:** `System/visualization/visualization_data.json`
- **Cmd-line:** `python System/visualization/transform_to_visualization_schema.py`
- **Dependencies:** json, random

### **System/visualization/generate_visualization.py**
- **Purpose:** Generates the interactive HTML visualization by injecting JSON data and configuration into a master HTML template.
- **Inputs:** `System/visualization/visualization_data.json`, `System/visualization/templates/visualization_template.html`, (optional: team configs)
- **Teams Panel Integration:** When generating the main visualization, `generate_visualization.py` reads `teams_panel_data.json` (created from Airtable by `extract_teams_panel_data.py`). This JSON contains all Teams, their proposition links, and pre-built URLs using the special `all_funders` token. The script then calls `generate_teams_panel_html_from_json.py` to inject the Teams panel into the HTML. The output is `outputs/opportunity_visualization.html` (or team-specific outputs if using the `--team` flag).
- **Outputs:** `System/visualization/outputs/opportunity_visualization.html` (or team-specific outputs)
- **Cmd-line:**
    - Global: `python System/visualization/generate_visualization.py`
    - Team-specific: `python System/visualization/generate_visualization.py --team <team_name>`
- **Dependencies:** argparse, json, create_mapping_dict.py

### **Other Notable Files**
- **checkboxer.js:** JS for dynamic checkbox and URL sync in the visualization.
- **airtable_mapping.json:** Canonical mapping file (auto-generated; do not edit by hand).
- **templates/visualization_template.html:** Master HTML template for visualization rendering.

---

*For any ambiguity or questions, consult the working agreement or escalate in `meta/decisions_log.md`.*
