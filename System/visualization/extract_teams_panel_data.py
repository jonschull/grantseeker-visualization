import os
import json
import sys
from pyairtable import Api
from dotenv import load_dotenv
from airtable_id_name_utils import load_airtable_mapping, id_to_name

# Load environment
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    print(f"ERROR: .env file not found at {env_path}")
    sys.exit(1)

AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')
TEAMS_TABLE_ID = 'tbloSod3H2GToBB14'  # Confirm this is correct for your base

if not AIRTABLE_API_KEY or not AIRTABLE_BASE_ID:
    print("ERROR: Missing Airtable credentials in .env")
    sys.exit(1)

api = Api(AIRTABLE_API_KEY)
teams_table = api.table(AIRTABLE_BASE_ID, TEAMS_TABLE_ID)

# Load canonical mapping
mapping = load_airtable_mapping()

# Fetch all Teams
records = teams_table.all()
teams_data = []

for rec in records:
    team_id = rec['id']
    fields = rec.get('fields', {})
    team_name = fields.get('Team Name')
    nickname = fields.get('Nickname')
    proposition_ids = fields.get('Propositions', [])

    # Nickname error handling
    if not nickname:
        print(f"ERROR: Team '{team_name or team_id}' is missing a Nickname. Please fix in Airtable.")
        sys.exit(1)

    # Resolve proposition names
    proposition_names = [id_to_name(pid, mapping, 'proposition') for pid in proposition_ids]

        # Build URL: use 'all_funders' token + this team's proposition IDs
    checked_ids = ['all_funders'] + proposition_ids
    url = '?checked=' + ','.join(checked_ids) if checked_ids else ''

    team_obj = {
        'id': team_id,
        'name': team_name,
        'nickname': nickname,
        'proposition_ids': proposition_ids,
        'proposition_names': proposition_names,
        'url': url
    }
    teams_data.append(team_obj)

# Output JSON
json_path = os.path.join(os.path.dirname(__file__), 'teams_panel_data.json')
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(teams_data, f, indent=2, ensure_ascii=False)

print(f"Wrote {len(teams_data)} teams to {json_path}\n")
for team in teams_data:
    print(f"Team: {team['nickname']} | Propositions: {team['proposition_names']} | URL: {team['url']}")
