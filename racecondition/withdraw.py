import requests
import threading
import concurrent.futures
import time
import json
import csv
import hashlib
import uuid
import statistics

from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


# ==========================================
# CONFIGURATION
# ==========================================

URL = "http://127.0.0.1:8000/api/v1/withdrawal/process"

AUTH_TOKEN = "FAKE_TEST_TOKEN_123456"

WORKERS = 5
ROUNDS = 3
TIMEOUT = 10

OUTPUT_DIR = Path("race_audit_results")

HEADERS = {
    "User-Agent": "ResearchClient/2.0",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "X-Device-Fingerprint": "FAKE-FINGERPRINT-001",
    "X-Request-Source": "authorized-lab",
    "Origin": "http://127.0.0.1:8000",
    "Referer": "http://127.0.0.1:8000/test"
}

PAYLOAD = {
    "amount": 100,
    "account": "TEST-ACCOUNT-001",
    "operation": "TEST_WITHDRAWAL"
}


# ==========================================
# UTILITIES
# ==========================================

def utc_now():
    return datetime.now(timezone.utc).isoformat()


def fingerprint(body):
    encoded = json.dumps(
        body,
        sort_keys=True,
        default=str
    ).encode()

    return hashlib.sha256(encoded).hexdigest()


def extract_transaction_id(body):
    if not isinstance(body, dict):
        return None

    possible_keys = (
        "transactionId",
        "transaction_id",
        "reference",
        "referenceId"
    )

    for key in possible_keys:
        if body.get(key) is not None:
            return str(body[key])

    return None


# ==========================================
# REQUEST WORKER
# ==========================================

def send_request(index, barrier, round_number):

    request_id = str(uuid.uuid4())
    session = requests.Session()

    result = {
        "round": round_number,
        "worker": index,
        "request_id": request_id,
        "status": None,
        "error_type": None,
        "duration": None,
        "response_fingerprint": None,
        "transaction_id": None,
        "response_headers": None,
        "response_body": None,
        "timestamp": utc_now()
    }

    try:

        # Synchronize workers before sending
        barrier.wait(timeout=15)

        start = time.perf_counter()

        response = session.post(
            URL,
            headers={
                **HEADERS,
                "X-Test-Request-ID": request_id
            },
            json=PAYLOAD,
            timeout=TIMEOUT
        )

        duration = time.perf_counter() - start

        try:
            body = response.json()
        except ValueError:
            body = response.text[:2000]

        result.update({
            "status": response.status_code,
            "duration": round(duration, 6),
            "response_fingerprint": fingerprint(body),
            "transaction_id": extract_transaction_id(body),
            "response_headers": json.dumps(
                dict(response.headers)
            ),
            "response_body": json.dumps(
                body,
                default=str
            )
        })

        if 200 <= response.status_code < 300:
            result["error_type"] = "NONE"
        elif response.status_code >= 500:
            result["error_type"] = "SERVER_ERROR"
        else:
            result["error_type"] = "HTTP_ERROR"

    except requests.Timeout as error:
        result["status"] = "TIMEOUT"
        result["error_type"] = "TIMEOUT"
        result["response_body"] = str(error)

    except requests.ConnectionError as error:
        result["status"] = "CONNECTION_ERROR"
        result["error_type"] = "CONNECTION_ERROR"
        result["response_body"] = str(error)

    except threading.BrokenBarrierError as error:
        result["status"] = "BARRIER_ERROR"
        result["error_type"] = "BARRIER_ERROR"
        result["response_body"] = str(error)

    except requests.RequestException as error:
        result["status"] = "REQUEST_ERROR"
        result["error_type"] = "REQUEST_ERROR"
        result["response_body"] = str(error)

    except Exception as error:
        result["status"] = "UNEXPECTED_ERROR"
        result["error_type"] = "UNEXPECTED_ERROR"
        result["response_body"] = str(error)

    finally:
        session.close()

    return result


# ==========================================
# CONCURRENT ROUND
# ==========================================

def run_round(round_number):

    print(f"\nStarting round {round_number}")

    barrier = threading.Barrier(WORKERS)

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=WORKERS
    ) as executor:

        futures = [
            executor.submit(
                send_request,
                worker,
                barrier,
                round_number
            )
            for worker in range(1, WORKERS + 1)
        ]

        return [
            future.result()
            for future in futures
        ]


# ==========================================
# ANALYSIS
# ==========================================

def analyze(results):

    print("\n========== ROUND ANALYSIS ==========")

    if not results:
        print("No results to analyze.")
        return {}

    statuses = Counter(
        str(item["status"])
        for item in results
    )

    errors = Counter(
        str(item["error_type"])
        for item in results
    )

    response_groups = defaultdict(list)
    transaction_groups = defaultdict(list)

    for item in results:

        fingerprint_value = item["response_fingerprint"]

        if fingerprint_value:
            response_groups[fingerprint_value].append(
                item["request_id"]
            )

        transaction_id = item["transaction_id"]

        if transaction_id:
            transaction_groups[transaction_id].append(
                item["request_id"]
            )

    durations = [
        item["duration"]
        for item in results
        if item["duration"] is not None
    ]

    successful = sum(
        1 for item in results
        if isinstance(item["status"], int)
        and 200 <= item["status"] < 300
    )

    duplicate_transaction_ids = {
        transaction_id: request_ids
        for transaction_id, request_ids
        in transaction_groups.items()
        if len(request_ids) > 1
    }

    duplicate_response_groups = [
        request_ids
        for request_ids in response_groups.values()
        if len(request_ids) > 1
    ]

    report = {
        "total_requests": len(results),
        "successful_responses": successful,
        "status_distribution": dict(statuses),
        "error_distribution": dict(errors),
        "duplicate_response_groups": duplicate_response_groups,
        "duplicate_transaction_ids": duplicate_transaction_ids,
        "timing": {}
    }

    if durations:

        report["timing"] = {
            "fastest": min(durations),
            "slowest": max(durations),
            "average": statistics.mean(durations),
            "median": statistics.median(durations)
        }

    print("Status distribution:", dict(statuses))
    print("Error distribution:", dict(errors))
    print("Successful responses:", successful)

    print(
        "Identical response groups:",
        len(duplicate_response_groups)
    )

    print(
        "Repeated transaction IDs:",
        len(duplicate_transaction_ids)
    )

    if durations:
        print("Fastest:", min(durations))
        print("Slowest:", max(durations))
        print("Average:", statistics.mean(durations))
        print("Median:", statistics.median(durations))

    return report


# ==========================================
# EVIDENCE STORAGE
# ==========================================

def save_csv(results):

    if not results:
        print("No CSV data available.")
        return

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    filename = OUTPUT_DIR / "race_evidence.csv"

    with filename.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=list(results[0].keys())
        )

        writer.writeheader()
        writer.writerows(results)

    print("\nCSV saved:", filename)


def save_json(report):

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    filename = OUTPUT_DIR / "race_summary.json"

    with filename.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=4
        )

    print("JSON summary saved:", filename)


# ==========================================
# MAIN
# ==========================================

def main():

    print("=" * 50)
    print("RACE CONDITION AUDIT LAB")
    print("=" * 50)

    print("Target:", URL)
    print("Workers:", WORKERS)
    print("Rounds:", ROUNDS)

    all_results = []
    round_reports = []

    for round_number in range(1, ROUNDS + 1):

        results = run_round(round_number)

        all_results.extend(results)

        report = analyze(results)

        report["round"] = round_number

        round_reports.append(report)

    overall_report = analyze(all_results)

    overall_report["round_reports"] = round_reports
    overall_report["generated_at"] = utc_now()

    save_csv(all_results)
    save_json(overall_report)

    print("\n========== AUDIT COMPLETE ==========")
    print("Total requests:", len(all_results))
    print("Evidence directory:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
