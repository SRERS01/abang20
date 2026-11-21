# CompTIA Security+ (SY0-701) – Practical Lab Guide
## Domain 1: General Security Concepts (12%–16%)
### Objective 1.1: Security Concepts and Controls

> **Objective:** Master the foundational security principles (CIA, AAA, Non-repudiation, Zero Trust, Least Privilege, Defense in Depth) and implement/classify security controls across **Categories** (Technical, Managerial, Operational, Physical) and **Functional Types** (Preventive, Deterrent, Detective, Corrective, Compensating, Directive).  
> **Recommended Lab Tools:** Linux Terminal / Bash, Windows PowerShell, OpenSSL, Python 3.

---

## Part A: Core Security Concepts

### 1. Confidentiality, Integrity, and Availability (CIA Triad)
* **Concept:**
  * **Confidentiality:** Preventing unauthorized disclosure of data (Encryption, Access Controls).
  * **Integrity:** Ensuring data has not been altered or tampered with without authorization (Hashing, Digital Signatures).
  * **Availability:** Ensuring systems and data are accessible to authorized users when needed (Redundancy, Backups, Load Balancing, Anti-DDoS).
* **Practical Task (Demonstrate All 3 Pillars via CLI):**
  ```bash
  # 1. CONFIDENTIALITY: Encrypt a sensitive file with AES-256
  echo "AccountBalance=500000" > payroll.txt
  openssl enc -aes-256-cbc -pbkdf2 -salt -in payroll.txt -out payroll.enc -pass pass:StrongSecret123!

  # 2. INTEGRITY: Generate a SHA-256 checksum to detect tampering
  sha256sum payroll.txt > payroll.sha256
  sha256sum -c payroll.sha256

  # 3. AVAILABILITY: Create a redundant local backup copy
  cp payroll.enc payroll.enc.bak && ls -lh payroll*
  ```

### 2. Authentication, Authorization, and Accounting (AAA)
* **Concept:**
  * **Authentication (AuthN):** Verifying *who* you are (Passwords, MFA, Certificates, Biometrics).
  * **Authorization (AuthZ):** Determining *what* you are allowed to access after authenticating (RBAC, ACLs, File Permissions).
  * **Accounting (Auditing):** Logging and tracking *what* you did while logged in (SIEM logs, `auditd`, Windows Event IDs).
* **Practical Task (Inspect AAA in Linux):**
  ```bash
  # Authentication: Verify password hash storage (shadow file requires root)
  sudo grep "^$USER:" /etc/shadow | cut -d: -f1,2

  # Authorization: Check group memberships & sudo privileges
  groups && sudo -l

  # Accounting: View recent authentication and privilege escalation audit trail
  last -n 5
  ```

### 3. Non-Repudiation
* **Concept:** Assurance that a sender or user cannot convincingly deny having performed an action or sent a message. Achieved through **asymmetric digital signatures** (signed with the sender's private key) and tamper-evident audit logs.
* **Practical Task (Create & Verify an RSA Digital Signature with OpenSSL):**
  ```bash
  # Generate a private/public keypair
  openssl genpkey -algorithm RSA -out sender_private.pem -pkeyopt rsa_keygen_bits:2048 2>/dev/null
  openssl rsa -pubout -in sender_private.pem -out sender_public.pem 2>/dev/null

  # Sign a transaction file using the Private Key
  echo "Approve wire transfer #9941 for 10,000 USD" > contract.txt
  openssl dgst -sha256 -sign sender_private.pem -out contract.sig contract.txt

  # Verify the signature using the Sender's Public Key (proves authenticity + non-repudiation)
  openssl dgst -sha256 -verify sender_public.pem -signature contract.sig contract.txt
  ```

### 4. Zero Trust Principles
* **Concept:** *"Never trust, always verify."* Eliminates implicit trust based on network location (internal LAN vs. external Internet). Consists of the **Control Plane** (Adaptive Identity, Policy Engine, Policy Administrator) and **Data Plane** (Policy Enforcement Point / Subject $\rightarrow$ System), enforcing continuous verification, microsegmentation, and least privilege per request.
* **Practical Task (Simulate a Zero Trust Policy Decision Point in Python):**
  ```python
  def policy_engine(request):
      if not request["mfa_verified"]:
          return "DENY: MFA required"
      if not request["device_compliant"]:
          return "DENY: Unmanaged/outdated endpoint posture"
      if request["risk_score"] > 50:
          return "DENY: Anomalous session risk detected"
      return "ALLOW: Short-lived session token issued to Data Plane PEP"

  login_attempt = {"user": "alice", "network": "Corporate_LAN", "mfa_verified": True, "device_compliant": False, "risk_score": 15}
  print("Zero Trust Decision:", policy_engine(login_attempt))
  ```

### 5. Least Privilege
* **Concept:** Granting users, processes, and applications **only** the minimum permissions required to perform their specific job functions—and nothing more.
* **Practical Task (Enforce Least Privilege on Files & Service Accounts):**
  ```bash
  # Lock down a configuration file so only the owner can read/write (no group/world read)
  touch app_secrets.conf
  chmod 600 app_secrets.conf
  ls -l app_secrets.conf
  ```

### 6. Defense in Depth (Layered Security)
* **Concept:** Deploying multiple independent layers of security controls (Perimeter Firewall $\rightarrow$ Network Segmentation $\rightarrow$ Host Hardening $\rightarrow$ Endpoint EDR $\rightarrow$ Application Auth $\rightarrow$ Data Encryption) so if one control fails, subsequent layers stop the attacker.
* **Practical Task (Audit Your Local Defense-in-Depth Stack):**
  Verify at least 3 distinct layers on your lab machine:
  1. **Network Layer:** Host firewall active (`sudo ufw status` on Linux or `Get-NetFirewallProfile` on Windows).
  2. **Host/OS Layer:** Automatic security updates enabled & non-root daily user (`whoami`).
  3. **Data Layer:** Sensitive files encrypted at rest (`payroll.enc`).

---

## Part B: Security Control Categories (How They Are Implemented)

### 7. Technical (Logical) Security Controls
* **Concept:** Controls implemented through technology, hardware, or software mechanisms (Firewalls, Encryption, Antivirus/EDR, MFA, IAM policies, IDS/IPS).
* **Practical Task:**
  1. Implement a technical control by enabling a host-based firewall rule blocking Telnet (`port 23`):
     ```bash
     sudo ufw deny 23/tcp 2>/dev/null || echo "Simulate: Block inbound TCP/23 on host firewall"
     ```

### 8. Managerial (Administrative) Security Controls
* **Concept:** Governance, risk management, policies, standards, procedures, and compliance frameworks defined by leadership (Acceptable Use Policy, Risk Assessments, Vendor Due Diligence, Vulnerability Management Policy).
* **Practical Task:**
  1. Draft a concise **Password & MFA Standard** snippet in Markdown (`security_policy.md`):
     ```bash
     cat << 'EOF' > security_policy.md
     # Corporate Access Control Standard (Managerial Control)
     1. Minimum password length: 14 characters.
     2. Phishing-resistant MFA (FIDO2/WebAuthn) is mandatory for all remote and privileged access.
     3. Access reviews must be conducted quarterly by department managers.
     EOF
     cat security_policy.md
     ```

### 9. Physical Security Controls
* **Concept:** Tangible hardware and environmental barriers protecting facilities, server rooms, and devices (Badge readers, Bollards, Biometric locks, CCTV cameras, Faraday cages, Cable locks, HVAC/Fire suppression).
* **Practical Task (Physical Hardware Port Lockdown Check):**
  1. Audit connected USB/removable storage devices on your machine (simulating physical port security verification):
     * **Linux:** `lsusb`
     * **Windows (PowerShell):** `Get-PnpDevice -Class USB | Select-Object Status, FriendlyName`

### 10. Operational Security Controls
* **Concept:** Day-to-day procedures executed by people rather than systems (Security awareness training, incident response drills, change management reviews, background checks, guard patrols, patch deployment cycles).
* **Practical Task:**
  1. Perform an operational **Change Management / Baseline Verification** check by logging your current listening ports with a timestamp before making any system changes:
     ```bash
     echo "=== Change Control Baseline: $(date) ===" > change_log.txt
     ss -tuln >> change_log.txt 2>/dev/null || netstat -an >> change_log.txt
     cat change_log.txt
     ```

---

## Part C: Security Control Functional Types (What They Do)

### 11. Preventive Controls
* **Concept:** Stops an attack or unauthorized event *before* it happens (Firewalls, ACLs, Encryption, MFA, Bollards, IPS in inline blocking mode).
* **Practical Task:**
  1. Test a preventive control by removing write permissions (`chmod 400`) on a critical file and attempting to overwrite it:
     ```bash
     echo "Critical Config" > critical.cfg
     chmod 400 critical.cfg
     echo "Malicious Edit" > critical.cfg 2>&1 || echo "[PREVENTED] Permission denied!"
     ```

### 12. Deterrent Controls
* **Concept:** Discourages an attacker from attempting an intrusion by increasing perceived risk or consequences (Login warning banners, "Protected by CCTV" signs, Barb wire, Fake cameras, Threat of legal prosecution).
* **Practical Task (Configure an SSH Legal Warning Banner):**
  1. Inspect or create `/etc/issue.net` (displayed before SSH authentication to deter unauthorized access):
     ```bash
     cat << 'EOF' > banner_preview.txt
     ***************************************************************************
     AUTHORIZED ACCESS ONLY. All activity on this system is monitored and logged.
     Unauthorized access is strictly prohibited and subject to legal prosecution.
     ***************************************************************************
     EOF
     cat banner_preview.txt
     ```

### 13. Detective Controls
### 13. Detective Controls
* **Concept:** Identifies, alerts on, and records unauthorized or anomalous activity *during* or *after* it occurs—without actively blocking the initial action. Examples include **SIEM alerts, IDS (Intrusion Detection Systems), Security/Audit Logs, File Integrity Monitoring (FIM), CCTV recording, and Motion Sensors**.
* **Practical Task 1 (Detect Failed Authentication Events in Logs):**
  * **Linux:**
    ```bash
    sudo grep -iE "failed|invalid user" /var/log/auth.log 2>/dev/null | tail -n 5 || journalctl -u ssh -n 10 --no-pager
    ```
  * **Windows (PowerShell — Event ID 4625 = Failed Logon):**
    ```powershell
    Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4625} -MaxEvents 5 -ErrorAction SilentlyContinue | Select-Object TimeCreated, Message
    ```
* **Practical Task 2 (Run a Detective File Integrity Check):**
  ```bash
  echo "System_Config_v1" > sys_baseline.conf
  sha256sum sys_baseline.conf > sys_baseline.sha256

  # Simulate unauthorized modification by an attacker
  echo "Backdoor_User=attacker" >> sys_baseline.conf

  # Detective control flags the tampering immediately
  sha256sum -c sys_baseline.sha256
  ```

---

### 14. Corrective Controls
* **Concept:** Restores systems to normal, secure operation and mitigates damage *after* an incident has been detected. Examples include **Restoring from Backups, Patching/Updating vulnerable software, Quarantining/Removing malware, Reimaging a compromised host, and Rolling back a VM snapshot**.
* **Practical Task (Simulate Ransomware Corruption & Corrective Recovery):**
  ```bash
  # 1. Create an encrypted, clean backup first
  echo "Critical_Financial_Ledger_2026" > ledger.txt
  openssl enc -aes-256-cbc -pbkdf2 -salt -in ledger.txt -out ledger.backup.enc -pass pass:RecoveryKey2026!

  # 2. Simulate ransomware encrypting/destroying the live file
  rm -f ledger.txt
  echo "YOUR FILES ARE ENCRYPTED!" > ledger.txt.locked

  # 3. Execute Corrective Control: Wipe malicious artifact and restore from clean backup
  rm -f ledger.txt.locked
  openssl enc -d -aes-256-cbc -pbkdf2 -in ledger.backup.enc -out ledger.txt -pass pass:RecoveryKey2026!
  cat ledger.txt
  ```

---

### 15. Compensating Controls
* **Concept:** An alternative or temporary security control implemented when the primary, ideal control is technically infeasible, unsupported by legacy hardware/software, or cost-prohibitive.
  * *Classic Exam Scenario:* A critical medical/industrial machine runs an outdated OS (e.g., Windows Server 2008) that cannot be patched or support modern TLS. The **compensating control** is isolating it inside a strict microsegmented VLAN with an IPS and firewall ACL permitting traffic *only* from one jump host.
* **Practical Task (Implement a Compensating Firewall Rule for an Unpatchable Legacy Service):**
  1. Suppose a legacy internal web service runs on unencrypted HTTP (`port 8080`) and cannot be upgraded to HTTPS (`443`). Apply a compensating host firewall rule restricting `8080/tcp` exclusively to a single trusted management IP (`10.10.50.5`):
     * **Linux (`ufw`):**
       ```bash
       sudo ufw allow from 10.10.50.5 to any port 8080 proto tcp
       sudo ufw deny 8080/tcp
       sudo ufw status numbered
       ```
     * **Windows (PowerShell):**
       ```powershell
       New-NetFirewallRule -DisplayName "Compensating-Restrict-8080" -Direction Inbound -LocalPort 8080 -Protocol TCP -RemoteAddress 10.10.50.5 -Action Allow
       ```

---

### 16. Directive Controls
* **Concept:** Instructs, guides, or mandates human behavior toward security compliance through written rules, policies, signage, or standard operating procedures (SOPs). Examples include **Acceptable Use Policies (AUP), Password Policies, Incident Response Playbooks, "Authorized Personnel Only" signs, and Data Classification Labels**.
* **Practical Task (Verify How Written Directives Map to OS Enforcement):**
  1. Inspect your operating system's local password policy settings to see how a written **Password Policy (Directive)** is technically enforced:
     * **Linux:**
       ```bash
       grep -E "^PASS_MAX_DAYS|^PASS_MIN_DAYS|^PASS_WARN_AGE" /etc/login.defs
       ```
     * **Windows (CMD):**
       ```cmd
       net accounts
       ```
  2. Create a **Data Classification Header Template** (Directive Control) for internal documents:
     ```bash
     cat << 'EOF' > classification_directive.txt
     [CLASSIFICATION: CONFIDENTIAL - INTERNAL USE ONLY]
     Handling Directive: Do not transmit outside the corporate network without AES-256 encryption.
     EOF
     cat classification_directive.txt
     ```

---

## Quick-Reference Exam Matrix: Control Categories vs. Functional Types

> **Exam Tip:** CompTIA Security+ questions frequently describe a real-world control and ask you to identify **both** its **Category** (how it is built) and its **Functional Type** (what it accomplishes).

| Real-World Security Control | Category (Implementation) | Functional Type (Purpose) |
| :--- | :--- | :--- |
| **Firewall / IPS / Encryption / MFA / ACLs** | Technical | Preventive |
| **SIEM / IDS / System Audit Logs / FIM** | Technical | Detective |
| **Antivirus Auto-Quarantine / Automated Patching** | Technical | Corrective |
| **Login Warning Banner (`issue.net` / GPO Banner)** | Technical | Deterrent |
| **Acceptable Use Policy (AUP) / Security Policy** | Managerial | Directive |
| **Risk Assessment / Vendor Due Diligence** | Managerial | Preventive / Detective |
| **Security Awareness & Phishing Training** | Operational | Directive / Preventive |
| **Restoring Data from Offline Backups / VM Snapshot** | Operational | Corrective |
| **Isolating an Unpatchable Legacy Host on a VLAN** | Technical / Operational | Compensating |
| **Bollards / Badge Access Locks / Mantraps** | Physical | Preventive |
| **CCTV Video Recording / Motion Sensors** | Physical | Detective |
| **"Warning: 24/7 Video Surveillance" Sign / Fake Camera** | Physical | Deterrent |

---

### Objective 1.1 Completion Checklist
- [ ] Demonstrated **Confidentiality** (AES-256), **Integrity** (SHA-256), and **Availability** (backup/restore) via CLI.
- [ ] Generated an RSA keypair and verified **Non-Repudiation** using a digital signature (`openssl dgst`).
- [ ] Simulated a **Zero Trust** Policy Decision Point evaluating user MFA and device posture.
- [ ] Implemented and tested **Preventive** (`chmod 400`), **Detective** (`sha256sum -c` & failed login log search), **Corrective** (encrypted backup recovery), **Compensating** (IP-restricted firewall ACL), and **Directive** (OS password policy & classification rules) controls.
- [ ] Memorized the **Categories vs. Functional Types** exam classification matrix.
