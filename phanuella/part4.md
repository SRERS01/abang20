# Part 4 – Professional Cybersecurity Extensions
## Practical Security Engineering, Threat Modeling, Forensics & AppSec Guide

> **Objective:** Bridge the gap between Security+ certification knowledge and hands-on roles in **AppSec / DevSecOps**, **SOC / Threat Hunting**, **Digital Forensics & Incident Response (DFIR)**, **Penetration Testing**, and **Cloud/Container Security**.  
> **Recommended Lab Tools:** Linux VM (Ubuntu/Kali), Python 3, Docker / `kubectl`, `strings` / `objdump` / `readelf`, `apktool` / `jadx`, Wireshark / `tshark`, Git.

---

## Part A: Application Security, DevSecOps & Threat Modeling

### 1. Secure Software Development Lifecycle (SDLC)
* **Concept:** Integrating security gates into every phase of software creation rather than bolting security on right before launch:
  * **Requirements:** Define abuse cases, compliance needs (PCI/GDPR), and authentication standards.
  * **Design:** Perform **Threat Modeling** and secure architecture reviews.
  * **Implementation:** Enforce secure coding standards, peer reviews, and IDE secret-leak linters.
  * **Verification:** Run automated **SAST** (static), **DAST** (dynamic), **SCA** (dependencies), and penetration tests.
  * **Release & Maintenance:** Cryptographically sign builds, deploy immutable containers, and monitor runtime telemetry.

### 2. OWASP Top 10 & 3. OWASP API Security Top 10
* **Concept:**
  * **OWASP Top 10 (Web):** Focuses on **Broken Access Control (IDOR)**, **Cryptographic Failures**, **Injection (SQLi/XSS/Command)**, **Insecure Design**, **Security Misconfiguration**, **Vulnerable Components**, **Authentication Failures**, **Software/Data Integrity Failures**, **Logging/Monitoring Failures**, and **SSRF**.
  * **OWASP API Security Top 10:** Targets API-specific flaws—**BOLA (Broken Object Level Authorization)**, **Broken Authentication**, **Broken Object Property Level Authorization (Mass Assignment)**, **Unrestricted Resource Consumption (Rate Limiting)**, **Broken Function Level Authorization (BFLA)**, and **Unsafe Consumption of APIs**.
* **Practical Task (Prevent Mass Assignment / Property-Level Over-Posting in Python):**
  ```python
  # VULNERABLE: Updating user profile directly from raw JSON payload allows attacker to pass {"is_admin": True}
  # SECURE: Explicitly allow-list permitted fields before updating database object
  incoming_api_payload = {"email": "ambe@corp.cm", "role": "superadmin", "is_admin": True}
  allowed_update_fields = {"email", "display_name"}

  sanitized_update = {k: v for k, v in incoming_api_payload.items() if k in allowed_update_fields}
  print("Safe API Update Payload (Mass Assignment Blocked):", sanitized_update)
  ```

### 4. Threat Modeling (STRIDE & DREAD)
* **Concept:** Structured brainstorming during system design to identify threats before a single line of code is written:
  * **STRIDE Categories:** **S**poofing (Identity), **T**ampering (Integrity), **R**epudiation (Non-repudiation/Logs), **I**nformation Disclosure (Confidentiality), **D**enial of Service (Availability), **E**levation of Privilege (Authorization).
* **Practical Task (Build a STRIDE Threat Model Matrix for a Payment API):**
  ```python
  stride_matrix = {
      "Spoofing":               "Mitigate via OAuth2/OIDC + FIDO2 MFA & mTLS client certs",
      "Tampering":              "Mitigate via TLS 1.3 + HMAC-SHA256 webhook payload signatures",
      "Repudiation":            "Mitigate via immutable WORM audit logs with synchronized UTC NTP",
      "Information Disclosure": "Mitigate via AES-256 column encryption + DTO field filtering",
      "Denial of Service":      "Mitigate via API Gateway sliding-window rate limiting + WAF",
      "Elevation of Privilege": "Mitigate via strict BOLA/RBAC checks on every endpoint"
  }
  for threat, control in stride_matrix.items():
      print(f"{threat:<23} -> {control}")
  ```

### 5. DevSecOps & 6. Security Automation
* **Concept:** Automating security testing (**SAST, DAST, SCA, Container Image Scanning, IaC Linting**) directly inside CI/CD pipelines (GitHub Actions, GitLab CI, Jenkins) and automating SOC response playbooks via Python/APIs.

---

## Part B: Threat Frameworks & Intelligence Operations

### 7. MITRE ATT&CK, 8. Cyber Kill Chain & 9. Threat Intelligence
* **Concept:** Operationalizing adversary TTPs (Tactics, Techniques, and Procedures) to measure SOC detection coverage and hunt proactively:
  * **MITRE ATT&CK:** Maps granular adversary behaviors (`Initial Access` $\rightarrow$ `Execution` $\rightarrow$ `Persistence` $\rightarrow$ `Privilege Escalation` $\rightarrow$ `Defense Evasion` $\rightarrow$ `Credential Access` $\rightarrow$ `Discovery` $\rightarrow$ `Lateral Movement` $\rightarrow$ `Collection` $\rightarrow$ `Command & Control` $\rightarrow$ `Exfiltration` $\rightarrow$ `Impact`).
  * **Cyber Kill Chain:** 7-stage intrusion lifecycle used to place layered defensive blocks early (`Delivery` / `Exploitation`) before `Actions on Objectives`.
  * **Threat Intelligence:** Converting raw technical IoCs (hashes, C2 domains) into **STIX 2.1** structured intelligence shared via **TAXII** servers.

---

## Part C: Digital Forensics, Malware Analysis & Reverse Engineering

### 10. Digital Forensics, 11. Memory Forensics & 12. Network Forensics
* **Concept:**
  * **Digital Forensics:** Bit-stream disk acquisition (`dd`/`FTK Imager`), timeline reconstruction, registry hive analysis (`SAM`, `SYSTEM`, `NTUSER.DAT`), and browser/artifact recovery.
  * **Memory Forensics:** Analyzing volatile RAM dumps using **Volatility 3** (`windows.pslist`, `windows.netscan`, `windows.malfind`) to uncover injected shellcode, fileless malware, encryption keys, and unlinked rootkit processes.
  * **Network Forensics:** Extracting transferred files, DNS tunneling queries, and C2 beacons from full `.pcap` captures using **Wireshark**, **`tshark`**, and **Zeek**.
* **Practical Task (Extract HTTP/DNS Metadata from a PCAP with `tshark` / `tcpdump`):**
  ```bash
  # Extract DNS queries from a packet capture using tcpdump
  # tcpdump -nn -r capture.pcap "port 53" | head -n 15
  echo "Network Forensics Filter: tshark -r capture.pcap -Y 'http.request || dns.qry.name' -T fields -e ip.src -e dns.qry.name"
  ```

### 13. Malware Analysis Fundamentals & 14. Reverse Engineering Fundamentals
* **Concept:**
  * **Static Analysis:** Examining a suspicious binary *without executing it*—computing `SHA-256` hashes, extracting ASCII/Unicode `strings`, inspecting PE/ELF headers (`readelf`, `objdump`), checking imported DLLs/APIs (`VirtualAlloc`, `WriteProcessMemory`, `CreateRemoteThread` = classic process injection!), and scanning with **YARA** rules.
  * **Dynamic (Behavioral) Analysis:** Detonating the sample inside an isolated, snapshot-backed sandbox VM while monitoring process spawns, file/registry writes, and fake network C2 listeners (INetSim).
  * **Reverse Engineering:** Disassembling/decompiling machine code into assembly and C-like pseudocode using **Ghidra** or **radare2** to uncover hidden C2 decryption routines, kill-switches, and DGA algorithms.
* **Practical Task (Inspect ELF Binary Headers & Imported Symbols Safely on Linux):**
  ```bash
  # Inspect ELF header and dynamic symbol imports of /bin/ls (safe system binary practice)
  readelf -h /bin/ls | head -n 10
  nm -D /bin/ls 2>/dev/null | head -n 10
  ```

---

## Part D: Offensive Security, Web/Cloud Pen-Testing & Bug Bounty

### 15. Web Penetration Testing & 16. Cloud Penetration Testing
* **Concept:**
  * **Web Pen-Testing:** Authorized methodology (**Reconnaissance $\rightarrow$ Mapping Endpoints $\rightarrow$ Authentication/Session Testing $\rightarrow$ Access Control/IDOR $\rightarrow$ Input Fuzzing [SQLi/XSS/SSRF] $\rightarrow$ Reporting**) using **Burp Suite** or **OWASP ZAP**.
  * **Cloud Pen-Testing:** Testing IAM privilege escalation paths, exposed metadata services (`IMDSv1`), misconfigured storage buckets, and serverless function injection strictly within Cloud Service Provider penetration testing policies.

### 17. Vulnerability Disclosure & 18. Bug Bounty Methodology
* **Concept:**
  * **Vulnerability Disclosure:** Following coordinated disclosure timelines (e.g., 90 days) and `/.well-known/security.txt` policies so vendors patch flaws before public release.
  * **Bug Bounty Methodology:** Structured workflow for authorized platforms (HackerOne, Bugcrowd): **1. Read Scope & Rules of Engagement carefully $\rightarrow$ 2. Subdomain & Asset Enumeration $\rightarrow$ 3. Content/Parameter Discovery $\rightarrow$ 4. Manual Business-Logic & Access Control Testing $\rightarrow$ 5. Write Clear Reproduction Steps & Business Impact Report**.

---

## Part E: Mobile, Container & Kubernetes Security

### 19. Mobile Application Security & 20. Android APK Security
* **Concept:** Protecting iOS/Android apps against **OWASP Mobile Top 10** risks—insecure local storage (`SharedPreferences` / unencrypted SQLite), hardcoded API keys inside compiled binaries, lack of **TLS Certificate Pinning**, exported Android components (`Activity`, `BroadcastReceiver`, `ContentProvider`), and root/jailbreak bypasses.
* **Practical Task (Inspect an Android APK Archive Structure Safely):**
  ```bash
  # An Android .apk file is a standard ZIP archive containing AndroidManifest.xml and classes.dex
  mkdir -p ~/pro_extensions_lab && cd ~/pro_extensions_lab
  echo "Simulated APK structure: unzip -l app.apk | grep -E 'AndroidManifest.xml|classes.dex|lib/'"
  # Professional tools: 'apktool d app.apk' (decompile resources/Smali) & 'jadx-gui app.apk' (Java source view)
  ```

### 21. Container Security & 22. Kubernetes Security
* **Concept:**
## Part E: Mobile, Container & Kubernetes Security

### 19. Mobile Application Security & 20. Android APK Security
* **Concept:** Securing iOS and Android applications against **OWASP Mobile Top 10** risks:
  * **Insecure Data Storage:** Storing sensitive tokens, PII, or keys in plaintext inside `SharedPreferences`, `NSUserDefaults`, unencrypted SQLite databases, or world-readable external storage (instead of hardware-backed **Android Keystore** / **iOS Keychain**).
  * **Hardcoded Secrets & Reverse Engineering:** Embedding API keys or backend URLs inside compiled APK binaries (`classes.dex`) where attackers easily extract them via static decompilation.
  * **Insufficient Transport Protection & Certificate Pinning:** Failing to enforce HTTPS or lacking **TLS Certificate Pinning** on high-security apps (mobile banking/fintech), allowing attackers on rogue Wi-Fi networks with custom proxy CAs (Burp Suite / mitmproxy) to intercept API traffic.
  * **Improper Platform Usage (Android Component Exposure):** Leaving `Activity`, `BroadcastReceiver`, `Service`, or `ContentProvider` components marked `android:exported="true"` in `AndroidManifest.xml` without permission checks, allowing rogue apps on the same device to invoke internal screens or steal data.
* **Hands-On Task (Build a Synthetic Android APK & Audit Its Manifest/Strings Safely):**
  ```bash
  mkdir -p ~/pro_extensions_lab/apk_audit && cd ~/pro_extensions_lab/apk_audit

  # 1. Create a simulated AndroidManifest.xml and compiled string artifact to practice static triage
  cat << 'EOF' > AndroidManifest.xml
  <manifest package="cm.secplus.mobilebanking">
    <application android:debuggable="true" android:allowBackup="true">
      <activity android:name=".TransferFundsActivity" android:exported="true" />
    </application>
  </manifest>
  EOF

  # 2. Audit AndroidManifest.xml for 3 critical Mobile Security misconfigurations:
  grep -E 'debuggable="true"|allowBackup="true"|exported="true"' AndroidManifest.xml && \
    echo "[MOBILE APPSEC FINDINGS] Debuggable build, backup enabled, and exported sensitive Activity detected!"

  # Note: On real APKs during authorized assessments, use:
  # apktool d target_app.apk   (decodes AndroidManifest.xml & Smali bytecode)
  # jadx -d out_src target_app.apk  (decompiles DEX bytecode into readable Java source)
  ```

---

### 21. Container Security & 22. Kubernetes Security
* **Concept:** Hardening containerized workloads and orchestration clusters across build, registry, and runtime phases:
  * **Container Security:**
    * **Minimal Base Images:** Use `distroless`, `scratch`, or `alpine` images to eliminate shells, package managers, and unnecessary binaries.
    * **Image Vulnerability Scanning:** Scan images in CI/CD before deployment (`trivy image myapp:latest`).
    * **Runtime Hardening:** Never run containers as `root` (`USER 1000:1000`), drop all Linux kernel capabilities (`--cap-drop=ALL`), mount root filesystems read-only (`--read-only`), and never mount `/var/run/docker.sock` inside untrusted containers.
  * **Kubernetes Security:**
    * **Control Plane & Secret Encryption:** Encrypt `etcd` at rest (Kubernetes Secrets are merely Base64-encoded by default, *not* encrypted!) and integrate external vaults (HashiCorp Vault, AWS Secrets Manager).
    * **RBAC & Service Accounts:** Enforce least-privilege `Role` / `RoleBinding` rules and disable automatic service-account token mounting (`automountServiceAccountToken: false`) when pods do not call the Kubernetes API.
    * **Pod Security Standards (PSS) & NetworkPolicies:** Enforce the `restricted` Pod Security profile (blocks privileged pods and hostPath mounts) and apply default-deny **NetworkPolicies** to restrict east-west pod-to-pod traffic.

* **Hands-On Task 1 (Run a Hardened Non-Root, Read-Only, Capability-Dropped Container):**
  ```bash
  docker run --rm \
    --user 1000:1000 \
    --cap-drop=ALL \
    --security-opt=no-new-privileges:true \
    --read-only \
    alpine:latest sh -c 'id && touch /test_write 2>&1 || echo "[PASS] Root filesystem is read-only and non-root!"'
  ```

* **Hands-On Task 2 (Audit a Kubernetes Pod & NetworkPolicy Manifest for Security Best Practices):**
  ```bash
  cd ~/pro_extensions_lab

  cat << 'EOF' > k8s_hardened_pod.yaml
  apiVersion: v1
  kind: Pod
  metadata:
    name: hardened-api-pod
  spec:
    automountServiceAccountToken: false
    securityContext:
      runAsNonRoot: true
      runAsUser: 1000
    containers:
    - name: api
      image: nginx:alpine
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        capabilities:
          drop: ["ALL"]
  EOF

  grep -E "runAsNonRoot|allowPrivilegeEscalation|readOnlyRootFilesystem" k8s_hardened_pod.yaml
  ```

---

## Part F: Enterprise Security Architecture & Auditing

### 23. Security Architecture Design
* **Concept:** Synthesizing business goals, threat models, compliance requirements, and technical controls into resilient, scalable enterprise blueprints:
  * **Defense-in-Depth & Zero Trust:** Combining microsegmented network zones, Identity-Aware Proxies (PEP/Control Plane), phishing-resistant MFA (FIDO2), end-to-end encryption (TLS 1.3 + KMS), and automated SOAR containment.
  * **Resilience by Design:** Eliminating single points of failure across compute, power, storage, and multi-region/multicloud deployments to guarantee **RTO/RPO** targets.
  * **Secure-by-Default & Shift-Left:** Embedding automated SAST/SCA/IaC guardrails into CI/CD pipelines so insecure configurations never reach production.

### 24. Security Auditing
* **Concept:** Conducting objective, evidence-driven evaluations of technical controls, governance policies, and operational processes against authoritative standards (**ISO/IEC 27001, SOC 2 Type II, PCI-DSS, NIST CSF, CIS Benchmarks**):
  * **Evidence Collection & Sampling:** Gathering cryptographic configuration proofs, SIEM/IAM logs, and statistical samples rather than relying solely on verbal assertions.
  * **Gap Analysis & Risk Prioritization:** Mapping control deficiencies to business risk (`Likelihood × Impact`), assigning Risk Owners, and tracking corrective action plans (**POA&Ms** — Plans of Action and Milestones) through independent verification.

---

### Professional Extensions Mastery Checklist
- [ ] Applied **STRIDE Threat Modeling** and prevented **OWASP API Mass Assignment** in Python.
- [ ] Practiced **ELF Binary Header/Symbol Inspection** (`readelf`, `nm`) and **PCAP DNS/HTTP Triage** (`tshark`/`tcpdump`).
- [ ] Audited a synthetic **Android `AndroidManifest.xml`** for mobile security flaws (`debuggable`, `allowBackup`, `exported`) and reviewed **APK static decompilation (`apktool`/`jadx`)**.
- [ ] Executed a hardened **non-root, capability-dropped, read-only container** and verified **Kubernetes Pod Security** controls.
- [ ] Integrated **Enterprise Security Architecture Design** and evidence-based **Security Auditing** across the full curriculum.
