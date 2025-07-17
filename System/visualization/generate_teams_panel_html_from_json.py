"""
Standalone utility to generate the Teams panel HTML from teams_panel_data.json.

Usage (import or script):
    from generate_teams_panel_html_from_json import generate_teams_panel_html_from_json
    html = generate_teams_panel_html_from_json('teams_panel_data.json')

Or run as a script for quick output:
    python generate_teams_panel_html_from_json.py [teams_panel_data.json]
"""
import json
import os
import sys

def generate_teams_panel_html_from_json(json_path):
    """
    Generates the Teams panel HTML from the given JSON file.
    Args:
        json_path (str): Path to teams_panel_data.json
    Returns:
        str: HTML string for the Teams panel
    """
    # Airtable Teams table link (hardcoded per current system)
    teams_table_url = "https://airtable.com/tbloSod3H2GToBB14"
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"File not found: {json_path}")
    with open(json_path, 'r', encoding='utf-8') as f:
        teams = json.load(f)
    html = []
    html.append('<div class="teams-panel" style="display:flex;gap:8px;margin-bottom:8px;align-items:center;">')
    html.append(f'<a href="{teams_table_url}"><button style="font-weight:bold;"><u>Pre-configured Teams</u></button></a>')
    for team in teams:
        url = team.get('url', '#')
        nickname = team.get('nickname', '[No Nickname]')
        html.append(f'<a href="{url}"><button>{nickname}</button></a>')
    html.append('</div>')
    return '\n'.join(html)

# Optional: allow running as a script for quick testing
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_teams_panel_html_from_json.py [teams_panel_data.json]")
        sys.exit(1)
    json_path = sys.argv[1]
    html = generate_teams_panel_html_from_json(json_path)
    print(html)
