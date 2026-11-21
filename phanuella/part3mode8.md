# Part 3 – Practical Security+ Laboratory Syllabus
## Module 8: Cloud Security Laboratory

> **Lab Environment:** Linux VM (Ubuntu/Debian), Python 3 (`json`, `re`, `hashlib`, `datetime`), **Terraform**, **Prowler** (open-source multi-cloud CSPM), Docker (for local S3-compatible **MinIO** & **LocalStack** cloud simulation), AWS/Azure/GCP Free Tier CLI (`aws`, `az`, `gcloud`).  
> **Safety Best Practice:** Never commit cloud credentials (`~/.aws/credentials`, service account JSON keys) to Git repositories; use temporary STS session tokens or IAM Roles.

---

### Lab 1: Cloud Identity Management (IAM Users, Roles & MFA Enforcement)
* **Objective:** Enforce the **Principle of Least Privilege**, eliminate standing root/admin keys, and audit cloud accounts for missing Multi-Factor Authentication (MFA) and stale access keys across AWS, Azure (Entra ID), and GCP.
* **Hands-On Steps:**
  * **AWS CLI Credential & MFA Audit:**
    ```bash
    # Generate and inspect an AWS IAM Credential Report (verifies root MFA & access key rotation)
    # aws iam generate-credential-report
    # aws iam get-credential-report --query 'Content' --output text | base64 -d

    # Local Python IAM Audit Simulation (detects Root MFA disabled & keys older than 90 days)
    python3 -c '
    iam_users = [
        {"user": "<root_account>", "mfa_active": False, "access_key_age_days": 0},
        {"user": "ci-deploy-bot",  "mfa_active": True,  "access_key_age_days": 145}
    ]
    for u in iam_users:
        if u["user"] == "<root_account>" and not u["mfa_active"]:
            print("[CRITICAL - CLOUD IAM] Root account MFA is DISABLED!")
        if u["access_key_age_days"] > 90:
            print(f"[HIGH - CLOUD IAM] {u[\"user\"]} access key is {u[\"access_key_age_days\"]} days old (>90d rotation policy)!")
    '
    ```

---

### Lab 2: Cloud Access Policies (Least-Privilege JSON Policies & Conditional Access)
* **Objective:** Write and audit declarative JSON IAM policies (AWS IAM / Azure RBAC / GCP IAM) to eliminate overly permissive wildcard (`"Action": "*"`, `"Resource": "*"`) permissions and enforce IP/MFA conditions.
* **Hands-On Steps (Audit & Harden an AWS IAM Policy JSON Document):**
  ```bash
  mkdir -p ~/cloud_sec_lab && cd ~/cloud_sec_lab

  cat << 'EOF' > s3_readonly_policy.json
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "EnforceTLSAndScopedRead",
        "Effect": "Allow",
        "Action": ["s3:GetObject", "s3:ListBucket"],
        "Resource": [
          "arn:aws:s3:::corp-audit-logs-prod",
          "arn:aws:s3:::corp-audit-logs-prod/*"
        ],
        "Condition": {
          "Bool": { "aws:SecureTransport": "true" }
        }
      }
    ]
  }
  EOF

  python3 -m json.tool s3_readonly_policy.json
  ```

---

### Lab 3: Cloud Storage Security (Bucket ACLs, Block Public Access & Versioning)
* **Objective:** Prevent public object storage leaks (**AWS S3**, **Azure Blob**, **GCP Cloud Storage**) by enforcing **Block Public Access**, private ACLs, and **Object Versioning / Object Lock (WORM)** for ransomware resilience.
* **Hands-On Steps (Run a Local S3-Compatible Storage Security Lab via Docker + MinIO):**
  ```bash
  # 1. Spin up local S3-compatible MinIO object storage
  docker run -d --name cloud-s3-lab -p 9000:9000 -p 9001:9001 \
    -e "MINIO_ROOT_USER=cloudadmin" -e "MINIO_ROOT_PASSWORD=StrongCloudPass2026!" \
    minio/minio server /data --console-address ":9001"

  # 2. Verify anonymous HTTP requests to a private bucket return 403 Access Denied
  sleep 2
  curl -sI http://127.0.0 | head -n 5

  # 3. Clean up lab container
  docker rm -f cloud-s3-lab
  ```

---

### Lab 4: Cloud Networking (VPC Subnets, Security Groups & NACLs)
* **Objective:** Segment cloud workloads into **Public Subnets** (load balancers/NAT gateways) and **Private Subnets** (databases/internal microservices), enforce stateful **Security Groups**, and block `0.0.0.0/0` administrative ingress.
* **Hands-On Steps (Simulate Cloud VPC Subnet Isolation & Security Group ACL Audit):**
  ```bash
  # Create an isolated Private Cloud Subnet (--internal blocks all direct Internet routing)
  docker network create --internal --subnet=10.80.2.0/24 vpc_private_db_subnet
  docker network inspect vpc_private_db_subnet | grep -E "Name|Internal|Subnet"
  docker network rm vpc_private_db_subnet
  ```

---

### Lab 5: Cloud Encryption (KMS, Customer-Managed Keys & TLS in Transit)
* **Objective:** Implement encryption at rest using Cloud **KMS (Key Management Service)** with **Customer-Managed Keys (CMKs)** and automatic annual key rotation, plus TLS 1.2/1.3 encryption in transit.
* **Hands-On Steps (Simulate Cloud KMS Envelope Encryption & Key Rotation in Python):**
  ```python
  import secrets

  kms_keys = {
      "arn:aws:kms:af-south-1:111122223333:key/cmk-prod-01": {
          "key_spec": "SYMMETRIC_DEFAULT (AES-256-GCM)",
          "origin": "AWS_KMS (HSM-backed)",
          "key_rotation_enabled": True,
          "state": "Enabled"
      }
  }
  for arn, meta in kms_keys.items():
      print(f"KMS Key: {arn}\n  Spec: {meta['key_spec']} | Rotation Enabled: {meta['key_rotation_enabled']}")
  ```

---

### Lab 6: Cloud Logging (CloudTrail, Azure Activity Log & VPC Flow Logs)
* **Objective:** Enable multi-region control-plane audit logging (**AWS CloudTrail**, **Azure Activity/Entra ID Logs**, **GCP Cloud Audit Logs**) and **VPC Flow Logs** to detect unauthorized API calls (`DeleteTrail`, `PutBucketPolicy`, `CreateUser`).
* **Hands-On Steps (Parse & Alert on Suspicious CloudTrail Control-Plane Events in Python):**
  ```python
  cloudtrail_events = [
      {"eventName": "ConsoleLogin",    "userIdentity": "admin",    "sourceIPAddress": "102.244.10.5", "mfaUsed": "No"},
      {"eventName": "StopLogging",     "userIdentity": "attacker", "sourceIPAddress": "198.51.100.88"},
      {"eventName": "PutBucketAcl",    "userIdentity": "dev_bob",  "requestParameters": {"ACL": "public-read"}}
  ]

  for ev in cloudtrail_events:
      if ev["eventName"] in {"StopLogging", "DeleteTrail"}:
          print(f"[CLOUDTRAIL CRITICAL] Defense Evasion: '{ev['eventName']}' executed by {ev['userIdentity']}!")
      elif ev["eventName"] == "ConsoleLogin" and ev.get("mfaUsed") == "No":
          print(f"[CLOUDTRAIL HIGH] Console login without MFA from IP {ev['sourceIPAddress']}!")
      elif ev.get("requestParameters", {}).get("ACL") == "public-read":
          print(f"[CLOUDTRAIL CRITICAL] Bucket made public-read by {ev['userIdentity']}!")
  ```

---

### Lab 7: Cloud Misconfiguration Detection with Prowler (CSPM)
* **Objective:** Use **Prowler** (open-source Cloud Security Posture Management tool supporting **AWS, Azure, GCP, and Kubernetes**) to run automated CIS Benchmark security assessments across cloud accounts.
* **Hands-On Steps:**
  ```bash
  # Install Prowler via pip in a virtual environment (or inspect CLI options)
  # python3 -m venv ~/prowler_venv && source ~/prowler_venv/bin/activate
  # pip install prowler

  # Example Prowler CSPM audit commands across all three major cloud providers:
  echo "AWS CIS Audit   : prowler aws --compliance cis_3.0_aws"
  echo "Azure Audit     : prowler azure --sp-env-auth"
  echo "GCP Audit       : prowler gcp --project-ids my-secplus-project"
  echo "Kubernetes Audit: prowler kubernetes"
  ```

---

### Lab 8: Cloud Vulnerability Management (Container & VM Image Scanning)
* **Objective:** Scan cloud VM images, container images, and serverless dependencies for OS/package CVEs before deploying into production clusters.
* **Hands-On Steps (Audit a Container Image Software Inventory):**
  ```bash
  # Inspect OS release and installed packages inside an Alpine container image
  docker run --rm alpine:latest sh -c "cat /etc/os-release && apk info -v"
  ```

---

### Lab 9: Infrastructure as Code (IaC) Security with Terraform
* **Objective:** Write a security-hardened **Terraform (`.tf`)** template enforcing private S3 storage, KMS encryption, and restricted security groups—and run static IaC security linting *before* `terraform apply`.
* **Hands-On Steps:**
  ```bash
  cd ~/cloud_sec_lab

  cat << 'EOF' > secure_storage.tf
  resource "aws_s3_bucket" "compliance_logs" {
    bucket = "secplus-corp-compliance-logs-2026"
  }

  resource "aws_s3_bucket_public_access_block" "block_public" {
    bucket                  = aws_s3_bucket.compliance_logs.id
    block_public_acls       = true
    block_public_policy     = true
    ignore_public_acls      = true
    restrict_public_buckets = true
  }

  resource "aws_s3_bucket_server_side_encryption_configuration" "sse_kms" {
    bucket = aws_s3_bucket.compliance_logs.id
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "aws:kms"
      }
    }
  }
  EOF

  # Validate Terraform syntax if installed, and run a local static IaC policy check
  terraform fmt -check secure_storage.tf 2>/dev/null || true
  grep -q "block_public_acls       = true" secure_storage.tf && \
    echo "[IaC PASSED] S3 Block Public Access and KMS encryption verified in Terraform code."
  ```

---

### Lab 10: Cloud Incident Response (Containment, Key Revocation & Snapshot Forensics)
* **Objective:** Respond to a compromised cloud IAM access key or breached EC2/VM instance by immediately revoking active sessions, attaching a deny-all quarantine policy, and taking an immutable forensic volume snapshot for offline investigation.
* **Hands-On Steps (Simulate Cloud IAM Compromised Key Containment Playbook in Python):**
  ```python
### Lab 10: Cloud Incident Response (Containment, Key Revocation & Snapshot Forensics)
* **Objective:** Execute a rapid cloud incident response playbook when an IAM access key (`AKIA...`), OAuth token, or cloud compute instance is compromised—immediately revoking active sessions, attaching a deny-all quarantine policy, preserving immutable forensic disk snapshots, and routing logs to an isolated security account.
* **Hands-On Step 1: Execute a Multi-Step Cloud IAM & VM Containment Playbook in Python:**
  ```python
  from datetime import datetime, timezone

  def cloud_ir_containment(provider, principal_id, compromised_key, instance_id):
      timestamp = datetime.now(timezone.utc).isoformat()
      actions = [
          f"[STEP 1 - IAM CONTAINMENT] Disabled/Deleted leaked Access Key '{compromised_key}' for '{principal_id}'.",
          f"[STEP 2 - SESSION REVOCATION] Revoked all temporary STS/OAuth tokens issued prior to {timestamp}.",
          f"[STEP 3 - QUARANTINE POLICY] Attached explicit 'DenyAll' policy to '{principal_id}' to stop privilege escalation.",
          f"[STEP 4 - NETWORK ISOLATION] Moved instance '{instance_id}' to 'IR-Quarantine-SG' (0.0.0.0/0 egress blocked).",
          f"[STEP 5 - FORENSIC SNAPSHOT] Created immutable volume snapshot & copied to isolated Security Forensics Account."
      ]
      print(f"=== {provider.upper()} CLOUD INCIDENT RESPONSE EXECUTION ({timestamp}) ===")
      for step in actions:
          print(" ", step)

  cloud_ir_containment("AWS", "ci-deploy-bot", "AKIAIOSFODNN7EXAMPLE", "i-0987654321abcdef0")
  ```

* **Hands-On Step 2: Reference Cloud CLI Commands for Immediate Containment (AWS / Azure / GCP):**
  ```bash
  # AWS CLI: Deactivate a leaked IAM access key immediately
  # aws iam update-access-key --user-name ci-deploy-bot --access-key-id AKIAIOSFODNN7EXAMPLE --status Inactive

  # Azure CLI: Revoke all active refresh tokens for a compromised Entra ID user
  # az rest --method POST --uri "https://microsoft.com"

  # GCP CLI: Disable a compromised service account key
  # gcloud iam service-accounts keys disable KEY_ID --iam-account=bot@://gserviceaccount.com
  ```

---

## Quick-Reference Multi-Cloud Security & CSPM Matrix (Exam & Lab Synthesis)

| Cloud Security Area | AWS Service / Tool | Microsoft Azure | Google Cloud (GCP) | Open-Source / Multi-Cloud Tool |
| :--- | :--- | :--- | :--- | :--- |
| **Identity & Access (IAM)** | AWS IAM, IAM Identity Center | Microsoft Entra ID, Azure RBAC | Cloud IAM, Workforce Identity | **Keycloak**, **OpenLDAP** |
| **Encryption & Key Mgmt** | AWS KMS, CloudHSM | Azure Key Vault, Dedicated HSM | Cloud KMS, Cloud HSM | **HashiCorp Vault**, **OpenSSL** |
| **Control-Plane Audit Logs** | AWS CloudTrail | Azure Activity Log / Entra Logs | Cloud Audit Logs | **Splunk**, **Wazuh** |
| **Network Traffic Logs** | VPC Flow Logs | NSG Flow Logs / VNet Flow Logs | VPC Flow Logs | **Security Onion / Zeek** |
| **Object Storage Security** | S3 Block Public Access / Object Lock | Azure Blob Immutable Storage | GCS Bucket Policy / Retention | **MinIO** (Local S3 lab) |
| **CSPM / Misconfig Audit** | AWS Security Hub / Config | Microsoft Defender for Cloud | Security Command Center | **Prowler**, **ScoutSuite** |
| **Infrastructure as Code** | CloudFormation, CDK | ARM Templates, Bicep | Deployment Manager | **Terraform**, **Checkov**, **tfsec** |

---

### Module 8 Lab Completion Checklist
- [ ] Audited **Cloud Identity (IAM)** for Root MFA enforcement and 90-day access key rotation across AWS/Azure/GCP.
- [ ] Authored a least-privilege **JSON IAM Policy** enforcing `aws:SecureTransport` (TLS-only access).
- [ ] Tested private vs. public **Object Storage** controls using **MinIO** and isolated **VPC Subnets** (`--internal`).
- [ ] Configured **Cloud KMS** encryption settings and built a **CloudTrail** anomaly detector flagging `StopLogging` and public bucket changes.
- [ ] Reviewed **Prowler** multi-cloud CSPM commands, wrote a hardened **Terraform (`.tf`)** template, and executed a **Cloud Incident Response** key-revocation and forensic snapshot playbook.
