import requests

session = requests.Session()

login_url = "https://www.betpawa.cm/api/user/v3/password/request-otp"

headers = {
    "User-Agent": "Mozilla/5.0", 
    "Content-Type": "application/json",
    "X-Pawa-Brand": "betpawa-cameroon",
    "X-Pawa-Language": "en"
}

payload = {
    "phoneNumber": "652223518",
    "resetMethodName": "SMS"
}

login_response = session.post(login_url, headers=headers, json=payload)

print("LOGIN STATUS:", login_response.status_code)

# Extract token automatically
token = session.cookies.get("x-pawa-token")

print("TOKEN:", token)
