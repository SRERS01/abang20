# Part 1 – Foundations Before Security+
## Module 5: Virtualization and Cloud Fundamentals (Practical Lab Guide)

> **Objective:** Gain hands-on experience with hypervisors, containers, cloud service/deployment models, cloud IAM/storage/networking, and Infrastructure as Code (IaC) security before entering Security+ domains.  
> **Recommended Lab Tools:** VirtualBox (or VMware/KVM), Docker Desktop / Docker Engine, `kubectl` (or Minikube/Kind), Python 3, AWS/Azure Free Tier (optional for cloud console tasks).

---

### 1. Virtual Machines (VMs)
* **Concept:** Software-emulated computers running a full Guest Operating System and virtualized hardware (CPU, RAM, NIC, Disk) isolated inside a Host OS.
* **Practical Task:**
  1. Check if your host CPU has hardware virtualization extensions enabled (`VT-x` for Intel, `AMD-V` for AMD):
     * **Windows (PowerShell):**
       ```powershell
       Get-CimInstance Win32_Processor | Select-Object Name, VirtualizationFirmwareEnabled
       ```
     * **Linux:**
       ```bash
       lscpu | grep -i virtualization
       ```
  2. Inside a VirtualBox VM, inspect its virtualized hardware vendor strings (attackers and malware use these exact checks to detect sandboxes):
     ```bash
     # Linux Guest VM:
     sudo dmidecode -s system-product-name   # Outputs: VirtualBox
     ```

### 2. Hypervisors
* **Concept:** The Virtual Machine Monitor (VMM) firmware/software layer that allocates physical host resources (CPU, RAM, storage) to VMs and enforces strict hardware isolation between guests.
* **Practical Task:**
  1. Detect whether your current OS is running directly on bare metal or inside a hypervisor:
     * **Linux:**
       ```bash
       systemd-detect-virt    # Returns 'oracle' (VirtualBox), 'vmware', 'kvm', or 'none'
       ```
     * **Windows (CMD):**
       ```cmd
       systeminfo | findstr /i "Hyper-V"
       ```

### 3. Type 1 and Type 2 Hypervisors
* **Concept:**
  * **Type 1 (Bare-Metal):** Runs directly on physical hardware without a host OS (e.g., VMware ESXi, Microsoft Hyper-V, Linux KVM, Proxmox). Used in enterprise data centers and public clouds.
  * **Type 2 (Hosted):** Runs as an application on top of a conventional Host OS (e.g., Oracle VirtualBox, VMware Workstation). Used for labs and testing.
* **Practical Task:**
  1. Use VirtualBox CLI (`VBoxManage`) on your host machine to list installed VMs, inspect allocated RAM/CPUs, and create a point-in-time **Snapshot** (essential for malware analysis and rollback):
     ```bash
     VBoxManage list vms
     VBoxManage snapshot "<YOUR_VM_NAME>" take "Clean_Baseline" --description "Pre-lab snapshot"
     ```

### 4. Containers
* **Concept:** Lightweight, isolated user-space environments that package an application and its dependencies together while **sharing the host OS kernel** (using Linux **Namespaces** for isolation and **cgroups** for resource limits). Much faster and smaller than full VMs.
* **Practical Task:**
  1. Inspect Linux kernel namespaces on your host/VM to see how processes are isolated:
     ```bash
     lsns | head -n 15
     ```

### 5. Docker Fundamentals
* **Concept:** The industry-standard container runtime platform. Builds immutable **Images** from a `Dockerfile` and runs them as isolated **Containers**.
* **Practical Task (Docker CLI):**
  1. Pull a lightweight Alpine Linux image, run an isolated interactive container, and verify it shares the host's kernel version while having its own isolated filesystem and process tree:
     ```bash
     docker run --rm -it alpine:latest sh -c "uname -r && ps aux && cat /etc/os-release"
     ```
  2. List running and stopped containers:
     ```bash
     docker ps -a
     ```

### 6. Kubernetes Fundamentals (K8s)
* **Concept:** An open-source container orchestration platform that automates deploying, scaling, load-balancing, and self-healing containerized applications across clusters of nodes (**Control Plane** + **Worker Nodes** running **Pods**).
* **Practical Task (`kubectl` / Minikube or Kind):**
  1. Inspect cluster nodes, namespaces, and running system pods:
     ```bash
     kubectl get nodes
     kubectl get pods -A
     ```
  2. Deploy a test Nginx web pod and expose it locally:
     ```bash
     kubectl run secplus-web --image=nginx:alpine --port=80
     kubectl get pod secplus-web -o wide
     kubectl delete pod secplus-web
     ```

### 7. Cloud Computing
* **Concept:** On-demand delivery of compute, storage, and networking resources over the Internet with pay-as-you-go pricing, rapid elasticity, and measured service (NIST definition).
* **Practical Task:**
  1. Trace DNS and routing to a major public cloud provider endpoint to observe cloud edge infrastructure (Anycast/CDN):
     ```bash
     nslookup ://amazonaws.com
     nslookup ://azure.com
     ```

### 8. Public Cloud
* **Concept:** Cloud infrastructure owned and operated by a third-party provider (AWS, Microsoft Azure, Google Cloud Platform) and shared across multiple tenants (**Multi-tenancy**).
* **Practical Task:**
  1. Inspect public cloud SSL/TLS certificates to verify multi-tenant domain Subject Alternative Names (SANs):
     ```bash
     echo | openssl s_client -connect ://amazon.com 2>/dev/null | openssl x509 -noout -subject -issuer
     ```

### 9. Private Cloud
* **Concept:** Cloud infrastructure dedicated exclusively to a single organization (hosted on-premises via OpenStack/VMware vSphere or in a dedicated facility) offering maximum control over compliance and data sovereignty.
* **Practical Task:**
  1. Compare architectural trade-offs in a local lab journal or VirtualBox setup: configure a local private VM network (`Host-Only` adapter) running an internal web app unreachable from the public Internet to simulate an on-premises private cloud boundary.

### 10. Hybrid Cloud
* **Concept:** Combining an on-premises **Private Cloud** with a **Public Cloud** connected via encrypted **Site-to-Site IPsec VPN** or dedicated private links (AWS Direct Connect / Azure ExpressRoute), allowing sensitive workloads to stay on-prem while bursting web traffic to the cloud.
* **Practical Task:**
  1. Map out a hybrid routing table conceptually or in Python: write a conditional routing rule demonstrating split traffic (internal RFC 1918 `10.0.0.0/8` routed to `vpn_gateway`, public `0.0.0.0/0` routed to `cloud_nat_gateway`).

### 11. Multicloud
* **Concept:** Using services from **two or more public cloud providers** simultaneously (e.g., running analytics on Google Cloud BigQuery while hosting primary apps on AWS) to prevent vendor lock-in and increase resilience.
* **Practical Task:**
  1. Query public IP ranges published by multiple cloud providers (e.g., AWS `ip-ranges.json`) to see how organizations identify which cloud hosts a given IP:
     ```bash
     curl -s https://amazonaws.com | grep -E "ip_prefix|region" | head -n 10
     ```

### 12. IaaS, PaaS, and SaaS
* **Concept:** Cloud service models defining how much of the technology stack the customer manages vs. the Cloud Service Provider (CSP):
  * **IaaS (Infrastructure as a Service):** Virtual servers, storage, networks (e.g., AWS EC2, Azure VMs). *You manage OS patching, firewalls, and apps.*
  * **PaaS (Platform as a Service):** Managed runtime/databases (e.g., AWS Elastic Beanstalk, Azure App Service, Heroku). *CSP manages OS; you manage app code and data.*
  * **SaaS (Software as a Service):** Complete cloud applications (e.g., Microsoft 365, Google Workspace, Salesforce). *CSP manages everything; you manage user access and data.*
* **Practical Task:**
  1. Classify 5 tools you use daily into IaaS, PaaS, or SaaS, and list **who is responsible for patching the underlying Linux/Windows OS** in each case.

### 13. Shared Responsibility Model
* **Concept:** Security is divided between the Cloud Provider (**Security *OF* the Cloud**: physical data centers, hypervisors, physical network) and the Customer (**Security *IN* the Cloud**: IAM permissions, data encryption, OS patching in IaaS, firewall rules). Misunderstanding this boundary is the #1 cause of cloud data breaches.
* **Practical Task:**
  1. Audit a sample misconfigured cloud storage policy (simulated below in Python) to identify customer-side failures under the Shared Responsibility Model:
     ```python
     s3_bucket_config = {
         "bucket_name": "corp-customer-backups",
         "block_public_acls": False,
         "encryption_at_rest": None,
         "versioning": "Suspended"
     }

     if not s3_bucket_config["block_public_acls"]:
         print("[CRITICAL] Customer Failure: Public ACLs allowed on sensitive bucket!")
     if not s3_bucket_config["encryption_at_rest"]:
         print("[HIGH] Customer Failure: Server-Side Encryption (SSE-AES256/KMS) disabled!")
     ```

### 14. Cloud Identity (IAM)
* **Concept:** Identity and Access Management controls **Authentication (AuthN)** and **Authorization (AuthZ)** in the cloud using Users, Groups, Roles, Temporary Security Tokens, MFA, and JSON Policy Documents enforcing **Least Privilege**.
* **Practical Task (Audit a Cloud IAM JSON Policy):**
  1. Analyze the following AWS-style IAM policy in Python to detect overly permissive wildcard (`*`) privileges:
     ```python
     import json

     iam_policy = '''
     {
       "Version": "2012-10-17",
       "Statement": [
         {
           "Effect": "Allow",
           "Action": "*",
           "Resource": "*"
         }
       ]
     }
     '''

     policy = json.loads(iam_policy)
     for stmt in policy["Statement"]:
         if stmt["Effect"] == "Allow" and (stmt["Action"] == "*" or stmt["Resource"] == "*"):
             print("[IAM VIOLATION] Overly permissive wildcard (*) detected! Violates Principle of Least Privilege.")
     ```

### 15. Cloud Storage
### 15. Cloud Storage
* **Concept:** Scalable cloud storage architectures categorized by access method and security controls:
  * **Object Storage (AWS S3, Azure Blob, GCS):** Stores unstructured data as objects inside buckets accessed over HTTP/HTTPS APIs. Most cloud data breaches occur due to **publicly exposed buckets**, disabled **Server-Side Encryption (SSE)**, or missing **Object Versioning / Object Lock** (needed for ransomware recovery).
  * **Block Storage (AWS EBS, Azure Managed Disks):** Raw virtual hard drives attached to cloud VMs (formatted with NTFS/ext4).
  * **File Storage (AWS EFS, Azure Files):** Shared network file systems mounted across multiple instances simultaneously via NFS/SMB.
* **Practical Task 1 (Run a Local S3-Compatible Object Storage Lab with MinIO):**
  1. Launch **MinIO** in Docker to practice S3 bucket policies, encryption, and access control locally without needing a credit card:
     ```bash
     docker run -d --name minio-lab \
       -p 9000:9000 -p 9001:9001 \
       -e "MINIO_ROOT_USER=secadmin" \
       -e "MINIO_ROOT_PASSWORD=StrongLabPassword123!" \
       minio/minio server /data --console-address ":9001"
     ```
  2. Open `http://127.0.0.1:9001` in your browser, log in with `secadmin` / `StrongLabPassword123!`, and complete these three security checks:
     * Create a bucket named `incident-logs`.
     * Verify its Access Policy defaults to **Private** (blocking anonymous HTTP `GET` requests).
     * Enable **Versioning** on the bucket so deleted or overwritten objects can be recovered after an accidental deletion or ransomware event.
  3. Test unauthorized anonymous access from your terminal (should return `403 Access Denied`):
     ```bash
     curl -I http://127.0.0
     ```
  4. Clean up when finished:
     ```bash
     docker rm -f minio-lab
     ```

---

### 16. Cloud Networking
* **Concept:** Software-defined networking inside a **VPC (Virtual Private Cloud)** or **VNet**:
  * **Public Subnet vs. Private Subnet:** Public subnets have a route to an **Internet Gateway (IGW)** (for load balancers/bastion hosts). Private subnets have *no* direct inbound route from the Internet and use a **NAT Gateway** for outbound OS patching only.
  * **Security Groups (SGs):** Stateful firewalls attached to cloud instances/ENIs (only `Allow` rules; return traffic is automatically permitted).
  * **NACLs (Network Access Control Lists):** Stateless firewalls attached at the subnet boundary (support both `Allow` and `Deny` rules; require explicit inbound *and* outbound rules).
* **Practical Task (Simulate Isolated Public & Private Cloud Subnets in Docker):**
  1. Create two isolated custom networks representing a **Public DMZ Subnet** and an **Internal Air-Gapped Database Subnet** (`--internal` blocks all external Internet routing, mimicking a private subnet without a NAT gateway):
     ```bash
     docker network create --subnet=10.20.1.0/24 public_dmz_subnet
     docker network create --internal --subnet=10.20.2.0/24 private_db_subnet
     ```
  2. Launch a simulated database container on `private_db_subnet` and verify it cannot reach the public Internet (`8.8.8.8`), enforcing true cloud subnet segmentation:
     ```bash
     docker run --rm --network private_db_subnet alpine:latest ping -c 2 8.8.8.8
     # Expected output: ping: sendto: Network unreachable
     ```
  3. Clean up the simulated VPC subnets:
     ```bash
     docker network rm public_dmz_subnet private_db_subnet
     ```

---

### 17. Virtualization Security
* **Concept:** Attack vectors and defenses unique to hypervisors and container engines:
  * **VM Escape:** Exploiting a hypervisor vulnerability to break out of a Guest VM into the Host Hypervisor (mitigated by timely hypervisor patching, disabling shared clipboard/drag-and-drop, and removing unused virtual hardware).
  * **VM Sprawl:** Unmonitored, unpatched VMs left running without owner oversight.
  * **Container Breakout:** Containers share the host kernel; running a container with `--privileged` or mounting `/var/run/docker.sock` gives the container root-equivalent control over the host OS.
* **Practical Task (Audit Running Containers for Privilege & Isolation Weaknesses):**
  1. Start a temporary test container and run a security audit command that checks for **Privileged Mode**, **Root User Execution**, and **Host Network Sharing**:
     ```bash
     docker run -d --name audit-target nginx:alpine

     docker inspect audit-target --format '
     Container Name : {{.Name}}
     Privileged Mode: {{.HostConfig.Privileged}}
     Network Mode   : {{.HostConfig.NetworkMode}}
     Read-Only FS   : {{.HostConfig.ReadonlyRootfs}}
     User           : {{.Config.User}} (blank means root inside container!)
     '

     docker rm -f audit-target
     ```

---

### 18. Infrastructure as Code (IaC)
* **Concept:** Provisioning and managing servers, networks, firewalls, and storage using declarative code files (**Terraform** `.tf`, **AWS CloudFormation**, **Ansible**, **Docker Compose** `.yml`) stored in Git. IaC enables **immutable infrastructure**, eliminates manual configuration drift, and allows automated security linting (e.g., Checkov, tfsec) *before* resources are deployed.
* **Practical Task 1 (Deploy a Security-Hardened IaC Stack with Docker Compose):**
  Create a `hardened-stack.yml` file that enforces **Least Privilege**, **Read-Only Root Filesystem**, **Localhost Binding**, and **Memory Limits**:
  ```bash
  cat << 'EOF' > hardened-stack.yml
  services:
    web-app:
      image: nginx:alpine
      container_name: iac_hardened_nginx
      ports:
        - "127.0.0.1:8088:80"
      read_only: true
      tmpfs:
        - /var/cache/nginx
        - /var/run
      security_opt:
        - no-new-privileges:true
      deploy:
        resources:
          limits:
            memory: 128M
  EOF

  docker compose -f hardened-stack.yml up -d
  curl -I http://127.0.0.1:8088
  docker compose -f hardened-stack.yml down
  ```

* **Practical Task 2 (Write a Python IaC Security Scanner for Terraform/Config Files):**
  Simulate static code analysis (SAST for IaC) by scanning a simulated Terraform configuration string for open `0.0.0.0/0` SSH firewall rules and unencrypted storage:
  ```python
  terraform_code = '''
  resource "aws_security_group" "web_sg" {
    ingress {
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }
  resource "aws_db_instance" "prod_db" {
    storage_encrypted = false
  }
  '''

  if 'cidr_blocks = ["0.0.0.0/0"]' in terraform_code and "from_port   = 22" in terraform_code:
      print("[IaC HIGH] SSH (Port 22) exposed to the entire internet (0.0.0.0/0)!")

  if "storage_encrypted = false" in terraform_code:
      print("[IaC MEDIUM] Database storage encryption is disabled!")
  ```

---

### Module 5 Completion Checklist
- [ ] Tested private vs. public object storage access policies and bucket versioning using **MinIO** (S3-compatible).
- [ ] Simulated isolated **Public DMZ** and **Private Internal Subnets** using Docker custom networks (`--internal`).
- [ ] Audited container runtime configurations (`docker inspect`) for `--privileged` mode, root user execution, and filesystem permissions.
- [ ] Deployed a hardened **Infrastructure as Code (`docker-compose.yml`)** service with `read_only` filesystem and `no-new-privileges`.
- [ ] Built a Python **IaC static security checker** to catch `0.0.0.0/0` firewall rules and unencrypted storage before deployment.

