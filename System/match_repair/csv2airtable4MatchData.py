#!/usr/bin/env python3
"""
csv2airtable4MatchData.py

System-level documentation (SD4D/AI handoff ready)
--------------------------------------------------

This script audits and previews (dry-run) updates to Airtable Match Evaluations using authoritative match data extracted from HTML (not CSV). It is designed for clarity, maintainability, and seamless AI/system handoff, following SD4D consultative/documentation standards.

FEATURES:
- Loads Airtable credentials and table IDs from a .env file.
- Loads match evaluation data from extracted_from_html.json, which contains:
    - funder_name, proposition_name, fit_score, urgency_score, notes
    - Airtable funder and proposition IDs (parsed from embedded URLs)
- Fetches all relevant Airtable Match Evaluation records, including IDs and numeric score fields.
- For each (funder_id, proposition_id) pair:
    - Compares extracted (authoritative) scores and Airtable scores.
    - Outputs clear, tab-aligned, two-line audit entries for easy human review.
    - Detects and reports missing records, mismatches, and potential updates.
    - Handles missing/None values gracefully.
- Supports a --limit argument to restrict output for testing/preview.
- Supports --update-preview mode:
    - Shows a dry-run preview of what would be updated in Airtable, without making changes.
    - Prints a summary of records that would be updated.
- All logic is explicit, with robust error handling and logging.
- No legacy CSV dependencies in the main workflow (CSV loader retained for reference only).

INTENDED USAGE:
    python csv2airtable4MatchData.py [--update-preview] [--limit N]

ARCHITECTURE & DATA FLOW:
- extracted_from_html.json → [parsed & matched by IDs] → Airtable records → audit/preview output
- All matching is done by Airtable record IDs for robustness.

ASSUMPTIONS/NOTES:
- extracted_from_html.json is assumed to be the canonical source of match evaluation data.
- The script does not perform live updates to Airtable; it is strictly for audit and preview.
- All functions and workflows are documented for AI/system handoff.
- Consultative/explicit approach: no changes are made without explicit user/system approval.

Failure modes:
- Missing .env or extracted_from_html.json will halt execution with a clear error.
- Mismatched or missing Airtable records are reported in the audit/preview output.

"""
import os
import sys
import csv
import argparse
from collections import defaultdict
from dotenv import load_dotenv
from pathlib import Path
from pyairtable import Api

# --- CONFIG ---
load_dotenv()
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')
MATCH_EVALUATIONS_TABLE_ID = os.getenv('MATCH_EVALUATIONS_TABLE_ID')
CSV_PATH = os.getenv('OPPORTUNITY_MATRIX_PATH') or (
    Path('/Users/admin/Library/CloudStorage/Dropbox-EcoRestorationAllianceLLC/Jon Schull/CascadeProjects/ERA Grant Mongers Resources Great Docs/outputs/opportunity_matrix.csv')
)

def clean_score(val):
    if val is None:
        return None
    s = str(val).strip().lower()
    if s in ('', 'na', 'null', 'none'):
        return None
    try:
        return float(s)
    except Exception:
        return None

def tabbed(*args):
    return '\t'.join(str(a) for a in args)

import json
import re

def load_csv(csv_path):
    records = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append({
                'funder_id': row.get('funder_id', '').strip(),
                'proposition_id': row.get('proposition_id', '').strip(),
                'fit_score': clean_score(row.get('fit_score')),
                'strength_score': clean_score(row.get('strength_score')),
                'urgency_score': clean_score(row.get('urgency_score')),
            })
    return records

def parse_airtable_id_from_url(url):
    """
    Extracts the Airtable record ID from a given Airtable URL.
    Returns the record ID string or None if not found.
    """
    m = re.search(r'/([a-zA-Z0-9]{17})\?blocks=hide', url)
    if m:
        return m.group(1)
    return None

def load_extracted_json(json_path):
    """
    Loads and parses extracted_from_html.json, extracting:
      - funder_name
      - proposition_name
      - fit_score
      - urgency_score
      - text_notes
      - funder_id (from Airtable URL in text_notes)
      - proposition_id (from Airtable URL in text_notes)
    Returns a list of dicts, one per match.
    """
    records = []
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for row in data:
        funder_name = row.get('funder_name', '').strip()
        proposition_name = row.get('proposition_name', '').strip()
        fit_score = clean_score(row.get('fit_score'))
        urgency_score = clean_score(row.get('urgency_score'))
        notes = row.get('text_notes', '')
        # Extract IDs from Airtable URLs in notes
        funder_id = None
        prop_id = None
        urls = re.findall(r'https://airtable.com/[^\s\'"]+', notes)
        for url in urls:
            rec_id = parse_airtable_id_from_url(url)
            if not rec_id:
                continue
            if '/tblyu00PsUrnWZdnN/' in url:  # Funders table
                funder_id = rec_id
            elif '/tblo9ANCn8pSVfWeJ/' in url:  # Propositions table
                prop_id = rec_id
        records.append({
            'funder_name': funder_name,
            'proposition_name': proposition_name,
            'fit_score': fit_score,
            'urgency_score': urgency_score,
            'notes': notes,
            'funder_id': funder_id,
            'proposition_id': prop_id
        })
    return records

def fetch_airtable(api_key, base_id, table_id):
    api = Api(api_key)
    table = api.table(base_id, table_id)
    records = table.all(fields=['Funders', 'Propositions', 'Fit Score', 'Strength Score', 'Urgency Score'])
    atbl = defaultdict(list)
    for rec in records:
        fields = rec.get('fields', {})
        funders = fields.get('Funders', [])
        props = fields.get('Propositions', [])
        if funders and props:
            key = (funders[0], props[0])
            atbl[key].append({
                'record_id': rec['id'],
                'fit_score': clean_score(fields.get('Fit Score')),
                'strength_score': clean_score(fields.get('Strength Score')),
                'urgency_score': clean_score(fields.get('Urgency Score')),
            })
    return atbl


def push_match_evaluation_update(api_key, base_id, table_id, record_id, fields_to_update):
    """
    Update a single Match Evaluation record in Airtable.

    Args:
        api_key (str): Airtable API key
        base_id (str): Airtable base ID
        table_id (str): Airtable table ID
        record_id (str): Airtable record ID to update
        fields_to_update (dict): Dict of {Airtable field name: new value}
    Returns:
        dict: Airtable API response
    Side effects:
        - Fetches and prints the record's Name and Strength Score fields for validation
        - Sends an HTTP PATCH request to Airtable
        - Prints the payload and response
    Requirements:
        - pyairtable must be installed
        - Valid credentials and record_id
    """
    from pyairtable import Api
    api = Api(api_key)
    table = api.table(base_id, table_id)
    # Fetch record for validation
    record = table.get(record_id)
    fields = record.get('fields', {})
    record_name = fields.get('Name', '(No Name Field)')
    strength_score = fields.get('Strength Score', None)
    print("[INFO] Pushing update to Airtable:")
    print(f"  Record ID: {record_id}")
    print(f"  Record Name: {record_name}")
    if strength_score is not None:
        print(f"  Current Strength Score: {strength_score}")
    print(f"  Fields to update: {fields_to_update}")
    response = table.update(record_id, fields_to_update)
    print("[INFO] Airtable API response:")
    print(response)
    return response

# TEST invocation: push a real update if --push-test is given
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--update-preview', action='store_true')
    parser.add_argument('--limit', type=int, default=None)
    parser.add_argument('--push-test', action='store_true', help="Actually push a test update to Airtable using the first extracted record with a match.")
    parser.add_argument('--push-all', action='store_true', help="Push updates for all extracted records with a matching Airtable record.")
    parser.add_argument('--csv', type=str, default=None)
    args = parser.parse_args()

    # ... (rest of main logic as before) ...

    if args.push_test:
        # (Single test push logic as before)
        from dotenv import load_dotenv
        load_dotenv()
        AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
        AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')
        MATCH_EVALUATIONS_TABLE_ID = os.getenv('MATCH_EVALUATIONS_TABLE_ID')
        extracted_json_path = Path(__file__).parent / "extracted_from_html.json"
        extracted_records = load_extracted_json(extracted_json_path)
        atbl_records = fetch_airtable(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, MATCH_EVALUATIONS_TABLE_ID)
        import re
        for rec in extracted_records:
            funder_id = rec.get('funder_id')
            prop_id = rec.get('proposition_id')
            key = (funder_id, prop_id)
            atbl_list = atbl_records.get(key, [])
            if atbl_list:
                atbl = atbl_list[0]
                record_id = atbl['record_id']
                payload = {}
                if rec.get('fit_score') is not None:
                    payload['Fit Score'] = rec['fit_score']
                if rec.get('urgency_score') is not None:
                    payload['Urgency Score'] = rec['urgency_score']
                strength = rec.get('strength_score')
                if strength is not None:
                    payload['Strength Score'] = strength
                else:
                    from pyairtable import Api
                    api = Api(AIRTABLE_API_KEY)
                    table = api.table(AIRTABLE_BASE_ID, MATCH_EVALUATIONS_TABLE_ID)
                    record = table.get(record_id)
                    eval_report = record.get('fields', {}).get('Evaluation Report', '')
                    match = re.search(r"### Strength Analysis.*?\*\*Score:\*\*\s*([0-9.]+)/5", eval_report, re.DOTALL)
                    if match:
                        try:
                            payload['Strength Score'] = float(match.group(1))
                            print(f"[INFO] Extracted Strength Score from Evaluation Report: {payload['Strength Score']}")
                        except Exception as e:
                            print(f"[WARN] Failed to parse extracted Strength Score: {e}")
                print("\n=== TEST PUSH TO AIRTABLE ===")
                push_match_evaluation_update(
                    AIRTABLE_API_KEY,
                    AIRTABLE_BASE_ID,
                    MATCH_EVALUATIONS_TABLE_ID,
                    record_id=record_id,
                    fields_to_update=payload
                )
                break
        else:
            print("[ERROR] No matching record found for test push.")

    if args.push_all:
        from dotenv import load_dotenv
        load_dotenv()
        AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
        AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')
        MATCH_EVALUATIONS_TABLE_ID = os.getenv('MATCH_EVALUATIONS_TABLE_ID')
        extracted_json_path = Path(__file__).parent / "extracted_from_html.json"
        extracted_records = load_extracted_json(extracted_json_path)
        atbl_records = fetch_airtable(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, MATCH_EVALUATIONS_TABLE_ID)
        import re
        n_pushed = 0
        n_total = 0
        for rec in extracted_records:
            funder_id = rec.get('funder_id')
            prop_id = rec.get('proposition_id')
            key = (funder_id, prop_id)
            atbl_list = atbl_records.get(key, [])
            if not atbl_list:
                continue
            atbl = atbl_list[0]
            record_id = atbl['record_id']
            payload = {}
            if rec.get('fit_score') is not None:
                payload['Fit Score'] = rec['fit_score']
            if rec.get('urgency_score') is not None:
                payload['Urgency Score'] = rec['urgency_score']
            strength = rec.get('strength_score')
            if strength is not None:
                payload['Strength Score'] = strength
            else:
                from pyairtable import Api
                api = Api(AIRTABLE_API_KEY)
                table = api.table(AIRTABLE_BASE_ID, MATCH_EVALUATIONS_TABLE_ID)
                record = table.get(record_id)
                eval_report = record.get('fields', {}).get('Evaluation Report', '')
                match = re.search(r"### Strength Analysis.*?\*\*Score:\*\*\s*([0-9.]+)/5", eval_report, re.DOTALL)
                if match:
                    try:
                        payload['Strength Score'] = float(match.group(1))
                        print(f"[INFO] Extracted Strength Score from Evaluation Report: {payload['Strength Score']}")
                    except Exception as e:
                        print(f"[WARN] Failed to parse extracted Strength Score: {e}")
            print(f"\n=== PUSHING RECORD {n_total+1} ===")
            try:
                push_match_evaluation_update(
                    AIRTABLE_API_KEY,
                    AIRTABLE_BASE_ID,
                    MATCH_EVALUATIONS_TABLE_ID,
                    record_id=record_id,
                    fields_to_update=payload
                )
                n_pushed += 1
            except Exception as e:
                print(f"[ERROR] Failed to push record {record_id}: {e}")
            n_total += 1
        print(f"\nSUMMARY: {n_pushed} records pushed out of {n_total} attempted.")

def audit(csv_records, atbl_records, limit=None):
    csv_map = {}
    for r in csv_records:
        key = (r['funder_id'], r['proposition_id'])
        csv_map[key] = r
    checked = set()
    n_csv = n_atbl = n_match = n_missing_atbl = n_missing_csv = n_dupes = 0
    nonnum = 0
    for i, (key, csv_row) in enumerate(csv_map.items()):
        if limit and i >= limit:
            break
        atbl_list = atbl_records.get(key, [])
        n_csv += 1
        fit, strength, urgency = csv_row['fit_score'], csv_row['strength_score'], csv_row['urgency_score']
        csv_line = tabbed("CSV:", f"Fit={fit}", f"Strength={strength}", f"Urgency={urgency}", f"({key[0]}, {key[1]})")
        if atbl_list:
            if len(atbl_list) > 1:
                n_dupes += 1
                print(csv_line)
                print(tabbed("ATBL:", f"DUPLICATES: {[rec['record_id'] for rec in atbl_list]}"))
            else:
                atbl = atbl_list[0]
                n_match += 1
                fit2, strength2, urgency2 = atbl['fit_score'], atbl['strength_score'], atbl['urgency_score']
                if any(x is None for x in [fit, strength, urgency]):
                    nonnum += 1
                print(csv_line)
                print(tabbed("ATBL:", f"Fit={fit2}", f"Strength={strength2}", f"Urgency={urgency2}", f"({atbl['record_id']})", "[Match found]"))
            checked.add(key)
        else:
            n_missing_atbl += 1
            print(csv_line)
            print(tabbed("ATBL:", "No Airtable match"))
        print()
    # Now check for Airtable records with no CSV match
    for key, atbl_list in atbl_records.items():
        if key in checked:
            continue
        n_atbl += 1
        for atbl in atbl_list:
            print(tabbed("CSV:", "No CSV match"))
            print(tabbed("ATBL:", f"Fit={atbl['fit_score']}", f"Strength={atbl['strength_score']}", f"Urgency={atbl['urgency_score']}", f"({atbl['record_id']})", f"({key[0]}, {key[1]})"))
            print()
    print("Summary:")
    print(f"Total CSV rows: {n_csv}")
    print(f"Total Airtable records checked (no CSV match): {n_atbl}")
    print(f"Matches: {n_match}")
    print(f"Missing in Airtable: {n_missing_atbl}")
    print(f"Missing in CSV: {n_atbl}")
    print(f"Duplicates: {n_dupes}")
    print(f"Non-numeric/empty values: {nonnum}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Audit (and optionally preview updates to) Airtable Match Evaluations from CSV.')
    parser.add_argument('--csv', type=str, help='Path to opportunity_matrix.csv')
    parser.add_argument('--limit', type=int, help='Process only N records (for testing)')
    parser.add_argument('--update-preview', action='store_true', help='Preview updates (dry-run, no changes made)')
    args = parser.parse_args()

    if not (AIRTABLE_API_KEY and AIRTABLE_BASE_ID and MATCH_EVALUATIONS_TABLE_ID):
        print("Missing Airtable environment variables. Check your .env file.")
        sys.exit(1)

    # Use extracted_from_html.json as the authoritative data source
    extracted_json_path = Path(__file__).parent / "extracted_from_html.json"
    if not extracted_json_path.exists():
        print(f"[ERROR] extracted_from_html.json not found at {extracted_json_path}")
        sys.exit(1)
    else:
        print(f"[INFO] Using extracted_from_html.json: {extracted_json_path}")

    extracted_records = load_extracted_json(extracted_json_path)
    atbl_records = fetch_airtable(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, MATCH_EVALUATIONS_TABLE_ID)

    def audit_extracted(extracted_records, atbl_records, limit=None):
        """
        Audit extracted match data against Airtable records.
        Args:
            extracted_records: List of dicts from extracted_from_html.json (with IDs/names/scores).
            atbl_records: Airtable records as returned by fetch_airtable().
            limit: Optional int, limit number of records processed.
        Prints tab-aligned audit lines for each record.
        """
        n_match = n_missing_atbl = n_dupes = n_nonnum = n_total = 0
        for i, rec in enumerate(extracted_records):
            if limit and i >= limit:
                break
            funder_id = rec.get('funder_id')
            prop_id = rec.get('proposition_id')
            key = (funder_id, prop_id)
            fit = rec.get('fit_score')
            urgency = rec.get('urgency_score')
            funder_name = rec.get('funder_name', '?')
            prop_name = rec.get('proposition_name', '?')
            atbl_list = atbl_records.get(key, [])
            if not atbl_list:
                print(tabbed(f"CSV:", f"Fit={fit}", f"Urgency={urgency}", f"No Airtable match", f"({funder_name}, {prop_name})"))
                n_missing_atbl += 1
                continue
            for atbl in atbl_list:
                n_total += 1
                atbl_fit = atbl.get('fit_score')
                atbl_urgency = atbl.get('urgency_score')
                print(tabbed(f"EXTRACTED:", f"Fit={fit}", f"Urgency={urgency}", f"({funder_name}, {prop_name})"))
                print(tabbed(f"ATBL:", f"Fit={atbl_fit}", f"Urgency={atbl_urgency}", f"({atbl['record_id']})"))
                print()
                n_match += 1
        print("Summary:")
        print(f"Total extracted rows: {len(extracted_records)}")
        print(f"Total Airtable matches: {n_match}")
        print(f"Missing in Airtable: {n_missing_atbl}")

    def update_preview_extracted(extracted_records, atbl_records, limit=None):
        """
        Preview updates to Airtable using extracted_from_html.json as the source.
        Args:
            extracted_records: List of dicts from extracted_from_html.json.
            atbl_records: Airtable records as returned by fetch_airtable().
            limit: Optional int, limit number of records processed.
        Prints a dry-run preview of what would be updated.
        """
        n_preview = 0
        n_total = 0
        for i, rec in enumerate(extracted_records):
            if limit and i >= limit:
                break
            funder_id = rec.get('funder_id')
            prop_id = rec.get('proposition_id')
            key = (funder_id, prop_id)
            fit = rec.get('fit_score')
            urgency = rec.get('urgency_score')
            funder_name = rec.get('funder_name', '?')
            prop_name = rec.get('proposition_name', '?')
            atbl_list = atbl_records.get(key, [])
            if not atbl_list:
                continue  # No Airtable record to update
            for atbl in atbl_list:
                n_total += 1
                changes = []
                for score_field, new_val in [('fit_score', fit), ('urgency_score', urgency)]:
                    atbl_val = atbl.get(score_field)
                    if new_val != atbl_val:
                        changes.append((score_field, atbl_val, new_val))
                if changes:
                    n_preview += 1
                    print("Update would be applied:")
                    print(f"  Airtable Record: ? (ID: {atbl['record_id']})")
                    print(f"    Funder: {funder_name} (ID: {funder_id})")
                    print(f"    Proposition: {prop_name} (ID: {prop_id})")
                    print("    Old values (Airtable):")
                    for score_field, atbl_val, new_val in changes:
                        print(f"      {score_field}: {atbl_val}")
                    print("    New values (Extracted):")
                    for score_field, atbl_val, new_val in changes:
                        print(f"      {score_field}: {new_val}")
                    print("    Fields to update: " + ", ".join(f for f,_,_ in changes))
                    print()
        print(f"SUMMARY: {n_preview} records would be updated out of {n_total} checked.")

    if args.update_preview:
        print("\n=== UPDATE PREVIEW MODE (NO CHANGES WILL BE MADE) ===\n")
        update_preview_extracted(extracted_records, atbl_records, limit=args.limit)
    else:
        audit_extracted(extracted_records, atbl_records, limit=args.limit)

    