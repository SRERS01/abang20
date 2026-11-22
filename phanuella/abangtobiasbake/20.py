import requests
import time
import csv
from itertools import cycle
from urllib.parse import urlparse

# LOCAL LAB ONLY
TARGET = "http://127.0.0.1:5000/login"

USERNAMES = [
    "alice",
    "bob",
    "charlie",
    "david"
]

TEST_PASSWORD = "LabPassword123!"

SIMULATED_IPS = [
    "192.0.2.10",
    "192.0.2.11",
    "198.51.100.20",
    "203.0.113.30"
]

# Local proxy instances only
LOCAL_PROXIES = [
    "http://127.0.0.1:8081",
    "http://127.0.0.1:8082",
    "http://127.0.0.1:8083"
]

DELAY_SECONDS = 3
MAX_ATTEMPTS = 4
OUTPUT_FILE = "lab_results.csv"


def verify_local_target():
    parsed = urlparse(TARGET)

    if parsed.hostname not in ("127.0.0.1", "localhost"):
        raise SystemExit("Safety stop: target must be localhost.")

    for proxy in LOCAL_PROXIES:
        parsed_proxy = urlparse(proxy)

        if parsed_proxy.hostname not in ("127.0.0.1", "localhost"):
            raise SystemExit(
                "Safety stop: only localhost proxies are permitted."
            )


def test_login(username, simulated_ip, proxy):
    headers = {
        "Content-Type": "application/json",
        "X-Lab-Source-IP": simulated_ip
    }

    payload = {
        "username": username,
        "password": TEST_PASSWORD
    }

    proxies = {
        "http": proxy,
        "https": proxy
    }

    try:
        response = requests.post(
            TARGET,
            json=payload,
            headers=headers,
            proxies=proxies,
            timeout=5
        )

        try:
            body = response.json()
        except ValueError:
            body = {"message": response.text[:200]}

        return {
            "username": username,
            "simulated_ip": simulated_ip,
            "proxy": proxy,
            "http_status": response.status_code,
            "result": body.get("status", "unknown"),
            "message": body.get(
                "message",
                body.get("reason", "")
            )
        }

    except requests.RequestException as error:
        return {
            "username": username,
            "simulated_ip": simulated_ip,
            "proxy": proxy,
            "http_status": "ERROR",
            "result": "error",
            "message": str(error)
        }


def main():
    verify_local_target()

    ip_cycle = cycle(SIMULATED_IPS)
    proxy_cycle = cycle(LOCAL_PROXIES)

    results = []

    for index, username in enumerate(USERNAMES[:MAX_ATTEMPTS]):
        simulated_ip = next(ip_cycle)
        proxy = next(proxy_cycle)

        result = test_login(
            username,
            simulated_ip,
            proxy
        )

        results.append(result)

        print(
            f"User: {username:10} | "
            f"Proxy: {proxy:25} | "
            f"Status: {result['http_status']} | "
            f"Result: {result['result']}"
        )

        if result["http_status"] == 429:
            print("\nRate limit detected. Stopping.")
            break

        if (
            isinstance(result["http_status"], int)
            and result["http_status"] >= 500
        ):
            print("\nServer error detected. Stopping.")
            break

        if index < MAX_ATTEMPTS - 1:
            time.sleep(DELAY_SECONDS)

    with open(OUTPUT_FILE, "w", newline="") as file:
        fields = [
            "username",
            "simulated_ip",
            "proxy",
            "http_status",
            "result",
            "message"
        ]

        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

    print(f"\nResults saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
