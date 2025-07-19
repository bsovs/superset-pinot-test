import requests
import os
import json

PINOT_CONTROLLER_URL = os.environ.get("PINOT_CONTROLLER_URL", "http://pinot-controller:9000")
SCHEMA_PATH = "schemas/user_metrics.schema.json"

# Load the new schema
with open(SCHEMA_PATH, "r") as f:
    schema = json.load(f)

# Send a PUT request to update the schema
response = requests.put(
    f"{PINOT_CONTROLLER_URL}/schemas/{schema['schemaName']}",
    headers={"Content-Type": "application/json"},
    data=json.dumps(schema)
)

if response.status_code == 200:
    print(f"✅ Schema '{schema['schemaName']}' upgraded successfully.")
else:
    print(f"❌ Failed to upgrade schema: {response.text}")
