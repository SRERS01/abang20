import time
import requests

url = "https://target.com"
attempts = 0

# Run indefinitely until we successfully break out of the loop
while True:
    attempts += 1
    print(f"Attempting exploit execution #{attempts}...")
    
    response = requests.post(url, json={"data": "test"})
    
    # Condition A: We hit a rate limit
    if response.status_code == 429:
        print("[-] Hit a rate limit (429). Pausing script for 60 seconds...")
        time.sleep(60)  # Wait for the server window to reset
        continue        # Restart the loop from the top to try again
        
    # Condition B: We successfully bypassed or executed our action
    elif response.status_code == 200:
        print("[+] Success! Action processed cleanly.")
        break           # Break out of the while loop entirely
        
    # Condition C: Any other server rejection
    else:
        print(f"[-] Server rejected request with status: {response.status_code}")
        break
