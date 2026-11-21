# CompTIA Security+ – Complete Cybersecurity Syllabus

If your goal is to become an exceptional cybersecurity professional, **Security+** is an excellent foundation.

CompTIA Security+ teaches you how computer systems, networks, applications, users, and organisations are protected against cyber threats.

It covers:

* Computer and network security
* Operating system security
* Web and application security
* Malware and attack techniques
* Vulnerability identification and assessment
* Cryptography and encryption
* Identity and access management
* Cloud and infrastructure security
* Security monitoring and incident response
* Risk management, governance, and compliance

> **Important:** CompTIA has introduced **Security+ V8 (SY0-801)**, so the new syllabus is the appropriate version to follow as of November 2026. The older **SY0-701** remains relevant for a limited transition period.

Below is a comprehensive learning roadmap, organised from absolute beginner to professional level. It includes foundational knowledge, certification topics, and practical laboratory skills.

---

## Part 1 – Foundations Before Security+

These are the prerequisites recommended before entering the five certification domains.

### Module 1: Introduction to Computer Science

* What is computer science?
* What is information technology?
* Computer architecture
* Hardware and software
* Input and output devices
* CPU, RAM, and ROM
* Storage devices
* Motherboards and processors
* Operating systems
* Files and file systems
* Binary, decimal, hexadecimal, and octal
* Bits, bytes, and data representation
* Boolean algebra
* Logic gates
* Number systems and conversions
* Data structures
* Algorithms
* Programming fundamentals
* Processes and threads
* Memory management

### Module 2: Operating Systems

* Windows fundamentals
* Linux fundamentals
* Android architecture
* macOS fundamentals
* Kernel architecture
* User space and kernel space
* System calls
* File permissions
* Users and groups
* Processes and services
* Memory allocation
* Virtual memory
* Boot processes
* File systems
* System logs
* Environment variables
* Command-line interfaces
* Shell scripting
* System administration
* Operating system hardening

**Practical Tools:**

* Linux Terminal
* Windows PowerShell
* Windows Command Prompt
* Bash
* Termux
* VirtualBox

### Module 3: Networking Fundamentals

* What is a computer network?
* LAN, WAN, MAN, and PAN
* Network topologies
* OSI model (7 layers)
* TCP/IP model
* Ethernet
* MAC addresses
* IPv4 addressing
* IPv6 addressing
* Public and private IP addresses
* Subnetting
* CIDR
* Default gateways
* Routing
* Switching
* VLANs
* ARP
* DHCP
* DNS
* NAT and PAT
* TCP and UDP
* Ports and protocols
* Wireless networking
* Wi-Fi security
* Network segmentation
* Firewalls
* Proxies
* VPNs
* Network troubleshooting
* Packet analysis

### Module 4: Programming and Scripting

* Programming fundamentals
* Python
* Bash scripting
* PowerShell
* JavaScript fundamentals
* Variables and data types
* Operators
* Conditional statements
* Loops
* Functions
* Classes and objects
* File handling
* Exception handling
* Regular expressions
* JSON and XML
* HTTP requests
* APIs
* Automation
* Log parsing
* Security scripting

### Module 5: Virtualization and Cloud Fundamentals

* Virtual machines
* Hypervisors
* Type 1 and Type 2 hypervisors
* Containers
* Docker fundamentals
* Kubernetes fundamentals
* Cloud computing
* Public cloud
* Private cloud
* Hybrid cloud
* Multicloud
* IaaS, PaaS, and SaaS
* Shared responsibility model
* Cloud identity
* Cloud storage
* Cloud networking
* Virtualization security
* Infrastructure as Code (IaC)

---

## Part 2 – Official Security+ SY0-801 Syllabus

**Five examination domains · 27 objectives · 100% examination coverage**

### Examination Weighting

| Domain | Title | Weight |
| :--- | :--- | :--- |
| **1** | General Security Concepts | 16% |
| **2** | Threats, Vulnerabilities, and Attacks | 24% |
| **3** | Security Architecture | 19% |
| **4** | Security Operations | 27% |
| **5** | Security Program Management and Oversight | 14% |

*Based on the SY0-801 Version 2.0 examination objectives.*

---

### Domain 1: General Security Concepts – 16% (3 Objectives)

#### 1.1 Security Concepts and Controls

* Confidentiality, Integrity, and Availability (CIA)
* Authentication, Authorization, and Accounting (AAA)
* Non-repudiation
* Zero Trust principles
* Least privilege
* Defense in depth
* Technical security controls
* Managerial security controls
* Physical security controls
* Operational security controls
* Preventive controls
* Deterrent controls
* Corrective controls
* Detective controls
* Compensating controls
* Directive controls

#### 1.2 Change Management and Security

* Change Advisory Board (CAB)
* Change approval
* Change ownership
* Stakeholder identification
* Impact analysis
* Testing and test results
* Backout planning
* Fail-forward strategies
* Maintenance windows
* Standard Operating Procedures (SOPs)
* Allow lists and deny lists
* Restricted activities
* Downtime
* Service restarts
* Application restarts
* Legacy applications
* Application dependencies
* Updating security diagrams
* Updating policies and procedures
* Version control

#### 1.3 Cryptographic Solutions

**Public Key Infrastructure (PKI):**

* Public keys
* Private keys
* Key escrow
* Certificate authorities (CAs)
* Certificate revocation lists (CRLs)
* OCSP
* Self-signed certificates
* Third-party certificates
* Root of trust
* Certificate Signing Requests (CSRs)
* Wildcard certificates

**Encryption:**

* Symmetric encryption
* Asymmetric encryption
* Full-disk encryption
* Partition encryption
* File encryption
* Volume encryption
* Database encryption
* Record-level encryption
* Transport encryption
* Key exchange
* Cryptographic algorithms
* Key lengths
* Secure communication protocols

**Other Cryptographic Concepts:**

* Digital signatures
* Salting
* Hashing algorithms
* Obfuscation
* Cryptographic tools
* Key management

---

### Domain 2: Threats, Vulnerabilities, and Attacks – 24% (6 Objectives)

#### 2.1 Characteristics of Threats and Vulnerabilities

* Threat intelligence
* Threat feeds
* Threat likelihood
* Threat impact
* Intelligence sources
* Threat intelligence lifecycle
* Vulnerability identification
* Vulnerability prioritisation
* Common Vulnerabilities and Exposures (CVE)
* Common Vulnerability Scoring System (CVSS)
* Vulnerability types
* Vulnerability severity

#### 2.2 Threat Actors and Motivations

**Threat Actors:**

* Organized crime
* Terrorists
* Unskilled attackers
* Hacktivists
* Insider threats
* Accidental attackers
* Competitors
* State-sponsored attackers

**Motivations:**

* Financial gain
* Influence
* Intellectual property theft
* Notoriety
* Espionage
* Fear and chaos
* Extortion
* Curiosity
* Revenge
* Ideological beliefs
* Political motivations
* Ethical motivations

**Threat Actor Characteristics:**

* Internal versus external
* Available resources
* Funding
* Technical sophistication
* Attack capabilities

#### 2.3 Threat Vectors and Sources

* Advanced Persistent Threats (APT)
* Email attacks
* SMS attacks
* Rich Communication Services (RCS)
* Instant messaging
* Collaboration tools
* QR code attacks
* Image-based attacks
* Embedded malicious content
* CAPTCHA abuse
* Malicious document attachments
* Macros
* RTF documents
* PDF attacks
* Browser extensions
* JavaScript
* Password manager threats
* Cookies
* Session tokens
* Network infrastructure attacks
* Virtualised infrastructure attacks
* Remote Desktop (RDP)
* VNC
* VPN attacks
* Mobile device attacks
* Workstation attacks
* Server attacks
* Living-off-the-land (LotL) techniques
* Supply chain attacks
* Third-party providers
* Managed Service Providers (MSPs)
* SaaS providers
* Malicious USB devices
* Impersonation
* Cloud-based attacks
#### 2.3 Threat Vectors and Sources

* Advanced Persistent Threats (APT)
* Email attacks
* SMS attacks
* Rich Communication Services (RCS)
* Instant messaging
* Collaboration tools
* QR code attacks
* Image-based attacks
* Embedded malicious content
* CAPTCHA abuse
* Malicious document attachments
* Macros
* RTF documents
* PDF attacks
* Browser extensions
* JavaScript
* Password manager threats
* Cookies
* Session tokens
* Network infrastructure attacks
* Virtualised infrastructure attacks
* Remote Desktop
* VNC
* VPN attacks
* Mobile device attacks
* Workstation attacks
* Server attacks
* Living-off-the-land techniques
* Supply chain attacks
* Third-party providers
* Managed Service Providers (MSPs)
* SaaS providers
* Malicious USB devices
* Impersonation
* Contractor and visitor threats
* Watering-hole attacks
* IoT attacks
* Operational Technology (OT) attacks
* Physical attacks
* Bluetooth attacks
* Radio Frequency attacks
* NFC attacks

#### 2.4 Vulnerability Types and Attack Surfaces

* Unsupported products
* Unpatched systems
* Obsolete systems
* Unmanaged systems
* Open ports and services
* Application vulnerabilities
* Race conditions
* Time-of-check (TOC)
* Time-of-use (TOU)
* Malicious updates
* Hardcoded secrets
* Unsafe exception handling
* Operating system vulnerabilities
* Virtualisation vulnerabilities
* Zero-day vulnerabilities
* Cryptographic vulnerabilities
* Stale credentials
* Rogue devices
* Shadow IT
* Wireless vulnerabilities
* Low-powered communication vulnerabilities
* Large Language Model vulnerabilities
* Identity provider vulnerabilities
* Mobile device vulnerabilities
* Misconfiguration
* Public code repositories
* Public object storage

#### 2.5 Indicators of Malicious Activity

**Malware:**

* Viruses
* Worms
* Trojans
* Ransomware
* Spyware
* Adware
* Rootkits
* Keyloggers
* Logic bombs
* Fileless malware

**Physical Attacks:**

* Tailgating
* Shoulder surfing
* Skimming
* Forced entry

**Network Attacks:**

* Distributed Denial of Service (DDoS)
* Protocol downgrade
* Rogue devices
* Packet sniffing
* Spoofing
* On-path attacks
* DNS attacks
* Cache poisoning

**Social Engineering:**

* Phishing
* Spear phishing
* Whaling
* Smishing
* Vishing
* Quishing
* Impersonation
* Deepfakes

**Indicators of Compromise:**

* File hashes
* Suspicious IP addresses
* Malicious domains
* Malicious processes
* File system artifacts
* Suspicious timestamps
* Log manipulation
* Excessive resource consumption
* Plaintext strings
* Account lockouts
* Impossible travel
* Concurrent sessions

**Application Attacks:**

* Injection
* Buffer overflow
* Replay attacks
* Privilege escalation
* Forgery
* Directory traversal

**Credential Attacks:**

* Password spraying
* Brute force
* User enumeration
* Replay
* MFA bypass

#### 2.6 Artificial Intelligence Security Threats
* Model manipulation
* Data poisoning
* Prompt injection
* Data leakage
* Bias
* Explainability
* AI hallucinations
* Jailbreaking
* Evasion attacks
* Privacy risks
* Ethical considerations
* Session hijacking
* Code execution risks

---

### Domain 3: Security Architecture – 19% (4 Objectives)

#### 3.1 Security Architecture Models

**Cloud Architectures:**

* Serverless architecture
* Multicloud architecture
* Public cloud
* Private cloud
* Hybrid cloud
* Community cloud
* Infrastructure as Code (IaC)

**Other Architectures:**

* Operational Technology (OT)
* On-premises infrastructure
* Air-gapped networks
* Microservices
* Logical segmentation
* Physical segmentation

**Technical Considerations:**

* Availability
* Resilience
* Proprietary versus open source
* Usability
* Responsibility
* Computing resources
* Power requirements
* Recovery

**Business Considerations:**

* Data sovereignty
* Data classification
* Cost
* Ownership
* Environmental requirements
* Scalability
* Risk

#### 3.2 Secure Enterprise Infrastructure

* Device placement
* Security zones
* Attack surface reduction
* Infrastructure diversity
* Zero Trust architecture
* User authentication
* Device management
* Device health
* Device inventory
* Application access control
* VPN
* Remote access
* Tunnelling
* User management
* User access
* Least privilege
* End-to-end encrypted messaging
* Out-of-band management
* Secure file transfer
* Security Service Edge (SSE)
* Group Managed Service Accounts (gMSA)
* Privileged access accounts
* Privilege creep
* Infrastructure failure modes

#### 3.3 Data Protection

**Data Types:**

* Structured data
* Unstructured data

**Data States:**

* Data at rest
* Data in transit
* Data in use

**Data Classifications:**

* Sensitive
* Secret
* Critical
* Confidential
* Public
* Top secret
* Restricted

**Data Protection Methods:**

* Data masking
* Hashing
* Filtering
* Tokenisation
* Encryption
* Data transposition
* De-identification
* Obfuscation

**Data Protection Responsibilities:**

* Data owner
* Data custodian
* Data steward
* Data operator
* Data controller
* Data subprocessor

**Data Handling:**

* Endpoint security
* Data marking
* Data labelling
* Geofencing
* Data location
* Data placement

**Data Lifecycle:**

* Creation
* Management
* Distribution
* Retention
* Disposal

**Data Compliance:**

* Health information
* Personal information
* Financial information
* Children's data
* Intellectual property
* Legal data
* Data protection standards

#### 3.4 Resilience and Recovery

* Hot sites
* Warm sites
* Cold sites
* Environmental considerations
* Platform diversity
* Hardware diversity
* Virtualisation diversity
* Load balancing
* Clustering
* Autoscaling
* High availability
* Multicloud resilience
* UPS
* Redundant power supplies
* Generators
* Surge protectors
* Storage redundancy
* Backup strategies
* Backup retention
* Immutable backups
* Backup scope
* Restoration testing
* Failover testing
* Simulation
* Parallel processing
* Disaster recovery
* Business continuity
* Capacity planning

**Recovery Metrics:**

* Recovery Time Objective (RTO)
* Recovery Point Objective (RPO)
* Mean Time to Repair (MTTR)
* Mean Time Between Failures (MTBF)

---

### Domain 4: Security Operations – 27% (8 Objectives)

*Largest examination domain*

#### 4.1 Security Controls and Defensive Technologies

* Network segmentation
* Access controls
* System hardening
* Sandboxing
* Honeypots
* Honeynets
* Honeyfiles
* Honeytokens
* Canary accounts
* Monitoring and alerting
* Mobile Device Management (MDM)
* Application allow lists
* Application block lists
* Network-based IDS (NIDS)
* Network-based IPS (NIPS)
* Host-based IDS (HIDS)
* Host-based IPS (HIPS)
* Wireless IPS (WIPS)
* Firewalls
* Rate limiting
* Web Application Firewalls (WAF)
* Rule-based firewalls
* Unified Threat Management (UTM)
* Layer 4 and Layer 7 filtering
* Content filtering
* Data Loss Prevention (DLP)
* Proxy servers
* Endpoint security
* Endpoint Detection and Response (EDR)
* Extended Detection and Response (XDR)
* Antivirus
* Network Access Control (NAC)
* Captive portals
* 802.1X
* Endpoint compliance
* Secrets scanning
* Input validation
* Secure cookies
* Static code analysis
* Code signing
* Email security
* DMARC
* SPF
* DKIM
* BIMI
* Group Policy
* SELinux

#### 4.2 Asset Management

* Asset planning
* Asset scoping
* Hardware acquisition
* Software procurement
* Data asset management
* Asset assignment
* Asset accounting
* Asset tracking
* Asset monitoring
* Asset disposal
* Asset decommissioning
* Secure data destruction

#### 4.3 Vulnerability Management
* Vulnerability scanning
* IP Address Management (IPAM)
* Cloud Security Posture Management (CSPM)
* Source code review
* Vulnerability identification
* Severity assessment
* Vulnerability prioritisation
* Penetration testing report analysis
* Vulnerability remediation
* Vulnerability verification
* Vulnerability reporting
* Internal vulnerability reporting
* External vulnerability reporting
* Bug bounty programmes
* Responsible disclosure

#### 4.4 Security Monitoring and Alerting

* System monitoring
* Application monitoring
* Infrastructure monitoring
* Log aggregation
* Alert generation
* Security scanning
* Log archiving
* Security reporting
* Alert tuning
* Security benchmarks
* Agent-based monitoring
* Agentless monitoring
* SIEM
* Antivirus
* DLP
* Vulnerability scanners
* Security orchestration
* Packet analysers
* NetFlow
* SNMP
* Syslog
* SCAP
* Automated alerts
* Port mirroring
* Security dashboards
* Network management systems

#### 4.5 Identity and Access Management (IAM)

* User provisioning
* User deprovisioning
* Permission assignment
* Identity proofing
* Identity federation
* Single Sign-On (SSO)
* SAML
* LDAP
* OAuth

**Account Types:**

* Standard user accounts
* Privileged accounts
* Global accounts
* Local accounts
* Service accounts
* Third-party accounts
* Emergency access accounts

**Multifactor Authentication (MFA):**

* Hardware tokens
* Software tokens
* Biometrics
* One-Time Passwords (OTP)
* Backup codes

**Access Control Models:**

* Rule-based
* Role-Based Access Control (RBAC)
* Time-based
* Mandatory Access Control (MAC)
* Discretionary Access Control (DAC)
* Just-in-Time access

**Password Security:**

* Passkeys
* Password managers
* Passwordless authentication
* Password length
* Password complexity
* Password reuse
* Expiration
* Password age
* Compromised credential monitoring
* Account auditing
* Password policy reporting

#### 4.6 Automation and Orchestration
* Security automation
* User provisioning automation
* Resource provisioning
* Desired-state management
* Anomaly detection
* Ticket management
* Automation guardrails
* Automation logic
* Process engineering
* Automation complexity
* Financial considerations
* Process risks
* Deployment considerations

**AI in Security Operations:**

* Agentic AI
* Chatbots
* Predictive analysis
* AI-augmented baselines

**Automation Outcomes:**

* Efficiency
* Time savings
* Baseline enforcement
* Continuous improvement
* Productivity
* Reduced downtime
* Proactive security

**SecOps:**

* Continuous Integration (CI)
* Continuous Deployment (CD)
* Automated workflows
* Integrations

#### 4.7 Incident Response

* Preparation
* Identification
* Investigation
* Containment
* Negotiation
* Eradication
* Recovery
* Notification and reporting
* Post-incident activities

**Detailed Concepts:**

* Security training
* Testing
* Tabletop exercises
* Incident response playbooks
* Simulation
* Incident response roles
* Threat detection
* Internal advisories
* External advisories
* Threat hunting
* Digital forensics
* Chain of custody
* E-discovery
* Evidence preservation
* Quarantine
* Network isolation
* Stakeholder notification
* Customer notification
* Law enforcement notification
* Mandatory reporting
* Lessons learned
* Root cause analysis
* Post-Incident Reports (PIR)

#### 4.8 Security Investigation and Forensic Data

**Log and Trace Data:**

* Access logs
* Accounting logs
* Physical access logs
* Device logs
* Server logs
* Application logs
* Authentication logs
* Communication logs
* Audit logs
* Endpoint logs
* Network logs
* Metadata

**Investigation Data Sources:**

* Vulnerability scan results
* Automated security reports
* NetFlow
* IPFIX
* Surveillance footage
* Security tools
* Dashboards
* Packet captures

**Digital Evidence:**

* File and log integrity
* System images
* Memory dumps
* Bit-level copies
* System snapshots
* Evidence preservation
* Log parsing
* Investigation stakeholders
* Human Resources
* Accounts department
* Legal department

---

### Domain 5: Security Program Management and Oversight – 14% (6 Objectives)

#### 5.1 Governance, Risk and Compliance Documentation

* Guidelines
* Benchmarks
* Advisories
* Implementation guides
* Reference architectures

**Standards:**

* Security baselines
* Password standards
* Physical security standards
* RFCs
* Encryption standards

**Procedures:**

* Standard Operating Procedures (SOPs)
* Runbooks

**Plans:**

* Business continuity plans
* Disaster recovery plans

**Policies:**

* Bring Your Own Device (BYOD)
* Acceptable Use Policy (AUP)
* Clean desk policy
* Information security policy
* Incident response policy
* Data classification policy
* Data retention policy
* Access control policy
* Data disposal policy
* Vulnerability disclosure policy
* Privacy policy

#### 5.2 Risk Management

* Risk identification
* Asset identification
* Stakeholder ownership
* Risk assessment
* Risk scoring
* Risk categorisation
* Risk analysis
* Risk impact
* Risk likelihood
* Risk ownership
* Existing security controls
* Qualitative risk analysis
* Quantitative risk analysis
* Risk registers
* Risk communication
* Risk reviews

**Risk Treatment:**

* Risk transfer
* Risk acceptance
* Risk avoidance
* Risk mitigation

**Business Considerations:**

* Business Impact Analysis (BIA)
* Risk appetite
* Residual risk
* Stakeholder involvement
* Management oversight
* Regulatory requirements
* Legal requirements
* Single Loss Expectancy (SLE)
* Annualised Loss Expectancy (ALE)
* Annualised Rate of Occurrence (ARO)

#### 5.3 Third-Party Risk Management

* Vendor selection
* Request for Proposal (RFP)
* Request for Information (RFI)
* Request for Quote (RFQ)
* Expression of Interest (EOI)
* Due diligence
* Conflict of interest
* Service Level Agreements (SLA)
* Service Level Objectives (SLO)
* Memorandum of Understanding (MOU)
* Memorandum of Agreement (MOA)
* Non-Disclosure Agreements (NDA)
* Master Services Agreements (MSA)
* Statements of Work (SOW)
* Vendor monitoring
* Right to audit
* Service-level monitoring
* Vendor registries
* Vendor assessments
* Compliance attestations
* Vendor penetration testing
* Staffing limitations
* Resource availability
* Environmental constraints
* Legal and regulatory requirements
* Geographical jurisdiction
* Financial considerations
* Return on Investment (ROI)
* Vendor lock-in
* Assurance mechanisms
* Rules of engagement

#### 5.4 Security Compliance

* Compliance training
* Data handling
* Anti-money laundering (AML)
* Counter-terrorism financing (CTF)
* Anti-bribery
* Compliance monitoring
* Attestations
* Acknowledgements

**Consequences of Non-Compliance:**

* Reputational damage
* Financial penalties
* Legal consequences
* Contractual penalties
* Sanctions
* Loss of licence

**Privacy:**

* Right to be forgotten
* Opt-in and opt-out
* Data correction
* Processing restrictions
* Processing prevention
* Data controller
* Data processor
* Data ownership

**Legal Compliance:**

* Legal holds
* Legal orders
* Data retention requirements

#### 5.5 Audits and Assessments
* Data gathering
* Sampling
* Questionnaires
* Surveys
* Interviews
* Assertions
* Reference sources
* MITRE ATT&CK
* Cyber Kill Chain
* Diamond Model of Intrusion Analysis
* Audit charters
* Audit frequency
* Gap analysis
* Internal audits
* Compliance audits
* Audit committees
* Self-assessments
* External examinations
* External assessments
* Regulatory assessments
* Independent third-party audits
* Benchmarking

**Penetration Testing:**

* Known environment
* Unknown environment
* Partially known environment
* Physical penetration testing
* Offensive testing
* Defensive testing
* Integrated testing
* Passive reconnaissance
* Active reconnaissance

**Standards:**

* Industry standards
* International standards
* Regional standards
* Functional testing
* Behavioural testing

#### 5.6 Security Awareness

**Training Types:**

* Initial onboarding
* Ongoing training
* Targeted training
* Corrective training

**Training Delivery:**

* Learning Management Systems (LMS)
* Self-service portals
* One-to-one training
* One-to-many training

**Measuring Effectiveness:**

* Security awareness metrics
* Management reports
* Personnel behaviour risk scoring

**Common Training Topics:**

* Social engineering
* Emerging security threats
* Password management
* Credential management
* Remote working
* Hybrid working
* BYOD
* Business Email Compromise (BEC)
* Removable media
* Security cables
* Situational awareness
* Operational security
---

## Part 3 – Practical Security+ Laboratory Syllabus

Knowing definitions is not enough. You should be able to configure, inspect, identify, analyse, and respond to security problems.

Here is the practical laboratory curriculum recommended:

### Module 1: Linux Security Laboratory

* Linux user and group management
* File permissions
* Ownership
* Process monitoring
* Service management
* Firewall configuration
* SSH security
* Log analysis
* System hardening
* File integrity monitoring
* Bash automation

**Tools:** Linux, Ubuntu, Kali Linux, Termux, UFW, OpenSSH

### Module 2: Network Security Laboratory

* IP address identification
* Port identification
* Service identification
* Network discovery
* Packet inspection
* DNS investigation
* TCP/UDP analysis
* Firewall testing
* Network segmentation
* Wireless security assessment

**Tools:**

| Tool | Main Purpose |
| :--- | :--- |
| **Nmap** | Network discovery and port scanning |
| **Wireshark** | Packet analysis |
| **tcpdump** | Command-line packet capture |
| **Netcat** | Network connection testing |
| **OpenSSL** | Cryptographic testing |
| **Zeek** | Network security monitoring |
| **Suricata** | Network threat detection |
| **Snort** | Intrusion detection |
| **pfSense** | Firewall management |

### Module 3: Vulnerability Assessment Laboratory

* Asset discovery
* Vulnerability scanning
* Vulnerability classification
* CVE research
* CVSS scoring
* False-positive identification
* Vulnerability prioritisation
* Remediation
* Verification
* Security reporting

**Tools:**

* Nessus
* Greenbone / OpenVAS
* Nuclei
* Nikto
* OWASP ZAP
* Burp Suite Community
* Metasploit Framework

> **Note:** Use intentionally vulnerable applications and systems you own or have permission to assess.

### Module 4: Web and Application Security
* HTTP and HTTPS
* Request and response analysis
* Cookies
* Sessions
* Authentication
* Authorization
* Input validation
* SQL injection concepts
* Cross-site scripting (XSS)
* Cross-site request forgery (CSRF)
* Directory traversal
* Server-side request forgery (SSRF)
* File upload security
* API security
* Secure coding
* Dependency security
* Application logging

**Tools:** Burp Suite, OWASP ZAP, Postman, browser developer tools, and OWASP Juice Shop

### Module 5: Cryptography Laboratory

* Generate public/private key pairs
* Hash files
* Verify file integrity
* Generate certificates
* Inspect certificates
* Test TLS configurations
* Understand digital signatures
* Generate random cryptographic values
* Manage encryption keys
* Verify certificate chains

**Tools:** OpenSSL, GnuPG, Hashcat (for authorised password auditing)

### Module 6: Identity and Access Management

* Create user accounts
* Configure groups
* Assign permissions
* Configure MFA
* Implement least privilege
* Configure access policies
* Investigate authentication logs
* Configure SSO concepts
* Audit privileged accounts
* Identify privilege escalation risks

**Tools:** Active Directory lab, Windows Server, Linux, LDAP, and Keycloak

### Module 7: Security Monitoring and Incident Response

* Collect system logs
* Analyse authentication events
* Identify suspicious processes
* Investigate unusual network traffic
* Detect malware indicators
* Correlate security events
* Investigate suspicious accounts
* Preserve forensic evidence
* Perform incident containment
* Write incident reports

**Tools:** Splunk, Wazuh, Security Onion, Velociraptor, and Sysmon

### Module 8: Cloud Security

* Cloud identity management
* Cloud access policies
* Cloud storage security
* Cloud networking
* Cloud encryption
* Cloud logging
* Cloud misconfiguration detection
* Cloud vulnerability management
* Infrastructure as Code (IaC) security
* Cloud incident response

**Tools:** AWS, Azure, Google Cloud, Terraform, and Prowler
---

## Part 4 – Professional Cybersecurity Extensions

These subjects extend beyond memorising the certification objectives and help develop professional cybersecurity competence.

* Secure Software Development Lifecycle (SDLC)
* OWASP Top 10
* OWASP API Security Top 10
* Threat modelling
* MITRE ATT&CK
* Cyber Kill Chain
* Digital forensics
* Malware analysis fundamentals
* Reverse engineering fundamentals
* Memory forensics
* Network forensics
* Cloud penetration testing
* Web penetration testing
* Mobile application security
* Android APK security
* Container security
* Kubernetes security
* DevSecOps
* Security automation
* Threat intelligence
* Security architecture design
* Security auditing
* Vulnerability disclosure
* Bug bounty methodology

> **Note:** These are useful extensions, not all mandatory Security+ examination topics.

---

## Part 5 – Recommended Learning Sequence

Follow this order rather than jumping directly into penetration testing:

1. **Stage 1: Computer Science Fundamentals**
   * Understand how computers represent, store, and process information.
2. **Stage 2: Operating Systems**
   * Understand how Windows, Linux, and Android work internally.
3. **Stage 3: Networking**
   * Understand how devices communicate and exchange data.
4. **Stage 4: Programming and Scripting**
   * Learn Python, Bash, and PowerShell.
5. **Stage 5: Security Fundamentals**
   * Study Domain 1.
6. **Stage 6: Threats and Attacks**
   * Study Domain 2.
7. **Stage 7: Security Architecture**
   * Study Domain 3.
8. **Stage 8: Security Operations**
   * Study Domain 4.
9. **Stage 9: Security Governance**
   * Study Domain 5.
10. **Stage 10: Practical Laboratories**
    * Perform practical exercises across all five domains.
11. **Stage 11: Examination Preparation**
    * Practise scenario questions, performance-based questions (PBQs), and timed examinations.
12. **Stage 12: Professional Development**
    * Extend your knowledge into penetration testing, digital forensics, cloud security, and application security.
---

## Part 6 – Tools You Should Gradually Master

Here is a consolidated tool checklist:

| Area | Tools |
| :--- | :--- |
| **Operating systems** | Ubuntu, Kali, Windows |
| **Networking** | Nmap, Wireshark, tcpdump |
| **Web security** | Burp Suite, OWASP ZAP |
| **Vulnerability scanning** | Nessus, OpenVAS |
| **Exploitation labs** | Metasploit |
| **Cryptography** | OpenSSL, GPG |
| **Password auditing** | John the Ripper, Hashcat |
| **Monitoring** | Wazuh, Splunk |
| **Forensics** | Autopsy, Volatility |
| **Cloud** | AWS, Azure |
| **Containers** | Docker, Kubernetes |
| **Programming** | Python, Bash, PowerShell |
| **Automation** | Ansible, Terraform |
| **Threat intelligence** | MITRE ATT&CK, VirusTotal |

---

## Part 7 – Track Your Progress

**Your Security+ Learning Tracker (`0/44 completed`)**

### 1. Computer Science Fundamentals

* [ ] Computer architecture and binary
* [ ] Boolean algebra and logic gates
* [ ] Data representation and algorithms
* [ ] Programming fundamentals

### 2. Operating Systems and Networking

* [ ] Linux and Windows
* [ ] Processes, memory, and permissions
* [ ] OSI and TCP/IP models
* [ ] IP addressing and subnetting
* [ ] Network protocols and ports

### 3. Security+ Domain 1

* [ ] Security controls
* [ ] Security principles
* [ ] Change management
* [ ] Cryptography

### 4. Security+ Domain 2

* [ ] Threat intelligence
* [ ] Threat actors
* [ ] Threat vectors
* [ ] Vulnerabilities
* [ ] Malicious activity
* [ ] AI security

### 5. Security+ Domain 3

* [ ] Architecture models
* [ ] Infrastructure security
* [ ] Data protection
* [ ] Resilience and recovery

### 6. Security+ Domain 4

* [ ] Security controls
* [ ] Asset management
* [ ] Vulnerability management
* [ ] Monitoring
* [ ] Identity and access
* [ ] Automation
* [ ] Incident response
* [ ] Forensics and investigation

### 7. Security+ Domain 5

* [ ] Governance
* [ ] Risk management
* [ ] Third-party risk
* [ ] Compliance
* [ ] Audits and assessments
* [ ] Security awareness

### 8. Practical Laboratories

* [ ] Linux security labs
* [ ] Network security labs
* [ ] Web security labs
* [ ] Cryptography labs
* [ ] IAM labs
* [ ] SIEM and incident response labs
* [ ] Cloud security labs

---

## Official Examination Information

**CompTIA Security+ V8 (`SY0-801`)**  
*Official examination objectives, Version 2.0*

* **Maximum questions:** 90 questions
* **Question types:** Multiple-choice and performance-based questions (PBQs)
* **Examination duration:** 90 minutes
* **Passing score:** 750 out of 900

> **Study Strategy Recommendation:**  
> Don't study Security+ as a collection of definitions. For every subject, learn three things:
> * **Construction:** How is the technology or system built?
> * **Logic:** How does it operate, make decisions, and process information?
> * **Diagnosis:** How do you inspect it, identify weaknesses, and verify that its security controls work?
>
> This approach will prepare you for both the certification and your longer-term goal of becoming a skilled offensive security researcher.
