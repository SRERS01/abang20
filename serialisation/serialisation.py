import urllib.request
import json
import os

# Define a local or mock testing endpoint
TARGET_URL = "http://127.0.0"

# Best practice: Retrieve authentication tokens from environment variables
# rather than hardcoding them into the testing script.
AUTH_TOKEN = os.getenv("MOCK_TEST_TOKEN", "PLACEHOLDER_TOKEN_VALUE")

# Define the structured payload (Query and Variables)
# Following standard GraphQL specifications, complex arguments are typically
# passed via a 'variables' dictionary rather than inline strings.
payload_structure = {
    "query": """
    mutation ExecuteTransaction($app: String!, $quantity: Int!, $itemName: String!, $cost: CostInput!) {
        createTransaction(app: $app, quantity: $quantity, name: $itemName, cost: $cost) {
            status
            referenceId
        }
    }
    """,
    "variables": {
        "app": "DEFAULT_APP",
        "quantity": 1,
        "itemName": "Standard Test Item",
        "cost": {
            "value": "10.00",
            "currency": "USD"
        }
    }
}

# Serialize the payload data to standard JSON bytes
encoded_data = json.dumps(payload_structure).encode('utf-8')

# Construct the HTTP Request object
request_object = urllib.request.Request(TARGET_URL, data=encoded_data, method="POST")

# Set standard integration headers
request_object.add_header("Content-Type", "application/json")
request_object.add_header("User-Agent", "QA-Integration-Client/1.0")

# Apply the authorization credential using the format required by the target schema
request_object.add_header("Authorization", f"Bearer {AUTH_TOKEN}")

print(f"Sending test vector to local endpoint: {TARGET_URL}...")

try:
    # Execute the request with a strict connection timeout
    with urllib.request.urlopen(request_object, timeout=5) as response_stream:
        response_body = response_stream.read().decode('utf-8')
        print("\nExecution Response Status: 200 OK")
        print("Response Body Received:")
        print(response_body)

except urllib.error.HTTPError as http_error:
    print(f"\nServer responded with HTTP Error Code: {http_error.code}")
    try:
        error_details = http_error.read().decode('utf-8')
        print("Error Details:")
        print(error_details)
    except Exception:
        print("Could not read error body.")

except Exception as connection_exception:
    print(f"\nNetwork layer exception occurred: {connection_exception}")
