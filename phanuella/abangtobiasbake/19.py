import requests
import time
import csv
from itertools import cycle

# LOCAL LAB ONLY
TARGET = "http://127.0.0.1:5000/login"

# Test accounts created in server.py
USERNAMES = [
    "alice",
    "bob",
    "charlie",
    "david"
]

# One known lab password for controlled testing
TEST_PASSWORD = "LabPassword123!"

# Reserved documentation addresses.
# These simulate source identities only.
SIMULATED_IPS = [
    "192.0.2.10",
    "192.0.2.11",
    "198.51.100.20",
    "203.0.113.30"
]

DELAY_SECONDS = 3
MAX_ATTEMPTS = 4
OUTPUT_FILE = "lab_results.csv"


def verify_local_target():
    allowed = (
        TARGET.startswith("http://127.0.0.1:")
        or TARGET.startswith("http://localhost:")
    )

    if not allowed:
        raise SystemExit(
            "Safety stop: this script only permits localhost."
        )


def test_login(session, username, simulated_ip):
    headers = {
        "Content-Type": "application/json",
        "X-Lab-Source-IP": simulated_ip
    }

    payload = {
        "username": username,
        "password": TEST_PASSWORD
    }

    try:
        response = session.post(
            TARGET,
            json=payload,
            headers=headers,
            timeout=5
        )

        try:
            body = response.json()
        except ValueError:
            body = {"message": response.text[:200]}

        return {
            "username": username,
            "simulated_ip": simulated_ip,
            "http_status": response.status_code,
            "result": body.get("status", "unknown"),
            "message": body.get("message", body.get("reason", ""))
        }

    except requests.RequestException as error:
        return {
            "username": username,
            "simulated_ip": simulated_ip,
            "http_status": "ERROR",
            "result": "error",
            "message": str(error)
        }


def main():
    verify_local_target()

    ip_cycle = cycle(SIMULATED_IPS)
    results = []

    with requests.Session() as session:
        for index, username in enumerate(USERNAMES[:MAX_ATTEMPTS]):
            simulated_ip = next(ip_cycle)

            result = test_login(
                session,
                username,
                simulated_ip
            )

            results.append(result)

            print(
                f"{username:10} | "
                f"{simulated_ip:15} | "
                f"{result['http_status']} | "
                f"{result['result']}"
            )

            # Stop if the server reports a block.
            if result["http_status"] == 429:
                print("\nServer rate limit detected. Stopping.")
                break

            # Stop if an unexpected server error occurs.
            if isinstance(result["http_status"], int) and \
               result["http_status"] >= 500:
                print("\nServer error detected. Stopping.")
                break

            if index < MAX_ATTEMPTS - 1:
                time.sleep(DELAY_SECONDS)

    with open(OUTPUT_FILE, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "username",
                "simulated_ip",
                "http_status",
                "result",
                "message"
            ]
        )
        writer.writeheader()
        writer.writerows(results)

    print(f"\nResults saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
