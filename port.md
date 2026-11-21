# Checking Active Ports & Investigating Services on Ubuntu

To check all active ports on Ubuntu, you can use several terminal commands. For offensive security and network diagnostics, these are the most useful.

---

## 1. Display all active listening ports

```bash
sudo ss -tulnp
```

This is the recommended command.

### Flag Breakdown

| Option | Meaning |
| :--- | :--- |
| `-t` | TCP ports |
| `-u` | UDP ports |
| `-l` | Listening ports |
| `-n` | Show numerical IP addresses and ports |
| `-p` | Show processes using ports |

---

## 2. Display all active connections

```bash
sudo ss -tunap
```

This shows:
* Established connections
* Listening ports
* Connections waiting to close
* TCP and UDP sockets
* Processes associated with connections

---

## 3. Check ports using netstat

If installed:
```bash
sudo netstat -tulnp
```

If not installed:
```bash
sudo apt install net-tools
```

---

## 4. Display only TCP listening ports

```bash
sudo ss -tlpn
```

---

## 5. Display only UDP listening ports

```bash
sudo ss -ulpn
```

---

## 6. Check which process is using a particular port

For example, port `8080`:

```bash
sudo lsof -i :8080
```

Or:
```bash
sudo fuser -v 8080/tcp
```

---

## 7. Display all ports with their processes using lsof

```bash
sudo lsof -i -P -n
```

---

## 8. Check whether a particular port is listening

For example, port `8080`:

```bash
sudo ss -lntp | grep ':8080'
```

---

## Important Distinction for Offensive Security

Understand these three concepts:

| Term | Meaning |
| :--- | :--- |
| **Open/listening port** | A service is waiting for connections. |
| **Established port** | An active connection exists. |
| **Closed port** | No service is listening on that port. |

---

## My Recommended Quick-Reference Commands

1. **All listening ports:**
   ```bash
   sudo ss -tulnp
   ```
2. **All active connections:**
   ```bash
   sudo ss -tunap
   ```
3. **All network processes:**
   ```bash
   sudo lsof -i -P -n
   ```

> **Security Researcher Tip:** Knowing which port is open is only the beginning. You should identify the service, its version, the process behind it, its configuration, and what network interfaces it listens on.

---

## Going Deeper: How to Investigate Everything Behind a Port

Once you spot an open port using `sudo ss -tulnp`, take the **PID** (Process ID) and **Local Address** from the output and run through this checklist in your authorized lab.

### Step 1: Check the Listening Interface (Exposure)
Look at the `Local Address:Port` column in `ss`:
* `127.0.0.1:8080` or `[::1]:8080` — Bound to **localhost only**. Only accessible from inside the machine (unless forwarded).
* `0.0.0.0:8080` or `*:8080` or `[::]:8080` — Bound to **all network interfaces**. Accessible externally if the firewall allows it.

### Step 2: Inspect the Exact Process & Command Line
Replace `<PID>` with the process ID you found:

* **See the full command and arguments used to start it:**
  ```bash
  ps -fp <PID>
  ```
* **Find the exact binary executable path on disk:**
  ```bash
  sudo ls -l /proc/<PID>/exe
  ```
* **Check the working directory and environment variables (often reveals config paths or secrets):**
  ```bash
  sudo ls -l /proc/<PID>/cwd
  sudo strings /proc/<PID>/environ
  ```

### Step 3: Check the Systemd Service & Configuration Files
If the process is managed by `systemd`, find its unit file and status:

```bash
systemctl status <PID>
```
Once you see the service name (e.g., `nginx.service`), inspect its unit file to locate its configuration files:
```bash
systemctl cat <service_name>
```
You can also list all open files and configuration files held by that process:
```bash
sudo lsof -p <PID>
```

### Step 4: Identify the Exact Software Version
Knowing the exact version helps you check for known CVEs or misconfigurations:

* **Using the binary directly:**
  ```bash
  /path/to/binary --version
  # or -v / -V depending on the program
  ```
* **Using Ubuntu's package manager (`dpkg`):**
  ```bash
  dpkg -S /path/to/binary
  dpkg -l | grep <package_name>
  ```

### Step 5: Banner Grabbing & Local Service Enumeration
Interact with the port locally to verify what protocol and banner it exposes:

* **Using Netcat (`nc`):**
  ```bash
  nc -vn 127.0.0.1 <PORT>
  ```
* **Using Nmap service/version detection locally:**
  ```bash
  sudo nmap -sV -sC -p <PORT> 127.0.0.1
  ```

### Step 6: Check Firewall Rules
Verify whether the host firewall is blocking or allowing external traffic to that port:
```bash
sudo ufw status verbose
# Or for raw iptables/nftables rules:
sudo iptables -L -n -v
```
