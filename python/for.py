import requests

url = "https://target.com"
# Predefined list of parameters to test
fuzz_parameters = ["admin", "debug", "test", "internal", "role", "dev"]

for param in fuzz_parameters:
    # Build a custom payload for each parameter
    payload = {param: "true"}
    
    response = requests.post(url, json=payload)
    
    # Check if the server responds differently to a hidden parameter
    if response.status_code == 200:
        print(f"[+] Potential Parameter Found! Parameter: '{param}' returned Status: 200")
    else:
        print(f"[-] Checked: {param} (Status: {response.status_code})")
