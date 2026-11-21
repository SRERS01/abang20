# Complete Guide: Termux + SSH for Bug Bounty Hunting & Offensive Security

**Termux** turns an Android device into a portable Linux environment capable of running **OpenSSH** as both a **client** and a **server**. For bug bounty hunters and offensive security researchers, pairing Termux with a cloud VPS or home Ubuntu rig enables 24/7 mobile reconnaissance, out-of-band (OAST) payload testing, and encrypted traffic pivoting.

---

## Part 1: Installing & Configuring SSH in Termux

### 1. Install OpenSSH
Open Termux and update packages before installing `openssh`:
```bash
pkg update && pkg upgrade -y
pkg install openssh -y
```

Verify the installation:
```bash
ssh -V
```

### 2. Use Termux as an SSH Client (Android ➔ Ubuntu / VPS)
Connect from your Android phone to your Ubuntu machine or cloud VPS:
```bash
ssh username@TARGET_IP
```
*Example:*
```bash
ssh hunter@192.168.1.10
```

### 3. Use Termux as an SSH Server (Ubuntu / VPS ➔ Android)
Because Android restricts non-root apps from binding to ports below 1024, Termux `sshd` listens on **port `8022`** by default.

1. **Set a login password** (or configure SSH keys in `~/.ssh/authorized_keys`):
   ```bash
   passwd
   ```
2. **Start the SSH daemon:**
   ```bash
   sshd
   ```
3. **Retrieve your username, port, and local IP:**
   ```bash
   whoami          # Displays your Termux username (e.g., u0_a245)
   ss -tln         # Confirms sshd is listening on 0.0.0.0:8022
   ip addr         # Shows your Android Wi-Fi IP (usually under wlan0)
   ```

### 4. Connect from Ubuntu to Termux
From your Ubuntu terminal, specify port `8022` using `-p`:
```bash
ssh -p 8022 u0_a245@ANDROID_IP
```

### 5. Stop the Termux SSH Server
When finished, kill the background daemon to save battery and close the listening port:
```bash
pkill sshd
```

> **⚠️ Android Stability Tip:** Android's battery optimizer aggressively kills background apps. Run `termux-wake-lock` inside Termux and disable battery optimization for Termux in Android Settings to keep SSH sessions alive.

---

## Part 2: Architecture Overview

```text
+--------------------------+          SSH (Port 22)          +---------------------------+

|   Android (Termux)       | ------------------------------> |  Ubuntu Rig / Cloud VPS   |
|  - Mobile Control Node   |                                 |  - Heavy Recon (Nuclei)   |
|  - SSH Client & Server   | <------------------------------ |  - Public IP for OAST     |
+--------------------------+       SSH (Port 8022) / SCP     +---------------------------+
```

---

## Part 3: Bug Bounty & Offensive Security Use Cases

Running heavy recon tools directly on a phone drains battery and burns mobile data. Instead, use **Termux as a lightweight command-and-control client** connected to an **Ubuntu VPS**.

### 1. 24/7 Recon Management with `tmux`
Launch heavy subdomain enumeration, port scans, or `nuclei` templates on your Ubuntu VPS from your phone, detach, and check results later—even if your phone switches between Wi-Fi and mobile data.

```bash
# 1. SSH into your Ubuntu Recon VPS from Termux
ssh hunter@your-vps-ip

# 2. Start a persistent terminal multiplexer session
tmux new -s recon

# 3. Run heavy recon pipeline
subfinder -d target.com -silent | httpx -silent | nuclei -t cves/ -o hits.txt

# 4. Detach safely (Press Ctrl+B, then D) and disconnect SSH
# Reattach anytime later from Termux:
tmux attach -t recon
```

### 2. Out-of-Band (OAST) Callbacks & Reverse Port Forwarding (`-R`)
When testing for **Blind SSRF, Blind XSS, or XXE**, targets cannot reach your Android phone behind Carrier-Grade NAT (CGNAT). Use **SSH Remote Port Forwarding** to expose a local listener on your phone through your VPS's public IP:

```bash
# Run from Termux: Forwards VPS port 9000 -> Termux local port 8080
ssh -R 9000:127.0.0.1:8080 hunter@your-vps-ip
```
* Start a simple listener in Termux (`python3 -m http.server 8080` or `nc -lvnp 8080`).
* Inject `http://YOUR_VPS_IP:9000/ssrf-test` into target parameters to capture callbacks directly on your phone.

### 3. Routing Mobile Traffic Through Your VPS (`-D` SOCKS Proxy)
Bypass IP rate-limits or WAF blocks while testing on the go by turning your SSH connection into an encrypted **SOCKS5 proxy**:

```bash
# Run from Termux: Opens local SOCKS5 proxy on port 1080
ssh -D 1080 -N hunter@your-vps-ip
```
* Configure Firefox on Android (or `proxychains` in Termux) to use `127.0.0.1:1080`. All bug bounty traffic now originates from your VPS IP.

### 4. Rapid Loot & Wordlist Syncing (`scp`)
Pull discovered endpoints, screenshots, or JS files from your Ubuntu machine straight to your Android device for manual code review while traveling:

```bash
# Download recon results from Ubuntu VPS to Termux
scp hunter@your-vps-ip:~/recon/://target.com ~/storage/downloads/
```

---

## Part 4: Operational Security (OpSec) Checklist for Hunters

* **Use Ed25519 Keys, Not Passwords:** Generate an SSH key in Termux (`ssh-keygen -t ed25519`) and copy it to your VPS (`ssh-copy-id hunter@your-vps-ip`), then disable password login on your VPS (`PasswordAuthentication no`).
* **Hardening Termux `sshd`:** Edit `\$PREFIX/etc/ssh/sshd_config` in Termux and set `PasswordAuthentication no` once your Ubuntu public key is added to `~/.ssh/authorized_keys`.
* **Never Leave `sshd` Running on Public Wi-Fi:** Always run `pkill sshd` when connecting to untrusted hotspots.
* **Authorized Scope Only:** Ensure all recon, scanning, and callback payloads strictly adhere to the target program's scope and rules of engagement.
