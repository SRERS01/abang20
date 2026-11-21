# Complete Guide to Installing and Using UFW on Ubuntu

**UFW (Uncomplicated Firewall)** is a user-friendly frontend for managing `iptables`/`nftables` firewall rules on Ubuntu. For offensive security and networking, understanding UFW helps you see how hosts filter incoming and outgoing traffic.

---

## 1. Installation & Verification

### Update Ubuntu Packages
```bash
sudo apt update
```

### Install UFW
```bash
sudo apt install ufw -y
```

### Verify Installation & Current Status
```bash
ufw version
sudo ufw status verbose
```

---

## 2. Safe Initial Setup (Recommended)

> **⚠️ Important:** If you are connected to your Ubuntu machine via **SSH**, you **must** allow SSH connections *before* enabling the firewall, or you will lock yourself out.

### Allow SSH (Remote Access Only)
```bash
sudo ufw allow OpenSSH
```

### Set Default Policies & Enable UFW
For a standard machine that should block unsolicited inbound connections while allowing outbound traffic:
```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw enable
```

---

## 3. Useful UFW Commands

| Command | Purpose |
| :--- | :--- |
| `sudo ufw status` | Check basic firewall status |
| `sudo ufw status verbose` | Check detailed status and default policies |
| `sudo ufw status numbered` | Display active rules with index numbers |
| `sudo ufw enable` | Enable the firewall |
| `sudo ufw disable` | Disable the firewall |
| `sudo ufw reload` | Reload firewall rules without disconnecting |
| `sudo ufw reset` | Disable UFW and reset all rules to defaults |
| `sudo ufw allow 80/tcp` | Allow incoming HTTP traffic (Port 80) |
| `sudo ufw allow 443/tcp` | Allow incoming HTTPS traffic (Port 443) |
| `sudo ufw deny 8080/tcp` | Block incoming TCP traffic on Port 8080 |
| `sudo ufw delete allow 80/tcp` | Remove a specific rule by syntax |
| `sudo ufw delete <number>` | Remove a specific rule by its index number |

---

## 4. Offensive Security Context

When testing or auditing a Linux target:
* **Rule Enumeration:** Running `sudo ufw status verbose` reveals which ports are exposed and whether outbound traffic is restricted (egress filtering).
* **Log Inspection:** UFW logs blocked packets to `/var/log/ufw.log` (when logging is enabled via `sudo ufw logging on`), which helps you see how port scans (like `nmap`) appear to defenders.
