import requests
import time
import csv
from datetime import datetime, timezone

# Fictional example: replace only with a program-approved
# authentication endpoint and approved test accounts.

LOGIN_URL = "https://api.example.com/v1/auth/login"

APPROVED_TEST_USERS = [
    "researcher-test-01",
    "researcher-test-02",
    "researcher-test-03",
    "researcher-test-04",
]

CANDIDATE_PASSWORD = "YOUR_APPROVED_TEST_PASSWORD"

DELAY_SECONDS = 10
TIMEOUT = 10

# Explicit authorization confirmation
AUTHORIZED = False

def main():

    if not AUTHORIZED:
        raise SystemExit(
            "Set AUTHORIZED=True only after confirming "
            "the bug bounty rules permit this test."
        )

    if "api.example.com" in LOGIN_URL:
        raise SystemExit("Replace the fictional endpoint.")

    session = requests.Session()

    results = []

    for number, username in enumerate(
        APPROVED_TEST_USERS, start=1
    ):

        print(f"\nTesting approved account {number}")
        print("Username:", username)

        start = time.monotonic()

        try:
            response = session.post(
                LOGIN_URL,
                json={
                    "username": username,
                    "password": CANDIDATE_PASSWORD
                },
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "Authorized-Bug-Bounty-Assessment"
                },
                timeout=TIMEOUT,
                allow_redirects=False
            )

            elapsed = round(
                time.monotonic() - start, 3
            )

            result = {
                "timestamp": datetime.now(
                    timezone.utc
                ).isoformat(),
                "username": username,
                "status": response.status_code,
                "elapsed_seconds": elapsed,
                "retry_after": response.headers.get(
                    "Retry-After", ""
                )
            }

            results.append(result)

            print("HTTP:", response.status_code)
            print("Response time:", elapsed, "seconds")
            print("Retry-After:", result["retry_after"])

            if response.status_code == 429:
                print("Rate limit encountered. Stopping.")
                break

            if response.status_code in (200, 201):
                print("Authentication may have succeeded.")
                print("Stopping immediately.")
                break

            if response.status_code >= 500:
                print("Server error. Stopping.")
                break

        except requests.RequestException as error:
            print("Request failed:", error)
            break

        if number < len(APPROVED_TEST_USERS):
            time.sleep(DELAY_SECONDS)

    with open(
        "spray_assessment.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "timestamp",
                "username",
                "status",
                "elapsed_seconds",
                "retry_after"
            ]
        )

        writer.writeheader()
        writer.writerows(results)

    print("\nAssessment finished.")
    print("Results saved to spray_assessment.csv")


if __name__ == "__main__":
    main()
