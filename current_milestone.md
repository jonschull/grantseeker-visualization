# Current Milestone: GrantSeekerWeb Migration and SD4D Alignment

## Key Objectives

- [x] **Transition to a Clean Web App Foundation**
- [x] **Dynamic Teams Filtering**
- [x] **SD4D and Handoff Alignment**

(See previous milestones and documentation for details on completed objectives.)


4. **Web App Planning**
   - Draft the architecture for a modern, maintainable web app (tech stack selection, UI/UX planning).
   - Plan for linking the ERA Grantseeker title to the Airtable base for direct data editing.
   - Establish robust, explicit guidelines for AI/human collaboration.

5. **Clean-Up and Documentation**
   - Remove all legacy/experimental files not needed for the web app milestone.
   - Update the README and meta docs to reflect the new structure and rationale.

---

## Immediate Next Steps
1. [x] **Publish `opportunity_visualization.html` to GitHub Pages**
    - Set up a public GitHub repository and enable GitHub Pages to host the current static visualization.
2. [x] **Automate the update process**
    - Create a workflow or script to automatically publish new versions of the visualization to the same GitHub Pages URL after each update.
3. Draft the architecture for a modern, maintainable web app (tech stack selection, UI/UX planning).
4. Prepare a plan for linking the ERA Grantseeker title to the Airtable base for direct data editing.
5. Establish robust, explicit guidelines for AI/human collaboration in the new web app context.
6. Present architecture and UI/UX sketches for your review and explicit approval before implementation.


---

## UI/UX and User Flow Sketch (Bootstrap Version)

### Main User Story
- A user lands on the homepage, sees a clear title (“ERA Grantseeker”), and is prompted to select one or more Teams.
- Upon selection, the app filters and displays matching Propositions and Funders (intersection logic).
- The user can click any record to view details, and (if permitted) follow a link to edit the Airtable record directly.

### UI Sketch (Textual Wireframe)

```
+-----------------------------------------------------+
| ERA Grantseeker                                     |
| [Airtable logo/link]                                |
+-----------------------------------------------------+
| Filter by Team: [Team 1] [Team 2] [Team 3] ...      |
|  (multi-select checkboxes, intersection logic)      |
+-----------------------------------------------------+
| [ Show Results ]                                    |
+-----------------------------------------------------+
| Results:                                            |
| --------------------------------------------------  |
| | Proposition | Funder | Team(s) | [Details] |      |
| --------------------------------------------------  |
| | ...         | ...    | ...     | [View]    |      |
| --------------------------------------------------  |
+-----------------------------------------------------+
| [Export/Download]   [Help]                          |
+-----------------------------------------------------+
```

- **Teams Filter:** Multi-select checkboxes (UNION logic).
- **Results:** There is no results "panel".  As is the case now, the graph and the checkboxes for Propositions and Funders should be updated.
- **Airtable Link:** App title or icon links directly to the Airtable base for editing (opens in new tab).
- **Minimal UI:** No unnecessary navigation or clutter.

- **Tri-state 'All' logic:** The 'All Teams', 'All Propositions', and 'All Funders' checkboxes all support an intermediate (indeterminate) state when only some items in their group are selected. This ensures users always have a clear visual cue about partial selections. See `System/visualization/checkboxer.js` for the authoritative source of this logic.

### User Flow (Stepwise)
1. **Landing:** User opens app → sees project title and Teams filter.
2. **Filter:** User adjusts filters selects one or more Teams (multi-select, intersection logic).
    1. The logic of the Team
3. **View Results:** Table updates to show only matches present in all selected teams. <this should be instantaneous and automatic when a filter cahnges, like now>
4. **Explore Details:** User clicks “View” on a row → sees details in a modal or panel.
<You've forgotten how are existing app works.  
Review the content o of the System of the Systme Folder.
5. **Edit in Airtable (if needed):** User clicks Airtable link (from title or details) → opens Airtable base in new tab for direct editing or exploration.

### Bootstrap-ability Notes
- All UI elements are simple, familiar, and require minimal explanation.
- No deep navigation or hidden features; everything is visible on the main screen.
- The codebase and UI are structured for easy handoff, with clear, inline comments (not verbose docs).
- “Help” links to a one-page quickstart or FAQ.
