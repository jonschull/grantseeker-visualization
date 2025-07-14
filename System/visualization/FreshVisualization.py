"""
FreshVisualization.py

Orchestrates the complete Airtable-to-Visualization pipeline in a single command, following the 'one right way' principle:

1. Regenerates the Airtable ID-to-name mapping (airtable_mapping.json) to ensure synchrony with the latest Airtable data.
2. Fetches match evaluation data from Airtable and writes minimal, canonical JSON for downstream use.
3. Transforms the raw data into the visualization schema, computing all derived fields.
4. Generates the interactive HTML visualization from the transformed data.

This script ensures:
- All intermediate and output files are co-located in the canonical scripts directory.
- Each step is auditable and prints explicit progress and error diagnostics.
- Designed for robust, traceable, and maintainable operation, suitable for AI or human handoff.

Usage:
    python FreshVisualization.py

Dependencies:
- Python 3.x
- All environment variables required by fetch_match_data.py (see that script)
- Scripts: fetch_match_data.py, transform_to_visualization_schema.py, generate_visualization.py must be present in the same or referenced directory

Outputs:
- match_data_sample.json
- visualization_data.json
- opportunity_visualization.html

Assumptions:
- All scripts in this kit use only local, relative paths for all file reads/writes, ensuring full portability and handoff.

See also:
- Visualization_from_airtable.md (system-level documentation)
- Each utility script's docstring for details
"""

import subprocess
import sys
import os
import argparse
import webbrowser

def run_step(description, command, cwd):
    """
    Runs a shell command as a pipeline step, printing progress and error diagnostics.
    Args:
        description (str): Human-readable step description
        command (list): Command to run as subprocess (e.g., ["python", "script.py"])
        cwd (str): Directory in which to run the command
    Returns:
        int: Exit code of the subprocess
    Side effects:
        Prints progress and error diagnostics
    Dependencies:
        subprocess, sys
    """
    print(f"[FreshVisualization] Starting: {description}")
    try:
        result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(result.stderr, file=sys.stderr)
            print(f"[FreshVisualization] ERROR: Step failed: {description}", file=sys.stderr)
            sys.exit(result.returncode)
        print(f"[FreshVisualization] Completed: {description}\n")
        return result.returncode
    except Exception as e:
        print(f"[FreshVisualization] EXCEPTION in {description}: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Orchestrate Airtable-to-Visualization pipeline.")
    parser.add_argument('--no-browser', action='store_true', help='Do not open the HTML output in a browser')
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Step 0: Regenerate mapping
    run_step(
        "Regenerate Airtable ID-to-name mapping (airtable_mapping.json)",
        [sys.executable, "create_mapping_dict.py"],
        cwd=script_dir
    )
    # Step 1: Fetch data
    run_step(
        "Fetch Airtable match data",
        [sys.executable, "fetch_match_data.py"],
        cwd=script_dir
    )
    # Step 2: Transform data
    run_step(
        "Transform to visualization schema",
        [sys.executable, "transform_to_visualization_schema.py"],
        cwd=script_dir
    )
    # Step 3: Generate visualization
    run_step(
        "Generate HTML visualization",
        [sys.executable, "generate_visualization.py"],
        cwd=script_dir
    )
    # Output HTML path (must match generate_visualization.py logic)
    output_html = os.path.join(script_dir, 'outputs', 'opportunity_visualization.html')
    rel_output_html = os.path.relpath(output_html, os.getcwd())
    print(f"[FreshVisualization] Pipeline complete. HTML output: {rel_output_html}")
    if not args.no_browser:
        print("[FreshVisualization] Opening HTML output in your default browser...")
        webbrowser.open(f'file://{output_html}')

if __name__ == "__main__":
    main()
