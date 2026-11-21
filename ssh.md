# Complete SSH (Secure Shell) Course: From Fundamentals to Security

**SSH (Secure Shell)** is a cryptographic network protocol used to securely access, manage, and transfer data between computers over an unsecured network. By default, SSH operates over **TCP Port 22**.

---

## Module 1: Installation & Service Management (Ubuntu/Linux)

Most Linux systems include the **SSH Client** by default, while servers require the **SSH Server** (`openssh-server`).

### 1. Install OpenSSH Server
```bash
sudo apt update
sudo apt install openssh-server -y
```

### 2. Manage the SSH Service
```bash
# Check if SSH is running
sudo systemctl status ssh

# Start or restart the SSH service
sudo systemctl start ssh
sudo systemctl restart ssh

# Enable SSH to start automatically on boot
sudo systemctl enable ssh
```

### 3. Allow SSH Through UFW Firewall
```bash
sudo ufw allow OpenSSH
sudo ufw enable
```

---

## Module 2: Connecting & Basic Usage

### 1. Basic Remote Login
```bash
ssh username@target_ip
```
*Example:* `ssh ubuntu@192.168.1.50`

### 2. Connecting on a Custom Port
```bash
ssh -p 2222 username@target_ip
```

### 3. Running a Single Remote Command (Without Opening a Shell)
```bash
ssh username@target_ip "uptime && df -h"
```

### 4. Host Key Verification (`known_hosts`)
The first time you connect to a server, SSH asks you to verify its fingerprint and saves it in `~/.ssh/known_hosts`. If a server's key suddenly changes, SSH warns you of a potential **Man-in-the-Middle (MITM)** attack.

---

## Module 3: Secure File Transfers (SCP & SFTP)

SSH encrypts file transfers using `scp` (Secure Copy) and `sftp` (SSH File Transfer Protocol).

### 1. Using SCP
```bash
# Upload a local file to a remote server
scp file.txt username@target_ip:/remote/directory/

# Download a remote file to your local machine
scp username@target_ip:/remote/directory/file.txt ./

# Copy an entire directory recursively (-r) on a custom port (-P)
scp -r -P 2222 ./my_folder username@target_ip:/remote/directory/
```

### 2. Using SFTP (Interactive File Session)
```bash
sftp username@target_ip
```
Common SFTP commands inside the session:
* `ls` / `lls` — List remote / local files
* `cd` / `lcd` — Change remote / local directory
* `get filename` — Download a file
* `put filename` — Upload a file
* `exit` — Close session

---

## Module 4: SSH Key-Based Authentication (Passwordless & Secure)

Passwords can be brute-forced. **SSH Key Pairs** use asymmetric cryptography (a **Private Key** on your machine and a **Public Key** on the server).

### 1. Generate an SSH Key Pair (Client Side)
Use the modern, fast, and secure **Ed25519** algorithm:
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```
* Saves private key to `~/.ssh/id_ed25519` (Keep secret! Permissions must be `600`).
* Saves public key to `~/.ssh/id_ed25519.pub` (Safe to share).

### 2. Copy Your Public Key to the Server
```bash
ssh-copy-id username@target_ip
```
*(Manually, this appends your `.pub` key into `~/.ssh/authorized_keys` on the server).*

### 3. Simplify Connections with `~/.ssh/config`
Create or edit `~/.ssh/config` on your local machine to create shortcuts:
```text
Host myserver
    HostName 192.168.1.50
    User ubuntu
    Port 2222
    IdentityFile ~/.ssh/id_ed25519
```
Now connect simply by typing:
```bash
ssh myserver
```

---

## Module 5: SSH Tunneling & Port Forwarding

SSH can tunnel unencrypted traffic through an encrypted connection—essential for both administration and penetration testing.

### 1. Local Port Forwarding (`-L`)
Access a service running internally on the remote server (e.g., a database on port 3306) from your local machine:
```bash
ssh -L 8080:127.0.0.1:3306 username@target_ip
```
*Connecting to `localhost:8080` on your PC now forwards securely to port `3306` on the server.*

### 2. Remote Port Forwarding (`-R`)
Expose a service running on your local machine to the remote server:
```bash
ssh -R 9000:127.0.0.1:80 username@target_ip
```

### 3. Dynamic Port Forwarding / SOCKS Proxy (`-D`)
Route your browser or tools (like `proxychains`) through the remote server:
```bash
ssh -D 1080 -N username@target_ip
```

---

## Module 6: Hardening an SSH Server (Defensive Security)

Edit the SSH daemon configuration file:
```bash
sudo nano /etc/ssh/sshd_config
```

Apply these recommended security settings:
```text
Port 2222                        # Change default port to reduce automated bot scans
PermitRootLogin no               # Disable direct root login
PasswordAuthentication no        # Force SSH key authentication only
PubkeyAuthentication yes         # Enable public key authentication
MaxAuthTries 3                   # Limit failed login attempts per connection
AllowUsers ubuntu admin          # Whitelist specific users allowed to SSH
```

Validate syntax and restart SSH to apply changes:
```bash
sudo sshd -t
sudo systemctl restart ssh
```
*(Remember to update UFW if you changed the port: `sudo ufw allow 2222/tcp`)*

---

## Module 7: Offensive Security & Auditing Notes

* **Reconnaissance & Banner Grabbing:**
  ```bash
  nmap -sV -p 22 target_ip
  ```
  Reveals the OpenSSH version and OS details to check for known CVEs.
* **Privilege Escalation / Post-Exploitation Checks:**
  * Check `~/.ssh/` for unencrypted private keys (`id_rsa`, `id_ed25519`) to pivot to other machines.
  * Check `authorized_keys` to see who has access or to maintain persistence in authorized lab environments.
  * Inspect `/etc/ssh/sshd_config` for weak configurations (e.g., `PermitRootLogin yes` or `PasswordAuthentication yes`).
* **Brute-Force Protection:** Defenders often pair SSH with **Fail2Ban** to automatically ban IPs after repeated failed login attempts.

---

## Quick Reference Cheat Sheet

| Command | Description |
| :--- | :--- |
| `ssh user@host` | Connect to remote host on port 22 |
| `ssh -p 2222 user@host` | Connect on custom port 2222 |
| `ssh-keygen -t ed25519` | Generate a modern Ed25519 key pair |
| `ssh-copy-id user@host` | Install your public key on a remote server |
| `scp file user@host:/path` | Securely copy a file to a remote host |
| `ssh -L 8080:localhost:80 user@host` | Forward local port 8080 to remote port 80 |
| `ssh -D 1080 user@host` | Start a local SOCKS5 proxy on port 1080 |
| `sudo sshd -t` | Test `/etc/ssh/sshd_config` for syntax errors |
