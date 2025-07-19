import requests
import time
import os

# Wait for Pinot Controller to be up
PINOT_CONTROLLER_URL = os.environ.get("PINOT_CONTROLLER_URL", "http://pinot-controller:9000")
SCHEMA_PATH = "schemas/user_metrics.schema.json"
TABLE_CONFIG_PATH = "schemas/user_metrics_realtime_table.json"

for _ in range(30):
    try:
        r = requests.get(f"{PINOT_CONTROLLER_URL}/health")
        if r.status_code == 200:
            break
    except Exception:
        pass
    time.sleep(2)

# Upload schema
with open(SCHEMA_PATH, "r") as f:
    schema = f.read()
requests.post(f"{PINOT_CONTROLLER_URL}/schemas", headers={"Content-Type": "application/json"}, data=schema)

# Upload table config
with open(TABLE_CONFIG_PATH, "r") as f:
    table_config = f.read()
requests.post(f"{PINOT_CONTROLLER_URL}/tables", headers={"Content-Type": "application/json"}, data=table_config)

print("✅ Pinot schema and table config uploaded.")
