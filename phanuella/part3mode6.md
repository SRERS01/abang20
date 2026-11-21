# Part 3 – Practical Security+ Laboratory Syllabus
## Module 6: Identity and Access Management (IAM) Laboratory

> **Lab Environment:** Windows Server VM (Active Directory Domain Services), Ubuntu/Debian Linux VM, Docker (for running a local **Keycloak** IdP + **OpenLDAP** lab), PowerShell, Bash.  
> **Safety Best Practice:** Snapshot your Windows Server and Linux VMs before modifying `sudoers`, PAM, or Group Policy Objects (GPOs).

---

### Lab 1: Create User Accounts (Active Directory & Linux)
* **Objective:** Provision standard user accounts and non-interactive service accounts following naming conventions and password-aging policies.
* **Hands-On Steps:**
  * **Windows Server (PowerShell — Active Directory):**
    ```powershell
    $SecurePass = ConvertTo-SecureString "Buea@Lab2026!Secure" -AsPlainText -Force
    New-ADUser -Name "Ambe Fon" `
      -SamAccountName "afon" `
      -UserPrincipalName "afon@secplus.local" `
      -AccountPassword $SecurePass `
      -Enabled $true `
      -ChangePasswordAtLogon $true
    ```
  * **Linux (Bash):**
    ```bash
    # Standard human user + non-interactive service account
    sudo useradd -m -s /bin/bash -c "Ambe Fon - SOC Analyst" afon
    sudo useradd -r -s /usr/sbin/nologin svc_siem_collector
    sudo chage -M 90 -m 2 -W 7 afon
    ```

---

### Lab 2: Configure Groups (RBAC Security Groups)
* **Objective:** Implement **Role-Based Access Control (RBAC)** by organizing users into functional security groups rather than assigning permissions to individual accounts.
* **Hands-On Steps:**
  * **Windows Server (PowerShell — Active Directory):**
    ```powershell
    New-ADGroup -Name "Role_SOC_Analysts" -GroupScope Global -GroupCategory Security
    Add-ADGroupMember -Identity "Role_SOC_Analysts" -Members "afon"
    Get-ADGroupMember -Identity "Role_SOC_Analysts" | Select-Object Name, SamAccountName
    ```
  * **Linux (Bash):**
    ```bash
    sudo groupadd -f role_soc_analysts
    sudo usermod -aG role_soc_analysts afon
    groups afon
    ```

---

### Lab 3: Assign Permissions (NTFS ACLs & Linux `chmod` / `setfacl`)
* **Objective:** Enforce Discretionary Access Control (DAC) permissions on shared folders so only authorized RBAC groups can read/write sensitive files.
* **Hands-On Steps:**
  * **Windows Server (PowerShell):**
    ```powershell
    New-Item -Path "C:\SOC_Evidence" -ItemType Directory -Force
    icacls "C:\SOC_Evidence" /inheritance:r
    icacls "C:\SOC_Evidence" /grant "Administrators:(OI)(CI)F" "Role_SOC_Analysts:(OI)(CI)M"
    icacls "C:\SOC_Evidence"
    ```
  * **Linux (Bash):**
    ```bash
    sudo mkdir -p /srv/soc_evidence
    sudo chown root:role_soc_analysts /srv/soc_evidence
    sudo chmod 2770 /srv/soc_evidence   # 2 = SGID (new files inherit group ownership), 770 = rwxrwx---
    ls -ld /srv/soc_evidence
    ```

---

### Lab 4: Configure MFA (Linux PAM TOTP & Keycloak FIDO2/OTP)
* **Objective:** Enforce Multi-Factor Authentication using Time-Based One-Time Passwords (**TOTP**) for Linux SSH and **Keycloak** web SSO.
* **Hands-On Steps:**
  * **Linux SSH TOTP (`libpam-google-authenticator`):**
    ```bash
    # Install PAM TOTP module on Ubuntu/Debian
    sudo apt update && sudo apt install -y libpam-google-authenticator

    # Initialize TOTP secret & emergency backup codes for current user (non-interactive demo flags)
    google-authenticator -t -d -f -r 3 -R 30 -w 3
    ```
  * **Keycloak IdP (Docker Quick-Start for MFA & SSO Lab):**
    ```bash
    docker run -d --name keycloak-lab -p 8080:8080 \
      -e KC_BOOTSTRAP_ADMIN_USERNAME=admin \
      -e KC_BOOTSTRAP_ADMIN_PASSWORD=AdminLabPassword2026! \
      quay.io/keycloak/keycloak:latest start-dev
    ```
    * Open `http://127.0.0.1:8080` → Log in as `admin` → **Authentication** → **Required Actions** → Enable **Configure OTP** and **WebAuthn Register (Passkey/Hardware Token)**.

---

### Lab 5: Implement Least Privilege (Scoped `sudo` & Windows JEA/Delegation)
* **Objective:** Replace blanket administrator/root access with granular, command-specific privileges using `/etc/sudoers.d/` and Active Directory OU delegation.
* **Hands-On Steps:**
  * **Linux (Grant `afon` permission to restart ONLY `nginx` via `sudo`, nothing else):**
    ```bash
    echo "afon ALL=(root) NOPASSWD: /usr/bin/systemctl restart nginx" | sudo tee /etc/sudoers.d/soc_nginx_only
    sudo chmod 440 /etc/sudoers.d/soc_nginx_only
    sudo visudo -cf /etc/sudoers.d/soc_nginx_only
    ```

---

### Lab 6: Configure Access Policies (Password, Lockout & Conditional Access)
* **Objective:** Enforce account lockout thresholds against online brute force and configure password length/complexity policies via Group Policy (`GPO`) and PAM.
* **Hands-On Steps:**
  * **Windows Server (PowerShell — Set Default Domain Password & Lockout Policy):**
    ```powershell
    Set-ADDefaultDomainPasswordPolicy -Identity "secplus.local" `
      -MinPasswordLength 14 `
      -PasswordHistoryCount 24 `
      -MaxPasswordAge (New-TimeSpan -Days 90) `
      -MinPasswordAge (New-TimeSpan -Days 2) `
      -LockoutThreshold 5 `
      -LockoutDuration (New-TimeSpan -Minutes 30) `
      -LockoutObservationWindow (New-TimeSpan -Minutes 30)
    ```
  * **Keycloak Conditional / Time-Based / IP Access Policy:**
    * Inside Keycloak Admin Console $\rightarrow$ **Realm Settings** $\rightarrow$ **Sessions** $\rightarrow$ Set **SSO Session Idle** to `15 minutes` and **SSO Session Max** to `8 hours`.

---

### Lab 7: Investigate Authentication Logs (Windows Event IDs & Linux `auth.log`)
* **Objective:** Hunt for brute-force logins, password spraying, account lockouts, and successful privileged logons across Windows Security Logs and Linux `journalctl`/`auth.log`.
* **Hands-On Steps:**
  * **Windows Server (PowerShell — Event ID `4625` Failed Logon, `4740` Lockout, `4624` Success):**
    ```powershell
    # Query last 10 failed logon events (Event ID 4625)
    Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4625} -MaxEvents 10 -ErrorAction SilentlyContinue |
      Select-Object TimeCreated, Id, Message
    ```
  * **Linux (Bash):**
    ```bash
    # Summarize failed vs. accepted SSH authentication events
    journalctl -u ssh --no-pager 2>/dev/null | grep -iE "Failed password|Accepted" | tail -n 15
    ```

---

### Lab 8: Configure SSO Concepts (SAML 2.0, OIDC & LDAP Federation)
* **Objective:** Understand how an Identity Provider (**Keycloak**) federates authentication with an **LDAP** directory and issues **SAML 2.0** / **OpenID Connect (OIDC)** tokens to Service Providers.
* **Hands-On Steps:**
  1. In **Keycloak (`http://127.0.0.1:8080`)** $\rightarrow$ Create a new Realm named `SecPlus-Corp`.
  2. Navigate to **User Federation** $\rightarrow$ **Add provider** $\rightarrow$ **LDAP** to inspect how Keycloak maps Active Directory/OpenLDAP users (`cn`, `uid`, `mail`) into centralized SSO sessions.
  3. Navigate to **Clients** $\rightarrow$ **Create client** $\rightarrow$ Compare **OpenID Connect (OIDC/OAuth2 JSON)** vs. **SAML 2.0 (XML Assertions)** client endpoints (`Redirect URIs`, `Signing Keys`).
  4. *(Clean up Docker container when done: `docker rm -f keycloak-lab`)*.

---

### Lab 9: Audit Privileged Accounts
* **Objective:** Identify all domain administrators, local administrators, `UID 0` accounts, and dormant privileged accounts to prevent privilege creep.
* **Hands-On Steps:**
  * **Windows Server (PowerShell):**
    ```powershell
    Get-ADGroupMember -Identity "Domain Admins" -Recursive | Select-Object Name, SamAccountName, ObjectClass
    Search-ADAccount -AccountInactive -TimeSpan 90.00:00:00 | Select-Object Name, SamAccountName, LastLogonDate
    ```
  * **Linux (Bash):**
    ```bash
    # Audit UID 0 accounts and members of sudo/wheel groups
    awk -F: '(\$3 == "0") {print "UID 0:", \$1}' /etc/passwd
    getent group sudo wheel 2>/dev/null
    ```

---

### Lab 10: Identify Privilege Escalation Risks
* **Objective:** Proactively scan Linux and Windows endpoints for common misconfigurations that allow low-privilege users to escalate to `root` or `NT AUTHORITY\SYSTEM`.
* **Hands-On Steps:**
  * **Linux Privilege Escalation Audit:**
    ```bash
    # 1. Check for unexpected SUID binaries
    find /usr/bin /usr/local/bin -perm -4000 -type f 2>/dev/null

    # 2. Check for world-writable cron scripts or /etc/passwd permissions
    ls -l /etc/passwd /etc/shadow
    find /etc/cron* -perm -0002 -type f 2>/dev/null || echo "[PASS] No world-writable cron files."
    ```
  * **Windows Privilege Escalation Audit (PowerShell — Unquoted Service Paths & AlwaysInstallElevated):**
    ```powershell
    # 1. Detect Unquoted Service Paths containing spaces
    Get-CimInstance Win32_Service | Where-Object { \(_.PathName -notlike '"*' -and \)_.PathName -like '* *' } | Select-Object Name, PathName

    # 2. Check if AlwaysInstallElevated registry key is dangerously enabled (1)
    Get-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\Installer" -Name "AlwaysInstallElevated" -ErrorAction SilentlyContinue
    ```

---

### Module 6 Lab Completion Checklist
- [ ] Created standard and service accounts in **Active Directory** and **Linux**, and assigned **RBAC Security Groups**.
- [ ] Configured restrictive **NTFS ACLs (`icacls`)** and **Linux SGID/DAC permissions (`chmod 2770`)**.
- [ ] Configured **MFA** via Linux PAM TOTP (`google-authenticator`) and **Keycloak** OTP/WebAuthn.
- [ ] Enforced **Least Privilege** (`visudo` command restriction) and **Domain Password/Lockout Policies**.
- [ ] Investigated **Authentication Logs** (`Event ID 4625/4740`, `journalctl`), explored **Keycloak SSO/LDAP Federation**, and audited **Privileged Accounts & Privilege Escalation Risks**.
