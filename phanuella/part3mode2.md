# Part 3 – Practical Security+ Laboratory Syllabus
## Module 2: Network Security Laboratory

> **Lab Environment:** Linux VM (Ubuntu/Kali) + Windows VM in VirtualBox, `nmap`, `tcpdump`, Wireshark, `dig`/`nslookup`, `nc` (Netcat), `ss`/`netstat`.  
> **Rules of Engagement Warning:** Only run active scans (`nmap`) and packet captures against `127.0.0.1` or your own isolated VirtualBox lab subnets (`192.168.x.x` / `10.x.x.x`).

---

### Lab 1: IP Address Identification (Private vs. Public & IPv4/IPv6)
* **Objective:** Identify local interface IPv4/IPv6 addresses, subnet masks, default gateways, MAC mappings, and external public NAT IP addresses.
* **Hands-On Steps:**
  ```bash
  # 1. Inspect local IPv4, IPv6, and MAC addresses on Linux (Windows: ipconfig /all)
  ip -brief addr show

  # 2. Inspect default gateway and kernel routing table (Windows: route print -4)
  ip route show

  # 3. Inspect local ARP table (IP-to-MAC mappings; look for duplicate MACs indicating ARP spoofing)
  arp -a

  # 4. Query your external Public WAN IP address
  curl -s https://ifconfig.me && echo ""
  ```

---

### Lab 2: Port Identification
* **Objective:** Audit locally bound listening ports (`0.0.0.0` vs. `127.0.0.1`) and scan an authorized target host for open TCP and UDP ports.
* **Hands-On Steps:**
  ```bash
  # 1. Audit all active listening TCP/UDP ports and bound PIDs on Linux (Windows: netstat -abno)
  sudo ss -tulnp

  # 2. Perform a TCP Connect scan (-sT) across top 100 common ports on localhost
  nmap -sT --top-ports 100 127.0.0.1

  # 3. Perform a targeted UDP port scan (-sU) on DNS (53) and DHCP/SNMP ports
  sudo nmap -sU -p 53,161 127.0.0.1
  ```

---

### Lab 3: Service Identification & Banner Grabbing
* **Objective:** Fingerprint exact service names, software versions, and TLS certificates running behind open ports to spot outdated or unencrypted services.
* **Hands-On Steps:**
  ```bash
  # 1. Run Nmap service & version detection (-sV) on localhost
  nmap -sV -p 22,80,443 127.0.0.1

  # 2. Perform manual HTTP banner grabbing using curl and Netcat (nc)
  curl -sI https://example.com | grep -iE "HTTP/|Server:|Strict-Transport-Security"

  # 3. Inspect TLS certificate subject, issuer, and expiration date on port 443
  echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -subject -issuer -dates
  ```

---

### Lab 4: Network Discovery (Host Enumeration)
* **Objective:** Discover live, active hosts on an isolated VirtualBox lab subnet using ICMP ping sweeps and ARP discovery to spot rogue or unmanaged devices.
* **Hands-On Steps:**
  ```bash
  # 1. Perform a host-discovery ping sweep (-sn, no port scan) across your local lab subnet
  # Replace 10.0.2.0/24 with your VirtualBox NAT/Host-Only subnet (check via 'ip -4 addr')
  nmap -sn 127.0.0.0/30

  # 2. View kernel neighbor discovery cache (NDP/ARP)
  ip neigh show
  ```

---

### Lab 5: Packet Inspection (`tcpdump` & Wireshark)
* **Objective:** Capture raw frames off the wire, save a `.pcap` forensic file, and filter packets in Wireshark to inspect cleartext credentials and anomalies.
* **Hands-On Steps:**
  ```bash
  mkdir -p ~/netsec_lab && cd ~/netsec_lab

  # 1. Capture 30 packets of DNS, ICMP, or HTTP traffic to a .pcap file
  sudo tcpdump -i any -nn -c 30 "icmp or port 53 or port 80" -w lab_capture.pcap

  # 2. Read and summarize the captured .pcap file in CLI
  tcpdump -nn -r lab_capture.pcap | head -n 15
  ```
  * **Wireshark GUI Analysis:** Open `lab_capture.pcap` in **Wireshark** and test these Security+ display filters:
    * `http.request.method == "POST"` $\rightarrow$ Exposes cleartext form submissions/passwords.
    * `arp.duplicate-address-detected` $\rightarrow$ Flags ARP spoofing / IP conflicts.
    * `dns.flags.rcode == 3` $\rightarrow$ Flags `NXDOMAIN` responses (indicator of DGA malware beaconing).

---

### Lab 6: DNS Investigation
* **Objective:** Query `A`, `AAAA`, `MX`, `TXT` (SPF/DMARC), and `NS` records, test DNSSEC validation flags, and detect DNS tunneling or cache poisoning indicators.
* **Hands-On Steps:**
  ```bash
  # 1. Query Mail Exchange (MX) and Name Server (NS) records
  dig example.com MX +short
  dig example.com NS +short

  # 2. Audit domain email security records (SPF & DMARC)
  dig google.com TXT +short | grep -i "v=spf1"
  dig _://google.com TXT +short

  # 3. Verify DNSSEC Authenticated Data (ad) flag using a DNSSEC-validating resolver (1.1.1.1)
  dig @1.1.1.1 cloudflare.com +dnssec | grep -E "flags:|RRSIG" | head -n 5
  ```

---

### Lab 7: TCP / UDP Analysis (3-Way Handshake & Connection States)
* **Objective:** Observe the TCP 3-Way Handshake (`SYN` $\rightarrow$ `SYN-ACK` $\rightarrow$ `ACK`), inspect socket states (`ESTABLISHED`, `TIME_WAIT`, `SYN_RECV`), and contrast connectionless UDP behavior.
* **Hands-On Steps:**
  ```bash
  # 1. View active TCP socket states (watch for excessive SYN_RECV indicating a SYN Flood DoS)
  ss -tan | awk '{print \$1}' | sort | uniq -c

  # 2. Start a local TCP listener in background, connect to it, and inspect the ESTABLISHED session
  nc -l 127.0.0.1 9444 &
  LISTENER_PID=\$!
  sleep 1
  echo "Testing TCP Stream" | nc -w 1 127.0.0.1 9444
  kill \$LISTENER_PID 2>/dev/null || true
  ```

---

### Lab 8: Firewall Testing (Rule Enforcement & Scan Verification)
* **Objective:** Configure stateful firewall rules (`ufw` / Windows Defender Firewall) and verify from an external/loopback scan that blocked ports report `filtered` rather than `open`.
* **Hands-On Steps:**
  ```bash
  # 1. Create a temporary test listener on TCP port 8888
  python3 -m http.server 8888 --bind 127.0.0.1 >/dev/null 2>&1 &
  WEB_PID=\$!

  # 2. Verify Nmap sees port 8888 as OPEN before firewall block
  nmap -p 8888 127.0.0.1 | grep 8888

  # 3. Apply firewall rule blocking port 8888, re-test, and clean up
  sudo ufw deny 8888/tcp 2>/dev/null || true
  sudo ufw delete deny 8888/tcp 2>/dev/null || true
  kill \$WEB_PID 2>/dev/null || true
  ```

---

### Lab 9: Network Segmentation (Isolated Subnets & ACLs)
* **Objective:** Build two isolated software-defined network segments (a **Public DMZ Subnet** and an **Internal Restricted Database Subnet**) and prove that direct external routing to the restricted subnet is blocked.
* **Hands-On Steps:**
  ```bash
  # 1. Create an external-capable DMZ network and an air-gapped (--internal) DB network in Docker
  docker network create --subnet=10.90.1.0/24 dmz_net
  docker network create --internal --subnet=10.90.2.0/24 restricted_db_net

  # 2. Verify a container inside restricted_db_net cannot reach the public Internet (8.8.8.8)
  docker run --rm --network restricted_db_net alpine:latest ping -c 2 8.8.8.8 || \
    echo "[PASS] Segmentation Verified: Restricted DB subnet is isolated from public Internet!"

  # 3. Clean up lab networks
  docker network rm dmz_net restricted_db_net
  ```

---

### Lab 10: Wireless Security Assessment
* **Objective:** Audit wireless interfaces, inspect surrounding Wi-Fi BSSIDs/channels/encryption protocols (`WPA2-CCMP` vs. `WPA3-SAE` vs. `Open`), and detect Evil Twin / weak encryption risks.
* **Hands-On Steps:**
  * **Linux:**
    ```bash
    # List nearby SSIDs, BSSIDs (AP MAC addresses), Channels, Signal Strength, and Security Protocols
    nmcli -f SSID,BSSID,CHAN,SIGNAL,SECURITY dev wifi list 2>/dev/null || echo "Run on wireless-enabled host"
    ```
  * **Windows (CMD):**
    ```cmd
    netsh wlan show interfaces
    netsh wlan show networks mode=bssid
    ```
  * **Assessment Checklist:**
    1. Flag any network broadcasting `WEP`, `TKIP`, or `Open` (unencrypted) authentication.
    2. Check for **Evil Twin** indicators: two different BSSIDs (MAC addresses) broadcasting the exact same corporate SSID on unusual channels with mismatched security modes.

---

### Module 2 Lab Completion Checklist
- [ ] Identified local IPv4/IPv6 addresses, routing tables (`ip route`), ARP caches (`arp -a`), and public WAN IP.
- [ ] Audited listening sockets (`ss -tulnp`) and executed TCP/UDP port & version scans (`nmap -sT -sV`, `nmap -sU`).
- [ ] Captured live packets with `tcpdump` (`.pcap`) and analyzed TCP streams and DNS queries in **Wireshark**.
- [ ] Audited live **SPF, DMARC, and DNSSEC** records using `dig`.
- [ ] Verified **Network Segmentation** isolation (`--internal` subnet) and audited **Wireless BSSID / WPA2 / WPA3** security profiles.
