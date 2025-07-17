from query_or_create_mapping_dict import load_mapping_from_file, lookup_id

mapping = load_mapping_from_file('airtable_mapping.json')

# --- 1. Get all Team names and IDs ---
team_names = set()
for key in mapping:
    if key[0] == 'Teams' and key[1] == 'Team Name':
        team_names.add(key[2])

# --- 2. For each Team, get Nickname, ID, and Proposition IDs ---
teams_data = []
for team_name in sorted(team_names):
    team_id = lookup_id(mapping, 'Teams', 'Team Name', team_name)
    nickname = mapping.get(('Teams', 'id', team_id), team_name)
    # Find all proposition IDs linked to this team
    prop_ids = [k[2] for k, v in mapping.items()
                if k[0] == 'Teams' and k[1] == 'Propositions' and v == team_id]
    teams_data.append({
        'name': team_name,
        'id': team_id,
        'nickname': nickname,
        'proposition_ids': prop_ids
    })

# --- 3. Get all Funder IDs ---
funder_ids = [v for k, v in mapping.items()
              if k[0] == 'Funders' and k[1] == "FUNDER'S NAME"]

def make_team_url(funder_ids, prop_ids):
    checked = ','.join(funder_ids + prop_ids)
    return f"?checked={checked}"

panel_html = '<div class="teams-panel" style="display:flex;gap:8px;margin-bottom:8px;">\n'
for team in teams_data:
    url = make_team_url(funder_ids, team['proposition_ids'])
    panel_html += f'<a href="{url}"><button>{team["nickname"]}</button></a>\n'
panel_html += '</div>'

print(panel_html)
