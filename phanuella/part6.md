# Part 6 – Tools You Should Gradually Master
## Consolidated Cybersecurity Tool Mastery Matrix & Starter Command Reference

> **Mastery Strategy:** Do not try to learn all 28+ tools simultaneously. Master them in progressive tiers—starting with core CLI inspection commands, moving to automated lab workflows, and progressing to multi-tool incident/assessment chains.

---

## 1. Core Foundations: Operating Systems & Programming

| Area | Tools | Starter Commands / Core Focus | Mastery Milestone |
| :--- | :--- | :--- | :--- |
| **Operating Systems** | **Ubuntu, Kali, Windows** | • **Ubuntu:** `systemctl`, `ufw`, `journalctl`, `chmod`/`chown`<br>• **Kali:** Offensive/auditing suite organization (`/usr/share/wordlists`)<br>• **Windows:** `Event Viewer`, `gpedit.msc`, `icacls`, `regedit` | Harden both Ubuntu and Windows Server from scratch and audit persistence mechanisms without GUI assistance. |
| **Programming** | **Python, Bash, PowerShell** | • **Bash:** `grep`, `awk`, `sed`, `sort \| uniq -c`, cron scripts<br>• **PowerShell:** `Get-WinEvent`, `Get-Process`, `Get-NetTCPConnection`<br>• **Python:** `hashlib`, `secrets`, `re`, `json`, `urllib`, `subprocess` | Write standalone scripts to parse logs, query REST APIs, verify file hashes, and automate triage tasks. |

---

## 2. Network Visibility, Scanning & Web Security

| Area | Tools | Starter Commands / Core Focus | Mastery Milestone |
| :--- | :--- | :--- | :--- |
| **Networking** | **Nmap, Wireshark, tcpdump** | • **Nmap:** `nmap -sn <subnet>`, `nmap -sV -sC <target>`<br>• **tcpdump:** `sudo tcpdump -i any -nn -c 50 -w cap.pcap`<br>• **Wireshark:** Display filters (`http.request`, `dns.qry.name`, `tcp.flags.syn==1`) | Perform full service/version enumeration, capture traffic via CLI, and reconstruct TCP streams or spot ARP/DNS anomalies in `.pcap` files. |
| **Web Security** | **Burp Suite, OWASP ZAP** | • Configure browser proxy (`127.0.0.1:8080`)<br>• **Burp Repeater:** Modify HTTP headers, cookies, and parameters manually<br>• **OWASP ZAP:** Run automated passive/active baseline web scans | Intercept and replay HTTP/S requests, test for IDOR, SQLi, XSS, and CSRF flaws, and verify `HttpOnly`/`Secure`/`SameSite` cookies. |

---

## 3. Vulnerability Scanning, Exploitation Labs & Password Auditing

| Area | Tools | Starter Commands / Core Focus | Mastery Milestone |
| :--- | :--- | :--- | :--- |
| **Vulnerability Scanning** | **Nessus, OpenVAS** | • Configure **Non-Credentialed** vs. **Credentialed** scan policies<br>• Filter results by CVSS severity and export CSV/PDF reports | Run authenticated scans against lab VMs, identify false positives via package changelogs, and verify patches via rescans. |
| **Exploitation Labs** | **Metasploit** | • `msfconsole` $\rightarrow$ `search <cve>` $\rightarrow$ `use <module>` $\rightarrow$ `show options` $\rightarrow$ `check`<br>• Understand `exploit` vs. `auxiliary` vs. `post` modules | Safely validate exploitability against intentionally vulnerable lab VMs (Metasploitable/DVWA) in an isolated host-only network. |
| **Password Auditing** | **John the Ripper, Hashcat** | • **John:** `john --wordlist=rockyou.txt hashes.txt`<br>• **Hashcat:** `hashcat -m 0 -a 0 hashes.txt wordlist.txt --force` | Benchmark weak (`MD5`/`NTLM`) vs. strong (`bcrypt`/`Argon2`) hash speeds to demonstrate passphrase and salting standards. |

---

## 4. Cryptography, Monitoring, Forensics & Threat Intelligence

| Area | Tools | Starter Commands / Core Focus | Mastery Milestone |
| :--- | :--- | :--- | :--- |
| **Cryptography** | **OpenSSL, GPG** | • **OpenSSL:** `genpkey`, `req -new`, `x509 -req`, `s_client -connect`, `dgst -sha256`<br>• **GPG:** `gpg --cipher-algo AES256 -c file.txt` / `gpg -d file.txt.gpg` | Build a two-tier Root CA + Server Certificate PKI, inspect live TLS 1.3 cipher suites, and sign/verify binaries. |
| **Monitoring** | **Wazuh, Splunk** | • **Wazuh:** Agent enrollment, FIM alerts, active response rules<br>• **Splunk:** SPL searches (`index=... \| stats count by src_ip`, `transaction`) | Ingest Windows Sysmon + Linux Syslog telemetry, tune noisy false positives, and build correlation alerts for brute force/lateral movement. |
| **Forensics** | **Autopsy, Volatility** | • **Autopsy:** Ingest disk images (`.dd`/`.E01`), timeline analysis, deleted file recovery<br>• **Volatility 3:** `vol -f mem.raw windows.pslist`, `windows.netscan`, `windows.malfind` | Extract deleted artifacts from disk images and uncover hidden processes, network sockets, or injected code in RAM dumps. |
| **Threat Intelligence** | **MITRE ATT&CK, VirusTotal** | • **MITRE ATT&CK:** Map incident behaviors to Tactics & Technique IDs (`T1566`, `T1059.001`)<br>• **VirusTotal:** Query suspicious file `SHA-256` hashes, IPs, and domains via web/API | Enrich raw SOC alerts with external reputation context and map defensive detection coverage against ATT&CK matrices. |

---

## 5. Cloud, Containers & Infrastructure Automation

| Area | Tools | Starter Commands / Core Focus | Mastery Milestone |
| :--- | :--- | :--- | :--- |
| **Cloud** | **AWS, Azure** | • **AWS:** IAM least-privilege policies, S3 Block Public Access, CloudTrail, KMS<br>• **Azure:** Entra ID Conditional Access, RBAC, Activity Logs, Key Vault | Audit cloud environments for public storage buckets, missing root MFA, and overly permissive IAM roles. |
| **Containers** | **Docker, Kubernetes** | • **Docker:** `docker run --rm --user 1000 --cap-drop=ALL --read-only --network=none`<br>• **Kubernetes:** `kubectl get pods,networkpolicies`, RBAC roles, Pod Security Standards | Build minimal non-root container images and enforce network isolation and least-privilege RBAC inside clusters. |
| **Automation** | **Ansible, Terraform** | • **Ansible:** YAML playbooks enforcing desired-state SSH/firewall baselines<br>• **Terraform:** `terraform init`, `terraform plan`, `terraform apply` for repeatable IaC | Automate CIS security hardening across multiple Linux servers and provision encrypted, private cloud resources via code. |

---

### Gradual Tool Mastery Roadmap (4-Quarter Plan)
- [ ] **Phase 1 (Foundations):** Master **Ubuntu, Windows, Bash, PowerShell, Python, Nmap, Wireshark, and tcpdump**.
- [ ] **Phase 2 (Crypto & Defense):** Master **OpenSSL, GPG, Wazuh, Splunk, MITRE ATT&CK, and VirusTotal**.
- [ ] **Phase 3 (Assessment & Testing):** Master **OpenVAS/Nessus, Burp Suite, OWASP ZAP, Hashcat/John, and Metasploit** (in isolated labs).
- [ ] **Phase 4 (Cloud, Automation & Forensics):** Master **AWS, Azure, Docker, Kubernetes, Terraform, Ansible, Autopsy, and Volatility**.
