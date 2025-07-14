# Match Repair (Self-Sufficient Bundle)

## Purpose

This bundle is a portable, reference snapshot for **auditing, previewing, and repairing match evaluation data** between a legacy data source (JSON extracted from HTML) and Airtable. It is designed for:
- **Auditing**: Comparing canonical match scores with Airtable records to find discrepancies.
- **Previewing**: Safely previewing what changes would be made to Airtable before any updates.
- **Repairing**: Pushing validated updates to Airtable in a controlled, consultative, and fully documented way.
- **Extraction**: Optionally extracting and reviewing 'strength' data for further human curation.

This bundle enables safe, transparent, and reproducible repair of match data, and is suitable for AI or human handoff.

## Contents
- `csv2airtable4MatchData.py` — Main audit and update script for Airtable match evaluations.
- `extract_strength_lines.py` — Utility to extract and review 'strength' data from evaluation reports.
- `extracted_from_html.json` — Canonical match evaluation data source.
- `airtable_mapping.json` — Airtable mapping reference.
- `.env` — (You must provide your own Airtable API credentials.)
- `requirements.txt` — Python dependencies for this bundle.

## Usage
1. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
2. **Create `.env` file** (if not present):
   ```
   AIRTABLE_API_KEY=your_api_key_here
   AIRTABLE_BASE_ID=your_base_id_here
   MATCH_EVALUATIONS_TABLE_ID=your_table_id_here
   ```
3. **Run scripts as needed:**
   ```
   python csv2airtable4MatchData.py --update-preview --limit 10
   python extract_strength_lines.py > strength_lines.md
   ```

## Notes
- All scripts are self-contained and do not require modification of any files outside this directory.
- For documentation and best practices, see `one_right_way.md` in the parent directory.
- This directory is intended as a reference or handoff bundle. Do not edit the originals in `works_do_not_modify/`.
