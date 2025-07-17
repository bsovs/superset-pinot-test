import requests
import json

PINOT_CONTROLLER_URL = "http://pinot-controller:9000"  # Change if needed

def upload_schema(schema_path):
    with open(schema_path, 'r') as f:
        schema = json.load(f)
    response = requests.post(
        f"{PINOT_CONTROLLER_URL}/schemas",
        headers={"Content-Type": "application/json"},
        data=json.dumps(schema),
    )
    if response.status_code == 200:
        print(f"✅ Schema '{schema.get('schemaName')}' uploaded successfully.")
    else:
        print(f"❌ Failed to upload schema: {response.text}")


def upload_table_config(table_config_path):
    with open(table_config_path, 'r') as f:
        table_config = json.load(f)
    response = requests.post(
        f"{PINOT_CONTROLLER_URL}/tables",
        headers={"Content-Type": "application/json"},
        data=json.dumps(table_config),
    )
    if response.status_code == 200:
        print(f"✅ Table '{table_config.get('tableName')}' uploaded successfully.")
    else:
        print(f"❌ Failed to upload table config: {response.text}")


if __name__ == "__main__":
    schema_file = "schemas/user_metrics.schema.json"
    table_config_file = "schemas/user_metrics_realtime_table.json"

    upload_schema(schema_file)
    upload_table_config(table_config_file)
