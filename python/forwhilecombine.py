import requests

page_number = 1
has_more_data = True

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
