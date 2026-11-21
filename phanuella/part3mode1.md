# Part 3 – Practical Security+ Laboratory Syllabus
## Module 1: Linux Security Laboratory

> **Lab Environment:** Ubuntu/Debian Linux VM (VirtualBox) with `sudo` privileges.  
> **Safety Best Practice:** Take a clean VM snapshot (`Snapshot_Clean_Linux`) before modifying SSH, firewall, or kernel settings.

---

### Lab 1: Linux User and Group Management
* **Objective:** Provision users with least privilege, enforce password expiration policies, audit UID 0 accounts, and cleanly deprovision accounts.
* **Hands-On Steps:**
  ```bash
  # 1. Create a dedicated security group and two users
  sudo groupadd -f secops_team
  sudo useradd -m -s /bin/bash -G secops_team analyst1
  sudo useradd -m -s /usr/sbin/nologin svc_backup   # Non-interactive service account

  # 2. Enforce password aging (max 90 days, min 2 days, 7-day warning)
  sudo chage -M 90 -m 2 -W 7 analyst1
  sudo chage -l analyst1

  # 3. Security Audit: Check for unauthorized root-equivalent accounts (UID 0)
  awk -F: '($3 == "0") {print "[ALERT] UID 0 Account:", $1}' /etc/passwd

  # 4. Deprovision test accounts cleanly
  sudo userdel -r analyst1
  sudo userdel svc_backup
  sudo groupdel secops_team
  ```

---

### Lab 2: File Permissions (DAC, Octal/Symbolic & Special Bits)
* **Objective:** Configure standard `rwx` permissions (`4/2/1`), protect sensitive credential files, and audit dangerous `SUID` (`4000`) / world-writable files.
* **Hands-On Steps:**
  ```bash
  mkdir -p ~/linux_sec_lab && cd ~/linux_sec_lab

  # 1. Create a sensitive API key file and lock it down to Owner Read/Write only (600)
  echo "API_TOKEN=998877665544" > api_secret.env
  chmod 600 api_secret.env
  ls -l api_secret.env

  # 2. Create a shared team directory with the Sticky Bit (+t) so users can only delete their own files
  mkdir shared_drop
  chmod 1777 shared_drop
  ls -ld shared_drop

  # 3. Privilege Escalation Audit: Find all SUID binaries on the system
  find /usr/bin -perm -4000 -type f 2>/dev/null | head -n 15
  ```

---

### Lab 3: Ownership (`chown` & `chgrp`)
* **Objective:** Enforce strict file and directory ownership so web servers and daemons cannot overwrite their own executables or configuration files.
* **Hands-On Steps:**
  ```bash
  # Create a simulated web configuration owned by root, readable by www-data group
  echo "ServerTokens Prod" > web_hardened.conf
  sudo chown root:www-data web_hardened.conf 2>/dev/null || sudo chown root:root web_hardened.conf
  sudo chmod 640 web_hardened.conf
  ls -l web_hardened.conf
  ```

---

### Lab 4: Process Monitoring
* **Objective:** Inspect running process trees, identify hidden/suspicious processes running out of `/tmp` or `/dev/shm`, and terminate rogue tasks.
* **Hands-On Steps:**
  ```bash
  # 1. View full parent-child process tree (spot suspicious spawns like apache2 -> bash)
  ps auxf | head -n 20

  # 2. Identify top 5 CPU-consuming processes (detects unauthorized cryptominers)
  ps -eo pid,ppid,user,%cpu,%mem,cmd --sort=-%cpu | head -n 6

  # 3. Hunt for processes executing from volatile/world-writable directories (/tmp, /dev/shm)
  ps -eo pid,user,cmd | grep -E "/tmp/|/dev/shm/" | grep -v grep || echo "[PASS] No processes running from /tmp or /dev/shm"
  ```

---

### Lab 5: Service Management (`systemd`)
* **Objective:** Audit enabled daemons to reduce the attack surface, disable unnecessary legacy services, and verify service status.
* **Hands-On Steps:**
  ```bash
  # 1. List all currently running background services
  systemctl list-units --type=service --state=running | head -n 15

  # 2. List all services enabled to start automatically at boot
  systemctl list-unit-files --type=service --state=enabled | head -n 15

  # 3. Check status of SSH and Cron daemons
  systemctl is-active ssh cron 2>/dev/null || true
  ```

---

### Lab 6: Firewall Configuration (`ufw` & `ss`)
* **Objective:** Implement a stateful default-deny host firewall, restrict management ports to trusted subnets, and enable anti-brute-force rate limiting.
* **Hands-On Steps:**
  ```bash
  # 1. Audit all currently listening TCP/UDP ports before configuring firewall
  sudo ss -tulnp

  # 2. Configure UFW with Default Deny Inbound / Allow Outbound
  sudo ufw default deny incoming
  sudo ufw default allow outgoing

  # 3. Rate-limit SSH (blocks IPs exceeding 6 connection attempts in 30 seconds)
  sudo ufw limit 22/tcp

  # 4. Allow HTTPS (443) and explicitly block legacy Telnet (23)
  sudo ufw allow 443/tcp
  sudo ufw deny 23/tcp

  # 5. Enable firewall and inspect numbered rules
  sudo ufw --force enable
  sudo ufw status numbered
  ```

---

### Lab 7: SSH Security Hardening
* **Objective:** Harden `/etc/ssh/sshd_config` against brute-force and root-login attacks, generate Ed25519 keys, and validate configuration syntax before reloading.
* **Hands-On Steps:**
  ```bash
  # 1. Generate a modern Ed25519 SSH keypair
  ssh-keygen -t ed25519 -f ~/.ssh/lab_ed25519 -N "" -C "secplus-admin"

  # 2. Backup existing sshd_config before editing (Change Management Backout Plan)
  sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak.$(date +%F)

  # 3. Create a hardened drop-in configuration in /etc/ssh/sshd_config.d/
  cat << 'EOF' | sudo tee /etc/ssh/sshd_config.d/99-secplus-hardening.conf
  PermitRootLogin no
  MaxAuthTries 3
  PermitEmptyPasswords no
  X11Forwarding no
  ClientAliveInterval 300
  ClientAliveCountMax 2
  EOF

  # 4. Validate SSH configuration syntax safely before reloading
  sudo sshd -t && echo "[PASS] SSH hardening syntax valid!"
  ```

---

### Lab 8: Log Analysis (`journalctl`, `auth.log`, `grep`, `awk`)
* **Objective:** Investigate authentication logs to detect brute-force attacks, identify top attacking source IPs, and trace `sudo` privilege escalations.
* **Hands-On Steps:**
  ```bash
  # 1. Generate test authentication log entries for analysis
  logger -p auth.warning -t sshd "Failed password for invalid user admin from 198.51.100.42 port 51234 ssh2"
  logger -p auth.warning -t sshd "Failed password for invalid user admin from 198.51.100.42 port 51238 ssh2"
  logger -p auth.warning -t sshd "Failed password for root from 203.0.113.88 port 44120 ssh2"

  # 2. Extract and count top attacking IP addresses from system/auth logs
  journalctl -t sshd --no-pager | grep "Failed password" | \
    awk '{for(i=1;i<=NF;i++) if($i=="from") print $(i+1)}' | sort | uniq -c | sort -nr

  # 3. Inspect recent sudo command executions
  journalctl _COMM=sudo -n 10 --no-pager 2>/dev/null || sudo grep "sudo:" /var/log/auth.log 2>/dev/null | tail -n 10
  ```

---

### Lab 9: System Hardening (`sysctl` Kernel & Legal Banner)
* **Objective:** Harden Linux kernel network parameters against SYN floods, IP spoofing, and ICMP redirects, and configure a deterrent legal login banner.
* **Hands-On Steps:**
  ```bash
  # 1. Configure a deterrent SSH pre-login legal banner
  cat << 'EOF' | sudo tee /etc/issue.net
  ***********************************************************************
  AUTHORIZED ACCESS ONLY. All sessions are monitored and logged.
  Unauthorized access is prohibited and subject to legal prosecution.
  ***********************************************************************
  EOF

  # 2. Apply runtime kernel hardening parameters via sysctl
  sudo sysctl -w net.ipv4.tcp_syncookies=1
  sudo sysctl -w net.ipv4.conf.all.rp_filter=1
  sudo sysctl -w net.ipv4.conf.all.accept_redirects=0
  sudo sysctl -w kernel.randomize_va_space=2

  # 3. Verify applied settings
  sysctl net.ipv4.tcp_syncookies net.ipv4.conf.all.rp_filter kernel.randomize_va_space
  ```

---

### Lab 10: File Integrity Monitoring (FIM)
* **Objective:** Establish a cryptographic SHA-256 baseline of critical system files (`/etc/passwd`, `/etc/group`, `/etc/ssh/sshd_config`) and detect unauthorized tampering.
* **Hands-On Steps:**
  ```bash
  cd ~/linux_sec_lab

  # 1. Generate a cryptographic baseline of critical configuration files
  sudo sha256sum /etc/passwd /etc/group /etc/hosts > fim_baseline.sha256
  chmod 600 fim_baseline.sha256

  # 2. Verify baseline integrity (Expected: OK for all files)
  sha256sum -c fim_baseline.sha256
  ```

---

### Lab 11: Bash Automation (Capstone Security Audit & Alert Script)
* **Objective:** Combine user auditing, port checking, FIM verification, and log analysis into an automated, cron-ready Bash security script.
* **Hands-On Steps:**
  ```bash
  cat << 'EOF' > ~/linux_sec_lab/linux_sec_audit.sh
  #!/bin/bash
  REPORT_FILE="/tmp/sec_audit_$(date +%F_%H%M).log"

  {
    echo "===================================================="
    echo "  AUTOMATED LINUX SECURITY AUDIT REPORT"
    echo "  Host: $(hostname) | Date: $(date -u)"
    echo "===================================================="

    echo -e "\n[1] UID 0 (Root) Accounts:"
    awk -F: '($3 == "0") {print "  - " $1}' /etc/passwd

    echo -e "\n[2] Listening Network Ports:"
    ss -tuln | grep LISTEN

    echo -e "\n[3] File Integrity Monitoring (FIM) Check:"
    if [ -f ~/linux_sec_lab/fim_baseline.sha256 ]; then
        sha256sum -c ~/linux_sec_lab/fim_baseline.sha256
    else
        echo "  [WARN] FIM baseline missing!"
    fi

    echo -e "\n[4] World-Writable Files in /tmp:"
    find /tmp -maxdepth 2 -type f -perm -0002 2>/dev/null | head -n 10
  } | tee "$REPORT_FILE"

  echo -e "\n[+] Audit saved to: $REPORT_FILE"
  EOF

  chmod +x ~/linux_sec_lab/linux_sec_audit.sh
  ~/linux_sec_lab/linux_sec_audit.sh
  ```

---

### Lab 11: Bash Automation (Capstone Security Audit, Alerting & Scheduled Cron Enforcement)
* **Objective:** Combine user auditing, listening port detection, SUID binary checks, SHA-256 File Integrity Monitoring (FIM), and failed SSH brute-force log parsing into a production-ready Bash automation script scheduled via `cron`.
* **Hands-On Step 1: Build the Comprehensive Security Audit & Alert Script (`linux_sec_audit.sh`):**
  ```bash
  mkdir -p ~/linux_sec_lab && cd ~/linux_sec_lab

  # Ensure FIM baseline exists before running the capstone script
  sudo sha256sum /etc/passwd /etc/group /etc/hosts > ~/linux_sec_lab/fim_baseline.sha256
  chmod 600 ~/linux_sec_lab/fim_baseline.sha256

  cat << 'EOF' > ~/linux_sec_lab/linux_sec_audit.sh
  #!/bin/bash
  set -uo pipefail

  REPORT_FILE="/tmp/sec_audit_\$(date +%F_%H%M).log"
  ALERT_COUNT=0

  {
    echo "============================================================"
    echo "  AUTOMATED LINUX SECURITY AUDIT & INTEGRITY REPORT"
    echo "  Host: (hostname) | Timestamp (UTC): (date -u +"%Y-%m-%dT%H:%M:%SZ")"
    echo "============================================================"

    # 1. Privilege Audit: Check for unauthorized UID 0 accounts
    echo -e "\n UID 0 (Root-Equivalent) Accounts:"
    UID0_ACCOUNTS=\$(awk -F: '(\$3 == "0") {print \$1}' /etc/passwd)
    for acct in \$UID0_ACCOUNTS; do
        echo "  - \$acct"
        if [ "\$acct" != "root" ]; then
            echo "    [ALERT] Unauthorized UID 0 account detected: \$acct"
            ((ALERT_COUNT++))
        fi
    done

    # 2. Attack Surface Audit: List active listening TCP/UDP sockets
    echo -e "\n Active Listening Network Ports:"
    ss -tuln | grep -E "LISTEN|UNCONN" | head -n 15

    # 3. File Integrity Monitoring (FIM): Verify critical system file hashes
    echo -e "\n File Integrity Monitoring (FIM) Verification:"
    if [ -f ~/linux_sec_lab/fim_baseline.sha256 ]; then
        if sha256sum -c ~/linux_sec_lab/fim_baseline.sha256; then
            echo "  [OK] All baseline system files match SHA-256 hashes."
        else
            echo "  [CRITICAL ALERT] File Integrity Violation detected!"
            ((ALERT_COUNT++))
        fi
    else
        echo "  [WARN] FIM baseline file missing!"
    fi

    # 4. Persistence & World-Writable File Hunt in /tmp & /dev/shm
    echo -e "\n Suspicious World-Writable Files in /tmp and /dev/shm:"
    WW_FILES=\$(find /tmp /dev/shm -maxdepth 2 -type f -perm -0002 2>/dev/null | head -n 10)
    if [ -n "\$WW_FILES" ]; then
        echo "\$WW_FILES"
    else
        echo "  [OK] None detected."
    fi

    # 5. Authentication Log Analysis: Top IPs with Failed SSH Logins
    echo -e "\n Top Source IPs with Failed Authentication Attempts:"
    if command -v journalctl >/dev/null 2>&1; then
        journalctl -t sshd --no-pager 2>/dev/null | grep "Failed password" | \
          awk '{for(i=1;i<=NF;i++) if(i=="from") print (i+1)}' | sort | uniq -c | sort -nr | head -n 5
    fi

    echo -e "\n============================================================"
    echo "  AUDIT SUMMARY: \$ALERT_COUNT Critical Security Alerts Triggered"
    echo "============================================================"
  } | tee "\$REPORT_FILE"

  # Forward summary event to local Syslog for SIEM ingestion
  logger -p auth.notice -t SECPLUS_AUDIT "Linux security audit completed on (hostname) with ALERT_COUNT alerts."
  echo -e "\n[+] Report saved to: \$REPORT_FILE"
  EOF

  chmod 700 ~/linux_sec_lab/linux_sec_audit.sh
  ~/linux_sec_lab/linux_sec_audit.sh
  ```

* **Hands-On Step 2: Schedule Automated Execution via `cron` (Desired-State Continuous Monitoring):**
  ```bash
  # View current user's crontab
  crontab -l 2>/dev/null || echo "No crontab configured yet"

  # Example cron entry to run the security audit daily at 02:00 AM:
  # (crontab -l 2>/dev/null; echo "0 2 * * * /home/\$USER/linux_sec_lab/linux_sec_audit.sh >/dev/null 2>&1") | crontab -
  ```

---

## Quick-Reference Linux Security CLI Cheat Sheet (Exam & Lab Synthesis)

| Security Task | Primary Linux Command | What It Verifies / Enforces |
| :--- | :--- | :--- |
| **Audit Root Accounts** | `awk -F: '($3 == "0") {print $1}' /etc/passwd` | Detects hidden backdoor accounts sharing `UID 0`. |
| **Find SUID Escalation Risks** | `find / -perm -4000 -type f 2>/dev/null` | Lists binaries executing with owner's root privileges. |
| **Inspect Process Hierarchy** | `ps auxf` | Exposes anomalous parent-child spawns (e.g., `nginx -> sh`). |
| **Audit Open Ports & PIDs** | `sudo ss -tulnp` | Identifies unauthorized listening services and bound interfaces. |
| **Check Host Firewall** | `sudo ufw status verbose` | Confirms default-deny inbound policy and active port rules. |
| **Validate SSH Config** | `sudo sshd -t` | Syntax-checks `sshd_config` before reloading to avoid lockouts. |
| **Check MAC Enforcement** | `getenforce` or `sudo aa-status` | Verifies SELinux or AppArmor Mandatory Access Control state. |
| **Verify File Integrity** | `sha256sum -c fim_baseline.sha256` | Detects unauthorized modifications to critical system configs. |

---

### Module 1 Lab Completion Checklist
- [ ] Provisioned, aged (`chage`), audited (`UID 0`), and deprovisioned Linux users and groups.
- [ ] Enforced restrictive file permissions (`chmod 600`), Sticky Bit (`1777`), ownership (`chown`), and audited `SUID` binaries.
- [ ] Monitored process trees (`ps auxf`), audited `systemd` services, and configured stateful `ufw` rate-limiting rules.
- [ ] Hardened SSH (`/etc/ssh/sshd_config.d/`), applied `sysctl` kernel protections, and configured `/etc/issue.net`.
- [ ] Built, executed, and scheduled the automated `linux_sec_audit.sh` script with **SHA-256 File Integrity Monitoring** and **Syslog** forwarding.
