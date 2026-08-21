import urllib.request
import json
import os

# Target destination pointing to your local development environment
TARGET_URL = "http://127.0.0"

# Retrieve a local testing token from your environment variables
AUTH_TOKEN = os.getenv("LOCAL_TEST_TOKEN", "MOCK_DEVELOPMENT_KEY")

# The testing payload deliberately includes a negative sign ("-100.00")
# to verify if the server's input-validation filters are working.
payload_structure = {
    "query": """
    mutation VerifyPriceValidation($app: String!, $quantity: Int!, $itemName: String!, $cost: CostInput!) {
        createTransaction(app: $app, quantity: $quantity, name: $itemName, cost: $cost) {
            status
            message
        }
    }
    """,
    "variables": {
        "app": "TEST_ENVIRONMENT",
        "quantity": 1,
        "itemName": "Validation Test Item",
        "cost": {
            "value": "-100.00",  # Test Vector: Negative financial parameter
            "currency": "USD"
        }
    }
}

# Serialize the payload into a network-ready byte stream
encoded_data = json.dumps(payload_structure).encode('utf-8')

# Construct the standard HTTP request wrapper
request_object = urllib.request.Request(TARGET_URL, data=encoded_data, method="POST")

# Set standard integration headers expected by local GraphQL frameworks
request_object.add_header("Content-Type", "application/json")
request_object.add_header("Authorization", f"Bearer {AUTH_TOKEN}")

print(f"📡 Sending validation test vector to local endpoint: {TARGET_URL}...")

try:
    with urllib.request.urlopen(request_object, timeout=5) as response_stream:
        response_body = response_stream.read().decode('utf-8')
        print("\n📥 Local Server Response (Connection Successful):")
        print(response_body)

except urllib.error.HTTPError as http_error:
    print(f"\n❌ Local Server returned HTTP Error Code: {http_error.code}")
    print("Error Details:", http_error.read().decode('utf-8'))

except Exception as connection_exception:
    print(f"\n❌ Local network layer exception: {connection_exception}")
    print("Ensure your local test server is running on port 8080.")
