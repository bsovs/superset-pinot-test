import os
import time
import requests

SUPERSET_URL = os.environ.get("SUPERSET_URL", "http://superset:8088")
PINOT_HOST = os.environ.get("PINOT_HOST", "pinot-controller")
PINOT_PORT = os.environ.get("PINOT_PORT", "9000")
ADMIN_USER = "admin"
ADMIN_PASS = "admin"

# Wait for Superset to be up
for _ in range(30):
    try:
        r = requests.get(f"{SUPERSET_URL}/health")
        if r.status_code == 200:
            break
    except Exception:
        pass
    time.sleep(2)

# Login to Superset
session = requests.Session()
login_resp = session.post(f"{SUPERSET_URL}/api/v1/security/login", json={
    "username": ADMIN_USER,
    "password": ADMIN_PASS,
    "provider": "db",
    "refresh": True
})
login_resp.raise_for_status()

# Extract JWT access token from login response
access_token = login_resp.json().get("access_token")
if not access_token:
    raise RuntimeError("No access_token found in Superset login response.")

# Fetch CSRF token with retries and debug output, using Authorization header
csrf_token = None
for attempt in range(10):
    csrf_headers = {"Authorization": f"Bearer {access_token}"}
    csrf_resp = session.get(f"{SUPERSET_URL}/api/v1/security/csrf_token/", headers=csrf_headers)
    print(f"CSRF token response: {csrf_resp.text}")
    csrf_token = csrf_resp.json().get("result") or csrf_resp.json().get("csrf_token")
    if csrf_token:
        break
    print("CSRF token is None, retrying...")
    time.sleep(2)
if not csrf_token:
    raise RuntimeError("Failed to fetch CSRF token from Superset API.")
session.cookies.set("csrf_token", csrf_token)
print(f"✅ Logged into Superset at {SUPERSET_URL} as {ADMIN_USER}")
headers = {
    "Content-Type": "application/json",
    "X-CSRFToken": csrf_token,
    "Authorization": f"Bearer {access_token}"
}

# Add Pinot database connection
db_payload = {
    "database_name": "Pinot",
    "sqlalchemy_uri": "pinot://pinot-broker:8099/",
    "expose_in_sqllab": True,
    "allow_run_async": True,
    "allow_dml": False,
    "allow_csv_upload": False
}
db_resp = session.post(f"{SUPERSET_URL}/api/v1/database/", json=db_payload, headers=headers)
db_resp.raise_for_status()
db_id = db_resp.json()["id"]

print(f"✅ Superset connected to Pinot at {PINOT_HOST}:{PINOT_PORT} using {db_id=}")

# Add Pinot table as dataset
dataset_payload = {
    "database": db_id,
    "schema": "default",  # Use empty schema for Pinot
    "table_name": "user_metrics"
}
dataset_resp = session.post(f"{SUPERSET_URL}/api/v1/dataset/", json=dataset_payload, headers=headers)
dataset_resp.raise_for_status()
print("✅ Superset Pinot connection and dataset created.")
