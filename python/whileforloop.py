In bug bounty hunting, loops are your primary tool for automation. You use for loops when you know exactly how many times you need to run an action (like iterating through a list of parameters or subdomains). You use while loops when you want to run an action continuously until a specific condition changes (like waiting for a rate-limit block to lift or listening for new data).
Here is a practical guide on how to use both loops effectively in your bug bounty scripts.
------------------------------
## 1. The for Loop: Iterating Over Known Targets
Use a for loop when you have a predefined list of assets (IPs, subdomains, endpoints, or payloads) and you want to test every single one of them.
## Example: Fuzzing Hidden URL Parameters
If you find a suspicious endpoint and want to test it against a checklist of common administrative or hidden parameters:

import requests
url = "https://target.com"# Predefined list of parameters to testfuzz_parameters = ["admin", "debug", "test", "internal", "role", "dev"]
for param in fuzz_parameters:
    # Build a custom payload for each parameter
    payload = {param: "true"}
    
    response = requests.post(url, json=payload)
    
    # Check if the server responds differently to a hidden parameter
    if response.status_code == 200:
        print(f"[+] Potential Parameter Found! Parameter: '{param}' returned Status: 200")
    else:
        print(f"[-] Checked: {param} (Status: {response.status_code})")

------------------------------
## 2. The while Loop: Waiting for Conditions to Change
Use a while loop when you do not know how many iterations it will take to complete a task. In bug bounty, this is most commonly used for handling Rate Limits (429), Pagination (fetching all pages of data), or Bypassing Timeout Lockouts.
## Example: Smart Bypassing of a Rate Limit Window
If a target blocks you with a 429 Too Many Requests status, you can use a while loop to pause your script and automatically resume the moment the lock lifts.

import timeimport requests
url = "https://target.com"attempts = 0
# Run indefinitely until we successfully break out of the loopwhile True:
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

------------------------------
## 3. Combining Both: for inside while (Nested Loops)
You will often use a while loop to manage a state (like pagination) and a nested for loop to process data inside that page.
## Example: Scraping All Pages of an API Endpoint
If an API leaks data but limits its output to 50 items per page, you can loop through the pages dynamically until the data runs dry.

import requests
page_number = 1has_more_data = True
while has_more_data:
    print(f"Fetching data from Page {page_number}...")
    api_url = f"https://target.com{page_number}"
    
    response = requests.get(api_url)
    data = response.json()  # Assuming the response is JSON
    
    # If the user list is empty, stop the while loop
    if not data.get("users"):
        print("No more users found. Stopping search.")
        has_more_data = False
        break
    # Use a FOR loop to look through every user on this specific page
    for user in data["users"]:
        if user["is_admin"] == True:
            print(f"[CRITICAL] Found exposed Admin User: {user['username']} on page {page_number}")
    # Increment the page number to request the next set of data in the next iteration
    page_number += 1

Are you currently testing a specific flaw right now (like IDOR, SQL Injection fuzzing, or Subdomain routing)? Tell me your objective, and I can write a tailored loop structure for that exact scenario.

