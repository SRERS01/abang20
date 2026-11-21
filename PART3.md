# Part 3 – Practical Security+ Laboratory Syllabus (100% Free & Open-Source)

Knowing definitions is not enough. You must be able to **configure, inspect, identify, analyse, and respond** to security problems using **100% free and open-source software (FOSS)** on Linux (Ubuntu / Kali).

> **Legal & Ethical Notice:** Only execute scanning, auditing, and testing commands against local virtual machines, Docker containers, or systems you explicitly own and have written permission to test.

---

## Module 1: Linux Security Laboratory

**Free Tools:** Ubuntu / Kali Linux, `ufw`, `openssh-server`, `auditd`, `aide`, `lynis`, Bash

### 1. User and Group Management

```bash
# Create a group and a user with a home directory and bash shell
sudo groupadd secops
sudo useradd -m -s /bin/bash -G secops analyst1
sudo passwd analyst1

# Inspect user ID, group memberships, and password aging
id analyst1
groups analyst1
sudo chage -l analyst1

# Lock and unlock an account
sudo usermod -L analyst1
sudo usermod -U analyst1

# Enforce password expiration (90 days max, 7 days warning)
sudo chage -M 90 -W 7 analyst1
```

### 2. File Permissions and Ownership

```bash
# Change ownership and group
sudo chown analyst1:secops /opt/secret_report.txt

# Set strict permissions (owner read/write, group read, others none)
chmod 640 /opt/secret_report.txt

# Set sticky bit on a shared directory (users can only delete their own files)
sudo mkdir -p /srv/shared_drop
sudo chmod 1777 /srv/shared_drop

# Find world-writable files and SUID/SGID binaries (privilege escalation audit)
find / -xdev -type f -perm -0002 2>/dev/null
find / -xdev -type f  -perm -4000 -o -perm -2000  2>/dev/null
```

### 3. Process and Service Management

```bash
# Inspect running processes and resource usage
ps aux --sort=-%cpu | head -n 15
ps -ef | grep sshd

# List active systemd services and failed units
systemctl list-units --type=service --state=running
systemctl --failed

# Disable unnecessary services
sudo systemctl stop bluetooth.service
sudo systemctl disable bluetooth.service
```

### 4. Firewall Configuration (UFW)

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw allow from 192.168.1.0/24 to any port 443 proto tcp
sudo ufw logging medium
sudo ufw enable
sudo ufw status numbered
```

### 5. SSH Security Hardening

```bash
# Generate an Ed25519 SSH key pair on the client
ssh-keygen -t ed25519 -C "analyst1@lab"

# Copy public key to target server
ssh-copy-id -i ~/.ssh/id_ed25519.pub analyst1@192.168.1.50

# Harden SSH daemon (/etc/ssh/sshd_config)
sudo sed -i 's/^#*PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sudo sed -i 's/^#*PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo sed -i 's/^#*MaxAuthTries.*/MaxAuthTries 3/' /etc/ssh/sshd_config

# Validate config and restart SSH
sudo sshd -t && sudo systemctl restart ssh
```

### 6. Log Analysis & File Integrity Monitoring (AIDE)

```bash
# Inspect authentication logs for failed logins
sudo grep "Failed password" /var/log/auth.log
sudo journalctl -u ssh -n 50 --no-pager

# Install and initialize AIDE (File Integrity Monitoring)
sudo apt install aide -y
sudo aideinit
sudo cp /var/lib/aide/aide.db.new /var/lib/aide/aide.db

# Run an integrity check against the baseline
sudo aide --check
```

### 7. System Hardening Audit & Bash Automation

```bash
# Run Lynis open-source security audit
sudo apt install lynis -y
sudo lynis audit system --quick

# Automated Bash script to alert on failed SSH attempts
cat << 'EOF' > ~/ssh_audit.sh
#!/bin/bash
echo "=== Top Failed SSH IPs ==="
grep "Failed password" /var/log/auth.log | awk '{print \$(NF-3)}' | sort | uniq -c | sort -nr | head -n 10
EOF
chmod +x ~/ssh_audit.sh && ./ssh_audit.sh
```

---

## Module 2: Network Security Laboratory

**Free Tools:** `iproute2`, `nmap`, `tcpdump`, `tshark` (Wireshark CLI), `netcat`, `dig`, `openssl`, `suricata`, `zeek`

### 1. IP, Port, and Service Identification

```bash
# View interfaces, IP addresses, and routing table
ip -br a
ip route show

# View listening sockets and associated PIDs
sudo ss -tulnp
```

### 2. Network Discovery and Scanning (Nmap)

```bash
# Host discovery (ping sweep) on local subnet
sudo nmap -sn 192.168.1.0/24

# SYN scan, service version detection, and default scripts
sudo nmap -sS -sV -sC -O -p- 192.168.1.50 -oN scan_report.txt

# UDP top 50 ports scan
sudo nmap -sU --top-ports 50 192.168.1.50

# Firewall evasion / fragmented packet test
sudo nmap -f -Pn -p 22,80,443 192.168.1.50
```

### 3. Packet Capture and Inspection (`tcpdump` & `tshark`)

```bash
# Capture 100 packets on eth0 and save to PCAP
sudo tcpdump -i eth0 -nn -c 100 -w capture.pcap

# Filter live HTTP/DNS traffic on CLI
sudo tcpdump -i eth0 -nn 'port 53 or port 80'

# Analyse PCAP with tshark (Wireshark CLI)
tshark -r capture.pcap -Y "http.request || dns.flags.response == 0"
tshark -r capture.pcap -q -z io,phs
```

### 4. DNS Investigation & Connection Testing (`dig` & `netcat`)

```bash
# Query DNS records (A, MX, TXT, NS) and test zone transfer
dig example.com ANY +noall +answer
dig @://example.com example.com AXFR

# Netcat banner grabbing and port listener test
nc -zv 192.168.1.50 20-80
nc -lvnp 4444
```

### 5. Intrusion Detection & Network Monitoring (`Suricata` & `Zeek`)

```bash
# Update Suricata open ruleset and test configuration
sudo apt install suricata -y
sudo suricata-update
sudo suricata -T -c /etc/suricata/suricata.yaml

# Run Suricata against an offline PCAP file
suricata -r capture.pcap -l ./suricata_logs/
cat ./suricata_logs/fast.log

# Run Zeek on a PCAP to generate structured conn.log, dns.log, http.log
zeek -r capture.pcap
cat conn.log | head -n 20
```
---

## Module 3: Vulnerability Assessment Laboratory

**Free Tools:** Greenbone Community Edition (OpenVAS), `nuclei`, `nikto`, `searchsploit` (Exploit-DB), Metasploit Framework (FOSS)

### 1. Asset Discovery & Vulnerability Scanning (`Nuclei` & `Nikto`)

```bash
# Update Nuclei community templates
nuclei -update-templates

# Scan a local target web application for medium, high, and critical vulnerabilities
nuclei -u http://127.0.0.1:3000 -severity medium,high,critical -o nuclei_results.txt

# Run Nikto web server vulnerability scanner and export HTML report
nikto -h http://127.0.0.1:3000 -o nikto_report.html -Format htm
```

### 2. Greenbone / OpenVAS Deployment (Free Docker Setup)

```bash
# Download and start official Greenbone Community Containers (100% free)
mkdir -p ~/greenbone && cd ~/greenbone
curl -f -L https://github.io -o docker-compose.yml
docker compose -f docker-compose.yml up -d

# Check container status (Web UI runs on http://127.0.0.1:9392)
docker compose ps
```

### 3. CVE Research, CVSS Lookup & Verification (`searchsploit` & Metasploit)

```bash
# Update offline Exploit-DB archive and search by service/version
sudo apt install exploitdb -y
searchsploit -u
searchsploit apache 2.4.49

# Inspect an exploit script without running it
searchsploit -x linux/webapps/50383.py

# Verify a service version/vulnerability safely with a Metasploit auxiliary scanner
msfconsole -q -x "use auxiliary/scanner/ssh/ssh_version; set RHOSTS 192.168.1.50; run; exit"
```

---

## Module 4: Web and Application Security

**Free Tools:** OWASP ZAP, `curl`, `sqlmap`, `ffuf`, `trivy`, OWASP Juice Shop (Docker)

### 1. Deploy Local Intentionally Vulnerable Target (OWASP Juice Shop)

```bash
# Pull and run OWASP Juice Shop locally on port 3000
docker run -d --name juice-shop -p 3000:3000 bkimminich/juice-shop
```

### 2. HTTP/HTTPS Request, Header, and Cookie Analysis (`curl`)

```bash
# Inspect HTTP response headers and missing security headers (HSTS, CSP, X-Frame-Options)
curl -I -s http://127.0.0.1:3000

# Send a custom JSON POST request and inspect returned session tokens/cookies
curl -i -X POST http://127.0.0 \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@juice-sh.op","password":"test"}'

# Test HTTP methods allowed on an endpoint (OPTIONS / PUT / DELETE check)
curl -i -X OPTIONS http://127.0.0
```

### 3. Directory Enumeration & Automated Web Scanning (`ffuf` & `OWASP ZAP`)

```bash
# Fuzz hidden endpoints and directories with ffuf
ffuf -u http://127.0.0 -w /usr/share/wordlists/dirb/common.txt -mc 200,301,302,403

# Run OWASP ZAP baseline passive/active scan via Docker (100% free)
docker run --rm --network host -v \$(pwd):/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py -t http://127.0.0.1:3000 -r zap_report.html
```

### 4. SQL Injection, Directory Traversal & Dependency Auditing (`sqlmap` & `Trivy`)

```bash
# Test a local lab URL parameter for SQL injection
sqlmap -u "http://127.0.0" --batch --dbs

# Test basic directory traversal via curl
curl -i --path-as-is "http://127.0.0"

# Scan application dependencies and container images for known CVEs using Trivy (FOSS)
sudo apt install trivy -y
trivy fs /path/to/web-app-source
trivy image bkimminich/juice-shop
```
---

## Module 5: Cryptography Laboratory

**Free Tools:** `openssl`, `gpg` (GnuPG), `sha256sum`, `hashcat`, `john` (John the Ripper)

### 1. Public/Private Key Pairs & Digital Signatures (`OpenSSL`)

```bash
# Generate a 4096-bit RSA private key and extract the public key
openssl genrsa -out private.pem 4096
openssl rsa -in private.pem -pubout -out public.pem

# Sign a file with your private key and verify with your public key
openssl dgst -sha256 -sign private.pem -out document.sig document.txt
openssl dgst -sha256 -verify public.pem -signature document.sig document.txt
```

### 2. Hashing & File Integrity Verification

```bash
# Generate SHA-256 checksums and verify file integrity
sha256sum document.txt > document.sha256
sha256sum -c document.sha256

# Generate cryptographically secure random values/tokens
openssl rand -hex 32
openssl rand -base64 24
```

### 3. Self-Signed Certificates, CSRs & TLS Inspection

```bash
# Create a Certificate Signing Request (CSR) and self-signed X.509 certificate
openssl req -new -newkey rsa:2048 -nodes -keyout server.key -out server.csr \
  -subj "/C=CM/ST=Southwest/L=Buea/O=SecLab/CN=lab.local"

openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

# Inspect certificate details and verify certificate chain
openssl x509 -in server.crt -text -noout
openssl verify -CAfile server.crt server.crt

# Test live remote TLS version and supported cipher suites
openssl s_client -connect example.com:443 -tls1_3
```

### 4. File Encryption (`GnuPG`) & Password Auditing (`John` / `Hashcat`)

```bash
# Symmetric file encryption with AES-256 via GPG
gpg --symmetric --cipher-algo AES256 confidential.txt
gpg --decrypt confidential.txt.gpg > decrypted.txt

# Asymmetric GPG key generation, encryption, and decryption
gpg --full-generate-key
gpg --encrypt --recipient "analyst1@lab.local" confidential.txt
gpg --decrypt confidential.txt.gpg > decrypted_asym.txt

# Audit weak hashes using John the Ripper (FOSS)
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt
john --show hashes.txt

# Audit hashes using Hashcat (FOSS - mode 0 = MD5, mode 1000 = NTLM)
hashcat -m 0 -a 0 hashes.txt /usr/share/wordlists/rockyou.txt
hashcat -m 0 hashes.txt --show
```

---

## Module 6: Identity and Access Management (IAM)

**Free Tools:** Linux PAM, `libpam-google-authenticator`, `sudo`, OpenLDAP (`ldap-utils`), Keycloak (Docker)

### 1. Least Privilege (`sudoers`) & MFA on Linux

```bash
# Grant granular sudo access to restart only nginx (no full root access)
echo "analyst1 ALL=(ALL) NOPASSWD: /bin/systemctl restart nginx" | sudo tee /etc/sudoers.d/analyst1
sudo chmod 440 /etc/sudoers.d/analyst1
sudo visudo -c

# Configure TOTP Multi-Factor Authentication for SSH
sudo apt install libpam-google-authenticator -y
google-authenticator
```

### 2. Deploy Local SSO / Identity Provider (`Keycloak` via Docker)

```bash
# Start Keycloak open-source IAM server (OIDC / SAML / RBAC / MFA)
docker run -d --name keycloak -p 8080:8080 \
  -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=AdminLabPass123! \
  quay.io/keycloak/keycloak:latest start-dev
```

### 3. Query OpenLDAP & Audit Privileged Accounts

```bash
# Install OpenLDAP client utilities and query a directory
sudo apt install ldap-utils -y
ldapsearch -x -H ldap://127.0.0.1 -b "dc=lab,dc=local" "(objectClass=inetOrgPerson)"

# Audit all users with UID 0 (root privileges) and sudo group members
awk -F: '(\$3 == "0") {print}' /etc/passwd
getent group sudo
```

### 4. Investigate Authentication Logs & Privilege Escalation Risks

```bash
# Track successful and failed sudo privilege escalations
sudo grep "sudo:" /var/log/auth.log | tail -n 20

# Check for dangerous sudo NOPASSWD permissions on current user
sudo -l
```
---

## Module 7: Security Monitoring and Incident Response

**Free Tools:** `auditd`, Wazuh (FOSS SIEM/XDR), Velociraptor (FOSS DFIR), `volatility3`, `dd`, `iptables`

### 1. Kernel & System Call Auditing (`auditd`)

```bash
# Install auditd and monitor changes to /etc/passwd and /etc/shadow
sudo apt install auditd audispd-plugins -y
sudo auditctl -w /etc/passwd -p wa -k identity_changes
sudo auditctl -w /etc/shadow -p wa -k shadow_changes

# Search audit logs for triggered alerts
sudo ausearch -k identity_changes
```

### 2. Process, Malware Indicator & Network Anomaly Hunting

```bash
# Check for processes running from deleted binaries (common malware indicator)
sudo ls -la /proc/*/exe 2>/dev/null | grep "(deleted)"

# Inspect active outbound connections and map to processes
sudo ss -tunap state established

# Check cron jobs and systemd timers for persistence
cat /etc/crontab
ls -la /etc/cron.* /var/spool/cron/crontabs/
systemctl list-timers --all
```

### 3. Forensic Evidence Preservation & Memory Analysis (`dd` & `Volatility 3`)

```bash
# Create a bit-level disk image and hash it immediately for chain of custody
sudo dd if=/dev/sdb of=/mnt/evidence/disk_image.dd bs=4M status=progress
sha256sum /mnt/evidence/disk_image.dd > /mnt/evidence/disk_image.dd.sha256

# Install and run Volatility 3 (FOSS) on a RAM dump
pip install volatility3
vol -f memory.raw windows.pslist
vol -f memory.raw windows.netscan
vol -f memory.raw windows.malfind
```

### 4. Incident Containment & Reporting Commands

```bash
# Immediately isolate a compromised host's network traffic while keeping SSH management open
sudo iptables -I INPUT 1 -s 192.168.1.100 -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -j DROP
sudo iptables -A OUTPUT -d 192.168.1.100 -p tcp --sport 22 -j ACCEPT
sudo iptables -A OUTPUT -j DROP

# Freeze (SIGSTOP) a suspicious process for memory capture before killing it
sudo kill -STOP <PID>

# Generate a quick system & network triage bundle for an incident report
mkdir -p ~/ir_bundle && cd ~/ir_bundle
date -u > timestamp.txt
ps aux > processes.txt
ss -tulnp > sockets.txt
last -a > logins.txt
```

---

## Module 8: Cloud Security

**Free Tools:** LocalStack (free local AWS cloud emulator), OpenTofu / Terraform (FOSS), `trivy`, `checkov`, `prowler` (FOSS)

### 1. Run a Free Local Cloud Environment (`LocalStack`)

```bash
# Emulate AWS S3, IAM, EC2, and CloudTrail locally without a paid cloud account
docker run -d --name localstack -p 4566:4566 localstack/localstack

# Configure AWS CLI to point to LocalStack
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
alias awslocal='aws --endpoint-url=http://localhost:4566'
```

### 2. Cloud IAM, Storage Security & Encryption Testing

```bash
# Create an S3 bucket and block all public access
awslocal s3api create-bucket --bucket sec-lab-private-data
awslocal s3api put-public-access-block --bucket sec-lab-private-data \
  --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"

# Enable default AES-256 server-side encryption on the bucket
awslocal s3api put-bucket-encryption --bucket sec-lab-private-data \
  --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'

# Audit IAM users and attached policies
awslocal iam list-users
awslocal iam list-attached-user-policies --user-name dev-user
```

### 3. Infrastructure as Code (IaC) & Cloud Misconfiguration Scanning (`Checkov` & `Trivy`)

```bash
# Install Checkov (FOSS IaC static analyser)
pip install checkov

# Scan Terraform / OpenTofu templates for insecure security groups or public buckets
checkov -d ./terraform-infrastructure/

# Scan Kubernetes manifests and Dockerfiles with Trivy (FOSS)
trivy config ./k8s-manifests/
trivy image nginx:latest
```

### 4. Cloud Posture Auditing & Incident Response (`Prowler` Open Source)

```bash
# Install and run Prowler (FOSS cloud security auditing tool)
pip install prowler
prowler aws --endpoint-url http://localhost:4566 --service s3 iam

# Cloud incident response: attach an emergency deny-all policy to a compromised IAM user
awslocal iam put-user-policy --user-name compromised-user --policy-name EmergencyQuarantine \
  --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Deny","Action":"*","Resource":"*"}]}'
```
