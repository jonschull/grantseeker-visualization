"""
airtable_id_name_utils.py

Utility functions for mapping Airtable record IDs to human-readable names using airtable_mapping.json.
"""
"""
airtable_id_name_utils.py

Utility functions for mapping Airtable record IDs to human-readable names using the tuple-keyed mapping from create_mapping_dict.py.

- Provides robust lookup and error logging if mapping is missing.
- Designed for SD4D/AI handoff: clear docstrings, explicit error handling.
"""
import json
import os
import logging

MAPPING_PATH = os.path.join(os.path.dirname(__file__), 'airtable_mapping.json')  # Local for kit portability

def load_airtable_mapping(mapping_path=MAPPING_PATH):
    """
    Load the Airtable ID-to-name mapping from JSON, converting string keys to tuple keys.
    Returns: dict with tuple keys (table, field, value) or ('*', 'id', record_id)
    """
    with open(mapping_path, 'r', encoding='utf-8') as f:
        raw = json.load(f)
    mapping = {}
    for k, v in raw.items():
        if '|' in k:
            parts = k.split('|', 2)
            mapping[tuple(parts)] = v
        else:
            mapping[k] = v
    return mapping

def id_to_name(record_id, mapping, entity_type):
    """
    Convert an Airtable record ID to a human-readable name using the mapping.
    entity_type: 'funder' or 'proposition'
    Returns: name (str) if found, else record_id
    Logs a warning if mapping is missing.
    """
    key = ('*', 'id', record_id)
    name = mapping.get(key)
    if name is None:
        logging.warning(f"No mapping found for {entity_type} ID: {record_id}")
        return record_id
    return name

def ids_to_names(record_ids, mapping, entity_type):
    """
    Map a list of Airtable record IDs to names.
    Returns: list of names (or IDs if missing)
    """
    return [id_to_name(rid, mapping, entity_type) for rid in record_ids]
