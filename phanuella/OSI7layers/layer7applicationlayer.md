## Layer 7: Application Layer (End-User Protocols, APIs & Web Services)

The Application Layer is the closest layer to the end user. It provides network services directly to software applications—defining message syntax, request/response semantics, authentication flows, and application-level logic across protocols like **HTTP/HTTPS**, **DNS**, **SMTP**, **SSH**, and **LDAP**.

### Environment Differences: Ubuntu vs. Termux
* **Ubuntu:** Full support for heavy GUI/CLI web auditing suites (`Burp Suite`, `OWASP ZAP`, `Caido`), headless browser fuzzers (`nuclei`, `ffuf`, `katana`), and directory/Active Directory tools (`bloodhound`, `ldapsearch`).
* **Termux:** Nearly all CLI-based Layer 7 auditing tools run natively without root—including Go/Python scanners (`ffuf`, `nuclei`, `sqlmap`, `httpx`, `subfinder`, `dalfox`), `curl`, `dig`, and `ssh`.

---

### Core Layer 7 Protocols & Testing Tools

| Protocol / Standard | Full Name & Role | Security Auditing Focus | Testing Tools (Ubuntu & Termux) |
| :--- | :--- | :--- | :--- |
| **HTTP / HTTPS (HTTP/1.1, HTTP/2, HTTP/3)** | Hypertext Transfer Protocol (web browsing, REST APIs, GraphQL, gRPC). | **OWASP Top 10** (SQLi, XSS, IDOR/BOLA, SSRF, CSRF, RCE), HTTP/2 rapid reset/smuggling, CORS misconfigurations, and JWT flaws. | `curl`, `ffuf`, `nuclei`, `sqlmap`, `httpx`, `burpsuite`, `caido` |
| **DNS** | Domain Name System (resolves human-readable domain names to IP records). | Zone transfers (`AXFR`), subdomain enumeration/takeovers, cache poisoning, DNS rebinding (SSRF bypass), and DNS tunneling. | `dig`, `nslookup`, `subfinder`, `amass`, `dnsx`, `fierce` |
| **SMTP / IMAP / POP3** | Simple Mail Transfer Protocol & Mail Retrieval (email routing and delivery). | Open mail relays, missing **SPF / DKIM / DMARC** (email spoofing), user enumeration (`VRFY`/`EXPN`/`RCPT TO`), and cleartext credential sniffing. | `swaks`, `nmap --script smtp-*`, `telnet`, `openssl s_client`, `hydra` |
| **SSH** | Secure Shell (encrypted remote administration, SFTP, and port forwarding). | Weak/default credentials, outdated SSH versions, exposed private keys, weak KEX/MAC algorithms, and SSH agent forwarding abuse. | `ssh`, `ssh-audit`, `hydra`, `nmap --script ssh-*` |
| **LDAP / LDAPS** | Lightweight Directory Access Protocol (centralized directory & Active Directory queries). | Anonymous binds, **LDAP Injection**, cleartext credential exposure on port 389, and Active Directory privilege path enumeration. | `ldapsearch`, `windapsearch`, `bloodhound-python`, `nmap --script ldap-*` |
| **FTP / TFTP** | File Transfer Protocol / Trivial FTP (legacy file transfer services). | Anonymous login access, cleartext credential/file interception, directory traversal, and unauthenticated TFTP config downloads. | `ftp`, `tftp`, `curl`, `nmap --script ftp-anon` |
| **SNMP** | Simple Network Management Protocol (network device monitoring and configuration). | Default/weak community strings (`public`/`private` in SNMPv1/v2c), full MIB tree dumping (leaking routing tables, IPs, running processes), and write-access RCE. | `snmpwalk`, `onesixtyone`, `snmp-check`, `nmap --script snmp-*` |

---

### Practical Layer 7 Auditing Commands (Ubuntu & Termux)

```bash
# 1. Probe live web hosts, status codes, page titles, and tech stacks (Ubuntu & Termux)
httpx -u https://example.com -status-code -title -tech-detect -follow-redirects

# 2. Fuzz hidden web directories, API endpoints, and files (Ubuntu & Termux)
ffuf -u https://example.com -w /path/to/wordlist.txt -mc 200,204,301,302,307,401,403

# 3. Test DNS for misconfigured Zone Transfers (AXFR) and inspect SPF/DMARC records (Ubuntu & Termux)
dig axfr @://example.com example.com
dig TXT _://example.com +short

# 4. Run template-based vulnerability checks against a web target (Ubuntu & Termux)
nuclei -u https://example.com -severity medium,high,critical

# 5. Audit an SSH server for weak cryptographic algorithms and configuration flaws (Ubuntu & Termux)
ssh-audit <target-ip>

# 6. Test an HTTP endpoint for SQL Injection vulnerabilities (Ubuntu & Termux)
sqlmap -u "https://example.com" --batch --banner
```

---

### Layer 7 -> Web Security Connection
* **Direct Attack Surface:** Layer 7 is where almost all modern web application vulnerabilities live—including **Broken Access Control (IDOR)**, **Injection (SQLi, Command, SSTI, LDAP)**, **XSS**, **CSRF**, and **Business Logic Flaws**.
* **Cross-Layer Chaining:** Effective web auditing combines all 7 layers—for example, using **Layer 7 DNS** enumeration to find an unproxied origin IP, scanning it at **Layer 4** to find an exposed staging port (`8443`), abusing **Layer 6** URL/Unicode encoding to bypass a regex filter, and exploiting a **Layer 7 SSRF** to pivot back down to **Layer 3** internal subnets.
