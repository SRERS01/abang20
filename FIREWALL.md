# Linux Firewall Command Reference for Ubuntu

Below is a comprehensive Linux firewall command reference for Ubuntu, covering **UFW**, **iptables**, **nftables**, and **firewall diagnostics**.

These are the main tools you should understand as an offensive security researcher and system administrator.

---

## 1. UFW Commands (Ubuntu Firewall)

UFW means **Uncomplicated Firewall**. It is a frontend for managing Linux firewall rules.

### Installation and Status

```bash
sudo apt update
sudo apt install ufw -y

sudo ufw status
sudo ufw status verbose
sudo ufw status numbered
sudo ufw version
```

### Enable and Disable

```bash
sudo ufw enable
sudo ufw disable
sudo ufw reload
sudo ufw reset
```

> **Be careful:** Enabling or resetting a firewall over SSH can disconnect you. Allow SSH first if you need remote access.

### Default Policies

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw default deny routed
```

### Allow Traffic

```bash
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443

sudo ufw allow 22/tcp
sudo ufw allow 53/udp
sudo ufw allow 53/tcp

sudo ufw allow OpenSSH
sudo ufw allow http
sudo ufw allow https
```

### Deny Traffic

```bash
sudo ufw deny 22
sudo ufw deny 80/tcp
sudo ufw deny 443/tcp
sudo ufw deny 53/udp
```

### Reject Traffic

```bash
sudo ufw reject 22/tcp
sudo ufw reject 80/tcp
sudo ufw reject 443/tcp
```

### Delete Rules

```bash
sudo ufw delete allow 80
sudo ufw delete deny 443/tcp

sudo ufw status numbered
sudo ufw delete 2
```

### Allow or Deny Specific IP Addresses

```bash
sudo ufw allow from 192.168.1.10
sudo ufw deny from 192.168.1.20

sudo ufw allow from 192.168.1.10 to any port 22
sudo ufw deny from 192.168.1.20 to any port 22
```

### Allow or Deny Subnets

```bash
sudo ufw allow from 192.168.1.0/24
sudo ufw deny from 192.168.2.0/24
```

### Interface-Specific Rules

```bash
sudo ufw allow in on eth0 to any port 443
sudo ufw deny in on eth0 to any port 22
sudo ufw allow out on eth0 to any port 53
```

### Logging

```bash
sudo ufw logging on
sudo ufw logging off
sudo ufw logging low
sudo ufw logging medium
sudo ufw logging high
```

---

## 2. iptables Commands

`iptables` directly manages firewall rules through Linux Netfilter.

### Display Rules

```bash
sudo iptables -L
sudo iptables -L -n
sudo iptables -L -v
sudo iptables -L -n -v
sudo iptables -L --line-numbers
sudo iptables -S
sudo iptables -t nat -L -n -v
sudo iptables -t mangle -L -n -v
```

### Main Tables

| Table | Purpose |
| :--- | :--- |
| `filter` | Traffic filtering |
| `nat` | Network address translation |
| `mangle` | Packet modification |
| `raw` | Connection tracking exemptions |
| `security` | Security-related rules |

### Main Chains

| Chain | Purpose |
| :--- | :--- |
| `INPUT` | Traffic arriving at the machine |
| `OUTPUT` | Traffic leaving the machine |
| `FORWARD` | Traffic passing through the machine |
| `PREROUTING` | Processing before routing |
| `POSTROUTING` | Processing after routing |

### Basic Firewall Actions

```bash
sudo iptables -A INPUT -j ACCEPT
sudo iptables -A INPUT -j DROP
sudo iptables -A INPUT -j REJECT

sudo iptables -A OUTPUT -j ACCEPT
sudo iptables -A FORWARD -j DROP
```

> **Warning:** These examples append broad rules. Do not run them indiscriminately on a production system.

### Allow Specific Ports

```bash
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

### Block Specific Ports

```bash
sudo iptables -A INPUT -p tcp --dport 23 -j DROP
sudo iptables -A INPUT -p tcp --dport 445 -j DROP
```

### Match Source IP Addresses

```bash
sudo iptables -A INPUT -s 192.168.1.10 -j ACCEPT
sudo iptables -A INPUT -s 192.168.1.20 -j DROP
```

### Match Protocols

```bash
sudo iptables -A INPUT -p tcp -j ACCEPT
sudo iptables -A INPUT -p udp -j ACCEPT
sudo iptables -A INPUT -p icmp -j ACCEPT
```

### Connection-State Tracking

```bash
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A INPUT -m conntrack --ctstate INVALID -j DROP
```

### Delete and Flush Rules

```bash
sudo iptables -D INPUT 1
sudo iptables -F
sudo iptables -X
sudo iptables -Z
```

* `-D`: Delete a rule.
* `-F`: Flush rules.
* `-X`: Delete user-defined chains.
* `-Z`: Reset counters.

### Save and Restore

```bash
sudo iptables-save
sudo iptables-save > firewall-backup.rules
sudo iptables-restore < firewall-backup.rules
```

---

## 3. nftables Commands

`nftables` is the modern Linux packet-filtering framework.

### Installation

```bash
sudo apt install nftables -y
```

### Inspect Firewall

```bash
sudo nft list ruleset
sudo nft list tables
sudo nft list chains
sudo nft list rules
sudo nft -a list ruleset
```

### Manage Tables

```bash
sudo nft add table inet myfirewall
sudo nft list table inet myfirewall
sudo nft delete table inet myfirewall
```

### Manage Chains

```bash
sudo nft add chain inet myfirewall input
sudo nft list chain inet myfirewall input
```

### Add a Basic Input Chain

```bash
sudo nft add chain inet myfirewall input '{ type filter hook input priority 0; policy drop; }'
```

### Add Rules

```bash
sudo nft add rule inet myfirewall input tcp dport 22 accept
sudo nft add rule inet myfirewall input tcp dport 80 accept
sudo nft add rule inet myfirewall input tcp dport 443 accept

sudo nft add rule inet myfirewall input ip protocol icmp accept
```

### Drop Traffic

```bash
sudo nft add rule inet myfirewall input tcp dport 23 drop
```

### Delete Rules

```bash
sudo nft -a list chain inet myfirewall input
sudo nft delete rule inet myfirewall input handle 5
```

> The handle number must come from your actual rule listing.

### Flush Ruleset

```bash
sudo nft flush ruleset
```

> **Warning:** This removes the entire `nftables` ruleset. Do not use it on a system whose firewall you need to preserve.

---

## 4. Firewall Inspection and Diagnostic Commands

These are particularly useful for security research.

| Command | What it reveals |
| :--- | :--- |
| `sudo ss -tulnp` | Listening TCP/UDP sockets |
| `sudo ss -tunap` | Connections and sockets |
| `sudo lsof -i -P -n` | Network activity by process |
| `sudo iptables -L -n -v` | `iptables` rules and counters |
| `sudo nft list ruleset` | `nftables` configuration |
| `sudo ufw status verbose` | UFW policy |
| `sudo journalctl -k` | Kernel logs |
| `sudo dmesg` | Kernel messages |
| `sudo tcpdump -ni any` | Network packet capture |
| `sudo conntrack -L` | Tracked connections (if installed) |

---

## 5. Firewall Concepts You Must Master

| Concept | Meaning |
| :--- | :--- |
| `ACCEPT` | Permit matching traffic |
| `DROP` | Silently discard matching traffic |
| `REJECT` | Discard and return an error |
| `LOG` | Record matching traffic |
| `RETURN` | Return to the calling chain |
| `QUEUE` | Send packets to userspace |
| **Policy** | Default chain decision |
| **Rule** | Condition and resulting action |
| **Chain** | Ordered collection of rules |
| **Table** | Groups chains and related rules |
| **Stateful filtering** | Tracks connection states |
| **Stateless filtering** | Evaluates packets individually |
| **NAT** | Translates network addresses |
| **DNAT** | Changes destination address |
| **SNAT** | Changes source address |
| **MASQUERADE** | Dynamic source NAT |

---

## 6. Practical Learning Sequence

I recommend studying these in this order:

1. **UFW**
   * Learn to configure, inspect, allow, deny, and delete firewall rules quickly for day-to-day Ubuntu administration.
2. **Diagnostics & Inspection**
   * Master `ss`, `tcpdump`, `conntrack`, and kernel logs to verify how rules behave in real time and spot blocked or unexpected traffic.
3. **iptables**
   * Understand Netfilter tables, chains, packet flow, stateful connection tracking, and NAT rules—essential for legacy systems and Docker/container networking.
4. **nftables**
   * Transition to the modern Linux kernel packet-filtering syntax, unified `inet` family tables, and handle-based rule management.
