"""
transform_to_visualization_schema.py

Transforms raw Airtable-derived match data (from match_data_sample.json) into the canonical visualization schema expected by legacy tools.
- Computes y_fit and x_urgency using the standardized jitter formula documented in BOOTSTRAP.md
- Preserves all original fields for traceability
- Outputs visualization_data.json in the same directory

Requirements:
- Python 3.x
- match_data_sample.json (produced by fetch_minimal_match_data.py)

Usage:
    python transform_to_visualization_schema.py

Output:
    visualization_data.json (in same directory)
"""
import json
import random
import os

def compute_coordinates(fit_score, urgency_score):
    """
    Computes y_fit and x_urgency using the standardized jitter formula.
    Args:
        fit_score (float|int|str): The fit score value
        urgency_score (float|int|str): The urgency score value
    Returns:
        tuple: (y_fit, x_urgency) as floats, or (None, None) if input invalid
    Side effects:
        None
    Dependencies:
        random.uniform
    """
    try:
        y_fit = float(fit_score) + random.uniform(-0.15, 0.15)
    except (TypeError, ValueError):
        y_fit = None
    try:
        x_urgency = float(urgency_score) + random.uniform(-0.15, 0.15)
    except (TypeError, ValueError):
        x_urgency = None
    return y_fit, x_urgency

def main():
    infile = os.path.join(os.path.dirname(__file__), 'match_data_sample.json')
    outfile = os.path.join(os.path.dirname(__file__), 'visualization_data.json')
    rel_infile = os.path.relpath(infile, os.getcwd())
    rel_outfile = os.path.relpath(outfile, os.getcwd())
    print(f"[INFO] Reading input from {rel_infile}")
    print(f"[INFO] Writing output to {rel_outfile}")
    if not os.path.exists(infile):
        raise FileNotFoundError(f"Input file {infile} not found.")
    with open(infile, 'r', encoding='utf-8') as f:
        data = json.load(f)
    output = []
    for rec in data:
        fit_score = rec.get('fit_score')
        urgency_score = rec.get('urgency_score')
        
        y_fit, x_urgency = compute_coordinates(fit_score, urgency_score)
        # Compose canonical visualization record
        output.append({
            'funder_name': rec.get('funder_name', ''),
            'proposition_name': rec.get('proposition_name', ''),
            'fit_score': fit_score,
            'urgency_score': urgency_score,
            'text_notes': rec.get('text_notes', ''),
            'record_id': rec.get('record_id', ''),
            'y_fit': y_fit,
            'x_urgency': x_urgency
        })
    with open(outfile, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    rel_outfile = os.path.relpath(outfile, os.getcwd())
    print(f"[INFO] Wrote {len(output)} records to {rel_outfile}")

if __name__ == '__main__':
    main()
