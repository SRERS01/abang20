### 2. Security Auditing & Web Vulnerabilities (Section 3: Email & Messaging)

In authorized penetration testing and bug bounty hunting, email and messaging protocols frequently connect to web vulnerabilities through contact form header injections, password reset poisoning, SSRF pivoting, and exposed webmail backends.

#### Environment Differences: Ubuntu vs. Termux

* **Ubuntu:** Full support for DNS query tools (`dig`), SMTP testing suites (`swaks`), and raw socket Nmap scripts.
* **Termux:** All standard CLI tools (`dig` via `dnsutils`, `openssl`, `nc`, `curl`, and Perl/Python tools like `swaks`) install cleanly and run without root.

#### Protocol-by-Protocol Breakdown

##### 1. SMTP (Ports 25, 465, 587)

* **How it is audited (Ubuntu & Termux):**
  * **Open Relay & User Enumeration:** Checking whether the mail server relays unauthenticated external emails (`smtp-open-relay`) or leaks valid internal usernames via `VRFY`, `EXPN`, or `RCPT TO` commands.
  * **Spoofing & DNS Record Checks:** Auditing SPF, DKIM, and DMARC DNS records to verify if an attacker can spoof emails from the target domain.
  * **Additional Auditing Commands:**
    ```bash
    # Enumerate SMTP commands, open relays, and users via Nmap
    nmap -sT -p 25,465,587 --script smtp-commands,smtp-open-relay,smtp-enum-users <target>

    # Check SPF and DMARC DNS records for email spoofing vulnerabilities
    dig TXT <target.com> +short
    dig TXT _dmarc.<target.com> +short

    # Manually test VRFY/EXPN commands via Netcat
    nc -nv <target> 25

    # Send a test email to verify relay rules using swaks (Ubuntu & Termux)
    swaks --to victim@target.com --from spoof@target.com --server <target>
    ```
* **Web Bugs Found:**
  * **SMTP Header Injection:** Web contact forms or "Share via Email" features that fail to sanitize newline characters (`%0A`, `%0D`), allowing attackers to inject `BCC:` headers and turn the web server into a spam/phishing relay.
  * **SSRF to Internal SMTP (`gopher://`):** Using a web SSRF vulnerability to send raw SMTP commands to an internal-only mail server (`127.0.0.1:25`), bypassing external firewall restrictions.

##### 2. IMAP (Ports 143, 993) & POP3 (Ports 110, 995)

* **How it is audited (Ubuntu & Termux):**
  * **Cleartext Authentication & TLS Checks:** Verifying whether unencrypted ports (143/110) allow plaintext login without enforcing `STARTTLS`, and inspecting SSL/TLS certificate details.
  * **Additional Auditing Commands:**
    ```bash
    # Check IMAP/POP3 capabilities and cleartext login support
    nmap -sT -p 110,143,993,995 --script imap-capabilities,pop3-capabilities <target>

    # Connect to IMAPS (port 993) via OpenSSL to inspect certificates and test login
    openssl s_client -connect <target>:993 -crlf

    # Connect to POP3S (port 995) via OpenSSL
    openssl s_client -connect <target>:995 -crlf
    ```
* **Web Bugs Found:**
  * **IMAP / POP3 Command Injection in Webmail:** Custom webmail interfaces that pass user-controlled search queries or folder names directly into backend IMAP commands without sanitization.
  * **Leaked Mail Credentials in Web Configs:** Discovering hardcoded IMAP/SMTP credentials inside exposed `.env`, `wp-config.php`, or `configuration.php` files.

##### 3. XMPP (Port 5222) & IRC (Ports 194, 6667)

* **How it is audited (Ubuntu & Termux):**
  * **Unauthenticated Access & Registration:** Checking if XMPP allows in-band account registration or unencrypted connections, and inspecting IRC servers for open channels.
  * **Additional Auditing Commands:**
    ```bash
    # Enumerate XMPP server features and authentication mechanisms
    nmap -sT -p 5222 --script xmpp-info <target>

    # Probe IRC server banners and info
    nmap -sT -p 6667 --script irc-info <target>

    # Connect to an unencrypted IRC port manually via Netcat
    nc -nv <target> 6667
    ```
* **Web Bugs Found:**
  * **Exposed Web-Based Chat Gateways (BOSH / WebSockets):** XMPP servers often expose HTTP binding endpoints (`/http-bind/` on ports `5280` or `7070`) vulnerable to SSRF, XSS in web chat clients, or sensitive information disclosure in public developer channels.

---

### 2. Security Auditing & Web Vulnerabilities (Section 5: Network Naming, Addressing & Configuration)

In authorized penetration testing and bug bounty hunting, naming and directory protocols are critical for attack surface discovery (subdomains), cloud takeovers, and web authentication bypasses.

#### Environment Differences: Ubuntu vs. Termux

* **Ubuntu:** Full support for raw packet DHCP/ARP auditing (`sudo`), DNS tools (`dig`, `subfinder`), and Active Directory suites (`ldapsearch`, `impacket`, `kerbrute`).
* **Termux:** DNS (`dig`, `subfinder`) and directory tools (`ldap-utils`, `kerbrute` Go binary, Python `impacket`) work natively without root. Raw Layer-2 DHCP testing is restricted on non-rooted Android devices.

#### Protocol-by-Protocol Breakdown

##### 1. DNS (Port 53)

* **How it is audited (Ubuntu & Termux):**
  * **Zone Transfers (`AXFR`) & Record Enumeration:** Testing if authoritative name servers misconfigure zone transfers, exposing every internal and external subdomain at once.
  * **Subdomain & CNAME Auditing:** Enumerating subdomains and inspecting CNAME records for dangling pointers to unclaimed third-party services.
  * **Additional Auditing Commands:**
    ```bash
    # Find authoritative nameservers for a domain
    dig NS <target.com> +short

    # Attempt a DNS Zone Transfer (AXFR) against a nameserver
    dig axfr @<://target.com> <target.com>

    # Enumerate DNS records and check for cache snooping via Nmap
    nmap -sT -p 53 --script dns-nsid,dns-recursion <target>

    # Passive subdomain discovery (Go binary works on both Ubuntu & Termux)
    subfinder -d <target.com> -silent
    ```
* **Web Bugs Found:**
  * **Subdomain Takeover:** When a subdomain (`://target.com`) has a CNAME record pointing to an expired cloud service (AWS S3, GitHub Pages, Heroku, Azure) that an attacker can claim to host malicious web content under the victim's domain.
  * **DNS Rebinding (SSRF Bypass):** Configuring a malicious DNS server to resolve a domain first to a public IP (passing web SSRF validation) and immediately afterward to `127.0.0.1` (accessing internal web admin panels).

##### 2. DHCP (Ports 67, 68 - UDP)

* **How it is audited (Ubuntu & Termux):**
  * **DHCP Discover & Rogue Server Checks:** Querying local DHCP servers to inspect offered gateway, DNS, and WPAD options (requires root on Ubuntu).
  * **Additional Auditing Commands:**
    ```bash
    # Broadcast a DHCP Discover packet to inspect server options (Ubuntu root required)
    sudo nmap --script broadcast-dhcp-discover
    ```
* **Web Bugs Found:**
  * **WPAD (Web Proxy Auto-Discovery) Poisoning:** If DHCP option 252 (`WPAD`) is unconfigured or spoofed on a local network, browsers automatically fetch `http://wpad/wpad.dat`, allowing an attacker to inject a malicious proxy PAC file and intercept all browser HTTP/HTTPS traffic.

##### 3. NTP (Port 123 - UDP)

* **How it is audited (Ubuntu & Termux):**
  * **System Info & Monlist Queries:** Querying NTP servers for OS details, internal IP addresses, and peer lists.
  * **Additional Auditing Commands:**
    ```bash
    # Query NTP server variables, OS version, and peer information
    nmap -sU -p 123 --script ntp-info,ntp-monlist <target>

    # Query NTP peers directly using ntpq (Ubuntu)
    ntpq -p <target>
    ```
* **Web Bugs Found:**
  * **Internal Infrastructure Disclosure:** Leaking internal hostnames and exact OS kernel versions used to fingerprint backend web servers.

##### 4. LDAP (Ports 389, 636)

* **How it is audited (Ubuntu & Termux):**
  * **Anonymous Bind & Base DN Enumeration:** Testing whether the LDAP directory allows unauthenticated read queries (`anonymous bind`) to dump usernames, email addresses, and group memberships.
  * **Additional Auditing Commands:**
    ```bash
    # Check for anonymous binds and dump root DSE information via Nmap
    nmap -sT -p 389,636 --script ldap-rootdse,ldap-search <target>

    # Query LDAP base naming contexts anonymously using ldapsearch (Ubuntu & Termux)
    ldapsearch -x -H ldap://<target>:389 -s base namingcontexts

    # Dump all directory entries if anonymous bind is enabled
    ldapsearch -x -H ldap://<target>:389 -b "DC=target,DC=com" "(objectClass=*)"
    ```
* **Web Bugs Found:**
  * **LDAP Injection:** Web login portals or employee search forms that concatenate user input directly into LDAP search filters (e.g., `(&(uid=USER_INPUT)(password=PASS))`), allowing authentication bypass via wildcards (`*)(uid=*))(|(uid=*`).

##### 5. Kerberos (Port 88) & RADIUS (Ports 1812, 1813)

* **How it is audited (Ubuntu & Termux):**
  * **User Enumeration & Pre-Auth Checks:** Identifying valid Active Directory usernames without triggering account lockouts by inspecting Kerberos error codes (`KDC_ERR_PREAUTH_REQUIRED` vs `KDC_ERR_C_PRINCIPAL_UNKNOWN`).
  * **Additional Auditing Commands:**
    ```bash
    # Enumerate valid Active Directory usernames via Kerberos (Ubuntu & Termux)
    kerbrute userenum --dc <target> -d <target.com> users.txt

    # Check for accounts vulnerable to AS-REP Roasting (Impacket - Ubuntu & Termux)
    GetNPUsers.py <target.com>/ -usersfile users.txt -no-pass -dc-ip <target>
    ```
* **Web Bugs Found:**
  * **SSO / Windows Integrated Auth Enumeration:** Using valid usernames discovered via Kerberos to target web-based Outlook Web Access (OWA), ADFS, or VPN portals, and abusing SPNEGO/NTLM HTTP authentication endpoints.
