import requests
import time 

url = "https://www.betpawa.cm/api/user/v3/password/request-otp"
headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json",
    "X-Pawa-Brand": "betpawa-cameroon",
    "X-Pawa-Language": "en"
}

# Initialize session
session = requests.Session()

# 2. Test numbers (change carefully)
numbers = [
    "678392088",   # real/test number 
    "600000000",   # random
    "699999999"    # random
]

# 3. Main testing function
def test_number(phone):
    payload = {
        "phoneNumber": phone,
        "resetMethodName": "SMS"
    }

    start = time.time()
    response = session.post(url, headers=headers, json=payload)
    end = time.time()

    print(f"\n=== TEST: {phone} ===")
    print("Status Code:", response.status_code)
    print("Response Time:", round(end - start, 3), "sec")

    # Show part of response (avoid long spam)
    print("Response Body:", response.text[:200])

    # Show cookies
    print("Cookies:", session.cookies.get_dict())


# 4. Run base tests
for num in numbers:
    test_number(num)


# 5. Small rate-limit check (SAFE: only few requests)
print("\n=== RATE LIMIT TEST ===")
for i in range(5):
    r = session.post(url, headers=headers, json={
        "phoneNumber": numbers[0],
        "resetMethodName": "SMS"
    })
    print(f"Attempt {i+1}: {r.status_code}")
    time.sleep(1)  # avoid spamming
