import requests

url = "https://www.betpawa.cm/api/user/v3/authenticate"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json",
    "X-Pawa-Brand": "betpawa-cameroon",
    "X-Pawa-Language": "en"
}

payload = {
    "username": "682887747",
    "password": "0519",
    "rememberMe": False
}

response = requests.post(
    url,
    headers=headers,
    json=payload,
    timeout=15
)

print("Status:", response.status_code)

try:
    data = response.json()
    print("Response fields:", list(data.keys()))

    print("\nPossible authentication fields:")
    for key, value in data.items():
        if "token" in key.lower() or "auth" in key.lower():
            print(key, "[PRESENT]" if value else "[EMPTY]")

except ValueError:
    print("Response is not JSON")

print("\nCookie names:", list(response.cookies.keys()))

print("\nAuthentication-related response header names:")
for key in response.headers:
    if "auth" in key.lower() or "token" in key.lower():
        print(key, "[PRESENT]")
