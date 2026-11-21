# Most Dangerous & Hard-to-Detect Web Attacks

## 1. Server-Side Request Forgery (SSRF)
* **Why it is dangerous:** Tricks the web server into making unauthorized requests inside the internal network, allowing attackers to bypass firewalls and steal sensitive cloud credentials (e.g., AWS/Azure metadata).
* **Why it is hard to notice:** To internal systems, the malicious traffic appears to originate from a trusted, authorized internal server rather than an external attacker.

## 2. Business Logic Flaws
* **Why it is dangerous:** Exploits legitimate application workflows in unintended ways—such as bypassing payment steps, manipulating coupon rules, or transferring negative balances.
* **Why it is hard to notice:** Involves no malicious code, malware, or malformed inputs. Web Application Firewalls (WAFs) treat it as normal, valid user activity.

## 3. Magecart / Digital Skimming (Client-Side Supply Chain)
* **Why it is dangerous:** Injects obfuscated JavaScript into checkout pages (often via compromised third-party plugins) to silently steal credit card details as users type them.
* **Why it is hard to notice:** Executes entirely inside the victim's web browser while the checkout process functions normally, leaving no trace on the company's backend servers.

## 4. Second-Order SQL Injection & Stored XSS
* **Why it is dangerous:** Malicious payloads are saved quietly inside a database and only execute later when triggered by a specific action (like an admin viewing a report), often granting high-level privileges.
* **Why it is hard to notice:** The initial input looks harmless and passes basic filters, and the actual execution happens days or weeks later, making it hard to trace.

## 5. HTTP Request Smuggling
* **Why it is dangerous:** Exploits discrepancies in how front-end proxies (CDNs/load balancers) and back-end servers interpret HTTP headers, allowing attackers to sneak hidden requests past security controls and hijack active user sessions.
* **Why it is hard to notice:** Both servers process what looks like standard HTTP traffic, leaving minimal evidence in traditional error logs.

## 6. Broken Object Level Authorization (BOLA / IDOR)
* **Why it is dangerous:** Occurs when an API verifies that a user is logged in, but fails to check if they own the requested resource (e.g., changing an ID in the URL to view another user's private records).
* **Why it is hard to notice:** Requests are made using legitimate authentication tokens and valid API endpoints, blending seamlessly into normal traffic.

## 7. Web Cache Poisoning
* **Why it is dangerous:** Manipulates a website's caching layer into storing and serving a malicious version of a webpage to every subsequent innocent visitor.
* **Why it is hard to notice:** Requires no modification to the site's actual source code or database, and evidence vanishes automatically once the cache expires.
