"""
Generates a single, self-contained HTML file for the interactive opportunity visualization.

This script reads a master HTML template, injects JSON data, and optionally
a team-specific view configuration to produce a final HTML file.

Workflow:
1.  Parses command-line arguments to check for a specific team context.
2.  Defines and resolves all necessary file paths.
3.  Reads the master data from `visualization_data.json`.
4.  Reads the HTML shell from `visualization_template.html`.
5.  If a `--team` is specified, it loads the team's `config.json` to determine
    which propositions and funders should be checked by default in the view.
6.  Creates a metadata object with the generation date and team name.
7.  Injects the data, view configuration, and metadata into the template.
8.  Writes the final, fully-formed HTML to the appropriate output directory
    (either the global `outputs/` or the team-specific `teams/<team_name>/outputs/`).

Usage:
- For a global report (all items checked by default):
  python scripts/generate_visualization.py

- For a team-specific report (team items checked by default):
  python scripts/generate_visualization.py --team <team_name>
"""
import json
import os
import argparse
from datetime import datetime
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from create_mapping_dict import load_mapping_from_file, lookup_id
from generate_teams_panel_html_from_json import generate_teams_panel_html_from_json

import subprocess
from datetime import timezone

# --- Teams Panel Generation ---
# def generate_teams_panel_html(mapping):
#     # [Legacy function removed in favor of standalone version. See generate_teams_panel_html_from_json.py]

def get_git_commit_hash():
    try:
        return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], cwd=os.path.dirname(os.path.abspath(__file__))).decode('utf-8').strip()
    except Exception:
        return 'unknown'

def get_file_mtime_iso(path):
    try:
        ts = os.path.getmtime(path)
        return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()
    except Exception:
        return 'unknown'

# --- Generate and log a reproducibility stamp ---
stamp = {
    'generation_date': datetime.now(timezone.utc).isoformat(),
    'code_version': get_git_commit_hash(),
    'mapping_version': None  # to be set after mapping_path is defined
}

# Will set mapping_version after mapping_path is known

# --- Argument Parsing ---
def parse_args():
    """Parses command-line arguments for the script."""
    parser = argparse.ArgumentParser(description='Generate an interactive opportunity visualization.')
    parser.add_argument('--team', type=str, help='The name of the team to generate a specific view for.')
    return parser.parse_args()

args = parse_args()

# --- Path Definitions ---
# Define file paths relative to the script's location for robustness.
script_dir = os.path.dirname(os.path.abspath(__file__))

# Paths relative to this script for portability
base_dir = script_dir
# Template is expected in the 'templates' subdirectory of the kit
template_path = os.path.join(base_dir, 'templates', 'visualization_template.html')
data_path = os.path.join(base_dir, 'visualization_data.json')
checkboxer_script_path = os.path.join(base_dir, 'checkboxer.js')
outputs_dir = os.path.join(base_dir, 'outputs')
os.makedirs(outputs_dir, exist_ok=True)

# Output path
if args.team:
    team_dir = os.path.join(base_dir, 'teams', args.team)
    team_outputs_dir = os.path.join(team_dir, 'outputs')
    os.makedirs(team_outputs_dir, exist_ok=True)
    output_path = os.path.join(team_outputs_dir, 'opportunity_visualization.html')
    config_path = os.path.join(team_dir, 'config.json')
else:
    output_path = os.path.join(outputs_dir, 'opportunity_visualization.html')

rel_template_path = os.path.relpath(template_path, os.getcwd())
rel_data_path = os.path.relpath(data_path, os.getcwd())
rel_checkboxer_path = os.path.relpath(checkboxer_script_path, os.getcwd())
rel_output_path = os.path.relpath(output_path, os.getcwd())
print(f"[INFO] Template path: {rel_template_path}")
print(f"[INFO] Data path: {rel_data_path}")
print(f"[INFO] Checkboxer path: {rel_checkboxer_path}")
print(f"[INFO] Output HTML: {rel_output_path}")

# --- Data and Template Loading ---
# Load the HTML template file into a string.
try:
    with open(template_path, 'r', encoding='utf-8') as f:
        template_string = f.read()
except FileNotFoundError:
    print(f"Error: Template file not found at {template_path}")
    exit()


# Load the main JSON data file.
try:
    with open(data_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
except FileNotFoundError:
    print(f"Error: Data file not found at {data_path}")
    exit()
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {data_path}")
    exit()

# --- Airtable Mapping Loading and Name-to-ID Dicts ---
# Set mapping_version in the stamp
stamp['mapping_version'] = get_file_mtime_iso(os.path.join(script_dir, 'airtable_mapping.json'))
print(f"[STAMP] {json.dumps(stamp, indent=2)}")

# Load the mapping from the canonical JSON file
mapping_path = os.path.join(script_dir, 'airtable_mapping.json')
try:
    mapping = load_mapping_from_file(mapping_path)
except Exception as e:
    print(f"Error loading mapping from {mapping_path}: {e}")
    mapping = None

# Build {name: id} for propositions and funders
proposition_name_to_id = {}
funder_name_to_id = {}
if mapping:
    # Get all unique proposition and funder names from data
    prop_names = sorted(list(set(item['proposition_name'] for item in json_data)))
    funder_names = sorted(list(set(item['funder_name'] for item in json_data)))
    for name in prop_names:
        rec_id = lookup_id(mapping, 'Propositions', 'Name', name)
        if rec_id:
            proposition_name_to_id[name] = rec_id
    for name in funder_names:
        rec_id = lookup_id(mapping, "Funders", "FUNDER'S NAME", name)
        if rec_id:
            funder_name_to_id[name] = rec_id
    # --- Inject Teams Panel HTML ---
    teams_panel_html = generate_teams_panel_html_from_json(os.path.join(script_dir, 'teams_panel_data.json'))
    # Insert panel above the plotly-div
    if '<!-- TEAMS_PANEL_PLACEHOLDER -->' in template_string:
        template_string = template_string.replace('<!-- TEAMS_PANEL_PLACEHOLDER -->', teams_panel_html)
    else:
        # Insert above the plotly-div
        template_string = template_string.replace('<div id="plotly-div"', teams_panel_html + '\n<div id="plotly-div"')
else:
    print("[WARN] No mapping loaded. Name-to-ID dicts will be empty.")

# Prepare JSON strings for embedding (not yet used in template)
proposition_name_to_id_json = json.dumps(proposition_name_to_id, indent=None)
funder_name_to_id_json = json.dumps(funder_name_to_id, indent=None)
# Next step: inject these into the template for use in checkbox generation.

# --- Team-Specific View Configuration ---
# If a team is specified, create a view configuration to pre-select items.
view_config = {}
if args.team:
    # Look for the config file in the visualization_original/teams directory
    team_config_path = os.path.abspath(os.path.join(script_dir, '..', 'teams', args.team, 'config.json'))
    try:
        # Load the team's configuration file.
        with open(team_config_path, 'r', encoding='utf-8') as f:
            team_config = json.load(f)

        # Get the list of propositions and funders for the team directly from the config
        team_propositions = team_config.get('propositions', [])
        team_funders = team_config.get('funders', [])

        # Get all unique propositions and funders from the data for the legend
        all_propositions = sorted(list(set(item['proposition_name'] for item in json_data)))
        all_funders = sorted(list(set(item['funder_name'] for item in json_data)))

        # Assemble the final view configuration object with proper initialization
        view_config = {
            'initial_propositions': team_propositions,
            'initial_funders': team_funders,  # Use the funders directly from config
            'all_propositions': all_propositions,
            'all_funders': all_funders
        }

    except FileNotFoundError:
        print(f"Warning: Config file for team '{args.team}' not found at {team_config_path}. Generating a global view.")
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON from {team_config_path}. Generating a global view.")

# --- Metadata Preparation ---
# Create a metadata object to inject into the template for dynamic titles.
metadata = {
    'team_name': args.team,
    'generation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
}

# --- Load Checkboxer Script ---
checkboxer_script_path = os.path.join(script_dir, 'checkboxer.js')
try:
    with open(checkboxer_script_path, 'r', encoding='utf-8') as f:
        checkboxer_script = f.read()
except FileNotFoundError:
    print(f"Warning: Checkboxer script not found at {checkboxer_script_path}")
    checkboxer_script = ""

# --- HTML Generation ---
# Convert the Python data structures to JSON strings for embedding in the HTML.
json_string_for_embedding = json.dumps(json_data, indent=None) # Compact representation
config_string_for_embedding = json.dumps(view_config, indent=None)
metadata_string_for_embedding = json.dumps(metadata)
checkboxer_script_escaped = json.dumps(checkboxer_script)  # Escape for JS embedding

# Replace the placeholders in the template with the prepared strings.
final_html = template_string.replace('{METADATA_PLACEHOLDER}', metadata_string_for_embedding)
# Prepare the metadata string for embedding
metadata_string_for_embedding = json.dumps(stamp, indent=None)
final_html = final_html.replace('{METADATA_PLACEHOLDER}', metadata_string_for_embedding)
final_html = final_html.replace('{CONFIG_PLACEHOLDER}', config_string_for_embedding)
final_html = final_html.replace('{DATA_PLACEHOLDER}', json_string_for_embedding)

# Inject name-to-id mappings as JS variables (for template use)
prop_id_js = f"<script>const propositionNameToId = {proposition_name_to_id_json}; const funderNameToId = {funder_name_to_id_json};</script>"
final_html = final_html.replace('// {NAME_TO_ID_PLACEHOLDER}', prop_id_js)

# Inject the checkboxer script content
script_tag = f'<script data-checkboxer>{checkboxer_script}</script>'
final_html = final_html.replace('<script data-checkboxer>\n        // The checkboxer script will be injected here\n    </script>', script_tag)

# --- File Output ---
# Write the final, fully-formed HTML string to the output file.
try:
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    rel_output_path = os.path.relpath(output_path, os.getcwd())
    print(f"Successfully generated {rel_output_path}")
except IOError as e:
    print(f"Error writing to output file {output_path}: {e}")
