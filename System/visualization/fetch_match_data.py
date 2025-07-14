"""
fetch_minimal_match_data.py

Extracts all Match Evaluation records from Airtable and outputs a minimal JSON for visualization pipeline development/testing.
- Uses proven pyairtable-based access pattern from extract_strength_lines.py
- Outputs all records (no limit) with key fields for downstream transformation
- Designed for SD4D/AI handoff: clear docstrings, explicit field mapping, robust error handling

Requirements:
- .env file with Airtable credentials
- pyairtable installed

Usage:
    python fetch_minimal_match_data.py

Output:
    match_data_sample.json (in same directory)
"""
import os
import json
from pyairtable import Api
from dotenv import load_dotenv
from airtable_id_name_utils import load_airtable_mapping, id_to_name

def get_field(fields, key, default=None):
    """Safely get a field from Airtable record fields dict."""
    val = fields.get(key, default)
    if isinstance(val, list) and val:
        return val[0]
    return val

def main():
    load_dotenv()
    AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
    AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')
    MATCH_EVALUATIONS_TABLE_ID = os.getenv('MATCH_EVALUATIONS_TABLE_ID')
    if not (AIRTABLE_API_KEY and AIRTABLE_BASE_ID and MATCH_EVALUATIONS_TABLE_ID):
        raise RuntimeError("Missing Airtable credentials or table IDs in .env file.")
    api = Api(AIRTABLE_API_KEY)
    table = api.table(AIRTABLE_BASE_ID, MATCH_EVALUATIONS_TABLE_ID)
    records = table.all()
    mapping = load_airtable_mapping()
    output = []
    for rec in records:
        fields = rec.get('fields', {})
        record_id = rec.get('id', '')
        # Get funder and proposition as IDs (first element if list)
        funder_id = get_field(fields, 'Funders') or get_field(fields, 'Funder Name') or ''
        proposition_id = get_field(fields, 'Propositions') or get_field(fields, 'Proposition Name') or ''
        if isinstance(funder_id, list):
            funder_id = funder_id[0] if funder_id else ''
        if isinstance(proposition_id, list):
            proposition_id = proposition_id[0] if proposition_id else ''
        funder_name = id_to_name(funder_id, mapping, 'funder')
        proposition_name = id_to_name(proposition_id, mapping, 'proposition')
        if funder_name == funder_id:
            print(f"[WARN] No mapping for funder_id: {funder_id}")
        if proposition_name == proposition_id:
            print(f"[WARN] No mapping for proposition_id: {proposition_id}")
        fit_score = get_field(fields, 'Fit Score') or get_field(fields, 'fit_score')
        urgency_score = get_field(fields, 'Urgency Score') or get_field(fields, 'urgency_score')
        
        text_notes = get_field(fields, 'Evaluation Report') or get_field(fields, 'Notes') or ''
        output.append({
            'record_id': record_id,
            'funder_id': funder_id,
            'funder_name': funder_name,
            'proposition_id': proposition_id,
            'proposition_name': proposition_name,
            'fit_score': fit_score,
            'urgency_score': urgency_score,
            'text_notes': text_notes
        })
    output_path = os.path.join(os.path.dirname(__file__), 'match_data_sample.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    rel_output_path = os.path.relpath(output_path, os.getcwd())
    print(f"[INFO] Wrote {len(output)} records to {rel_output_path}")

if __name__ == '__main__':
    main()
