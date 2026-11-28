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
print("Response:", response.text)
