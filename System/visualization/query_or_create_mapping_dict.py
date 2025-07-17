"""
Query or create a comprehensive mapping dictionary of all Airtable records, including Teams.

The dictionary uses tuples of (Table, FieldName, Value) as keys and the record ID as the value.
This allows for efficient lookups in any direction.

Requirements:
- A .env file in the same directory with these variables:
  AIRTABLE_API_KEY=your_api_key_here
  AIRTABLE_BASE_ID=your_base_id_here

Example output:
    Creating Airtable mapping dictionary...
    Processing table: Funders
      - Processed 65 records
    Processing table: Propositions
      - Processed 8 records
    Processing table: MatchEvaluations
      - Processed 10 records
    Processing table: Teams
      - Processed X records
    Mapping saved to airtable_mapping.json
    Mapping contains N entries

    Example lookups:
    ID for funder 'The Nature Conservancy': recU735K8mkxXgcn8
    ID for proposition 'Panama Restoration Lab': rec62E9tEGDRbE90c
    ID for team 'EcoRestorers': rec1234567890ABCDE
"""
import os
import json
from pyairtable import Api
from dotenv import load_dotenv
from typing import Dict, Tuple, Any
import pathlib

# The .env file must be in the same directory as this script
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, '.env')
output_path = os.path.join(script_dir, 'airtable_mapping.json')

if not os.path.exists(env_path):
    print(f"Error: .env file not found at {env_path}")
    print("\nPlease create it with the following contents:")
    print("# Airtable API Configuration")
    print("AIRTABLE_API_KEY=your_api_key_here")
    print("AIRTABLE_BASE_ID=your_base_id_here\n")
    print("You can find your API key at: https://airtable.com/create/tokens")
    print("The Base ID can be found in your Airtable API documentation")
    exit(1)

# Load and verify environment variables
print(f"Loading environment from: {env_path}")
load_dotenv(env_path)

API_KEY = os.getenv('AIRTABLE_API_KEY')
BASE_ID = os.getenv('AIRTABLE_BASE_ID')

if not all([API_KEY, BASE_ID]):
    print("Error: Missing required environment variables in .env file")
    print(f"API_KEY: {'Set' if API_KEY else 'Not set'}")
    print(f"BASE_ID: {'Set' if BASE_ID else 'Not set'}")
    exit(1)

# Table configurations
TABLES = {
    'Funders': {
        'id': 'tblyu00PsUrnWZdnN',
        'name_field': "FUNDER'S NAME",
        'fields_to_index': ["FUNDER'S NAME", 'WEBSITE']
    },
    'Propositions': {
        'id': 'tblo9ANCn8pSVfWeJ',
        'name_field': 'Name',
        'fields_to_index': ['Name']
    },
    'MatchEvaluations': {
        'id': 'tblvolX79j3xJWMT7',
        'name_field': 'Name',
        'fields_to_index': ['Name']
    },
    'Teams': {
        'id': 'tbloSod3H2GToBB14',
        'name_field': 'Team Name',
        'fields_to_index': ['Team Name', 'Nickname', 'Propositions']
    }
}

def create_mapping_dictionary() -> Dict[Tuple[str, str, str], str]:
    """
    Create a mapping dictionary for all records in specified tables.
    Returns:
        Dict[Tuple[str, str, str], str]: A dictionary with (Table, FieldName, Value) as keys
                                         and record IDs as values.
    """
    mapping = {}
    api = Api(API_KEY)
    for table_name, config in TABLES.items():
        table_id = config['id']
        name_field = config['name_field']
        fields_to_index = config['fields_to_index']
        print(f"Processing table: {table_name}")
        table = api.table(BASE_ID, table_id)
        try:
            for record in table.all():
                record_id = record['id']
                fields = record.get('fields', {})
                # Add mapping for each field we want to index
                for field in fields_to_index:
                    if field in fields:
                        value = fields[field]
                        # Handle both single values and arrays of values
                        values = [value] if not isinstance(value, list) else value
                        for v in values:
                            if v:  # Only add non-empty values
                                # Special handling for Teams->Propositions: map using proposition ID, not name
                                if table_name == 'Teams' and field == 'Propositions':
                                    # The value is a proposition record ID; use it directly
                                    prop_id = str(v).strip()
                                    key = (table_name, field, prop_id)
                                    mapping[key] = record_id
                                    # Also add a reverse mapping for the record ID
                                    mapping[(table_name, 'id', record_id)] = v
                                else:
                                    key = (table_name, field, str(v).strip())
                                    mapping[key] = record_id
                                    # Also add a reverse mapping for the record ID
                                    mapping[(table_name, 'id', record_id)] = v
        except Exception as e:
            print(f"Error processing table {table_name}: {e}")
    return mapping

def save_mapping_to_file(mapping: Dict[Tuple[str, str, str], str], filename: str = 'airtable_mapping.json'):
    """
    Save the mapping dictionary to a JSON file.
    Args:
        mapping: The mapping dictionary to save.
        filename: The name of the output JSON file.
    """
    # Convert tuple keys to strings for JSON serialization
    mapping_serializable = {"|".join(key): value for key, value in mapping.items()}
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(mapping_serializable, f, indent=2)
    print(f"Mapping saved to {filename}")

def load_mapping_from_file(filename: str = 'airtable_mapping.json') -> Dict[Tuple[str, str, str], str]:
    """
    Load a mapping dictionary from a JSON file.
    Args:
        filename: The name of the input JSON file.
    Returns:
        Dict[Tuple[str, str, str], str]: The loaded mapping dictionary.
    """
    with open(filename, 'r', encoding='utf-8') as f:
        mapping_serializable = json.load(f)
    # Convert string keys back to tuples
    mapping = {tuple(key.split("|")): value for key, value in mapping_serializable.items()}
    return mapping

def lookup_id(mapping: Dict[Tuple[str, str, str], str], table: str, field: str, value: str):
    """
    Look up a record ID in the mapping dictionary.
    Args:
        mapping: The mapping dictionary.
        table: The table name.
        field: The field name.
        value: The field value to look up.
    Returns:
        str: The record ID if found, or None.
    """
    return mapping.get((table, field, str(value).strip()))

if __name__ == "__main__":
    # Create and save the mapping
    print("Creating Airtable mapping dictionary...")
    mapping = create_mapping_dictionary()
    # Save to file
    output_file = 'airtable_mapping.json'
    save_mapping_to_file(mapping, output_file)
    # Print some stats
    print(f"\nMapping contains {len(mapping)} entries")
    # Example usage
    print("\nExample lookups:")
    example_funder = "The Nature Conservancy"
    example_prop = "Panama Restoration Lab"
    funder_id = lookup_id(mapping, 'Funders', "FUNDER'S NAME", example_funder)
    prop_id = lookup_id(mapping, 'Propositions', 'Name', example_prop)
    print(f"ID for funder '{example_funder}': {funder_id}")
    print(f"ID for proposition '{example_prop}': {prop_id}")
    # Team example lookups
    example_team = "EcoRestorers"  # Replace with a real team name
    team_id = lookup_id(mapping, 'Teams', 'Team Name', example_team)
    print(f"ID for team '{example_team}': {team_id}")
    if team_id:
        team_nickname = mapping.get(('Teams', 'id', team_id))
        print(f"Nickname for team '{example_team}': {team_nickname}")
        # List propositions for this team (IDs)
        print(f"Propositions for team '{example_team}':")
        for key, value in mapping.items():
            if key[:2] == ('Teams', 'Propositions') and value == team_id:
                print(f"  - Proposition ID: {key[2]}")
