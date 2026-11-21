# Part 5 – Recommended Learning Sequence
## 12-Stage Progression Roadmap from Foundations to Security+ Certification & Professional Practice

> **Core Philosophy:** True cybersecurity mastery is built from the bottom up. You cannot effectively secure, audit, or test an operating system, network protocol, or cloud application until you understand how it operates normally under the hood.

---

## Phase I: Technical Foundations (Stages 1–4)

| Stage | Focus Area | Core Mastery Milestone (Readiness Gate Before Advancing) |
| :--- | :--- | :--- |
| **Stage 1** | **Computer Science Fundamentals** | Convert fluently between **Binary, Hexadecimal, Decimal, and Base64**; explain CPU registers, stack vs. heap memory, endianness, file systems, and character encoding (`ASCII` / `UTF-8`). |
| **Stage 2** | **Operating Systems** *(Windows, Linux, Android)* | Navigate Linux (`systemd`, `/etc/passwd`, `chmod`/`chown`, `ps`) and Windows (`Registry`, `Event Viewer`, `Services`, `NTFS ACLs`, `Active Directory`) from the CLI; explain Android sandboxing and permissions. |
| **Stage 3** | **Networking** | Map protocols/ports across the **OSI & TCP/IP models** (`DNS 53`, `HTTP/S 80/443`, `SSH 22`, `SMB 445`, `RDP 3389`, `LDAP/S 389/636`); calculate **CIDR subnets**; explain the **TCP 3-way handshake**, **ARP**, **DHCP**, **NAT**, **VLANs**, and **TLS**. |
| **Stage 4** | **Programming and Scripting** *(Python, Bash, PowerShell)* | Write clean scripts to parse log files, query REST APIs (`JSON`), compute `SHA-256` hashes, automate user/firewall audits, and read unfamiliar code safely to spot injection or hardcoded secret flaws. |

---

## Phase II: CompTIA Security+ Core Domains (Stages 5–9)

| Stage | Security+ Domain & Weight | Core Mastery Milestone (Readiness Gate Before Advancing) |
| :--- | :--- | :--- |
| **Stage 5** | **Security Fundamentals** *(Domain 1 – 12%)* | Classify **Security Control Categories** (Technical, Managerial, Operational, Physical) vs. **Functional Types** (Preventive, Detective, Corrective, Deterrent, Compensating, Directive); trace **Zero Trust** planes, **Change Management** workflows, and **PKI / Cryptographic** solutions. |
| **Stage 6** | **Threats and Attacks** *(Domain 2 – 22%)* | Attribute **Threat Actors** & motivations; distinguish **Vulnerability Types** (`SQLi`, `XSS`, `SSRF`, `TOCTOU`, `Zero-day`), **Malware**, **Social Engineering**, **IoCs**, **Credential Attacks** (Password Spraying vs. Brute Force), and **AI/LLM Security Threats**. |
| **Stage 7** | **Security Architecture** *(Domain 3 – 18%)* | Evaluate **Cloud, On-Prem, OT/ICS, Air-Gapped, and Microservices** models; place firewalls/DMZs/sensors in secure zones; apply **Data Protection** methods (Encryption, Tokenization, Masking) and **Resilience Metrics** (`RTO`, `RPO`, `MTTR`, `MTBF`, `RAID`). |
| **Stage 8** | **Security Operations** *(Domain 4 – 28% – Largest Domain)* | Configure defensive controls (**WAF, NIPS, EDR/XDR, NAC/802.1X, SPF/DKIM/DMARC/BIMI, SELinux/GPO**); manage asset lifecycles; prioritize CVEs; operate **SIEM/SOAR** alerts; execute the **Incident Response Lifecycle** and **Digital Forensics** (Order of Volatility & Chain of Custody). |
| **Stage 9** | **Security Governance** *(Domain 5 – 20%)* | Differentiate **Policies, Standards, Procedures, Runbooks, and Guidelines**; calculate quantitative risk ($\text{SLE} = \text{AV} \times \text{EF}$, $\text{ALE} = \text{SLE} \times \text{ARO}$); govern third-party contracts (`SLA`, `MSA`, `SOW`, `NDA`, `DPA/BAA`), audits, and **Security Awareness** programs. |

---

## Phase III: Hands-On Labs, Exam Readiness & Career Extension (Stages 10–12)

### Stage 10: Practical Laboratories (Modules 1–8)
* **Focus:** Execute every lab hands-on inside your isolated **VirtualBox + Linux + Windows Server + Docker** environment without relying on copy-paste crutches:
  1. **Linux & Windows Hardening:** Users/groups, permissions, SSH/GPO hardening, `ufw`/Defender Firewall, `sysctl`, File Integrity Monitoring.
  2. **Network & Packet Analysis:** `nmap` enumeration, `tcpdump` / Wireshark `.pcap` filtering, `dig` DNS/SPF/DMARC/DNSSEC checks.
  3. **Vulnerability & Web App Security:** NVD CVE/CVSS triage, parameterized SQL queries, XSS escaping, CSRF tokens, SSRF & file upload defenses.
  4. **Cryptography, IAM & SOC IR:** OpenSSL PKI/CA certificate chains, GPG, Keycloak SSO/MFA, Splunk/Wazuh/Sysmon log correlation, forensic hashing & containment.
  5. **Cloud Security:** Least-privilege IAM JSON policies, S3/MinIO access blocks, Terraform IaC security, and CloudTrail incident containment.

### Stage 11: Examination Preparation (SY0-701)
* **Focus:** Master CompTIA's exam format, pacing, and elimination strategy:
  * **Timed Practice Exams:** Complete full **90-question / 90-minute** practice tests targeting consistent **85%+** scores before scheduling exam day.
  * **Performance-Based Questions (PBQs):** Practice interactive drag-and-drop architecture diagrams, firewall ACL rule ordering, log interpretation, and certificate/attack remediation simulations (flag PBQs first, complete multiple-choice questions quickly, then return with 25–30 minutes reserved for PBQs).
  * **Scenario Keyword Mapping:** Train yourself to spot decisive exam keywords (*"first/initial step"*, *"best compensating control"*, *"most cost-effective"*, *"preventive vs. detective"*).

### Stage 12: Professional Development (Post-Certification Specialization)
* **Focus:** Extend your core competence into specialized career tracks from **Part 4**:
  * **SOC Analyst / Incident Responder (Blue Team):** Deepen **Splunk/KQL**, **Volatility 3 Memory Forensics**, **Zeek/Suricata**, **YARA**, and **MITRE ATT&CK** threat hunting.
  * **Penetration Tester / Red Team:** Progress to **OWASP Web & API Pen-Testing (Burp Suite)**, Active Directory attack paths, and **Bug Bounty** methodology.
  * **AppSec / DevSecOps Engineer:** Build automated **CI/CD** security pipelines (**SAST, DAST, SCA, Trivy, Terraform/Checkov**) and lead **STRIDE Threat Modeling** sessions.
  * **Cloud Security Engineer:** Architect zero-trust multi-account environments across **AWS, Azure, and GCP** using **Prowler** CSPM and hardened **Kubernetes** clusters.

---

### Master Curriculum Completion Tracker
- [ ] **Phase I (Stages 1–4):** CS Fundamentals, Linux/Windows/Android OS, Networking, and Python/Bash/PowerShell scripting completed.
- [ ] **Phase II (Stages 5–9):** All 5 CompTIA Security+ (SY0-701) Domains studied and mapped.
- [ ] **Phase III (Stages 10–12):** All 8 Practical Lab Modules executed, PBQs & timed mock exams practiced at 85%+, and professional specialization chosen.
