# CompTIA Security+ (SY0-701) – Practical Lab Guide
## Domain 2: Threats, Vulnerabilities, and Mitigations
### Objective 2.5: Indicators of Malicious Activity

> **Objective:** Recognize, investigate, and write detection rules for malware behaviors, network/application/credential attacks, social engineering lures, physical intrusions, and host/network Indicators of Compromise (IoCs).  
> **Recommended Lab Tools:** Python 3, Linux Terminal / Bash, Windows PowerShell, `tcpdump` / Wireshark, `strings`, `sha256sum`.

---

## Part A: Malware (10 Types)

| Malware Type | Core Behavior & Propagation Mechanism | Key Indicator / Practical Detection Signal |
| :--- | :--- | :--- |
| **1. Viruses** | Attaches itself to a clean host executable/document; requires **human action** (opening/running the infected file) to spread. | Unexpected hash changes or altered file sizes on legitimate binaries. |
| **2. Worms** | **Self-replicating** malware that spreads autonomously across networks by exploiting vulnerabilities without human interaction. | Sudden spike in outbound SMB (`445`), RDP (`3389`), or SSH (`22`) scans from an internal host. |
| **3. Trojans** | Disguises itself as legitimate software (cracked apps, fake installers) to trick users into executing hidden backdoors/RATs. | Unsigned binary executing out of `C:\Users\*\Downloads` making outbound C2 connections. |
| **4. Ransomware** | Encrypts user/server files (and often exfiltrates data for double extortion), demanding payment for the decryption key. | High disk I/O, mass file renaming (`.locked`), deletion of Windows Volume Shadow Copies (`vssadmin delete shadows`). |
| **5. Spyware** | Silently monitors user browsing, screen activity, microphone/webcam, and exfiltrates sensitive personal/corporate data. | Unauthorized persistent background process sending periodic HTTPS beacons. |
| **6. Adware** | Displays unwanted pop-up advertisements, hijacks browser homepages/search engines, and tracks browsing habits. | Unapproved browser extensions, modified proxy settings, or DNS redirects. |
| **7. Rootkits** | Modifies OS kernel, drivers, or bootloader (`UEFI`) to hide processes, files, and network sockets from standard OS tools. | Discrepancy between raw disk/memory forensics (Volatility) and live OS `ps` / `tasklist` output. |
| **8. Keyloggers** | Captures keystrokes (via software API hooks `SetWindowsHookEx` or inline USB hardware) to steal passwords and PINs. | Unknown process hooking keyboard input events or writing hidden keystroke log files. |
| **9. Logic Bombs** | Malicious code dormant inside legitimate software until triggered by a specific condition (date/time, deleted employee account). | Scheduled tasks or code triggers tied to calendar dates or user-table checks. |
| **10. Fileless Malware** | Resides purely in **volatile RAM** using built-in tools (`PowerShell`, `WMI`, `.NET` reflection) without writing `.exe` files to disk. | Obfuscated Base64 PowerShell commands (`-EncodedCommand`) or WMI event subscriptions. |

* **Practical Task (Detect Ransomware Shadow-Copy Deletion & Fileless PowerShell in Python):**
  ```python
  endpoint_events = [
      "vssadmin.exe delete shadows /all /quiet",
      "powershell.exe -NoP -W Hidden -Enc UwB0AGEAcgB0AC0AUAByAG8AYwBlAHMAcwA=",
      "notepad.exe C:\\Users\\alice\\notes.txt"
  ]

  for cmd in endpoint_events:
      if "delete shadows" in cmd.lower():
          print(f"[RANSOMWARE ALERT] Volume Shadow Copy deletion detected: {cmd}")
      elif "-enc " in cmd.lower():
          print(f"[FILELESS MALWARE ALERT] Encoded in-memory PowerShell execution: {cmd}")
  ```

---

## Part B: Physical Attacks (4 Types)

### 1. Tailgating (Piggybacking)
* **Concept:** An unauthorized person follows an authorized employee through a badge-controlled door before it closes (Tailgating = without consent; Piggybacking = employee knowingly holds the door). *Mitigation:* Mantraps / access control vestibules, turnstiles, security awareness.
### 2. Shoulder Surfing
* **Concept:** Observing a user's screen, keyboard, or keypad over their shoulder (or via zoom lens/reflection) to capture passwords or PINs. *Mitigation:* Privacy screen filters, biometric/FIDO2 login.
### 3. Skimming
* **Concept:** Attaching a covert hardware card-reader overlay onto ATMs, fuel pumps, or POS terminals (or skimming contactless RFID/NFC badges) to clone magnetic stripe/card data.
### 4. Forced Entry
* **Concept:** Breaking locks, doors, windows, or server cages physically. *Mitigation:* Reinforced doors, bollards, door contact alarms, glass-break sensors, CCTV.
* **Practical Task:**
  1. Audit badge-reader logs for **"Impossible Physical Access"** (e.g., two badge swipes at the same door within 1 second, or an exit swipe without a prior entry swipe—classic tailgating indicator).

---

## Part C: Network Attacks (8 Types)

### 1. Distributed Denial of Service (DDoS)
* **Concept:** Flooding a target's bandwidth, TCP state tables, or web application endpoints using thousands of compromised botnet devices so legitimate users cannot connect.
### 2. Protocol Downgrade
* **Concept:** Forcing a client and server to abandon strong modern encryption (`TLS 1.3`) and fall back to weak, crackable legacy protocols (`TLS 1.0`, `SSLv3`, `NTLMv1`).
### 3. Rogue Devices
* **Concept:** Unauthorized hardware connected to the network (Rogue APs, Evil Twin hotspots, unauthorized switches/drop-boxes).
### 4. Packet Sniffing
* **Concept:** Capturing raw network traffic in promiscuous mode to steal unencrypted credentials (`HTTP`, `Telnet`, `FTP`, `POP3`).
### 5. Spoofing
* **Concept:** Falsifying source identity fields—**IP Spoofing**, **MAC Spoofing**, **ARP Spoofing**, or **Email/Caller ID Spoofing**.
### 6. On-Path Attacks (Man-in-the-Middle / MitM)
* **Concept:** Positioning between two communicating endpoints (via ARP poisoning, Evil Twin Wi-Fi, or rogue proxy) to silently intercept, read, or alter packets in real time.
### 7. DNS Attacks & 8. Cache Poisoning
* **Concept:** Corrupting a DNS resolver's cache with forged IP records (**DNS Cache Poisoning**) or hijacking domain registrar settings so users typing `bank.com` are silently routed to an attacker's phishing server. *(Mitigated by **DNSSEC** and **DoH/DoT**)*.
* **Practical Task (Detect ARP Spoofing / Duplicate MACs & DNS Anomalies):**
  ```bash
  # Check local ARP table for two different IPs sharing the exact same MAC address (On-Path ARP Spoofing indicator)
  arp -a
  ```

---

## Part D: Social Engineering (8 Types)

| Technique | Delivery Channel & Mechanism |
| :--- | :--- |
| **1. Phishing** | Mass-sent deceptive emails urging recipients to click credential-harvesting links or open malicious attachments. |
| **2. Spear Phishing** | Highly targeted phishing crafted using OSINT details specific to one individual or department. |
| **3. Whaling** | Spear phishing aimed specifically at high-profile executives (CEO, CFO, Board Members) to authorize wire fraud or leak board secrets. |
| **4. Smishing** | Phishing delivered via SMS text messages (e.g., fake package delivery or bank fraud alerts). |
| **5. Vishing** | Voice phishing over phone calls or VoIP impersonating IT helpdesk, bank fraud teams, or tax authorities. |
| **6. Quishing** | Embedding malicious phishing URLs inside **QR codes** to bypass email URL scanners and move victims onto mobile phones. |
| **7. Impersonation** | Posing as a trusted authority figure, vendor, or colleague to manipulate targets into bypassing controls. |
| **8. Deepfakes** | AI-generated synthetic audio or real-time video cloning an executive's voice/face during vishing or video calls to authorize urgent transfers. |

* **Practical Task (Analyze Phishing Email Headers & Urgency Triggers in Python):**
  ```python
  subject = "URGENT: Executive Wire Transfer Required Immediately - Confidential"
  reply_to = "cfo.office@corp-billing-support.xyz"
  sender_domain = "corp.com"

  if sender_domain not in reply_to and any(w in subject.lower() for w in ["urgent", "wire transfer", "immediately"]):
      print("[WHALING / BEC ALERT] Domain mismatch + high-urgency financial lure detected!")
  ```

---

## Part E: Indicators of Compromise (IoCs — 12 Types)

* **Practical Task (All-in-One Python IoC Triage Scanner):**
  Run this script to see how a SOC analyst programmatically checks all **12 IoC categories** from your syllabus:
  ```python
  import re
  from datetime import datetime

  # 1. File Hashes (Known malware SHA-256)
  known_bad_hashes = {"44d88612fea8a8f36de82e1278abb02f"}
  # 2. Suspicious IP Addresses & 3. Malicious Domains
  bad_ips = {"198.51.100.88"}
  bad_domains = {"c2-beacon-update.xyz"}
  # 4. Malicious Processes & 5. File System Artifacts
  running_procs = ["systemd", "sshd", "xmrig_miner"]
  suspicious_files = ["/tmp/.hidden_backdoor.sh"]
  # 6. Suspicious Timestamps (Timestomping: file modified in future or 1970)
  file_mtime_year = 2099
  # 7. Log Manipulation (Cleared Windows Security Log Event ID 1102 / truncated auth.log)
  log_events = ["EventID 1102: The audit log was cleared"]
  # 8. Excessive Resource Consumption (Cryptomining / DDoS)
  cpu_usage_percent = 98.5
  # 9. Plaintext Strings (Hardcoded C2 URL inside binary)
  binary_strings = "LoadLibraryA http://c2-beacon-update.xyz"
  # 10. Account Lockouts
  failed_logins = 12
  # 11. Impossible Travel & 12. Concurrent Sessions
  login_1 = {"user": "alice", "city": "Buea", "time": "10:00"}
  login_2 = {"user": "alice", "city": "Tokyo", "time": "10:15"}

  print("=== AUTOMATED IoC TRIAGE REPORT ===")
  if "xmrig_miner" in running_procs or cpu_usage_percent > 95:
      print("[IoC: Process & Resource Spike] Cryptominer 'xmrig_miner' consuming 98.5% CPU!")
  if file_mtime_year > 2026:
## Part E: Indicators of Compromise (IoCs — 12 Types)

> **Exam Tip:** An **Indicator of Compromise (IoC)** is forensic evidence on a host or network showing an intrusion has likely occurred (reactive), whereas an **Indicator of Attack (IoA)** focuses on the adversary's real-time intent and behavior.

| IoC Category | What Analysts Look For | Practical CLI / Forensic Verification Command |
| :--- | :--- | :--- |
| **1. File Hashes** | Cryptographic digests (`SHA-256`, `MD5`) matching known malware samples in Threat Intel feeds (VirusTotal, MISP). | `sha256sum /tmp/suspicious_binary` (Windows: `Get-FileHash file.exe -Algorithm SHA256`) |
| **2. Suspicious IP Addresses** | Outbound connections/beacons to known Command-and-Control (C2) servers, Tor exit nodes, or bulletproof hosting. | `ss -tunp` (Windows: `netstat -ano`) |
| **3. Malicious Domains** | DNS queries to Newly Registered Domains (NRDs), typosquatted domains, or high-entropy **DGA (Domain Generation Algorithm)** names. | `grep "query" /var/log/syslog` or Wireshark filter `dns.qry.name` |
| **4. Malicious Processes** | Unknown binaries, misspelled system processes (`svch0st.exe`), or processes running from `/tmp`, `/dev/shm`, or `C:\Users\Public`. | `ps auxf` (Windows: `Get-Process \| Select-Object Name, Id, Path`) |
| **5. File System Artifacts** | Hidden files/directories (`.backdoor`), unauthorized SSH `authorized_keys`, webshells (`.php`/`.jsp`) in web roots, or dropped ransomware notes. | `find /var/www -name "*.php" -mtime -2` |
| **6. Suspicious Timestamps** | **Timestomping**—altering MACB (Modified, Accessed, Created, Born) timestamps to match old OS files (e.g., `1999-01-01` or future years) to evade timeline analysis. | `stat /etc/passwd` (Windows: `Get-Item file.exe \| Select-Object CreationTime, LastWriteTime`) |
| **7. Log Manipulation** | Cleared Windows Security logs (**Event ID 1102**), truncated `/var/log/auth.log` (0 bytes), or disabled `auditd` / Sysmon services. | `ls -lh /var/log/auth.log` (Windows: `Get-WinEvent -FilterHashtable @{LogName='Security'; ID=1102}`) |
| **8. Excessive Resource Consumption** | Sudden, sustained 95–100% CPU/GPU usage (unauthorized **cryptomining**), massive disk I/O (ransomware encryption), or saturated outbound bandwidth (DDoS bot). | `top -b -n 1 \| head -n 12` |
| **9. Plaintext Strings** | Hardcoded C2 IP addresses, URLs, registry keys, mutex names, or ransom demands embedded inside compiled binaries. | `strings /bin/ls \| grep -iE "http\|/etc/\|password" \| head -n 10` |
| **10. Account Lockouts** | Sudden spikes in locked-out user accounts (`Event ID 4740` on Windows) indicating active password guessing or misconfigured service accounts. | `grep -i "pam_faillock" /var/log/auth.log` |
| **11. Impossible Travel** | A single user authenticating from two geographically distant locations within a timeframe physically impossible to travel (e.g., Buea, Cameroon at `10:00 UTC` and London, UK at `10:20 UTC`). | Correlate GeoIP city/coordinates + timestamps in SIEM auth logs |
| **12. Concurrent Sessions** | Multiple active simultaneous sessions for the same non-service user account from different IP addresses or devices. | `who` / `w` (Windows: `qwinsta`) |

* **Practical Task (Build a Complete 12-Point Automated IoC Hunter in Python):**
  ```python
  from datetime import datetime

  host_telemetry = {
      "file_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "outbound_ip": "198.51.100.88",
      "dns_query": "xk92mq81z-c2.xyz",
      "process_path": "/dev/shm/.kworker_miner",
      "dropped_file": "/var/www/html/uploads/shell.php",
      "file_created_year": 2031,
      "security_log_size_bytes": 0,
      "cpu_percent": 99.2,
      "extracted_strings": ["Mozilla/5.0", "http://198.51.100"],
      "locked_accounts_last_5m": 14,
      "sessions": [
          {"user": "ambe.fon", "location": "Buea, CM",  "ip": "102.244.10.5", "time": "2026-11-21 13:00"},
          {"user": "ambe.fon", "location": "Tokyo, JP", "ip": "203.0.113.9",  "time": "2026-11-21 13:18"}
      ]
  }

  known_bad_iocs = {"198.51.100.88", "xk92mq81z-c2.xyz"}

  print("=== FULL 12-POINT IoC FORENSIC SCAN ===")
  if host_telemetry["outbound_ip"] in known_bad_iocs or host_telemetry["dns_query"] in known_bad_iocs:
      print(f"[IoC 2 & 3] Malicious C2 IP/Domain matched: {host_telemetry['outbound_ip']} / {host_telemetry['dns_query']}")
  if "/dev/shm/" in host_telemetry["process_path"] or host_telemetry["cpu_percent"] > 95:
      print(f"[IoC 4 & 8] Suspicious hidden process '{host_telemetry['process_path']}' at {host_telemetry['cpu_percent']}% CPU!")
  if host_telemetry["dropped_file"].endswith(".php") and "/uploads/" in host_telemetry["dropped_file"]:
      print(f"[IoC 5] Potential Webshell artifact in upload directory: {host_telemetry['dropped_file']}")
  if host_telemetry["file_created_year"] > 2026:
      print(f"[IoC 6] Timestomping detected: Future creation year ({host_telemetry['file_created_year']})!")
  if host_telemetry["security_log_size_bytes"] == 0:
      print("[IoC 7] Log manipulation detected: Security audit log truncated to 0 bytes!")
  if any("http://" in s for s in host_telemetry["extracted_strings"]):
      print(f"[IoC 9] Plaintext C2 URL found in binary strings: {host_telemetry['extracted_strings'][-1]}")
  if host_telemetry["locked_accounts_last_5m"] >= 5:
      print(f"[IoC 10] Spike in account lockouts: {host_telemetry['locked_accounts_last_5m']} accounts locked!")
  if len(host_telemetry["sessions"]) > 1:
      s1, s2 = host_telemetry["sessions"], host_telemetry["sessions"]
      print(f"[IoC 11 & 12] Concurrent Sessions & Impossible Travel for '{s1['user']}': {s1['location']} -> {s2['location']} in 18 mins!")
  ```

---

## Part F: Application Attacks (6 Types)

| Application Attack | How It Works | Primary Mitigation |
| :--- | :--- | :--- |
| **1. Injection** | Untrusted user input is interpreted as executable commands (**SQLi**, **OS Command Injection**, **XSS**, **LDAP Injection**). | **Parameterized queries (prepared statements)**, strict input validation, context-aware output encoding. |
| **2. Buffer Overflow** | Writing more bytes into a fixed-size memory buffer than allocated, overwriting adjacent stack/heap variables or the return instruction pointer (`EIP`/`RIP`) to hijack execution. | Bounds checking, memory-safe languages (Rust, Python, Go), **ASLR**, **DEP/NX**, stack canaries. |
| **3. Replay Attacks** | Capturing valid authentication frames, API requests, or session tokens off the wire and re-sending them verbatim to impersonate the user. | Cryptographic **nonces** (number used once), strict timestamps, short token TTLs, **TLS**. |
| **4. Privilege Escalation** | **Vertical:** Standard user elevates privileges to `root` / `SYSTEM` (e.g., abusing misconfigured SUID binaries or unquoted service paths). **Horizontal:** User A accesses User B's peer account/data (IDOR). | Principle of Least Privilege, patching kernel/OS vulnerabilities, removing unnecessary SUID bits, server-side authorization checks. |
| **5. Forgery (CSRF / SSRF)** | **CSRF (Cross-Site Request Forgery):** Forces an authenticated user's browser to execute unwanted actions on a trusted site. **SSRF:** Tricks a backend server into making internal HTTP requests (e.g., to cloud metadata `169.254.169.254`). | **CSRF:** Anti-CSRF tokens + `SameSite=Strict` cookies. **SSRF:** URL allow-listing + blocking internal IP ranges. |
| **6. Directory Traversal (Path Traversal)** | Manipulating file path parameters with dot-dot-slash sequences (`../../../../etc/passwd` or `..\..\Windows\win.ini`) to read/write files outside the web root directory. | Canonicalizing file paths, enforcing chroot/base-directory confinement, rejecting `../` sequences. |

* **Practical Task (Audit Linux SUID Binaries & Build a Web Application Attack Detector):**
  1. **Check for Privileged SUID Binaries on Linux (Common Vertical Privilege Escalation Vector):**
     ```bash
     find /usr/bin -perm -4000 2>/dev/null | head -n 15
     ```
  2. **Detect Injection, Directory Traversal & SSRF in HTTP Logs (Python):**
     ```python
     access_logs = [
         'GET /download?doc=../../../../etc/passwd HTTP/1.1',
         'POST /login HTTP/1.1 | body: user=admin\' OR 1=1--&pass=x',
         'GET /fetch?url=http://169.254.169 HTTP/1.1'
     ]

     for log in access_logs:
         if "../" in log or "..\\" in log:
             print(f"[APP ATTACK - DIRECTORY TRAVERSAL] {log}")
         elif "or 1=1" in log.lower() or "union select" in log.lower():
             print(f"[APP ATTACK - SQL INJECTION] {log}")
         elif "169.254.169.254" in log or "127.0.0.1" in log:
             print(f"[APP ATTACK - SSRF] {log}")
     ```

---

## Part G: Credential Attacks (5 Types)

### 1. Password Spraying
* **Concept:** Testing **one or two commonly used passwords** (e.g., `Welcome2026!`, `Password123`) across **many different user accounts** slowly—intentionally staying below per-account lockout thresholds (e.g., 5 failed attempts).
### 2. Brute Force
* **Concept:** Rapidly trying thousands or millions of password combinations (dictionary, hybrid, or exhaustive keyspace) against a **single account** online—or cracking stolen password hashes offline using high-speed GPUs (`Hashcat`).
### 3. User Enumeration
* **Concept:** Probing login, registration, or "Forgot Password" endpoints to harvest valid usernames by comparing distinct error messages (`"User not found"` vs. `"Incorrect password"`) or HTTP response timing differences.
### 4. Replay (Credential / Hash / Ticket Replay)
* **Concept:** Reusing captured authentication material—such as **Pass-the-Hash (PtH)** with NTLM hashes, **Pass-the-Ticket (PtT)** with Kerberos TGTs, or stolen session cookies—to authenticate laterally without cracking the plaintext password.
### 5. MFA Bypass
## Part G: Credential Attacks (5 Types)

> **Exam Tip:** CompTIA Security+ heavily tests how attackers bypass authentication—especially the difference between **Password Spraying** (few passwords $\rightarrow$ many accounts) and **Brute Force** (many passwords $\rightarrow$ one account), as well as how **MFA Bypass** occurs even when MFA is turned on.

---

### 1. Password Spraying
* **Concept:** Trying **one or two common passwords** (e.g., `Welcome2026!`, `Summer2026`, `Password123`) across **hundreds or thousands of different user accounts** slowly over time.
  * *Why attackers use it:* It deliberately avoids triggering per-account lockout thresholds (e.g., locking after 5 failed attempts on a single username).
  * *Primary Mitigations:* Banned/common password lists (blocking predictable seasonal passwords), phishing-resistant MFA, smart lockout / IP rate-limiting, and SIEM correlation across unique target usernames per source IP.

### 2. Brute Force
* **Concept:** Systematically testing a large number of password guesses against a **single target account**:
  * **Online Brute Force:** Sending automated login requests directly to an authentication portal (SSH, RDP, VPN, web login).
  * **Offline Brute Force / Dictionary / Hybrid Attacks:** Stealing password hashes (e.g., from an Active Directory `NTDS.dit` dump or `/etc/shadow`) and cracking them locally on high-speed GPUs using tools like **Hashcat** or **John the Ripper** without network rate limits.
  * *Primary Mitigations:* Account lockout policies (for online attacks), strong salted key-stretching password hashes (`Argon2id`, `bcrypt`, `PBKDF2`) + 14+ character passwords (for offline cracking).

### 3. User Enumeration
* **Concept:** Probing login pages, password-reset forms, or SMTP/LDAP endpoints to discover valid usernames before launching password attacks. Attackers exploit **verbose error messages** (e.g., `"Username does not exist"` vs. `"Incorrect password"`) or **response timing discrepancies** (valid usernames take slightly longer to verify a password hash than nonexistent ones).
  * *Primary Mitigation:* Uniform, generic error responses (`"Invalid username or password"`) and constant-time authentication handling.

### 4. Replay (Credential / Hash / Ticket Replay)
* **Concept:** Capturing valid authentication material off the network or out of system memory (`LSASS`) and re-transmitting it to authenticate without knowing the plaintext password:
  * **Pass-the-Hash (PtH):** Reusing a stolen NTLM password hash to authenticate to remote Windows systems.
  * **Pass-the-Ticket (PtT):** Stealing a valid Kerberos Ticket Granting Ticket (**TGT**) or Service Ticket from memory to impersonate a user laterally.
  * **Session Token Replay:** Reusing a stolen session cookie or OAuth bearer token.
  * *Primary Mitigations:* Cryptographic **nonces** (number used once), short ticket/token lifetimes, Windows Credential Guard, and **TLS** transport encryption.

### 5. MFA Bypass
* **Concept:** Circumventing Multi-Factor Authentication using social engineering, proxy interception, or protocol weaknesses:
  * **MFA Fatigue (Push Bombing):** Flooding a user's mobile authenticator app with dozens of push approval prompts until the user taps "Approve" out of frustration or confusion.
  * **Adversary-in-the-Middle (AiTM) Phishing Proxy:** Using a reverse-proxy phishing kit (e.g., Evilginx) that sits between the victim and the real login page, capturing the username, password, *and* the post-MFA session cookie in real time.
  * **SIM Swapping / SS7 Interception:** Tricking a mobile carrier into porting a victim's phone number to an attacker-controlled SIM card to intercept SMS one-time passcodes.
  * **Legacy Authentication Protocol Downgrade:** Authenticating over older protocols (`IMAP`, `POP3`, `SMTP Basic Auth`) that do not support modern MFA challenges.
  * *Primary Mitigation:* **Phishing-resistant MFA** (**FIDO2 / WebAuthn hardware security keys** or cryptographic **Passkeys**, which bind authentication to the exact legitimate domain origin) and disabling legacy authentication protocols.

---

### Practical Task 1: Build a Unified 5-Vector Credential Attack Detector in Python
Run this script to detect **Password Spraying**, **Brute Force**, **User Enumeration**, **Credential Replay**, and **MFA Fatigue / Bypass** from authentication logs:

```python
from collections import defaultdict

auth_logs = [
    # 1. User Enumeration (Probing usernames via password reset endpoint)
    {"ip": "198.51.100.12", "user": "test1",   "event": "PWD_RESET", "response": "User not found"},
    {"ip": "198.51.100.12", "user": "test2",   "event": "PWD_RESET", "response": "User not found"},
    {"ip": "198.51.100.12", "user": "finance", "event": "PWD_RESET", "response": "Reset link sent"},

    # 2. Password Spraying (1 attempt each across 4 distinct accounts)
    {"ip": "45.33.32.10",   "user": "alice",   "event": "LOGIN_FAIL", "response": "Bad password"},
    {"ip": "45.33.32.10",   "user": "bob",     "event": "LOGIN_FAIL", "response": "Bad password"},
    {"ip": "45.33.32.10",   "user": "charlie", "event": "LOGIN_FAIL", "response": "Bad password"},
    {"ip": "45.33.32.10",   "user": "david",   "event": "LOGIN_FAIL", "response": "Bad password"},

    # 3. Single-Account Brute Force (5 rapid failures against 'admin')
    {"ip": "203.0.113.88",  "user": "admin",   "event": "LOGIN_FAIL", "response": "Bad password"},
    {"ip": "203.0.113.88",  "user": "admin",   "event": "LOGIN_FAIL", "response": "Bad password"},
    {"ip": "203.0.113.88",  "user": "admin",   "event": "LOGIN_FAIL", "response": "Bad password"},
    {"ip": "203.0.113.88",  "user": "admin",   "event": "LOGIN_FAIL", "response": "Bad password"},
    {"ip": "203.0.113.88",  "user": "admin",   "event": "LOGIN_FAIL", "response": "Bad password"},

    # 4. Credential / Session Replay (Same token replayed simultaneously from two continents)
    {"ip": "102.244.12.5",  "user": "ambe",    "event": "TOKEN_USE",  "response": "TokenID=TOK-99182 (Cameroon)"},
    {"ip": "185.220.101.9", "user": "ambe",    "event": "TOKEN_USE",  "response": "TokenID=TOK-99182 (Germany)"},

    # 5. MFA Bypass via Push Fatigue (3 rapid denials followed by approval)
    {"ip": "91.132.44.10",  "user": "cfo",     "event": "MFA_PUSH",   "response": "DENIED"},
    {"ip": "91.132.44.10",  "user": "cfo",     "event": "MFA_PUSH",   "response": "DENIED"},
    {"ip": "91.132.44.10",  "user": "cfo",     "event": "MFA_PUSH",   "response": "DENIED"},
    {"ip": "91.132.44.10",  "user": "cfo",     "event": "MFA_PUSH",   "response": "APPROVED"}
]

failed_by_ip = defaultdict(list)
enum_by_ip = defaultdict(int)
token_ips = defaultdict(set)
mfa_denials = defaultdict(int)

print("=== CREDENTIAL ATTACK DETECTION ENGINE ===")
for log in auth_logs:
    if log["event"] == "PWD_RESET":
        enum_by_ip[log["ip"]] += 1
        if "Reset link sent" in log["response"] and enum_by_ip[log["ip"]] >= 3:
            print(f"[3. USER ENUMERATION] {log['ip']} enumerated valid account '{log['user']}' via verbose responses!")

    elif log["event"] == "LOGIN_FAIL":
        failed_by_ip[log["ip"]].append(log["user"])

    elif log["event"] == "TOKEN_USE":
        tok = log["response"].split()
        token_ips[tok].add(log["ip"])
        if len(token_ips[tok]) > 1:
            print(f"[4. CREDENTIAL/TOKEN REPLAY] {tok} replayed across multiple IPs: {token_ips[tok]}")

    elif log["event"] == "MFA_PUSH":
        if log["response"] == "DENIED":
            mfa_denials[log["user"]] += 1
        elif log["response"] == "APPROVED" and mfa_denials[log["user"]] >= 3:
            print(f"[5. MFA BYPASS / PUSH FATIGUE] '{log['user']}' approved MFA after {mfa_denials[log['user']]} denials from {log['ip']}!")

for ip, users in failed_by_ip.items():
    if len(set(users)) >= 4:
        print(f"[1. PASSWORD SPRAYING] {ip} tested passwords across {len(set(users))} unique accounts!")
    elif len(users) >= 5 and len(set(users)) == 1:
        print(f"[2. BRUTE FORCE] {ip} hammered single account '{users}' {len(users)} times!")
```

---

### Practical Task 2: Fix a User Enumeration Vulnerability in Python
Compare how verbose authentication error messages leak valid usernames vs. uniform secure error handling:

```python
users_db = {"alice": "hashed_pw_123", "ambe": "hashed_pw_456"}

# VULNERABLE: Reveals whether the username exists in the database
def login_vulnerable(username, password):
    if username not in users_db:
        return "Error: Username does not exist."
    if users_db[username] != password:
        return "Error: Incorrect password for this user."
    return "Login successful."

# SECURE REMEDIATION: Returns the exact same generic error message regardless of failure reason
def login_secure(username, password):
    if username not in users_db or users_db[username] != password:
        return "Error: Invalid username or password."
    return "Login successful."

print("Vulnerable Output:", login_vulnerable("unknown_user", "1234"))
print("Secure Output    :", login_secure("unknown_user", "1234"))
```

---

### Objective 2.5 Completion Checklist
- [ ] Differentiated all **10 Malware types** and scripted detections for **Ransomware shadow-copy deletion** and **Fileless PowerShell**.
- [ ] Reviewed **Physical Attacks** (Tailgating, Shoulder Surfing, Skimming, Forced Entry) and **Social Engineering** lures (Phishing, Spear Phishing, Whaling, Smishing, Vishing, Quishing, Impersonation, Deepfakes).
- [ ] Built a 12-point forensic triage script covering all **Indicators of Compromise (IoCs)** (Hashes, C2 IPs/Domains, Hidden Processes, Timestomping, Log Clearing, Resource Spikes, Strings, Lockouts, Impossible Travel, Concurrent Sessions).
### Objective 2.5 Completion Checklist
- [ ] Differentiated all **10 Malware types** (Viruses, Worms, Trojans, Ransomware, Spyware, Adware, Rootkits, Keyloggers, Logic Bombs, Fileless Malware) and scripted detections for **Ransomware shadow-copy deletion** and **Fileless PowerShell**.
- [ ] Identified all **4 Physical Attacks** (Tailgating, Shoulder Surfing, Skimming, Forced Entry) and matched each to physical countermeasures (mantraps, privacy filters, tamper-evident overlays, bollards).
- [ ] Analyzed all **8 Network Attacks** (DDoS, Protocol Downgrade, Rogue Devices, Packet Sniffing, Spoofing, On-Path Attacks, DNS Attacks, Cache Poisoning) and checked local ARP tables for spoofing indicators.
- [ ] Classified all **8 Social Engineering vectors** (Phishing, Spear Phishing, Whaling, Smishing, Vishing, Quishing, Impersonation, Deepfakes) and built a header/urgency lure scanner.
- [ ] Built a 12-point forensic triage script covering all **Indicators of Compromise (IoCs)** (File Hashes, Suspicious IPs, Malicious Domains, Malicious Processes, File System Artifacts, Suspicious Timestamps, Log Manipulation, Excessive Resource Consumption, Plaintext Strings, Account Lockouts, Impossible Travel, Concurrent Sessions).
- [ ] Implemented detection and remediation logic for all **6 Application Attacks** (Injection, Buffer Overflow, Replay Attacks, Privilege Escalation, Forgery, Directory Traversal).
- [ ] Built a unified detector and remediation for all **5 Credential Attacks** (**Password Spraying**, **Brute Force**, **User Enumeration**, **Credential/Token Replay**, and **MFA Bypass**).

---

## Quick-Reference Exam Matrix: Attack Indicator $\rightarrow$ Primary Mitigation

| Category | Indicator / Attack Scenario | Best Security+ Mitigation |
| :--- | :--- | :--- |
| **Malware** | Encoded in-memory PowerShell (`-Enc`) without disk artifacts | Behavioral **EDR**, PowerShell Script Block Logging, Constrained Language Mode |
| **Malware** | Mass file encryption + `vssadmin delete shadows` | Offline/immutable backups, EDR ransomware rollback, least privilege |
| **Network** | Duplicate MAC addresses in `arp -a` (On-Path ARP Spoofing) | **Dynamic ARP Inspection (DAI)**, DHCP Snooping, TLS encryption |
| **Network** | Users redirected to fake banking IP despite typing valid URL | **DNSSEC**, DNS over HTTPS (DoH), TLS certificate validation |
| **Social Eng.** | Executive deepfake voice call requesting urgent wire transfer | Out-of-band callback verification using a known trusted phone number |
| **IoC** | User logs in from Buea and London within 15 minutes | Conditional Access **Impossible Travel** policy + session token revocation |
| **Application** | `GET /download?file=../../../../etc/passwd` | Canonical path validation, chroot/container isolation, input sanitization |
| **Credential** | 1 password guessed across 200 accounts without triggering lockouts | **Password Spraying** $\rightarrow$ Phishing-resistant **FIDO2 MFA** + smart lockout |
| **Credential** | User tricked into approving push notification after 10 rapid prompts | **MFA Fatigue** $\rightarrow$ **Number Matching** or FIDO2 hardware keys |
