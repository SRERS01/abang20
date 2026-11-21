# Part 1 – Foundations Before Security+
## Module 4: Programming and Scripting (Practical Lab Guide)

> **Objective:** Build practical fluency in reading, writing, and debugging scripts across **Python, Bash, PowerShell, and JavaScript** for log parsing, API interaction, automation, and security analysis before entering Security+ domains.  
> **Recommended Lab Tools:** Python 3, Bash (Linux/macOS/WSL), Windows PowerShell, Node.js (or Browser DevTools Console), VS Code.

---

### 1. Programming Fundamentals
* **Concept:** Compiled languages (C/C++, Go) translate source code directly into machine binaries before execution. Interpreted/Scripting languages (Python, Bash, PowerShell, JavaScript) execute line-by-line via an interpreter—making them ideal for rapid security automation and incident response.
* **Practical Task:**
  1. Verify your local interpreters are ready for the lab:
     ```bash
     python3 --version
     bash --version | head -n 1
     node --version        # Or press F12 -> Console in any web browser for JavaScript
     ```

### 2. Python
* **Concept:** The dominant language in cybersecurity for threat hunting, exploit prototyping, log analysis, and interacting with security APIs due to its clean syntax and rich standard library.
* **Practical Task:**
  1. Write a Python script using the built-in `hashlib` module to generate a **SHA-256** cryptographic hash of a string (used for verifying file integrity):
     ```python
     import hashlib

     data = b"SecurityPlus_Lab_File"
     sha256_hash = hashlib.sha256(data).hexdigest()
     print(f"SHA-256 Digest: {sha256_hash}")
     ```

### 3. Bash Scripting
* **Concept:** The native automation language of Linux/Unix servers. Essential for incident response triage, text manipulation (`grep`, `awk`, `sed`), and system hardening.
* **Practical Task:**
  1. Create a Bash script (`triage.sh`) that checks for world-writable files in `/tmp` (a common privilege escalation vector):
     ```bash
     cat << 'EOF' > triage.sh
     #!/bin/bash
     echo "[*] Scanning /tmp for world-writable files..."
     find /tmp -maxdepth 2 -type f -perm -0002 2>/dev/null
     EOF

     chmod +x triage.sh
     ./triage.sh
     ```

### 4. PowerShell
* **Concept:** Object-oriented administrative shell built on .NET. Heavily used by Windows administrators for Active Directory/endpoint auditing—and frequently abused by attackers for "fileless" memory-resident attacks (`EncodedCommand`).
* **Practical Task (Windows PowerShell or `pwsh` on Linux):**
  1. Encode and decode a Base64 PowerShell command (crucial skill for SOC analysts investigating obfuscated PowerShell alerts):
     ```powershell
     $cmd = 'Get-Process | Select-Object -First 3'
     $encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($cmd))
     Write-Host "Encoded Payload: $encoded"

     # Decode it back to inspect what an attacker is hiding:
     $decoded = [Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($encoded))
     Write-Host "Decoded Command: $decoded"
     ```

### 5. JavaScript Fundamentals
* **Concept:** The execution language of web browsers (and Node.js backends). Understanding JavaScript is mandatory for analyzing **Cross-Site Scripting (XSS)** payloads, malicious browser redirects, and web APIs.
* **Practical Task (Browser Console `F12` or Node.js):**
  1. Run a simple script demonstrating how JavaScript accesses the browser Document Object Model (`document.cookie`), which is the primary target of XSS attacks:
     ```javascript
     const userSession = { username: "analyst01", role: "admin", isAuthenticated: true };
     console.log(`User ${userSession.username} logged in with role: ${userSession.role}`);
     ```

### 6. Variables and Data Types
* **Concept:** Storing data in memory using appropriate types: **Strings** (`"192.168.1.1"`), **Integers** (`443`), **Floats** (`99.5`), **Booleans** (`True/False`), **Lists/Arrays** (`["22", "80"]`), and **Dictionaries/Objects** (`{"port": 22, "state": "open"}`).
* **Practical Task (Python):**
  1. Model a host scan result using core data types:
     ```python
     target_ip = "10.0.0.15"          # String
     open_ports = [22, 80, 443]       # List
     is_vulnerable = True             # Boolean
     host_profile = {"ip": target_ip, "ports": open_ports, "vuln": is_vulnerable} # Dict
     print(type(host_profile), host_profile)
     ```

### 7. Operators
* **Concept:** Arithmetic (`+`, `-`, `*`, `/`, `%`), Comparison (`==`, `!=`, `>`, `<`), Logical (`and`, `or`, `not`), and Bitwise (`&`, `|`, `^` XOR) operators used in firewall logic, subnetting, and encryption.
* **Practical Task (Python):**
  1. Implement a simple **XOR cipher** (single-byte key encryption/decryption—widely seen in malware obfuscation):
     ```python
     secret = "ATTACK"
     key = 0x55
     encrypted = "".join([chr(ord(c) ^ key) for c in secret])
     decrypted = "".join([chr(ord(c) ^ key) for c in encrypted])
     print("Encrypted:", repr(encrypted), "| Decrypted:", decrypted)
     ```

### 8. Conditional Statements
* **Concept:** Decision-making branches (`if`, `elif`, `else`) that evaluate Boolean conditions to trigger alerts or block actions.
* **Practical Task (Python):**
  1. Classify a CVSS vulnerability score into severity tiers:
     ```python
     cvss_score = 8.6

     if cvss_score >= 9.0:
         severity = "CRITICAL"
     elif cvss_score >= 7.0:
         severity = "HIGH"
     elif cvss_score >= 4.0:
         severity = "MEDIUM"
     else:
         severity = "LOW"

     print(f"CVSS {cvss_score} -> Severity: {severity}")
     ```

### 9. Loops
* **Concept:** Repeating actions across collections (`for` loops) or until a condition changes (`while` loops)—used for scanning port ranges, iterating through log files, or brute-force simulations.
* **Practical Task (Python):**
  1. Iterate over a list of ports and flag insecure cleartext protocols:
     ```python
     discovered_ports = [21, 22, 23, 80, 443, 3389]
     insecure_ports = {21: "FTP", 23: "Telnet", 80: "HTTP"}

     for port in discovered_ports:
         if port in insecure_ports:
             print(f"[!] ALERT: Insecure cleartext service {insecure_ports[port]} on port {port}")
     ```

### 10. Functions
* **Concept:** Reusable, modular blocks of code accepting inputs (parameters) and returning outputs—keeping security tools clean and maintainable.
* **Practical Task (Python):**
  1. Write a reusable function to check if an IPv4 address belongs to the `192.168.` private range:
     ```python
     def is_local_subnet(ip_addr):
         return ip_addr.startswith("192.168.")

     print("192.168.1.50 local? ->", is_local_subnet("192.168.1.50"))
     print("8.8.8.8 local?      ->", is_local_subnet("8.8.8.8"))
     ```

### 11. Classes and Objects (OOP)
* **Concept:** Object-Oriented Programming bundles data (attributes) and behavior (methods) into blueprints (`class`) to model real-world entities like network assets, alerts, or firewall rules.
* **Practical Task (Python):**
  1. Create a `SecurityAlert` class and instantiate two alert objects:
     ```python
     class SecurityAlert:
         def __init__(self, source_ip, alert_type, severity):
             self.source_ip = source_ip
             self.alert_type = alert_type
             self.severity = severity

         def summary(self):
             return f"[{self.severity}] {self.alert_type} detected from {self.source_ip}"

     alert1 = SecurityAlert("45.33.32.156", "SSH Brute Force", "HIGH")
     print(alert1.summary())
     ```

### 12. File Handling
* **Concept:** Reading from and writing to files (`open()`, `read()`, `write()`, `with` context managers) to ingest raw logs, wordlists, and IOC feeds, and export incident reports.
* **Practical Task (Python):**
  1. Create a sample firewall log file and read it back line by line:
     ```python
     sample_logs = [
         "2026-11-21 10:01:12 ALLOW TCP 192.168.1.10 -> 142.250.190.46:443\n",
         "2026-11-21 10:02:45 DENY TCP 185.220.101.4 -> 192.168.1.10:22\n",
         "2026-11-21 10:03:01 DENY TCP 185.220.101.4 -> 192.168.1.10:3389\n"
     ]

     with open("firewall.log", "w") as f:
         f.writelines(sample_logs)

     with open("firewall.log", "r") as f:
         for line in f:
             if "DENY" in line:
                 print(line.strip())
     ```

### 13. Exception Handling
* **Concept:** Gracefully catching runtime errors (`try / except / finally`) such as network timeouts, permission denied errors, or malformed log lines so an automation script does not crash mid-investigation.
* **Practical Task (Python):**
  1. Safely handle missing files and permission errors:
     ```python
     try:
         with open("/root/nonexistent_shadow_copy.txt", "r") as f:
             print(f.read())
     except FileNotFoundError:
         print("[ERROR] Target file does not exist.")
     except PermissionError:
         print("[ERROR] Insufficient privileges to read file.")
     ```

### 14. Regular Expressions (Regex)
* **Concept:** Pattern-matching syntax used to extract IP addresses, email addresses, hashes, URLs, or credit card numbers from unstructured logs and memory dumps.
* **Practical Task (Python `re` module):**
  1. Extract all IPv4 addresses from a messy text string:
     ```python
     import re

     raw_text = "Failed SSH login from 203.0.113.42 and port scan from 198.51.100.19 on port 22."
     ip_pattern = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
     extracted_ips = re.findall(ip_pattern, raw_text)
     print("Extracted IPs:", extracted_ips)
     ```

### 15. JSON and XML
### 15. JSON and XML
* **Concept:** Structured data formats used across cybersecurity tools:
  * **JSON (JavaScript Object Notation):** Lightweight key-value pairs used by REST APIs, SIEM log pipelines (Elasticsearch/Splunk), and Cloud IAM policies (AWS/Azure).
  * **XML (eXtensible Markup Language):** Tag-based structured data used by **Windows Event Logs**, **Nmap** scan exports (`-oX`), and **SAML** authentication tokens (vulnerable to **XXE — XML External Entity** injection if improperly parsed).
* **Practical Task 1 (Parse & Generate JSON Threat Intelligence in Python):**
  ```python
  import json

  raw_siem_event = '''
  {
      "timestamp": "2026-11-21T12:45:00Z",
      "event_type": "authentication_failure",
      "source_ip": "185.220.101.45",
      "target_user": "administrator",
      "risk_score": 85,
      "mitre_tactics": ["Credential Access", "Brute Force"]
  }
  '''

  event = json.loads(raw_siem_event)
  if event["risk_score"] >= 80:
      print(f"[HIGH RISK ALERT] User '{event['target_user']}' targeted from {event['source_ip']}")
      print("MITRE Tactics:", ", ".join(event["mitre_tactics"]))
  ```

* **Practical Task 2 (Parse an XML Security Alert / Windows Event Snippet in Python):**
  ```python
  import xml.etree.ElementTree as ET

  xml_log = '''
  <Event>
      <System>
          <EventID>4625</EventID>
          <Computer>WIN-DC01.corp.local</Computer>
      </System>
      <EventData>
          <Data Name="TargetUserName">admin_backup</Data>
          <Data Name="IpAddress">203.0.113.88</Data>
      </EventData>
  </Event>
  '''

  root = ET.fromstring(xml_log)
  event_id = root.find("./System/EventID").text
  computer = root.find("./System/Computer").text
  print(f"Parsed XML Event ID: {event_id} on Host: {computer}")
  for data in root.findall("./EventData/Data"):
      print(f"  {data.attrib['Name']}: {data.text}")
  ```

---

### 16. HTTP Requests
* **Concept:** Security analysts and penetration testers script HTTP requests (`GET`, `POST`, `HEAD`, `OPTIONS`) to inspect web server configurations, check for missing security headers (like `Strict-Transport-Security` or `Content-Security-Policy`), and test authentication endpoints.
* **Practical Task (Audit HTTP Security Headers with Python):**
  ```python
  import urllib.request

  url = "https://example.com"
  req = urllib.request.Request(url, headers={"User-Agent": "SecPlus-HeaderAuditor/1.0"})

  security_headers = [
      "Strict-Transport-Security",
      "Content-Security-Policy",
      "X-Frame-Options",
      "X-Content-Type-Options"
  ]

  with urllib.request.urlopen(req, timeout=5) as response:
      print(f"Target: {url} | HTTP Status: {response.status}\n")
      for header in security_headers:
          value = response.headers.get(header)
          status = f"PRESENT ({value})" if value else "MISSING [!]"
          print(f"{header:<28}: {status}")
  ```

---

### 17. APIs (Application Programming Interfaces)
* **Concept:** Security orchestration (**SOAR**) and threat intelligence workflows rely on REST APIs (sending JSON over HTTPS with `Authorization: Bearer <API_KEY>` headers) to automatically enrich suspicious IPs, file hashes, or domains without manual browser lookups.
* **Practical Task (Query a Threat/IP Enrichment API & Handle Rate Limits):**
  ```python
  import urllib.request
  import json

  suspicious_ips = ["8.8.8.8", "1.1.1.1"]

  for ip in suspicious_ips:
      endpoint = f"http://ip-api.com{ip}?fields=status,country,isp,org,query"
      try:
          with urllib.request.urlopen(endpoint, timeout=5) as resp:
              result = json.loads(resp.read().decode("utf-8"))
              if result.get("status") == "success":
                  print(f"[ENRICHED] {result['query']} -> Country: {result['country']} | Org: {result['org']}")
      except Exception as e:
          print(f"[ERROR] Failed to query API for {ip}: {e}")
  ```

---

### 18. Automation
* **Concept:** Replacing manual, error-prone security checks with repeatable, scheduled scripts (**File Integrity Monitoring**, automated blocklist generation, or daily vulnerability baseline checks).
* **Practical Task (Build a Mini File Integrity Monitor — FIM):**
  1. Save this script as `fim_monitor.py`. Run it once to create a baseline hash database, modify a watched file, and run it again to detect unauthorized tampering:
     ```python
     import hashlib
     import json
     import os

     WATCHED_FILES = ["triage.sh", "firewall.log"]
     BASELINE_DB = "fim_baseline.json"

     def compute_sha256(filepath):
         h = hashlib.sha256()
         with open(filepath, "rb") as f:
             while chunk := f.read(4096):
                 h.update(chunk)
         return h.hexdigest()

     # Create dummy files if they don't exist yet
     for file in WATCHED_FILES:
         if not os.path.exists(file):
             with open(file, "w") as f:
                 f.write("Initial clean content\n")

     current_hashes = {f: compute_sha256(f) for f in WATCHED_FILES if os.path.exists(f)}

     if not os.path.exists(BASELINE_DB):
         with open(BASELINE_DB, "w") as db:
             json.dump(current_hashes, db, indent=2)
         print("[*] Baseline created! Modify 'firewall.log' and re-run this script to test detection.")
     else:
         with open(BASELINE_DB, "r") as db:
             saved_hashes = json.load(db)
         for file, current_hash in current_hashes.items():
             if saved_hashes.get(file) != current_hash:
                 print(f"[ALERT - INTEGRITY VIOLATION] {file} has been modified!")
             else:
                 print(f"[OK] {file} matches baseline.")
     ```

---

### 19. Log Parsing
* **Concept:** SOC analysts regularly parse gigabytes of raw web server, firewall, and SSH logs to identify **brute-force attacks**, **directory enumeration**, and **SQL injection probes**.
* **Practical Task (Detect Brute-Force & Suspicious Web Probes from Raw Logs):**
  ```python
  import re
  from collections import Counter

  raw_access_logs = [
      '192.168.1.50 - - [21/Nov/2026:12:10:01] "GET /index.html HTTP/1.1" 200 1024',
      '45.33.32.156 - - [21/Nov/2026:12:10:05] "POST /wp-login.php HTTP/1.1" 401 512',
      '45.33.32.156 - - [21/Nov/2026:12:10:06] "POST /wp-login.php HTTP/1.1" 401 512',
      '45.33.32.156 - - [21/Nov/2026:12:10:07] "POST /wp-login.php HTTP/1.1" 401 512',
      '198.51.100.9 - - [21/Nov/2026:12:11:12] "GET /../../etc/passwd HTTP/1.1" 403 256'
  ]

  failed_auth_ips = Counter()

  for entry in raw_access_logs:
      ip_match = re.search(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", entry)
      ip = ip_match.group(0) if ip_match else "Unknown"

      # Detect Directory Traversal attack signatures
      if "../" in entry:
          print(f"[CRITICAL - PATH TRAVERSAL] Source IP: {ip} -> {entry}")

      # Count HTTP 401 Unauthorized failures
      if '" 401 ' in entry:
          failed_auth_ips[ip] += 1

  for ip, count in failed_auth_ips.items():
      if count >= 3:
          print(f"[HIGH - BRUTE FORCE DETECTED] IP {ip} triggered {count} failed logins.")
  ```

---

### 20. Security Scripting (Capstone Mini-Tool)
* **Concept:** Combining **sockets, loops, exception handling, functions, and JSON reporting** into a complete, reusable security recon & auditing utility.
* **Practical Task (Multi-Port TCP Scanner & Banner Grabber with JSON Report Export):**
  Save as `mini_recon.py` and run against `127.0.0.1` (localhost) to safely map open local ports and export a structured JSON report:
  ```python
  import socket
  import json
  from datetime import datetime, timezone

  def scan_port(target_ip, port, timeout=0.5):
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.settimeout(timeout)
      try:
          if sock.connect_ex((target_ip, port)) == 0:
              banner = "No banner"
              try:
                  sock.sendall(b"HEAD / HTTP\(/1.0\r\n\r\\)n")
                  banner = sock.recv(1024).decode("utf-8", errors="ignore").splitlines()
              except Exception:
                  pass
              return {"port": port, "state": "open", "banner": banner}
      except socket.error:
          pass
      finally:
          sock.close()
      return None

  def run_audit(target_ip, ports):
      print(f"[*] Starting TCP Security Audit on {target_ip}...")
      results = []
      for p in ports:
          finding = scan_port(target_ip, p)
          if finding:
              print(f"  [+] Port {finding['port']} OPEN | {finding['banner']}")
              results.append(finding)

      report = {
          "target": target_ip,
          "scan_time_utc": datetime.now(timezone.utc).isoformat(),
          "open_ports_count": len(results),
          "findings": results
      }

      with open("recon_report.json", "w") as outfile:
          json.dump(report, outfile, indent=2)
      print("[*] Report saved to recon_report.json")

  if __name__ == "__main__":
      common_ports =
      run_audit("127.0.0.1", common_ports)
  ```

---

### Module 4 Completion Checklist
- [ ] Parsed structured **JSON** and **XML** security events in Python.
- [ ] Audited live **HTTP security headers** (`HSTS`, `CSP`, `X-Frame-Options`) programmatically.
- [ ] Queried a live **REST API** to enrich IP addresses with geolocation and ISP metadata.
- [ ] Built and tested an automated **File Integrity Monitor (`fim_monitor.py`)** using SHA-256 hashes.
- [ ] Wrote a **Regex log parser** to detect path traversal (`../`) and brute-force (`401`) attacks.
- [ ] Built and ran the **Capstone TCP Port Scanner (`mini_recon.py`)** exporting results to `recon_report.json`.

