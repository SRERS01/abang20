# CompTIA Security+ (SY0-701) – Practical Lab Guide
## Domain 1: General Security Concepts
### Objective 1.2: Change Management and Security

> **Objective:** Understand how structured change control prevents outages, blocks unauthorized configuration drift, and maintains security posture across systems, applications, and documentation.  
> **Recommended Lab Tools:** Git, Linux Terminal / Bash (`systemctl`, `ldd`), Windows PowerShell (`Get-Service`, `Restart-Service`), Python 3, Markdown/Mermaid.

---

## Part A: Governance, Approval & Risk Assessment

### 1. Change Advisory Board (CAB)
* **Concept:** A cross-functional committee (IT ops, security, network, business leads) that reviews, evaluates risks, prioritizes, and approves/rejects non-standard or high-impact changes before production deployment. *(Note: Emergency changes use an Emergency CAB / ECAB for expedited review).*
* **Practical Task:**
  1. Create a structured **Change Request (RFC)** template in Markdown (`rfc_042.md`) ready for CAB review:
     ```bash
     cat << 'EOF' > rfc_042.md
     # Request for Change (RFC-042)
     - **Title:** Upgrade OpenSSH & Enforce Key-Only Auth on Prod-Web-01
     - **Change Type:** Normal (Requires CAB Approval)
     - **Change Owner:** Alice Nguyen (SecOps Lead)
     - **Maintenance Window:** Sunday 02:00 - 04:00 UTC
     - **Risk Level:** Medium
     - **Backout Plan:** Revert `/etc/ssh/sshd_config.bak` & restore VM snapshot `Pre_RFC042`
     EOF
     cat rfc_042.md
     ```

### 2. Change Approval
* **Concept:** Formal sign-off required before executing a change. Distinguishes between **Standard Changes** (pre-approved, low-risk, repeatable), **Normal Changes** (require CAB review), and **Emergency Changes** (urgent security patch/outage fix, documented retrospectively).
* **Practical Task:**
  1. Simulate an automated CI/CD or Git Pull Request approval gate in Python that blocks deployment unless CAB sign-off and test verification flags are `True`:
     ```python
     change_ticket = {
         "id": "RFC-042",
         "type": "Normal",
         "cab_approved": True,
         "sandbox_tests_passed": False
     }

     if change_ticket["cab_approved"] and change_ticket["sandbox_tests_passed"]:
         print(f"[APPROVED] {change_ticket['id']} cleared for Maintenance Window.")
     else:
         print(f"[BLOCKED] {change_ticket['id']} cannot deploy: Missing CAB approval or failed test results.")
     ```

### 3. Change Ownership
* **Concept:** Assigning a single accountable individual (**Change Owner**) responsible for planning, testing, communicating, executing, and verifying a specific change from start to finish.
* **Practical Task:**
  1. Enforce accountability in Git commits by verifying author identity metadata in your configuration repository:
     ```bash
     git init change_mgmt_repo && cd change_mgmt_repo
     git config user.name "SecOps Change Owner"
     git config user.email "secops-owner@corp.local"
     git config --list | grep user
     ```

### 4. Stakeholder Identification
* **Concept:** Identifying all internal teams, application owners, end users, and external vendors affected by a system change so they can provide input, prepare for downtime, and validate functionality afterward.
* **Practical Task:**
  1. Append a **Stakeholder Notification Matrix** to `rfc_042.md` mapping affected groups (`SOC Team`, `Web App Developers`, `Customer Support`) to notification triggers (`T-24h Advance Notice`, `Start of Window`, `Post-Change Verification`).

### 5. Impact Analysis
* **Concept:** Assessing the technical, operational, and security consequences of a proposed change—including affected upstream/downstream services, potential security gaps introduced, and expected downtime.
* **Practical Task (Analyze Service & Port Dependencies Before Making a Change):**
  1. Before modifying a firewall or stopping a service, inspect active network connections tied to that port/process so you know who will be impacted:
     * **Linux:** `ss -tpn`
     * **Windows (PowerShell):** `Get-NetTCPConnection -State Established | Select-Object LocalAddress, LocalPort, RemoteAddress, OwningProcess`

### 6. Testing and Test Results
* **Concept:** Validating a change in an isolated **Sandbox / Staging** environment before production deployment and recording objective **Test Results** (functional checks + security regression scans) as evidence for the CAB.
* **Practical Task (Validate Configuration Syntax Before Applying):**
  1. Always test service configurations before restarting live daemons (prevents locking yourself out of remote servers):
     ```bash
     # Test SSH daemon configuration syntax without restarting the service:
     sudo sshd -t && echo "[PASS] sshd_config syntax valid" || echo "[FAIL] Syntax error!"
     ```

---

## Part B: Execution, Recovery & Scheduling

### 7. Backout Planning (Rollback Plan)
* **Concept:** A documented, tested procedure to cleanly undo a failed change and restore the previous known-good state (e.g., restoring configuration backups, reverting database transactions, or rolling back a VM snapshot).
* **Practical Task (Create a Backup & Test Rollback Workflow):**
  ```bash
  echo "PermitRootLogin no" > app_security.conf
  # Step 1: Take timestamped backup before editing
  cp app_security.conf app_security.conf.bak.$(date +%F)

  # Step 2: Apply broken/bad change
  echo "INVALID_DIRECTIVE_XYZ" > app_security.conf

  # Step 3: Execute Backout Plan
  cp app_security.conf.bak.$(date +%F) app_security.conf
  cat app_security.conf
  ```

### 8. Fail-Forward Strategies
* **Concept:** When rolling back is impossible or riskier than moving ahead (e.g., an irreversible database schema migration or a live zero-day patch), engineers deploy a rapid **hotfix / patch forward** to stabilize the system instead of reverting.
* **Practical Task:**
  1. Document a **Decision Rule** comparing when to use **Backout** (e.g., firewall rule broke VPN connectivity $\rightarrow$ revert ACL) vs. **Fail-Forward** (e.g., critical active zero-day vulnerability where reverting leaves the server exposed $\rightarrow$ apply emergency hotfix patch).

### 9. Maintenance Windows
* **Concept:** Pre-scheduled, low-traffic time blocks (e.g., Sundays `02:00–05:00 UTC`) authorized for disruptive changes, patching, and reboots so business impact is minimized and SOC analysts know alerts during that window are expected.
* **Practical Task (Suppress/Tag Alerts During a Maintenance Window in Python):**
  ```python
  from datetime import datetime, time

  maint_start = time(2, 0)   # 02:00 UTC
  maint_end   = time(4, 0)   # 04:00 UTC
  alert_time  = time(2, 45)  # Service restart alert at 02:45 UTC

  if maint_start <= alert_time <= maint_end:
      print("[INFO] Event occurred inside authorized Maintenance Window (RFC-042). Suppressing pager alert.")
  else:
      print("[ALERT] Unauthorized service disruption outside Maintenance Window!")
  ```

### 10. Standard Operating Procedures (SOPs)
* **Concept:** Step-by-step, repeatable written instructions ensuring every technician executes routine operational and security tasks (e.g., onboarding a user, rotating TLS certificates, patching servers) consistently and without missed security steps.
* **Practical Task:**
  1. Write a clean, 4-step **TLS Certificate Renewal SOP** (`sop_tls_renewal.md`) covering: (1) Backup existing cert/key, (2) Generate CSR / renew cert, (3) Verify private key permissions (`chmod 600`), (4) Reload web server & verify expiry via `openssl s_client`.

---

## Part C: Operational Controls, Restarts & Legacy Systems

### 11. Allow Lists and Deny Lists
* **Concept:**
  * **Allow List (Whitelisting):** Default-deny model permitting *only* explicitly approved applications, IPs, or domains (strongest security posture, e.g., AppLocker / WDAC).
  * **Deny List (Blacklisting):** Default-allow model blocking *only* known malicious hashes, IPs, or apps (easier to manage, less secure against zero-days).
* **Practical Task (Implement an Application Allow-List Check in Python):**
  ```python
  approved_binaries = {"sshd", "nginx", "python3", "systemd"}
  running_processes = ["systemd", "sshd", "nginx", "ncat_reverse_shell.bin"]

  for proc in running_processes:
      if proc not in approved_binaries:
          print(f"[ALLOW-LIST VIOLATION] Unauthorized binary blocked/flagged: {proc}")
  ```

### 12. Restricted Activities
* **Concept:** High-risk actions prohibited during peak business hours, freeze periods (e.g., holiday retail freezes or fiscal year-end), or without explicit privileged authorization (e.g., modifying production firewall rules, schema drops, or rebooting core domain controllers).
* **Practical Task (Enforce a Change Freeze Check):**
  1. Add a freeze-period guard to a deployment script:
     ```python
     change_freeze_active = True
     is_emergency_security_patch = False

     if change_freeze_active and not is_emergency_security_patch:
         print("[DENIED] Restricted Activity: Production changes frozen until fiscal quarter close.")
     ```

### 13. Downtime
* **Concept:** Planned (scheduled maintenance) or unplanned (outage/incident) periods during which a system or service is unavailable. Security changes must balance risk reduction against Service Level Agreement (**SLA**) uptime targets.
* **Practical Task:**
  1. Measure system uptime and recent reboot history to audit historical downtime:
     * **Linux:** `uptime -p && last reboot | head -n 5`
     * **Windows (PowerShell):** `(Get-Date) - (Get-CimInstance Win32_OperatingSystem).LastBootUpTime`

### 14. Service Restarts
### 14. Service Restarts
* **Concept:** Restarting or reloading an OS background daemon/service (e.g., `sshd`, `nginx`, `ufw`, `WinDefend`) so updated security policies, firewall rules, or patches load into active memory.
  * **`reload` vs. `restart`:** `reload` gracefully re-reads configuration files without dropping existing user sessions; `restart` terminates the process and starts a fresh instance (causing brief interruption).
* **Practical Task:**
  * **Linux (`systemd`):**
    ```bash
    # Verify service configuration before reloading/restarting
    sudo systemctl status ssh
    sudo systemctl reload sshd 2>/dev/null || sudo systemctl restart ssh
    ```
  * **Windows (PowerShell):**
    ```powershell
    Get-Service -Name W32Time | Select-Object Name, Status, StartType
    # Simulate a safe restart check using -WhatIf before executing in production:
    Restart-Service -Name W32Time -WhatIf
    ```

---

### 15. Application Restarts
* **Concept:** Restarting a user-space application, web worker pool, or container runtime so updated environment variables, rotated API secrets, or patched application libraries take effect.
* **Practical Task (Verify Process ID & Start Time Before and After Restart):**
  * **Linux (Bash / Docker):**
    ```bash
    # Launch a background test web container, check its PID/uptime, and restart it
    docker run -d --name app_restart_lab nginx:alpine
    docker inspect app_restart_lab --format 'PID: {{.State.Pid}} | StartedAt: {{.State.StartedAt}}'

    docker restart app_restart_lab
    docker inspect app_restart_lab --format 'New PID: {{.State.Pid}} | New StartedAt: {{.State.StartedAt}}'

    docker rm -f app_restart_lab
    ```
  * **Windows (PowerShell):**
    ```powershell
    Get-Process -Name explorer | Select-Object ProcessName, Id, StartTime
    ```

---

### 16. Legacy Applications
* **Concept:** Outdated software, frameworks, or OS platforms that no longer receive vendor security patches or rely on deprecated, broken cryptography (e.g., SSLv3, TLS 1.0/1.1, SMBv1, NTLMv1).
  * *Change Management Approach:* Because upgrading legacy apps often breaks business workflows, teams must run thorough regression tests in staging and deploy **compensating controls** (network microsegmentation, WAF virtual patching, strict ACLs) until migration is complete.
* **Practical Task (Audit an Endpoint for Deprecated/Legacy TLS Protocols):**
  1. Use `openssl` to verify that a modern HTTPS server properly rejects deprecated **TLS 1.0** and **TLS 1.1** handshakes while accepting **TLS 1.2 / 1.3**:
     ```bash
     # Attempt a legacy TLS 1.1 connection (Secure servers should reject with an alert/error)
     openssl s_client -connect example.com:443 -tls1_1 </dev/null 2>&1 | grep -iE "Protocol|alert|error"

     # Confirm modern TLS 1.3 negotiation succeeds
     openssl s_client -connect example.com:443 -tls1_3 </dev/null 2>&1 | grep -iE "Protocol|Cipher"
     ```

---

### 17. Application Dependencies
* **Concept:** Shared OS libraries (`.so` on Linux, `.dll` on Windows), third-party packages (`pip`, `npm`, `Maven`), databases, or external APIs required by an application.
  * *Security Impact:* Updating or removing a shared library during a change can break downstream apps—and vulnerable third-party dependencies introduce **Software Supply Chain** risks (e.g., Log4Shell).
* **Practical Task (Map Binary & Package Dependencies Before Patching):**
  * **Linux (Inspect dynamically linked shared libraries of `/usr/bin/ssh` or `/bin/ls`):**
    ```bash
    ldd /bin/ls
    ```
  * **Windows (PowerShell — Inspect loaded DLL modules of a running process):**
    ```powershell
    Get-Process -Id \$PID | Select-Object -ExpandProperty Modules | Select-Object -First 10 ModuleName, FileName
    ```
  * **Python (Generate a Software Bill of Materials / dependency freeze list):**
    ```bash
    pip freeze > requirements_baseline.txt && head -n 10 requirements_baseline.txt
    ```

---

## Part D: Documentation & Configuration Tracking

### 18. Updating Security Diagrams
* **Concept:** Updating network topology maps, firewall boundary charts, data-flow diagrams (DFDs), and cloud architecture schematics immediately after any infrastructure change. Outdated diagrams blind incident responders during live breaches and cause compliance audit failures.
* **Practical Task (Maintain Diagram-as-Code in Markdown / Mermaid):**
  1. Whenever a firewall, WAF, or segmented subnet is added via a Change Request, update the Mermaid diagram directly inside your Git documentation repository so diagram changes are version-controlled alongside code:
     ```markdown
     ```mermaid
     flowchart LR
       User([External Client]) -->|HTTPS :443| WAF[Cloud WAF - Added RFC-042]
       WAF -->|TLS 1.3| RP[Reverse Proxy / Load Balancer]
       RP -->|Segmented VLAN 20| App[Application Server 10.20.1.15]
       App -->|Encrypted SQL :5432| DB[(Restricted DB Subnet 10.20.2.50)]
     ```
     ```

---

### 19. Updating Policies and Procedures
* **Concept:** Revising organizational governance documents—including **Policies** (high-level mandates), **Standards** (specific technical requirements like AES-256 or TLS 1.3), and **SOPs/Runbooks** (step-by-step instructions)—whenever new technologies, threats, or regulatory rules are introduced.
* **Practical Task (Update a Security Standard with Revision Metadata):**
  ```bash
  cat << 'EOF' > crypto_standard.md
  # Cryptographic & Transport Security Standard (v2.1)
  - **Effective Date:** 2026-11-21
  - **Approved By:** Change Advisory Board (RFC-042)
  - **Mandate:** TLS 1.0 and TLS 1.1 are strictly prohibited across all public and internal endpoints. Only TLS 1.2 (with AEAD ciphers) and TLS 1.3 are permitted.
  - **Procedure Reference:** See `sop_tls_renewal.md` for certificate rotation steps.
  EOF
  cat crypto_standard.md
  ```

---

### 20. Version Control
* **Concept:** Using a distributed Version Control System (**Git**) to track every modification to source code, Infrastructure as Code (IaC), firewall rules, and security policies. Provides:
  * **Accountability / Non-repudiation:** Cryptographic commit hashes (`SHA-1`/`SHA-256`), author identity, and timestamps.
  * **Diff Auditing:** Exact line-by-line comparison of what changed (`git diff`).
  * **Instant Backout:** One-command rollback (`git revert`) if a change introduces a bug or security regression.
* **Practical Task (Complete Git Change Control, Audit & Rollback Lab):**
  ```bash
  # 1. Initialize a configuration & policy repository
  mkdir -p ~/secplus_change_lab && cd ~/secplus_change_lab
  git init
  git config user.name "SecOps Change Owner"
  git config user.email "secops@corp.local"

  # 2. Commit baseline secure firewall config
  cat << 'EOF' > firewall_rules.conf
  DEFAULT_INBOUND=DENY
  ALLOW_TCP=443
  ALLOW_SSH_FROM=10.10.0.0/24
  EOF
  git add firewall_rules.conf
  git commit -m "Baseline: Approved production firewall policy (RFC-001)"

  # 3. Simulate an unauthorized or risky change (opening SSH to the entire internet)
  sed -i 's|10.10.0.0/24|0.0.0.0/0|' firewall_rules.conf

  # 4. Audit the exact configuration drift using git diff
  git diff

  # 5. Commit the bad change to history, then safely roll back using git revert
  git commit -am "RFC-099: Temporary SSH access"
  git revert HEAD --no-edit

  # 6. Verify the clean backout and inspect the full immutable audit log
  cat firewall_rules.conf
  git log --oneline
  ```

---

### Objective 1.2 Completion Checklist
- [ ] Executed graceful vs. full **service and application restarts** (`systemctl`, `Restart-Service`, `docker restart`) and verified PID/timestamp changes.
- [ ] Tested an endpoint with `openssl s_client` to detect deprecated **legacy TLS protocols** (`-tls1_1`) vs. modern TLS 1.3.
- [ ] Mapped binary and package **application dependencies** (`ldd`, `Get-Process -Modules`, `pip freeze`).
- [ ] Updated **Diagram-as-Code** architecture maps and **Cryptographic Security Standards** to reflect infrastructure changes.
- [ ] Practiced **Git version control** auditing (`git diff`, `git log`) and executed a clean **backout/rollback** using `git revert`.
