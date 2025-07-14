"""
extract_strength_lines.py

Utility to extract lines mentioning 'strength' from the 'Evaluation Report' field of all Airtable Match Evaluation records.

Outputs a markdown table with:
- Record ID
- Record Name
- Funder ID
- Proposition ID
- Context line(s) containing 'strength' (case-insensitive)

This script is intended for rapid human review and cleanup of strength-related data.

Requirements:
- .env file with Airtable credentials
- pyairtable installed

Usage:
    python extract_strength_lines.py > strength_lines.md
"""
import os
import re
from pyairtable import Api
from dotenv import load_dotenv

def extract_strength_context(text, window=1):
    """
    Extracts lines containing the word 'strength' (case-insensitive) and a window of lines around it.
    Args:
        text (str): The text to search.
        window (int): Number of lines before/after to include for context.
    Returns:
        List[str]: List of context snippets (one per match).
    """
    lines = text.splitlines()
    matches = []
    for i, line in enumerate(lines):
        if 'strength' in line.lower():
            start = max(0, i - window)
            end = min(len(lines), i + window + 1)
            snippet = '\n'.join(lines[start:end]).strip()
            matches.append(snippet)
    return matches

def main():
    load_dotenv()
    AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
    AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')
    MATCH_EVALUATIONS_TABLE_ID = os.getenv('MATCH_EVALUATIONS_TABLE_ID')
    api = Api(AIRTABLE_API_KEY)
    table = api.table(AIRTABLE_BASE_ID, MATCH_EVALUATIONS_TABLE_ID)
    records = table.all()
    print('| Record ID | Name | Funder ID | Proposition ID | Strength Context |')
    print('|-----------|------|-----------|---------------|-----------------|')
    for rec in records:
        fields = rec.get('fields', {})
        record_id = rec.get('id', '')
        name = fields.get('Name', '')
        funders = fields.get('Funders', [''])
        props = fields.get('Propositions', [''])
        eval_report = fields.get('Evaluation Report', '')
        if not eval_report:
            continue
        contexts = extract_strength_context(eval_report, window=1)
        for snippet in contexts:
            # Escape pipe for markdown
            snippet_md = snippet.replace('|', '\|').replace('\n', '<br>')
            print(f'| {record_id} | {name} | {funders[0]} | {props[0]} | {snippet_md} |')

if __name__ == '__main__':
    main()
