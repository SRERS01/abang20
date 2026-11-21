# Part 3 – Practical Security+ Laboratory Syllabus
## Module 7: Security Monitoring and Incident Response Laboratory

> **Lab Environment:** Linux VM (Ubuntu) + Windows Endpoint/Server VM in VirtualBox, **Splunk Free / Wazuh**, **Security Onion** (or `tcpdump`/Zeek), **Velociraptor**, **Sysmon**, Python 3, Bash/PowerShell.  
> **Safety Best Practice:** Isolate lab VMs on a Host-Only / Internal VirtualBox network (`10.50.0.0/24`) before detonating simulated attack artifacts.

---

### Lab 1: Collect System Logs (Sysmon, Wazuh Agent & Syslog Forwarding)
* **Objective:** Configure deep endpoint and OS telemetry collection using **Sysmon** (Windows) and **rsyslog / Wazuh Agent** (Linux) so process creations, network sockets, and registry edits stream centrally into **Splunk / Wazuh**.
* **Hands-On Steps:**
  * **Windows Endpoint (Install Sysmon with SwiftOnSecurity / Olaf Hartong Modular Config):**
    ```powershell
    # Verify Sysmon service is running and generating Event IDs 1 (Process Create) & 3 (Network Connect)
    Get-Service -Name Sysmon64 -ErrorAction SilentlyContinue
    Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-Sysmon/Operational'; ID=1} -MaxEvents 5 |
      Select-Object TimeCreated, Id, Message
    ```
  * **Linux Endpoint (Verify `rsyslog` / `auditd` & Wazuh Agent Telemetry):**
    ```bash
    # Verify syslog/journald and Wazuh agent status
    systemctl is-active rsyslog wazuh-agent 2>/dev/null || systemctl is-active systemd-journald
    logger -p auth.info -t LAB_TEST "Endpoint telemetry stream verified"
    ```

---

### Lab 2: Analyse Authentication Events (Brute Force, Password Spraying & Logon Types)
* **Objective:** Query authentication logs in **Splunk (SPL)**, **PowerShell**, and **Linux CLI** to detect brute-force attacks, password spraying, and anomalous logon types (`Type 3` Network, `Type 10` RDP).
* **Hands-On Steps:**
  * **Splunk Search Processing Language (SPL) Queries:**
    ```spl
    # 1. Detect Password Spraying (1 source IP failing across >= 5 unique usernames)
    index=security EventCode=4625 OR "Failed password"
    | stats dc(user) as unique_users, count as total_failures by src_ip
    | where unique_users >= 5

    # 2. Detect Single-Account Brute Force followed by Successful Logon
    index=security (EventCode=4625 OR EventCode=4624)
    | transaction user maxspan=10m
    | where eventcount >= 5 AND EventCode=4624
    ```
  * **Windows PowerShell Quick Triage:**
    ```powershell
    Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4625} -MaxEvents 10 -ErrorAction SilentlyContinue |
      Group-Object { $_.Properties.Value } | Select-Object Count, Name
    ```

---

### Lab 3: Identify Suspicious Processes (Parent-Child Trees & LOLBins)
* **Objective:** Hunt for anomalous process execution—such as `winword.exe` or `nginx` spawning `powershell.exe`/`bash`, encoded PowerShell payloads (`-Enc`), or binaries executing from `/tmp` or `C:\Users\Public`.
* **Hands-On Steps:**
  * **Velociraptor VQL (Velociraptor Query Language) Live Endpoint Hunt:**
    ```sql
    SELECT Pid, Ppid, Name, CommandLine, Exe
    FROM pslist()
    WHERE CommandLine =~ "(?i)-enc|certutil.*urlcache|/tmp/|/dev/shm/"
    ```
  * **Linux CLI Process Tree & Volatile Path Check:**
    ```bash
    ps auxf | grep -E "nc |ncat|python3 -c|/tmp/|/dev/shm/" | grep -v grep || echo "[OK] Clean process tree"
    ```

---

### Lab 4: Investigate Unusual Network Traffic (Security Onion, Zeek & NetFlow)
* **Objective:** Analyze outbound C2 beaconing, DNS tunneling (`NXDOMAIN` spikes), and large data exfiltration transfers using **Security Onion** (Zeek/Suricata) or `tcpdump`.
* **Hands-On Steps:**
  * **Security Onion / Zeek Log Triage (`conn.log` & `dns.log`):**
    ```bash
    # Top 10 external destination IPs ranked by outbound bytes transferred (Exfiltration detection)
    # zeek-cut id.orig_h id.resp_h id.resp_p orig_bytes < /nsm/zeek/logs/current/conn.log | sort -k4 -nr | head -n 10

    # Local tcpdump check for suspicious outbound DNS or high-port connections
    sudo tcpdump -i any -nn -c 20 "port 53 or port 4444"
    ```

---

### Lab 5: Detect Malware Indicators (Hashes, Strings, Persistence & YARA)
* **Objective:** Triage a suspicious file using static analysis (**SHA-256 hashing**, **`strings` inspection**, **YARA rules**) and check persistence locations without executing the sample.
* **Hands-On Steps:**
  ```bash
  mkdir -p ~/ir_soc_lab && cd ~/ir_soc_lab

  # 1. Create a harmless simulated suspicious artifact (EICAR-style test string)
  cat << 'EOF' > suspect_dropper.bin
  #!/bin/bash
  # Simulated malware artifact for static triage only
  C2_URL="http://198.51.100"
  MUTEX="Global\SecPlusLabBot_2026"
  EOF

  # 2. Compute SHA-256 hash & extract embedded plaintext strings
  sha256sum suspect_dropper.bin
  strings suspect_dropper.bin | grep -iE "http|mutex|gate"

  # 3. Check Linux persistence locations (Cron jobs & systemd timers)
  ls -la /etc/cron.d/ /var/spool/cron/crontabs/ 2>/dev/null || true
  ```

---

### Lab 6: Correlate Security Events (Multi-Source Attack Timeline)
* **Objective:** Stitch together separate alerts across **Email/Web Logs**, **Endpoint Sysmon/EDR**, and **Firewall/Network Logs** into a single chronological attack chain.
* **Hands-On Steps (Run Multi-Source SIEM Correlation Script in Python):**
  ```python
  events = [
      {"ts": "2026-11-21T13:10:02Z", "sensor": "Email_Gateway", "msg": "Attachment 'Invoice.docm' delivered to user afon"},
      {"ts": "2026-11-21T13:12:15Z", "sensor": "Sysmon_ID_1",   "msg": "WINWORD.EXE spawned powershell.exe -Enc ... on WKSTN-07"},
      {"ts": "2026-11-21T13:12:19Z", "sensor": "Firewall_NIDS", "msg": "Outbound TCP/443 C2 connection from WKSTN-07 to 198.51.100.88"}
  ]

  print("=== CORRELATED INCIDENT ATTACK CHAIN ===")
  for ev in sorted(events, key=lambda x: x["ts"]):
      print(f"{ev['ts']} | [{ev['sensor']:<14}] | {ev['msg']}")
  ```

---

### Lab 7: Investigate Suspicious Accounts (Privilege Escalation & Impossible Travel)
* **Objective:** Audit newly created accounts (`Event ID 4720`), unauthorized additions to privileged groups (`Event ID 4732` / `sudo`), and anomalous login locations.
* **Hands-On Steps:**
  * **Windows PowerShell:**
    ```powershell
    # Check for recent user creations (4720) or group additions (4728 / 4732)
    Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4720,4728,4732} -MaxEvents 10 -ErrorAction SilentlyContinue |
      Select-Object TimeCreated, Id, Message
    ```
  * **Linux CLI:**
    ```bash
    # Inspect recent account/group changes in /var/log/auth.log
    sudo grep -iE "useradd|usermod|groupadd|sudo:" /var/log/auth.log 2>/dev/null | tail -n 10
    ```

---

### Lab 8: Preserve Forensic Evidence (Order of Volatility & Chain of Custody)
* **Objective:** Collect volatile artifacts first (`Order of Volatility`: RAM/sockets $\rightarrow$ disk), acquire cryptographic **SHA-256** hashes, and log a legally defensible **Chain of Custody**.
* **Hands-On Steps:**
  ```bash
  mkdir -p ~/ir_soc_lab/forensic_vault && cd ~/ir_soc_lab

  # 1. Capture volatile network connections & running processes before containment
  ss -tulnp > forensic_vault/volatile_sockets.txt
  ps auxf > forensic_vault/volatile_processes.txt

  # 2. Copy suspicious artifact into read-only vault and generate SHA-256 manifest
  cp -p suspect_dropper.bin forensic_vault/EVID-001_suspect_dropper.bin
  sha256sum forensic_vault/* > forensic_vault/EVIDENCE_MANIFEST.sha256
  chmod 444 forensic_vault/*

  # 3. Record Chain of Custody entry
  cat << EOF > forensic_vault/CHAIN_OF_CUSTODY.txt
  Case ID       : INC-2026-1121
  Collector     : Ambe Fon (SOC Analyst)
  Date/Time UTC : $(date -u +"%Y-%m-%dT%H:%M:%SZ")
  Integrity Hash: $(grep EVID-001 forensic_vault/EVIDENCE_MANIFEST.sha256 | awk '{print $1}')
  Action        : Acquired volatile telemetry & artifact hash prior to host isolation.
  EOF

  cat forensic_vault/CHAIN_OF_CUSTODY.txt
  ```

---

### Lab 9: Perform Incident Containment (Host Isolation & Account/IP Blocking)
* **Objective:** Stop active attacker C2 communication and lateral movement immediately—using **Velociraptor Quarantine**, **Wazuh Active Response**, host firewall isolation, and credential/session revocation—*without* powering off the machine (preserving RAM).
* **Hands-On Steps:**
  * **Velociraptor Built-In Quarantine Artifact:** Run `Windows.Remediation.Quarantine` (or `Linux.Remediation.Quarantine`) to block all traffic except the Velociraptor C2 management server.
  * **Linux Emergency Firewall Isolation Simulation:**
    ```bash
    # Block outbound C2 IP immediately on host firewall
    sudo ufw insert 1 deny out to 198.51.100.88 2>/dev/null || echo "Simulated Firewall Block: DENY OUT TO 198.51.100.88"

    # Lock compromised user account & terminate active SSH sessions
    # sudo usermod -L compromised_user && sudo pkill -u compromised_user
    ```

---

### Lab 10: Write Incident Reports (Executive Summary, Timeline & Root Cause Analysis)
* **Objective:** Produce a structured **Post-Incident Report (PIR)** documenting Executive Summary, Timeline of Events, Indicators of Compromise (IoCs), Root Cause Analysis (RCA), and Lessons Learned remediation tasks.
* **Hands-On Steps (Generate a Formal Markdown Incident Report Template):**
  ```bash
  cat << 'EOF' > ~/ir_soc_lab/INC-2026-1121_Post_Incident_Report.md
  # Post-Incident Report (PIR): INC-2026-1121
  - **Date (UTC):** 2026-11-21
  - **Severity:** High | **Status:** Contained, Eradicated & Recovered
  - **Lead Responder:** Ambe Fon

  ## 1. Executive Summary
### Lab 10: Write Incident Reports (Executive Summary, Technical Timeline, IoCs & Lessons Learned)
* **Objective:** Produce a comprehensive, audit-ready **Post-Incident Report (PIR)** combining an executive business overview, a chronological UTC attack timeline, verified Indicators of Compromise (IoCs), Root Cause Analysis (RCA), containment/recovery verification, and assigned remediation action items.
* **Hands-On Steps (Generate a Complete Structured Markdown & JSON Post-Incident Report):**
  ```bash
  mkdir -p ~/ir_soc_lab && cd ~/ir_soc_lab

  cat << 'EOF' > ~/ir_soc_lab/INC-2026-1121_Post_Incident_Report.md
  # Post-Incident Report (PIR): INC-2026-1121
  - **Incident Title:** Spear-Phishing Macro Execution & C2 Beacon Containment
  - **Date of Incident (UTC):** 2026-11-21
  - **Severity Level:** High | **Final Status:** Closed (Contained, Eradicated & Recovered)
  - **Incident Commander / Lead Responder:** Ambe Fon (SOC Tier-2 Analyst)

  ---

  ## 1. Executive Summary
  On 2026-11-21 at 13:10 UTC, workstation `WKSTN-07` (Finance Department) received a spear-phishing email containing a weaponized macro document (`Invoice.docm`). At 13:12 UTC, **Sysmon (Event ID 1)** and **Wazuh** detected `WINWORD.EXE` spawning an encoded PowerShell process, which initiated an outbound Command-and-Control (C2) connection to `198.51.100.88:8443` captured by **Security Onion**. Within 4 minutes of detection, the host was isolated via **Velociraptor Quarantine**, volatile forensic evidence was preserved, and the malicious IP was blocked perimeter-wide. No sensitive financial data was exfiltrated.

  ## 2. Chronological Incident Timeline (UTC)

  | Timestamp (UTC) | Detection Source | Event Description |
  | :--- | :--- | :--- |
  | `2026-11-21T13:10:02Z` | Email Gateway | External email with attachment `Invoice.docm` delivered to `WKSTN-07`. |
  | `2026-11-21T13:12:15Z` | Sysmon ID 1 / Wazuh | `WINWORD.EXE` spawned `powershell.exe -NoP -W Hidden -Enc ...`. |
  | `2026-11-21T13:12:19Z` | Security Onion (Zeek) | Outbound TCP/8443 C2 beacon detected from `10.50.0.17` to `198.51.100.88`. |
  | `2026-11-21T13:14:00Z` | Splunk SIEM Alert | High-severity correlation rule triggered; SOC triage initiated. |
  | `2026-11-21T13:16:30Z` | Velociraptor / UFW | `WKSTN-07` placed in network quarantine; volatile RAM & sockets acquired. |
  | `2026-11-21T14:05:00Z` | IT SecOps | `WKSTN-07` reimaged from clean golden baseline; user credentials reset. |

  ## 3. Indicators of Compromise (IoCs)
  - **Malicious C2 IP Address:** `198.51.100.88` (Port `8443/TCP`)
  - **Malicious URL:** `http://198.51.100`
  - **Host Mutex:** `Global\SecPlusLabBot_2026`
  - **Forensic Vault Manifest:** `forensic_vault/EVIDENCE_MANIFEST.sha256` (Chain of Custody verified)

  ## 4. Root Cause Analysis (RCA)
  - **Primary Technical Root Cause:** Microsoft Office macro execution from Internet-originated attachments was not blocked via Group Policy (`GPO`), allowing user interaction to trigger PowerShell execution.
  - **Secondary Contributing Factor:** Domain DMARC policy was set to `p=none` (monitor-only) rather than `p=reject`, allowing spoofed external invoice lures to reach the inbox.

  ## 5. Lessons Learned & Corrective Action Plan

  | Action Item | Control Type | Assigned Owner | Target SLA | Status |
  | :--- | :--- | :--- | :--- | :--- |
  | Deploy GPO blocking Office macros in files from the Internet | Preventive (Technical) | Windows Admin | 48 Hours | Open |
  | Enforce domain DMARC policy `p=reject` and external email banners | Preventive (Technical) | Email SecOps | 7 Days | Open |
  | Block `198.51.100.88` across Edge Firewall and Web Proxy | Preventive (Technical) | Network SecOps | Immediate | **Completed** |
  | Enroll affected user in targeted phishing & macro awareness training | Directive (Operational) | Security Awareness | 5 Days | Open |
  EOF

  cat ~/ir_soc_lab/INC-2026-1121_Post_Incident_Report.md
  ```

---

## Quick-Reference SOC & Incident Response Tool Matrix (Exam & Lab Synthesis)

| SOC / IR Tool | Primary Role in Lab & Enterprise | Key Query / Operational Action |
| :--- | :--- | :--- |
| **Sysmon** | Deep Windows host telemetry (Process Create `ID 1`, Network `ID 3`, File Create `ID 11`, Registry `ID 13`, DNS `ID 22`). | `Get-WinEvent -LogName "Microsoft-Windows-Sysmon/Operational"` |
| **Wazuh** | Open-source SIEM + XDR/HIDS agent performing log analysis, File Integrity Monitoring (FIM), vulnerability detection, and active response. | Monitors `/var/log/auth.log`, Windows Event Logs, and triggers automated IP blocks. |
| **Splunk** | Enterprise SIEM for log aggregation, SPL correlation searches, incident transactions, and SOC dashboards. | `index=security EventCode=4625 \| stats dc(user) by src_ip` |
| **Security Onion** | Network Security Monitoring (NSM) platform integrating **Suricata** (IDS/IPS), **Zeek** (protocol metadata logs), and **Wireshark/Stenographer** (PCAP). | `zeek-cut id.orig_h id.resp_h orig_bytes < conn.log` |
| **Velociraptor** | Endpoint visibility, live VQL threat hunting, volatile forensic artifact collection, and instant host network quarantine. | `SELECT Pid, Name, CommandLine FROM pslist()` / `Quarantine` artifact |

---

### Module 7 Lab Completion Checklist
- [ ] Verified endpoint log collection using **Sysmon** (Windows) and **`rsyslog` / `journald` / Wazuh** (Linux).
- [ ] Analyzed authentication anomalies (**Password Spraying** vs. **Brute Force**) using **Splunk SPL** and PowerShell/Bash.
- [ ] Hunted suspicious process trees and **LOLBins** using **Velociraptor VQL** and `ps auxf`.
- [ ] Inspected network traffic flows (**Security Onion / Zeek / `tcpdump`**) and triaged malware artifacts via **SHA-256** and `strings`.
- [ ] Correlated a multi-source attack timeline, preserved volatile evidence with a **Chain of Custody**, executed **Host/IP Containment**, and authored a complete **Post-Incident Report (PIR)** with **Root Cause Analysis (RCA)**.
