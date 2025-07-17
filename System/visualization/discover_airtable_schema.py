import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.environ.get("AIRTABLE_API_KEY")
BASE_ID = os.environ.get("AIRTABLE_BASE_ID")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Airtable Metadata API endpoint
url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables"

response = requests.get(url, headers=headers)
if response.status_code == 200:
    data = response.json()
    for table in data.get('tables', []):
        print(f"Table: {table['name']} (id: {table['id']})")
        for field in table.get('fields', []):
            print(f"  - Field: {field['name']} (type: {field['type']})")
        print()
else:
    print(f"Error: {response.status_code} - {response.text}")
