import requests
import os
import json
import time

PINOT_CONTROLLER_URL = os.environ.get("PINOT_CONTROLLER_URL", "http://pinot-controller:9000")
TABLE_CONFIG_PATH = "schemas/user_metrics_realtime_table.json"

# Load the table config
with open(TABLE_CONFIG_PATH, "r") as f:
    table_config = json.load(f)

# Delete the table if it exists
table_name = table_config["tableName"]
resp = requests.delete(f"{PINOT_CONTROLLER_URL}/tables/{table_name}")
if resp.status_code == 200:
    print(f"✅ Deleted table '{table_name}' (if existed).")
else:
    print(f"ℹ️ Table '{table_name}' may not have existed or delete failed: {resp.text}")

# Wait for external view cleanup
external_view_url = f"{PINOT_CONTROLLER_URL}/v2/tables/{table_name}_REALTIME/externalview"
max_wait = 60  # seconds
interval = 5
waited = 0
while waited < max_wait:
    resp = requests.get(external_view_url)
    if resp.status_code == 404:
        print(f"✅ External view for '{table_name}_REALTIME' cleaned up.")
        break
    print(f"⏳ Waiting for external view cleanup...")
    time.sleep(interval)
    waited += interval
else:
    print(f"⚠️ External view for '{table_name}_REALTIME' still exists after {max_wait}s. Consider restarting Pinot servers.")

# Recreate the table
resp = requests.post(
    f"{PINOT_CONTROLLER_URL}/tables",
    headers={"Content-Type": "application/json"},
    data=json.dumps(table_config)
)
if resp.status_code == 200:
    print(f"✅ Table '{table_name}' created successfully.")
else:
    print(f"❌ Failed to create table: {resp.text}")
