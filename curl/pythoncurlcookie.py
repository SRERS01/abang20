Let's go deeper into Method 2: Loading a curl cookie file directly into Python.

The idea is to authenticate with curl, save the cookies in a file, and then let Python read that same file and use the saved session when communicating with your local API.

You won't need to manually copy and paste the cookie value.

### 1\. Understand what we are building

Imagine your local Flask application is running at:

```text
http://127.0.0.1:8000
```

You have two clients:

* curl: communicates with the server from your terminal.

* Python Requests: communicates with the server through a Python script.

Both clients can use the same cookie file.

1\. curl login

Sends username and password to local server

2\. cookies.txt

Stores the session cookie returned by the server

3\. Python Requests

Loads the saved cookie file

4\. Local API

Receives Python's authenticated request

### 2\. Step one: Open your local lab directory

In Ubuntu:

```bash
cd ~/edf/withdrawal_lab
```

Activate your virtual environment:

```bash
source myvenv/bin/activate
```

If your virtual environment is in another directory, activate it using its actual path.

### 3\. Step two: Install Requests

Run:

```bash
pip install requests
```

This installs the Python library used to communicate with HTTP servers.

### 4\. Step three: Authenticate using curl

Make sure your local protected server is running on port 8000.

Run:

```bash
curl -i -c cookies.txt -X POST \
http://127.0.0.1:8000/login \
-H "Content-Type: application/json" \
-d '{"username":"testuser","password":"testpass"}'
```

What happens?

* curl sends the login information.

* Flask checks the credentials.

* Flask creates a session.

* Flask returns a session cookie.

* curl saves the cookie in `cookies.txt`.

You can check whether the file exists:

```bash
ls -l cookies.txt
```

Avoid sharing its contents because the session cookie is sensitive.

### 5\. Step four: Understand the Python code

Here is the important part:

```python
import requests
import http.cookiejar
```

* `requests` allows Python to send HTTP requests.

* `http.cookiejar` provides cookie storage and handling.

Create a session:

```python
session = requests.Session()
```

A Session object is important because it can retain cookies across multiple requests.

Now load the cookie file:

```python
session.cookies = http.cookiejar.MozillaCookieJar("cookies.txt")
```

This tells Python that your cookie file uses the Netscape/Mozilla cookie-file format.

Load the stored cookies:

```python
session.cookies.load(
    ignore_discard=True,
    ignore_expires=True
)
```

The two arguments mean:

| Argument            | Meaning                                                    |
| ------------------- | ---------------------------------------------------------- |
| ignore_discard=True | Load cookies marked as non-persistent                      |
| ignore_expires=True | Load cookies even if their recorded expiry time has passed |

Be careful: loading an expired cookie does not make it valid again. The server can still reject it.

### 6\. Step five: Send an authenticated request

Now create a Python file:

```bash
nano cookie_test.py
```

Put this complete code inside:

```python

import requests
import http.cookiejar

# Create a persistent HTTP session
session = requests.Session()

# Load cookies saved by curl
cookie_file = "cookies.txt"

session.cookies = http.cookiejar.MozillaCookieJar(cookie_file)

session.cookies.load(
    ignore_discard=True,
    ignore_expires=True
)

# Local API endpoint
url = "http://127.0.0.1:8000/profile"

# Send request using the loaded cookies
response = session.get(url)

# Display results
print("Status code:", response.status_code)

print("Response headers:")
print(response.headers)

print("Response body:")
print(response.text)
```

Save the file:

* Press `CTRL + O`.

* Press Enter.

* Press `CTRL + X`.

Run:

```bash
python cookie_test.py
```

If the session cookie is valid, your local profile endpoint should return the authenticated user's information.

### 7\. Step six: Understand what happens internally

When Python executes:

```python
response = session.get(url)
```

The Requests library performs several operations:

* Checks its cookie jar.

* Identifies cookies applicable to the destination URL.

* Adds the appropriate `Cookie` header.

* Sends the HTTP request.

* Receives the server response.

* Updates the session cookie jar if the server sends new cookies.

The outgoing request is conceptually similar to:

```http
GET /profile HTTP/1.1
Host: 127.0.0.1:8000
Cookie: session=LOCAL_TEST_SESSION
```

You don't need to manually write the Cookie header.

### 8\. curl versus Python: What is different?

| Activity          | curl                | Python Requests   |
| ----------------- | ------------------- | ----------------- |
| Login             | Yes                 | Yes               |
| Save cookies      | -c                  | Cookie jar        |
| Load cookies      | -b                  | Cookie jar        |
| Send GET          | Yes                 | Yes               |
| Send POST         | Yes                 | Yes               |
| Automate requests | Shell scripts       | Python scripts    |
| Analyze responses | Basic output        | Python processing |
| Maintain session  | Cookie file options | Session()         |

### 9\. Test your understanding

Suppose you have this sequence:

```bash
curl -c cookies.txt ...
```

Then:

```python
session.cookies.load(...)
```

Then:

```python
response = session.get(url)
```

What does each stage do?

1. What does curl's -c option do?

Sends cookies to the server

Saves cookies received from the server

Deletes cookies

2. What does MozillaCookieJar do?

Loads and manages cookies in a compatible file format

Creates a new API endpoint

Encrypts the server response

3. What does requests.Session() provide?

A new server

A reusable HTTP session that can retain cookies

A database connection

Check answers

The main concept to remember: curl and Python are two different clients. The cookie file allows them to share session information when communicating with the same local server.
