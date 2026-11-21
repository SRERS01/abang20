# Part 1 – Foundations Before Security+
## Module 2: Operating Systems (Practical Lab Guide)

> **Objective:** Master OS internals, privilege boundaries, administration, and hardening across Windows, Linux, macOS, and Android before entering Security+ domains.  
> **Practical Tools Used:** Linux Terminal, Windows PowerShell, Windows Command Prompt (CMD), Bash, Termux (Android), VirtualBox.

---

### 1. Windows Fundamentals
* **Concept:** Windows relies on the NT kernel, the Windows Registry (hierarchical configuration database), Drive Letters (`C:\`), and Active Directory/Workgroup security models.
* **Practical Task (PowerShell & CMD):**
  1. Query OS edition, build number, and architecture:
     ```powershell
     Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsHardwareAbstractionLayer
     ```
  2. Query the Windows Registry from Command Prompt to view startup programs (a common malware persistence location):
     ```cmd
     reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Run
     ```

### 2. Linux Fundamentals
* **Concept:** Linux follows the Filesystem Hierarchy Standard (FHS) rooted at `/`, treats everything as a file (including hardware devices under `/dev`), and relies heavily on text-based configuration files in `/etc`.
* **Practical Task (Linux Terminal / Bash):**
  1. Explore core directories and inspect distribution details:
     ```bash
     cat /etc/os-release
     ls -la / /etc /var/log /dev | head -n 25
     ```

### 3. Android Architecture
* **Concept:** Android runs on a modified Linux kernel, isolates every app inside its own sandbox with a unique Linux User ID (UID), and uses the Android Runtime (ART) and SELinux for mandatory access control.
* **Practical Task (Termux on Android):**
  1. Open **Termux** on an Android device (or Android VM in VirtualBox) and inspect the underlying Linux kernel and app UID isolation:
     ```bash
     uname -a
     id                  # Notice your Termux app runs as a dedicated UID (e.g., u0_a215)
     getenforce          # Checks SELinux status (Enforcing = Secure)
     ```

### 4. macOS Fundamentals
* **Concept:** macOS is built on Darwin (a Unix-like OS combining the XNU hybrid kernel with BSD userland) and enforces security via Gatekeeper, System Integrity Protection (SIP), and Keychain.
* **Practical Task (macOS Terminal / Concept Check):**
  1. Inspect macOS build details and check if System Integrity Protection (SIP) is active:
     ```bash
     sw_vers
     csrutil status      # Should return: System Integrity Protection status: enabled.
     ```

### 5. Kernel Architecture (Monolithic vs. Hybrid vs. Microkernel)
* **Concept:** The kernel is the core bridge between applications and hardware. Linux uses a modular monolithic kernel; Windows NT and macOS XNU use hybrid kernels.
* **Practical Task (Linux Terminal):**
  1. List dynamically loaded kernel modules (drivers) currently running in memory:
     ```bash
     lsmod | head -n 15
     modinfo e1000       # Inspect metadata of a specific kernel module (or pick one from lsmod)
     ```

### 6. User Space and Kernel Space
* **Concept:** **User Space (Ring 3)** runs standard applications with restricted hardware access. **Kernel Space (Ring 0)** has unrestricted hardware access. Separating them prevents a crashing app from crashing the entire OS.
* **Practical Task (Linux Terminal):**
  1. Measure the split between CPU time spent in User Space (`us`) vs. Kernel Space (`sy`):
     ```bash
     vmstat 1 5          # Watch the 'us' (user) and 'sy' (system/kernel) columns
     ```

### 7. System Calls (Syscalls)
* **Concept:** Programs in User Space request privileged operations (like reading a file or opening a network socket) from the Kernel via System Calls (`open`, `read`, `write`, `execve`).
* **Practical Task (Linux Terminal):**
  1. Use `strace` to intercept and view the exact system calls made by a simple command:
     ```bash
     strace -e trace=openat,read,write ls > /dev/null
     ```

### 8. File Permissions (DAC & ACLs)
* **Concept:** Permissions control who can Read (`r`/4), Write (`w`/2), or Execute (`x`/1) files. Security+ heavily tests misconfigured permissions and privilege escalation.
* **Practical Task (Bash & PowerShell):**
  1. **Linux (Bash):** Create a sensitive file, lock down permissions, and verify:
     ```bash
     echo "TopSecretKey" > secret.key
     chmod 600 secret.key          # Owner: RW (6), Group: None (0), Others: None (0)
     ls -l secret.key
     ```
  2. **Windows (PowerShell):** View Access Control Lists (ACLs) on a file:
     ```powershell
     New-Item -Path .\secret.txt -ItemType File -Force
     icacls .\secret.txt
     ```

### 9. Users and Groups
* **Concept:** Operating systems assign unique identifiers (UID/GID on Linux; SID on Windows) to accounts and enforce Least Privilege via administrative groups (`sudo`/`wheel` on Linux, `Administrators` on Windows).
* **Practical Task:**
  1. **Linux (Bash):** Inspect user accounts and privileged group memberships:
     ```bash
     cat /etc/passwd | grep -v "nologin"
     getent group sudo wheel
     ```
  2. **Windows (CMD):** List local users and check who belongs to the local Administrators group:
     ```cmd
     net user
     net localgroup Administrators
     ```

### 10. Processes and Services
* **Concept:** Processes are active programs; Services (Windows) or Daemons (Linux) are background processes running without user interaction (often with elevated privileges).
* **Practical Task:**
  1. **Linux (Bash):** List running background services (`systemd`):
     ```bash
     systemctl list-units --type=service --state=running | head -n 15
     ```
  2. **Windows (PowerShell):** List running background services:
     ```powershell
     Get-Service | Where-Object {$_.Status -eq "Running"} | Select-Object -First 15
     ```

### 11. Memory Allocation
* **Concept:** The OS assigns isolated memory blocks (Stack for static/local variables, Heap for dynamic allocation) to each process so one process cannot read another process's secrets.
* **Practical Task (Linux Terminal):**
  1. Inspect detailed memory allocation regions (`Heap`, `Stack`, `Anon` pages) of your current shell:
     ```bash
     grep -E "Heap|Stack|VmRSS" /proc/$$/status
     ```

### 12. Virtual Memory
* **Concept:** Uses disk space (`pagefile.sys` on Windows, `swap` partition/file on Linux) to extend physical RAM and maps virtual addresses to physical RAM frames via page tables.
* **Practical Task:**
  1. **Windows (PowerShell):** Check active pagefile location and usage:
     ```powershell
     Get-CimInstance Win32_PageFileUsage | Select-Object Name, AllocatedBaseSize, CurrentUsage
     ```
  2. **Linux (Bash):** Check swap space and kernel swappiness value:
     ```bash
     free -h && cat /proc/sys/vm/swappiness
     ```

### 13. Boot Processes
* **Concept:** Power On $\rightarrow$ UEFI/BIOS (POST) $\rightarrow$ Bootloader (GRUB / Windows Boot Manager) $\rightarrow$ Kernel Initialization $\rightarrow$ Init System (`systemd` / `wininit.exe`) $\rightarrow$ Login Prompt.
* **Practical Task:**
  1. **Linux (Bash):** Analyze boot timing and kernel ring buffer boot messages:
     ```bash
     systemd-analyze
     dmesg | head -n 20
     ```
  2. **Windows (CMD):** Inspect Boot Configuration Data (BCD):
     ```cmd
     bcdedit
     ```

### 14. File Systems
* **Concept:** Structure how data is stored and indexed: **NTFS** (supports encryption EFS, compression, ACLs), **ext4** (Linux journaling), **APFS** (macOS snapshots/encryption), **FAT32/exFAT** (cross-platform, lacks modern permissions).
* **Practical Task (VirtualBox + Linux/Windows):**
  1. Attach a small virtual disk (e.g., 1GB VDI) in **VirtualBox** $\rightarrow$ Storage Settings, then format and mount it:
     * **Linux:**
       ```bash
       lsblk
       # Assuming the new disk is /dev/sdb:
       sudo mkfs.ext4 /dev/sdb
       sudo mkdir -p /mnt/labdisk && sudo mount /dev/sdb /mnt/labdisk
       df -Th /mnt/labdisk
       ```

### 15. System Logs
* **Concept:** Logs are the primary evidence source for incident response and threat hunting (authentication attempts, service crashes, privilege escalation).
* **Practical Task:**
  1. **Linux (Bash):** View recent authentication and system logs:
     ```bash
     journalctl -n 20 --no-pager
     ```
  2. **Windows (PowerShell):** Query the last 10 Security or System Event Logs:
     ```powershell
     Get-EventLog -LogName System -Newest 10 | Format-Table TimeGenerated, EntryType, Source, Message -AutoSize
     ```

### 16. Environment Variables
* **Concept:** Dynamic key-value pairs (`PATH`, `HOME`, `USERPROFILE`, `TEMP`) that dictate how processes run. Attackers abuse `PATH` hijacking to trick users into running malicious binaries.
* **Practical Task:**
  1. **Linux (Bash):** Print all environment variables and inspect executable search order (`$PATH`):
     ```bash
     env | head -n 15
     echo $PATH
     ```
  2. **Windows (PowerShell & CMD):**
     ```cmd
     set PATH
     ```

### 17. Command-Line Interfaces (CMD vs. PowerShell vs. Bash)
* **Concept:** CMD processes plain text; PowerShell processes structured .NET objects; Bash is the standard Unix/Linux command shell.
* **Practical Task:**
  1. Compare object filtering in **PowerShell** vs. text filtering (`grep`) in **Bash**:
     * **PowerShell:** `Get-Process | Where-Object {$_.CPU -gt 10}`
     * **Bash:** `ps aux | grep root`

### 18. Shell Scripting
### 18. Shell Scripting (Bash & PowerShell)
* **Concept:** Security analysts and system administrators use shell scripts (`.sh` in Bash, `.ps1` in PowerShell) to automate repetitive tasks, parse logs, enforce configurations, and hunt for indicators of compromise (IoCs).
* **Practical Task 1 (Linux / Bash — Automated Security Audit Script):**
  Create a script that collects system baseline info, checks for unauthorized UID 0 (root-level) accounts, and lists active network listeners:
  ```bash
  cat << 'EOF' > sec_baseline.sh
  #!/bin/bash
  echo "========================================="
  echo "  LINUX SECURITY BASELINE REPORT"
  echo "  Generated: \$(date)"
  echo "========================================="

  echo -e "\n[+] Current User & Privileges:"
  id

  echo -e "\n[+] Accounts with Root Privileges (UID 0):"
  awk -F: '(\$3 == "0") {print \$1}' /etc/passwd

  echo -e "\n[+] Active Listening Network Ports:"
  ss -tuln

  echo -e "\n[+] Last 5 Failed Login Attempts:"
  grep "Failed password" /var/log/auth.log 2>/dev/null | tail -n 5 || echo "No auth.log access or zero failed logins."
  EOF

  chmod +x sec_baseline.sh
  ./sec_baseline.sh
  ```

* **Practical Task 2 (Windows / PowerShell — Suspicious Process & Service Check):**
  Run a PowerShell script to check execution policy and list any non-Microsoft services currently running:
  ```powershell
  Get-ExecutionPolicy
  Get-CimInstance Win32_Service | Where-Object { \(_.State -eq "Running" -and \)_.PathName -notlike "*Windows*" } | Select-Object Name, DisplayName, PathName
  ```

---

### 19. System Administration
* **Concept:** Maintaining system availability, integrity, and hygiene through patch management, user lifecycle management, disk monitoring, and scheduled jobs (`cron` in Linux, Task Scheduler in Windows). Attackers frequently abuse scheduled tasks for **persistence**.
* **Practical Task 1 (Linux / Bash — Patching & Scheduled Tasks):**
  1. Check for pending security updates and inspect system-wide scheduled `cron` jobs:
     ```bash
     sudo apt update && apt list --upgradable    # Debian/Ubuntu
     crontab -l                                  # Current user's cron jobs
     ls -la /etc/cron.d /etc/cron.daily          # System-wide scheduled jobs
     ```
  2. Create a temporary user, add them to a group, and then safely remove them (User Lifecycle):
     ```bash
     sudo useradd -m labuser
     sudo usermod -aG sudo labuser
     id labuser
     sudo userdel -r labuser                     # Cleans up user and home directory
     ```

* **Practical Task 2 (Windows / CMD & PowerShell — Persistence & Patch Audit):**
  1. Check installed Windows hotfixes/patches:
     ```powershell
     Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 10
     ```
  2. Audit non-Microsoft scheduled tasks (common malware persistence check):
     ```powershell
     Get-ScheduledTask | Where-Object { \(_.TaskPath -notlike "\Microsoft*" -and \)_.State -eq "Ready" } | Select-Object TaskName, TaskPath, State
     ```

---

### 20. Operating System Hardening
* **Concept:** Hardening shrinks the attack surface by disabling unnecessary services/ports, enforcing strong password/account lockout policies, enabling host firewalls, applying Principle of Least Privilege, and enabling full-disk encryption. *(Perform these steps inside your **VirtualBox** lab VMs).*
* **Practical Task 1 (Linux VM — SSH, Firewall & Kernel Hardening):**
  1. **Host Firewall (`ufw`):** Set default deny for incoming traffic and allow only required ports:
     ```bash
     sudo ufw default deny incoming
     sudo ufw default allow outgoing
     sudo ufw allow 22/tcp
     sudo ufw enable
     sudo ufw status verbose
     ```
  2. **SSH Daemon Hardening (`/etc/ssh/sshd_config`):** Inspect critical SSH security settings (disabling direct root login and empty passwords):
     ```bash
     sudo grep -E "^PermitRootLogin|^PasswordAuthentication|^PermitEmptyPasswords" /etc/ssh/sshd_config
     ```
  3. **Kernel Network Hardening (`sysctl`):** Verify protections against SYN flood attacks and IP spoofing:
     ```bash
     sysctl net.ipv4.tcp_syncookies              # Should be 1 (Enabled)
     sysctl net.ipv4.conf.all.rp_filter          # Should be 1 (Strict Reverse Path Filtering)
     ```

* **Practical Task 2 (Windows VM — Firewall, Account Lockout & Defender Hardening):**
  1. **Verify Windows Defender Real-Time Protection & Firewall:**
     ```powershell
     Get-MpComputerStatus | Select-Object RealTimeProtectionEnabled, AntivirusEnabled, IoavProtectionEnabled
     Get-NetFirewallProfile | Select-Object Name, Enabled, DefaultInboundAction, DefaultOutboundAction
     ```
  2. **Audit Password & Account Lockout Policies (Defends against Brute-Force Attacks):**
     ```cmd
     net accounts
     ```
     *(Optional Hardening)* Enforce account lockout after 5 failed attempts:
     ```cmd
     net accounts /lockoutthreshold:5 /lockoutduration:15 /lockoutwindow:15
     ```
  3. **Disable Legacy/Insecure Protocols (SMBv1):**
     ```powershell
     Get-WindowsOptionalFeature -Online -FeatureName SMB1Protocol
     ```

---

## Practical Tools: Hands-On Lab Matrix

Use this checklist to ensure you have practiced every required tool from Module 2 in a real or virtualized environment:

| Tool | Environment | Core Practical Exercise Completed |
| :--- | :--- | :--- |
| **VirtualBox** | Host Machine | Created a Linux VM (Ubuntu) and Windows VM; took a **Snapshot** before applying OS hardening rules so you can safely roll back changes. |
| **Linux Terminal** | Ubuntu VM | Navigated `/etc`, `/var/log`, and `/proc`; inspected kernel modules (`lsmod`) and system calls (`strace`). |
| **Bash** | Ubuntu VM | Modified file permissions (`chmod 600`), managed users/groups, configured `ufw`, and wrote `sec_baseline.sh`. |
| **Windows PowerShell** | Windows VM | Queried objects (`Get-Process`, `Get-Service`), audited Event Logs (`Get-EventLog`), checked Defender status, and inspected ACLs (`icacls`). |
| **Windows Command Prompt** | Windows VM | Queried Registry Run keys (`reg query`), checked boot config (`bcdedit`), and configured account lockout policies (`net accounts`). |
| **Termux** | Android Device / VM | Verified Android's Linux kernel (`uname -a`), checked isolated app UID (`id`), and verified SELinux enforcement (`getenforce`). |

