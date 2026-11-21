# Part 3 – Practical Security+ Laboratory Syllabus
## Module 3: Vulnerability Assessment Laboratory

> **Lab Environment:** Linux VM (Ubuntu/Kali) + Windows VM in VirtualBox, `nmap` (with NSE scripts), `curl`, Python 3 (`urllib`, `json`, `re`, `datetime`), OpenSSL.  
> **Rules of Engagement Warning:** Only execute discovery and vulnerability scans against `127.0.0.1` or your isolated VirtualBox lab network (`10.x.x.x` / `192.168.x.x`).

---

### Lab 1: Asset Discovery
* **Objective:** Identify all live hosts, MAC addresses, operating systems, and listening network interfaces on your lab segment to build an accurate scan scope before launching vulnerability checks.
* **Hands-On Steps:**
  ```bash
  mkdir -p ~/vuln_lab && cd ~/vuln_lab

  # 1. Perform host discovery (-sn) on loopback/local lab subnet and export XML/greppable output
  nmap -sn 127.0.0.0/30 -oG discovered_hosts.gnmap
  grep "Status: Up" discovered_hosts.gnmap

  # 2. Check local ARP/Neighbor table to spot any uninventoried devices on your LAN segment
  ip neigh show
  ```

---

### Lab 2: Vulnerability Scanning
* **Objective:** Run service-version detection (`-sV`) and Nmap Scripting Engine (`--script vuln`) checks against an authorized local test service to uncover outdated software versions and missing security headers.
* **Hands-On Steps:**
  ```bash
  # 1. Start a temporary local Python HTTP server on port 8080 as a safe scan target
  python3 -m http.server 8080 --bind 127.0.0.1 >/dev/null 2>&1 &
  TARGET_PID=$!
  sleep 1

  # 2. Run Nmap version detection + HTTP security header & enum NSE scripts
  nmap -sV -p 8080 --script=http-headers,http-methods,http-enum 127.0.0.1 -oN scan_results.txt
  cat scan_results.txt

  # Stop temporary test server
  kill $TARGET_PID 2>/dev/null || true
  ```

---

### Lab 3: Vulnerability Classification
* **Objective:** Categorize raw scanner findings into standardized vulnerability classes (**Missing Security Headers**, **Deprecated Cryptographic Protocols**, **Default Credentials**, **Outdated Packages**, **Unnecessary Open Ports**) so engineering teams can route fixes efficiently.
* **Hands-On Steps (Classify Raw Findings in Python):**
  ```python
  raw_findings = [
      {"port": 8080, "issue": "Missing X-Frame-Options & HSTS Headers", "category": "Web Misconfiguration"},
      {"port": 22,   "issue": "PermitRootLogin enabled in sshd_config", "category": "Identity / Access Control"},
      {"port": 443,  "issue": "Server accepts deprecated TLSv1.0",       "category": "Cryptographic Weakness"},
      {"port": 21,   "issue": "Cleartext FTP service active",           "category": "Insecure Legacy Protocol"}
  ]

  for f in raw_findings:
      print(f"Port {f['port']:<4} | Category: {f['category']:<28} | Finding: {f['issue']}")
  ```

---

### Lab 4: CVE Research (NVD REST API & CISA KEV)
* **Objective:** Look up authoritative vulnerability descriptions, affected software versions (CPEs), and active exploitation status using the official **NIST National Vulnerability Database (NVD)** API and **CISA KEV** catalog.
* **Hands-On Steps:**
  ```bash
  # Query the NIST NVD 2.0 REST API for CVE-2024-3094 (XZ Utils backdoor)
  curl -s "https://nist.gov" | \
    python3 -c '
  import sys, json
  data = json.load(sys.stdin)
  vuln = data["vulnerabilities"]["cve"]
  print("CVE ID     :", vuln["id"])
  print("Published  :", vuln["published"])
  print("Description:", vuln["descriptions"]["value"][:180] + "...")
  '
  ```

---

### Lab 5: CVSS Scoring (Vector Parsing & Severity Calculation)
* **Objective:** Parse a **CVSS v3.1 Vector String** to understand how **Attack Vector (`AV`)**, **Attack Complexity (`AC`)**, **Privileges Required (`PR`)**, **User Interaction (`UI`)**, and **CIA Impact (`C/I/A`)** produce severity scores (`0.0–10.0`).
* **Hands-On Steps (Build a CVSS Vector Decoder in Python):**
  ```python
  cvss_vector = "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H"
  lookup = {
      "AV:N": "Network (Remotely exploitable)",
      "AV:L": "Local access required",
      "AC:L": "Low complexity (No special conditions)",
      "PR:N": "No privileges required (Unauthenticated)",
      "UI:N": "No user interaction required (Zero-click)",
      "S:C":  "Scope Changed (Impacts resources beyond vulnerable component)",
      "C:H":  "Confidentiality Impact: HIGH",
      "I:H":  "Integrity Impact: HIGH",
      "A:H":  "Availability Impact: HIGH"
  }

  print(f"Analyzing Vector: {cvss_vector}")
  for metric in cvss_vector.split("/")[1:]:
      if metric in lookup:
          print(f"  {metric:<5} -> {lookup[metric]}")
  ```

---

### Lab 6: False-Positive Identification
* **Objective:** Manually verify automated scanner alerts to filter out **False Positives** (e.g., Linux distributions like Debian/Ubuntu backporting security patches while keeping the older upstream version number in the service banner).
* **Hands-On Steps (Verify Debian/Ubuntu Backported CVE Patch Status):**
  ```bash
  # Check installed OpenSSH version vs. distribution security changelog (backported patches)
  ssh -V
  apt-cache policy openssh-server 2>/dev/null | head -n 6
  ```
  * **Analyst Rule:** If an unauthenticated scanner flags `OpenSSH 8.9p1` solely by reading its TCP banner, inspect `apt-cache policy` or `/usr/share/doc/openssh-server/changelog.Debian.gz` to verify whether the vendor already applied the security patch—documenting it as a **False Positive** with package version proof.

---

### Lab 7: Vulnerability Prioritization
* **Objective:** Rank verified vulnerabilities into a realistic patching queue by combining **CVSS Base Score**, **CISA KEV Active Exploitation**, **External Internet Exposure**, and **Asset Criticality**.
* **Hands-On Steps (Run a Contextual Prioritization Engine in Python):**
  ```python
  verified_vulns = [
      {"cve": "CVE-2024-9001", "host": "Internal-Test-VM",   "cvss": 9.8, "internet_facing": False, "actively_exploited": False},
      {"cve": "CVE-2024-9002", "host": "Public-API-Gateway", "cvss": 8.1, "internet_facing": True,  "actively_exploited": True},
      {"cve": "CVE-2024-9003", "host": "Staff-Print-Server", "cvss": 5.3, "internet_facing": False, "actively_exploited": False}
  ]

  ranked = sorted(
      verified_vulns,
      key=lambda x: (x["actively_exploited"], x["internet_facing"], x["cvss"]),
      reverse=True
  )

  print("=== PRIORITIZED REMEDIATION QUEUE ===")
  for idx, v in enumerate(ranked, 1):
      print(f"#{idx} | {v['cve']} | Host: {v['host']:<20} | CVSS: {v['cvss']} | Exploited: {v['actively_exploited']} | Public: {v['internet_facing']}")
  ```

---

### Lab 8: Remediation
* **Objective:** Apply concrete technical fixes—upgrading vulnerable packages, disabling insecure services/protocols, and hardening configurations under Change Management control.
* **Hands-On Steps:**
  ```bash
  # 1. Apply OS security updates on Debian/Ubuntu (or simulate package upgrade)
  # sudo apt update && sudo apt upgrade -y openssh-server

  # 2. Remediate a configuration vulnerability: enforce strong file permissions & disable root SSH login
  mkdir -p ~/vuln_lab/remediation_demo
  echo "PermitRootLogin yes" > ~/vuln_lab/remediation_demo/sshd_test.conf
  sed -i 's/PermitRootLogin yes/PermitRootLogin no/' ~/vuln_lab/remediation_demo/sshd_test.conf
  cat ~/vuln_lab/remediation_demo/sshd_test.conf
  ```

---

### Lab 9: Verification (Rescanning & Regression Testing)
* **Objective:** Confirm that every applied remediation closed the vulnerability without breaking service functionality before closing the remediation ticket.
* **Hands-On Steps:**
  ```bash
  # Verify configuration fix is active and service passes syntax validation
  grep -q "^PermitRootLogin no" ~/vuln_lab/remediation_demo/sshd_test.conf && \
    echo "[VERIFIED - CLOSED] PermitRootLogin is disabled. Safe to close remediation ticket."
  ```

---

### Lab 10: Security Reporting (Executive & Technical Assessment Report)
* **Objective:** Compile discovery scope, verified findings, false-positive exclusions, prioritized SLA timelines, and remediation verification evidence into a structured Markdown/JSON report.
* **Hands-On Steps (Generate an Automated Vulnerability Assessment Report in Python):**
  ```python
  import json
  from datetime import datetime, timezone

  assessment_report = {
      "report_title": "Internal Lab Vulnerability Assessment Report",
      "assessment_date_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
      "scope": ["127.0.0.1", "10.0.2.0/24"],
      "executive_summary": {
          "total_scanned_hosts": 2,
          "critical_findings": 0,
          "high_findings": 1,
          "medium_findings": 2,
          "false_positives_filtered": 1
      },
      "verified_findings": [
          {
              "id": "VULN-001",
              "title": "SSH Root Login Permitted",
              "cvss_score": 7.5,
              "severity": "HIGH",
              "remediation": "Set PermitRootLogin no in /etc/ssh/sshd_config",
              "status": "REMEDIATED & VERIFIED"
          }
      ]
  }

  with open("vuln_assessment_report.json", "w") as f:
      json.dump(assessment_report, f, indent=2)

  print(json.dumps(assessment_report, indent=2))
  ```

---

### Module 3 Lab Completion Checklist
- [ ] Executed **Asset Discovery** (`nmap -sn`, `ip neigh`) and **Service/Header Vulnerability Scanning** (`nmap -sV --script`).
