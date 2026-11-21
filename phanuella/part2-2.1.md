# CompTIA Security+ (SY0-701) – Practical Lab Guide
## Domain 2: Threats, Vulnerabilities, and Mitigations (22%–24%)
### Objective 2.1: Characteristics of Threats and Vulnerabilities

> **Objective:** Collect and operationalize threat intelligence, query CVE/CVSS databases, identify common vulnerability classes, and prioritize remediation based on likelihood, impact, and severity.  
> **Recommended Lab Tools:** Python 3 (`urllib`, `json`), `curl`, `nmap` (with NSE vuln scripts), Linux Terminal / Windows PowerShell.

---

### 1. Threat Intelligence
* **Concept:** Evidence-based knowledge (context, mechanisms, indicators of compromise [IoCs], tactics, techniques, and procedures [TTPs]) used to inform security decisions. Categorized into **Strategic** (executive risk trends), **Tactical** (attacker TTPs / MITRE ATT&CK), **Operational** (specific campaign details), and **Technical** (hashes, malicious IPs, domains).
* **Practical Task (Map Technical IoCs to Tactical MITRE ATT&CK Behavior in Python):**
  ```python
  threat_intel_report = {
      "campaign": "Operation ShadowRelay",
      "technical_iocs": {
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "c2_domain": "update-cdn-service[.]net",
          "malicious_ip": "198.51.100.88"
      },
      "tactical_ttp": "T1059.001 - PowerShell Encoded Command Execution"
  }
  print(f"Campaign: {threat_intel_report['campaign']} | TTP: {threat_intel_report['tactical_ttp']}")
  ```

### 2. Threat Feeds
* **Concept:** Continuous, machine-readable streams of real-time threat data (STIX/TAXII, JSON, CSV) ingested by SIEMs, firewalls, and EDRs to block known malicious IPs, domains, and file hashes automatically.
* **Practical Task (Fetch & Parse a Live Open-Source Threat Feed — Feodo Tracker Botnet C2 IPs):**
  ```bash
  # Download a real-world public C2 IP blocklist and inspect the top 10 malicious IPs
  curl -s https://abuse.ch | grep -v "^#" | head -n 10
  ```

### 3. Threat Likelihood & 4. Threat Impact
* **Concept:** Risk calculation components ($\text{Risk} = \text{Likelihood} \times \text{Impact}$):
  * **Threat Likelihood:** Probability that a threat actor will successfully exploit a vulnerability (driven by public exploit availability, internet exposure, and attacker motivation).
  * **Threat Impact:** Magnitude of business, financial, operational, or reputational harm if exploitation succeeds (data breach, ransomware downtime, safety risk).
* **Practical Task (Build a Risk Scoring Matrix Script in Python):**
  ```python
  vulnerabilities = [
      {"asset": "Public-Web-Server", "cve": "CVE-2024-3094", "likelihood": 5, "impact": 5},
      {"asset": "Internal-Print-Host", "cve": "CVE-2023-1111", "likelihood": 2, "impact": 2},
      {"asset": "Core-Finance-DB", "cve": "CVE-2024-9999", "likelihood": 3, "impact": 5}
  ]

  for v in vulnerabilities:
      risk_score = v["likelihood"] * v["impact"]
      priority = "IMMEDIATE" if risk_score >= 15 else "SCHEDULED"
      print(f"{v['asset']:<20} | {v['cve']} | Risk Score: {risk_score:>2}/25 | Action: {priority}")
  ```

### 5. Intelligence Sources
* **Concept:** Where organizations obtain threat data:
  * **OSINT (Open-Source Intelligence):** Publicly accessible feeds, CERT advisories, CISA KEV (Known Exploited Vulnerabilities), GitHub, VirusTotal, Shodan.
  * **ISACs (Information Sharing and Analysis Centers):** Sector-specific trusted sharing groups (FS-ISAC for finance, H-ISAC for healthcare).
  * **Commercial / Proprietary Feeds:** Paid vendor intelligence (Recorded Future, Mandiant, CrowdStrike).
  * **Dark Web / Closed Forums:** Underground marketplaces monitored for leaked credentials and zero-day chatter.
* **Practical Task (Query CISA's Live Known Exploited Vulnerabilities [KEV] JSON Catalog):**
  ```python
  import urllib.request, json

  url = "https://cisa.gov"
  req = urllib.request.Request(url, headers={"User-Agent": "SecPlus-Lab/1.0"})
  with urllib.request.urlopen(req, timeout=10) as resp:
      data = json.loads(resp.read().decode())
      print("Total CISA KEV Active Exploits:", len(data["vulnerabilities"]))
      latest = data["vulnerabilities"][-1]
      print(f"Latest Entry: {latest['cveID']} - {latest['vendorProject']} {latest['product']}")
  ```

### 6. Threat Intelligence Lifecycle
* **Concept:** The 6-stage continuous intelligence cycle:
  1. **Direction / Requirements:** Define what assets and threats matter most.
  2. **Collection:** Gather raw logs, OSINT feeds, and telemetry.
  3. **Processing:** Normalize, deduplicate, and format raw data (e.g., into STIX/JSON).
  4. **Analysis:** Correlate indicators to identify campaigns and false positives.
  5. **Dissemination:** Deliver actionable alerts/reports to SOC, firewall teams, and executives.
  6. **Feedback:** Review effectiveness and refine collection requirements.
* **Practical Task:**
  1. Simulate Stages 2–5 in Bash by downloading a raw IP feed (**Collection**), stripping comments/duplicates (**Processing**), matching against a simulated firewall log (**Analysis**), and generating an alert file (**Dissemination**):
     ```bash
     echo -e "192.168.1.5\n198.51.100.88\n8.8.8.8" > local_connections.txt
     echo "198.51.100.88" > threat_feed.txt
     grep -Fxf threat_feed.txt local_connections.txt > soc_alert.txt && cat soc_alert.txt
     ```

### 7. Vulnerability Identification
* **Concept:** Proactively discovering security weaknesses via **Authenticated vs. Unauthenticated Vulnerability Scans** (Nessus, OpenVAS, Qualys), **Software Composition Analysis (SCA)**, **Static/Dynamic Code Analysis (SAST/DAST)**, and **Penetration Testing**.
* **Practical Task (Run a Local Service & Vulnerability Enumeration Scan with `nmap`):**
  ```bash
  # Scan localhost to identify open ports, exact service versions, and run default safe NSE scripts
  nmap -sV -sC 127.0.0.1
  ```

### 8. Vulnerability Prioritization
* **Concept:** Ranking which vulnerabilities to patch first when resources are limited—combining **CVSS base score**, **active exploitation status (CISA KEV / EPSS)**, **internet exposure (attack surface)**, and **asset criticality**.
* **Practical Task (Prioritize Patching Order Using Exposure + Active Exploit Context in Python):**
  ```python
  findings = [
      {"cve": "CVE-2024-0001", "cvss": 9.8, "internet_exposed": False, "actively_exploited": False},
      {"cve": "CVE-2024-0002", "cvss": 8.1, "internet_exposed": True,  "actively_exploited": True}
  ]

  # CVE-2024-0002 has a lower raw CVSS (8.1 vs 9.8) but is internet-facing AND actively exploited!
  prioritized = sorted(findings, key=lambda x: (x["actively_exploited"], x["internet_exposed"], x["cvss"]), reverse=True)
  print("Patch First:", prioritized["cve"], "| Reason: Actively Exploited + Internet Exposed")
  ```

### 9. Common Vulnerabilities and Exposures (CVE)
* **Concept:** A standardized, publicly disclosed dictionary of unique identifiers (`CVE-YEAR-NUMBER`, e.g., `CVE-2021-44228` for Log4Shell) maintained by MITRE and the NVD so security tools and teams reference the exact same flaw unambiguously.
* **Practical Task (Query the Official NVD [National Vulnerability Database] REST API for a Specific CVE):**
  ```bash
  curl -s "https://nist.gov" | \
    python3 -m json.tool | grep -E '"id":|"baseScore":|"baseSeverity":' | head -n 6
  ```

### 10. Common Vulnerability Scoring System (CVSS)
* **Concept:** An open industry standard (`0.0` to `10.0`) quantifying vulnerability technical severity using **Base Metrics** (Exploitability: Attack Vector `AV`, Attack Complexity `AC`, Privileges Required `PR`, User Interaction `UI`; Scope `S`; Impact: Confidentiality `C`, Integrity `I`, Availability `A`), plus **Temporal** and **Environmental** metric groups.
* **Practical Task (Decode a CVSS v3.1 Vector String in Python):**
  ```python
  vector = "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"
  meanings = {
      "AV:N": "Attack Vector: Network (Remotely exploitable over Internet)",
      "AC:L": "Attack Complexity: Low (Easy to exploit)",
      "PR:N": "Privileges Required: None (Unauthenticated)",
      "UI:N": "User Interaction: None (Zero-click)",
      "C:H":  "Confidentiality Impact: High",
      "I:H":  "Integrity Impact: High",
      "A:H":  "Availability Impact: High"
  }
  for token in vector.split("/")[1:]:
      if token in meanings:
          print(f"  {token:<6} -> {meanings[token]}")
  ```

### 11. Vulnerability Types
### 11. Vulnerability Types
* **Concept:** CompTIA Security+ requires recognizing distinct vulnerability classes, how attackers exploit them, and how engineers remediate them:
  * **Zero-Day Vulnerability:** A previously unknown flaw discovered by attackers before the vendor knows about it or releases a patch (mitigated via defense-in-depth, behavioral EDR, and microsegmentation).
  * **Buffer Overflow / Memory Corruption:** Writing more data into a fixed-length memory buffer than it can hold, overwriting adjacent stack/heap memory or instruction pointers (mitigated via memory-safe languages like Rust/Python, bounds checking, **ASLR**, and **DEP/NX**).
  * **Injection Vulnerabilities (SQLi, OS Command Injection, XSS, LDAPi):** Untrusted user input is concatenated directly into an interpreter command without sanitization or parameterization.
  * **Race Condition (TOCTOU — Time-of-Check to Time-of-Use):** A flaw where a system checks a security condition (e.g., file ownership/permissions) and then uses the resource later, giving an attacker a brief millisecond window to swap or alter the resource in between.
  * **Cryptographic Weaknesses:** Hardcoded keys, weak hashing (`MD5`/`SHA-1`), deprecated protocols (`TLS 1.0/1.1`, `SMBv1`), or improper certificate validation.
  * **Misconfiguration, Default Credentials & End-of-Life (EOL) Software:** Unchanged factory passwords, open cloud storage buckets, or unsupported OS versions no longer receiving security patches.

* **Practical Task 1 (SQL Injection: Vulnerable String Concatenation vs. Secure Parameterized Query):**
  Run this local SQLite demo in Python to see how unvalidated input bypasses authentication—and how **Parameterized Queries (Prepared Statements)** completely neutralize it:
  ```python
  import sqlite3

  conn = sqlite3.connect(":memory:")
  cursor = conn.cursor()
  cursor.execute("CREATE TABLE users (username TEXT, role TEXT)")
  cursor.execute("INSERT INTO users VALUES ('admin', 'Administrator'), ('guest', 'ReadOnly')")

  malicious_input = "' OR '1'='1"

  # 1. VULNERABLE QUERY (String formatting allows SQL Injection!)
  vuln_sql = f"SELECT * FROM users WHERE username = '{malicious_input}'"
  print("Vulnerable SQL Result:", cursor.execute(vuln_sql).fetchall())

  # 2. SECURE REMEDIATION (Parameterized query treats input strictly as literal data)
  safe_sql = "SELECT * FROM users WHERE username = ?"
  print("Secure SQL Result    :", cursor.execute(safe_sql, (malicious_input,)).fetchall())
  ```

* **Practical Task 2 (OS Command Injection: `shell=True` vs. `shell=False` Argument List):**
  ```python
  import subprocess

  # Suppose a web diagnostic tool accepts an IP address from a user:
  attacker_payload = "127.0.0.1; echo PWNED_VIA_COMMAND_INJECTION"

  # VULNERABLE PATTERN (Never do this):
  # subprocess.run("ping -c 1 " + attacker_payload, shell=True)

  # SECURE REMEDIATION (shell=False passes the payload as a single literal argument to ping):
  result = subprocess.run(["ping", "-c", "1", attacker_payload], shell=False, capture_output=True, text=True)
  print("Return Code:", result.returncode)
  print("Error Output (Injection Blocked):", result.stderr.strip())
  ```

* **Practical Task 3 (Audit a Configuration for Default Credentials & Weak Crypto):**
  ```python
  app_config = {
      "admin_user": "admin",
      "admin_pass": "admin",
      "tls_min_version": "TLSv1.0",
      "password_hash_algo": "MD5"
  }

  if app_config["admin_user"] == app_config["admin_pass"]:
      print("[VULN - DEFAULT CREDS] Username and password are identical ('admin')!")
  if app_config["tls_min_version"] in ["SSLv3", "TLSv1.0", "TLSv1.1"]:
      print(f"[VULN - DEPRECATED PROTOCOL] {app_config['tls_min_version']} is insecure!")
  if app_config["password_hash_algo"] in ["MD5", "SHA1"]:
      print(f"[VULN - WEAK HASH] {app_config['password_hash_algo']} is collision-vulnerable!")
  ```

---

### 12. Vulnerability Severity
* **Concept:** Qualitative severity ratings standardized by **CVSS v3.x / v4.0** (`0.0` to `10.0`) that dictate organizational **Service Level Agreements (SLAs)** for remediation timelines and executive risk reporting:

| CVSS Base Score Range | Severity Rating | Typical Enterprise Remediation SLA |
| :--- | :--- | :--- |
| **`0.0`** | **None (Informational)** | Best effort / Next major release |
| **`0.1 – 3.9`** | **Low** | 60 – 90 Days |
| **`4.0 – 6.9`** | **Medium** | 30 Days |
| **`7.0 – 8.9`** | **High** | 7 – 14 Days |
| **`9.0 – 10.0`** | **Critical** | 24 – 72 Hours (Emergency Change) |

* **Practical Task (Automated Vulnerability Triage & SLA Deadline Calculator in Python):**
  ```python
  from datetime import datetime, timedelta

  scan_findings = [
      {"cve": "CVE-2024-3094", "asset": "Internet-SSH-Gateway", "cvss": 10.0, "kev": True},
      {"cve": "CVE-2024-21626", "asset": "Prod-Docker-Host",    "cvss": 8.6,  "kev": True},
      {"cve": "CVE-2023-48795", "asset": "Internal-Build-Node", "cvss": 5.9,  "kev": False},
      {"cve": "CVE-2022-0001",  "asset": "Dev-Sandbox-VM",      "cvss": 3.1,  "kev": False}
  ]

  def evaluate_finding(item):
      score = item["cvss"]
      if score >= 9.0:
          severity, sla_days = "CRITICAL", 2
      elif score >= 7.0:
          severity, sla_days = "HIGH", 7
      elif score >= 4.0:
          severity, sla_days = "MEDIUM", 30
      elif score > 0.0:
          severity, sla_days = "LOW", 90
      else:
          severity, sla_days = "NONE", 180

      # Escalate SLA by 50% if listed on CISA Known Exploited Vulnerabilities (KEV)
      if item["kev"] and sla_days > 2:
          sla_days = max(2, sla_days // 2)

      due_date = (datetime.now() + timedelta(days=sla_days)).strftime("%Y-%m-%d")
      return severity, sla_days, due_date

  print(f"{'CVE ID':<16} | {'Asset':<22} | {'CVSS':<4} | {'Severity':<8} | {'KEV':<5} | {'Due Date'}")
  print("-" * 78)
  for f in scan_findings:
      sev, days, due = evaluate_finding(f)
      print(f"{f['cve']:<16} | {f['asset']:<22} | {f['cvss']:<4.1f} | {sev:<8} | {str(f['kev']):<5} | {due} ({days}d)")
  ```

---

### Objective 2.1 Completion Checklist
- [ ] Fetched and parsed live **Threat Feeds** (Feodo Tracker) and **OSINT** (CISA KEV JSON catalog).
- [ ] Modeled the 6-stage **Threat Intelligence Lifecycle** from collection to SOC dissemination.
- [ ] Queried the **NVD API** for a specific **CVE** and decoded a **CVSS v3.1 Vector String** (`AV:N/AC:L/PR:N...`).
- [ ] Demonstrated **SQL Injection** and **OS Command Injection** vulnerabilities vs. secure parameterized/list-argument remediations in Python.
- [ ] Built an automated **Vulnerability Severity & SLA Triage** script combining CVSS scores with CISA KEV active exploitation status.

