"""
Create a comprehensive mapping dictionary of all Airtable records.

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
    
    Mapping saved to airtable_mapping.json
    
    Mapping contains 166 entries
    
    Example lookups:
    ID for funder 'The Nature Conservancy': recU735K8mkxXgcn8
    ID for proposition 'Panama Restoration Lab': rec62E9tEGDRbE90c
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
                                key = (table_name, field, str(v).strip())
                                mapping[key] = record_id
                                
                                # Also add a reverse mapping for the record ID
                                mapping[('*', 'id', record_id)] = v
            
            print(f"  - Processed {len(table.all())} records")
            
        except Exception as e:
            print(f"  - Error processing {table_name}: {str(e)}")
    
    return mapping

def save_mapping_to_file(mapping: Dict[Tuple[str, str, str], str], 
                        filename: str = 'airtable_mapping.json') -> None:
    """
    Save the mapping dictionary to a JSON file.
    
    Args:
        mapping: The mapping dictionary to save.
        filename: The name of the output JSON file.
    """
    # Convert tuple keys to strings for JSON serialization
    serializable = {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in mapping.items()}
    
    with open(filename, 'w') as f:
        json.dump(serializable, f, indent=2)
    
    print(f"\nMapping saved to {filename}")

def load_mapping_from_file(filename: str = 'airtable_mapping.json') -> Dict[Tuple[str, str, str], str]:
    """
    Load a mapping dictionary from a JSON file.
    
    Args:
        filename: The name of the input JSON file.
        
    Returns:
        Dict[Tuple[str, str, str], str]: The loaded mapping dictionary.
    """
    with open(filename, 'r') as f:
        serializable = json.load(f)
    
    # Convert string keys back to tuples
    return {tuple(k.split('|', 2)): v for k, v in serializable.items()}

def lookup_id(mapping: Dict[Tuple[str, str, str], str], 
             table: str, field: str, value: str) -> str:
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
    
    print(40*'-')
    print("\nDirect lookups:")
    funder_id = 'recU735K8mkxXgcn8'  # Example ID
    funder_name = mapping.get(('Funders', 'id', funder_id))
    print(f"Funder name for ID {funder_id}: {funder_name}")

    funder_name = "The Nature Conservancy"
    funder_id = mapping.get(('Funders', "FUNDER'S NAME", funder_name))
    if funder_id:
        print(f"\nPropositions for {funder_name}:")
        for key, value in mapping.items():
            if key[:2] == ('Propositions', 'Funder') and value == funder_id:
                prop_name = mapping.get(('Propositions', 'id', key[2]))
                print(f"  - {prop_name} (ID: {key[2]})")
