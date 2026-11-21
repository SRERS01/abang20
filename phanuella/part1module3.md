# Part 1 – Foundations Before Security+
## Module 3: Networking Fundamentals (Practical Lab Guide)

> **Objective:** Build practical, packet-level fluency in how data moves across networks, how devices address and route traffic, and how network boundaries are secured before entering Security+ domains.  
> **Recommended Lab Tools:** Terminal/CMD/PowerShell, Python 3, Wireshark (or `tcpdump`), `nmap`, Cisco Packet Tracer / GNS3 (optional for VLANs/Switching).

---

### 1. What is a Computer Network?
* **Concept:** Two or more interconnected nodes sharing data and resources over wired or wireless media using agreed-upon protocols.
* **Practical Task:**
  1. Test basic host-to-host connectivity using ICMP (`ping`) and measure round-trip latency:
     ```bash
     ping -c 4 8.8.8.8       # Linux/macOS (Use 'ping -n 4 8.8.8.8' on Windows)
     ```

### 2. LAN, WAN, MAN, and PAN
* **Concept:** Networks categorized by geographic scope: **PAN** (Bluetooth/personal devices), **LAN** (home/office local network), **MAN** (city-wide), **WAN** (global/Internet).
* **Practical Task:**
  1. Identify your local LAN adapter vs. external WAN route:
     * **Linux/macOS:** `ip a` (or `ifconfig`) to see local interfaces (`eth0`/`wlan0`) and loopback (`lo`).
     * **Windows:** `ipconfig /all`

### 3. Network Topologies
* **Concept:** Physical and logical layout of nodes (Star, Mesh, Bus, Ring, Hybrid). Modern LANs use Star/Extended Star; core WANs and enterprise Wi-Fi use Mesh.
* **Practical Task:**
  1. Map the logical path (hops) from your host to an external server to visualize point-to-point routing topology:
     * **Linux/macOS:** `traceroute 1.1.1.1`
     * **Windows:** `tracert 1.1.1.1`

### 4. OSI Model (7 Layers)
* **Concept:** Conceptual framework dividing network communication into 7 layers: **7. Application, 6. Presentation, 5. Session, 4. Transport, 3. Network, 2. Data Link, 1. Physical**.
* **Practical Task:**
  1. Verify layers bottom-up on your machine:
     * **Layer 1 (Physical):** Check link carrier state (`ethtool eth0` on Linux or check Ethernet/Wi-Fi link status).
     * **Layer 2 (Data Link):** View MAC address (`ip link`).
     * **Layer 3 (Network):** View IP address (`ip -4 addr`).
     * **Layer 4 (Transport):** View open TCP/UDP sockets (`ss -tuln` or `netstat -ano`).
     * **Layer 7 (Application):** Fetch HTTP headers (`curl -I https://example.com`).

### 5. TCP/IP Model (4 Layers)
* **Concept:** The practical implementation model used by the Internet: **Network Interface (Link), Internet, Transport, Application**.
* **Practical Task:**
  1. Capture a live HTTP request in **Wireshark** (or `tcpdump`) and expand the packet details pane to inspect the real-world encapsulation stack: `Frame (Link) -> IPv4 (Internet) -> TCP (Transport) -> HTTP (Application)`.

### 6. Ethernet
* **Concept:** The standard wired LAN protocol (IEEE 802.3) defining framing, cabling (Cat5e/Cat6/Fiber), and speed/duplex signaling.
* **Practical Task:**
  1. Check interface speed, duplex mode, and frame error counters:
     * **Linux:** `ip -s link show` (inspect `RX/TX` dropped/error packet counts).
     * **Windows (PowerShell):** `Get-NetAdapter | Select-Object Name, Status, LinkSpeed, FullDuplex`

### 7. MAC Addresses
* **Concept:** A 48-bit (6-byte) hexadecimal hardware address burned into a NIC (e.g., `00:1A:2B:3C:4D:5E`), where the first 24 bits represent the **OUI** (vendor) and the last 24 bits are unique to the device.
* **Practical Task:**
  1. Extract your NIC's MAC address and identify the vendor prefix (first 3 octets):
     * **Linux:** `ip link show | grep link/ether`
     * **Windows:** `getmac /v`

### 8. IPv4 Addressing
* **Concept:** 32-bit logical addresses written in dotted-decimal format (4 octets, `0–255` each), divided into a Network portion and a Host portion.
* **Practical Task:**
  1. Inspect your IPv4 address and subnet mask:
     * **Linux:** `ip -4 addr show`
     * **Windows:** `ipconfig | findstr /i "IPv4 Subnet"`

### 9. IPv6 Addressing
* **Concept:** 128-bit hexadecimal addresses (8 groups of 4 hex digits) designed to replace IPv4, featuring link-local (`fe80::/10`) and global unicast (`2000::/3`) addresses.
* **Practical Task:**
  1. Inspect your IPv6 link-local address and ping the IPv6 loopback (`::1`):
     ```bash
     ip -6 addr show         # Linux (Use 'ipconfig' on Windows)
     ping -6 ::1             # Tests local IPv6 stack
     ```

### 10. Public and Private IP Addresses
* **Concept:** RFC 1918 defines non-routable private ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`) for internal LANs, while Public IPs are globally routable on the Internet.
* **Practical Task:**
  1. Compare your internal private IP against your external public WAN IP:
     ```bash
     curl -s https://ifconfig.me && echo ""   # Displays your Public IP
     ```

### 11. Subnetting
* **Concept:** Dividing a larger IP network into smaller logical sub-networks to improve performance and security isolation.
* **Practical Task:**
  1. Use Python's built-in `ipaddress` module to calculate network ID, broadcast address, and usable host count for `192.168.10.0/26`:
     ```python
     import ipaddress
     net = ipaddress.IPv4Network("192.168.10.0/26")
     print("Network Address :", net.network_address)
     print("Broadcast Addr  :", net.broadcast_address)
     print("Usable Hosts    :", net.num_addresses - 2)
     ```

### 12. CIDR (Classless Inter-Domain Routing)
* **Concept:** Replaces legacy Class A/B/C boundaries with slash notation (e.g., `/24` = `255.255.255.0`), indicating how many leading bits belong to the network mask.
* **Practical Task:**
  1. Convert CIDR prefix lengths (`/8`, `/16`, `/24`, `/27`, `/30`) into dotted-decimal subnet masks in Python:
     ```python
     import ipaddress
     for prefix in:
         net = ipaddress.IPv4Network(f"10.0.0.0/{prefix}")
         print(f"/{prefix} -> Netmask: {net.netmask} | Usable IPs: {max(0, net.num_addresses - 2)}")
     ```

### 13. Default Gateways
* **Concept:** The local router IP address where a host sends packets destined for external networks outside its local subnet.
* **Practical Task:**
  1. Identify your system's Default Gateway:
     * **Linux:** `ip route | grep default`
     * **Windows:** `ipconfig | findstr /i "Default Gateway"`

### 14. Routing
* **Concept:** Forwarding packets across different IP networks using routing tables (Static routes or Dynamic protocols like OSPF/BGP).
* **Practical Task:**
  1. View your OS kernel's local routing table:
     * **Linux:** `ip route show`
     * **Windows:** `route print -4`

### 15. Switching
* **Concept:** Layer 2 forwarding within a LAN using MAC address tables (CAM tables) to send frames directly to the destination switch port rather than flooding all ports.
* **Practical Task:**
  1. **Simulation (Cisco Packet Tracer) or Concept Lab:** Connect two PCs to a switch, ping between them, and run `show mac address-table` on the switch CLI to observe dynamic MAC learning.

### 16. VLANs (Virtual Local Area Networks)
* **Concept:** Logically segmenting a single physical switch into multiple isolated broadcast domains (IEEE 802.1Q tagging) to separate traffic (e.g., Guest Wi-Fi vs. Corporate Servers).
* **Practical Task:**
  1. Inspect VLAN tagging (`802.1Q`) fields inside a Wireshark sample capture, or configure a sub-interface on Linux:
     ```bash
     # View 802.1Q VLAN kernel support on Linux
     lsmod | grep 8021q
     ```

### 17. ARP (Address Resolution Protocol)
* **Concept:** Resolves a known Layer 3 IPv4 address into an unknown Layer 2 MAC address on a local LAN. Vulnerable to **ARP Spoofing/Poisoning** (MitM attacks).
* **Practical Task:**
  1. View your system's local ARP cache (IP-to-MAC mappings):
     ```bash
     arp -a                  # Works on Windows, Linux, and macOS
     ```

### 18. DHCP (Dynamic Host Configuration Protocol)
* **Concept:** Automatically leases IP addresses, subnet masks, default gateways, and DNS servers to clients using the 4-step **DORA** process (Discover, Offer, Request, Acknowledge) over UDP ports `67/68`.
* **Practical Task:**
  1. Inspect your current DHCP lease details and DHCP server IP:
     * **Windows:** `ipconfig /all | findstr /i "DHCP"`
     * **Linux:** `grep -i "dhcp" /var/log/syslog 2>/dev/null || journalctl -u NetworkManager | grep -i dhcp | tail -n 10`

### 19. DNS (Domain Name System)
* **Concept:** Translates human-readable domain names (e.g., `comptia.org`) into IP addresses using record types (`A`, `AAAA`, `MX`, `CNAME`, `TXT`) over UDP/TCP port `53`.
* **Practical Task:**
  1. Query DNS records and trace resolution:
     ```bash
     nslookup -type=A example.com
     nslookup -type=MX gmail.com
     ```
     *(On Linux/macOS, also test `dig example.com +short`)*

### 20. NAT and PAT
* **Concept:** **NAT** translates private internal IPs to public IPs; **PAT (Port Address Translation)** maps thousands of private internal devices to a *single* public IP by tracking unique source port numbers.
* **Practical Task:**
  1. Run `ss -tn` (Linux) or `netstat -ano` (Windows) while browsing a website. Observe how your OS assigns high **ephemeral source ports** (e.g., `51422`) to distinguish your session when translated by your router's PAT table.

### 21. TCP and UDP
* **Concept:** **TCP** is connection-oriented, reliable, and uses a 3-way handshake (`SYN -> SYN-ACK -> ACK`). **UDP** is connectionless, low-latency, and best-effort (used for DNS, streaming, VoIP).
* **Practical Task:**
  1. Start a local TCP listener on port `9999` in one terminal and connect to it from another to observe a live TCP session:
     * **Terminal 1 (Listener):** `nc -lvnp 9999` (Linux/macOS) or Python socket listener.
     * **Terminal 2 (Client):** `nc 127.0.0.1 9999`

### 22. Ports and Protocols
### 22. Ports and Protocols
* **Concept:** Logical endpoints (`0–65535`) categorized into **Well-Known Ports (`0–1023`)**, **Registered Ports (`1024–49151`)**, and **Dynamic/Ephemeral Ports (`49152–65535`)**. Security+ requires instant recognition of insecure cleartext protocols (`21` FTP, `23` Telnet, `80` HTTP) vs. secure encrypted alternatives (`22` SSH/SFTP, `443` HTTPS, `993` IMAPS).
* **Practical Task 1 (Audit Listening Ports & Associated Processes):**
  * **Linux:**
    ```bash
    sudo ss -tulnp
    ```
  * **Windows (CMD / PowerShell):**
    ```cmd
    netstat -abno | findstr LISTENING
    ```
* **Practical Task 2 (Banner Grabbing & Service Verification):**
  Use `nc` (Netcat) or `curl` to connect directly to a service port and read its banner:
  ```bash
  curl -I http://example.com
  nc -zv scanme.nmap.org 22 80 443
  ```

---

### 23. Wireless Networking
* **Concept:** IEEE **802.11** standards (`802.11ac` / Wi-Fi 5, `802.11ax` / Wi-Fi 6, `802.11be` / Wi-Fi 7) operating across `2.4 GHz` (longer range, 3 non-overlapping channels: 1, 6, 11), `5 GHz` (faster, shorter range), and `6 GHz` bands using **CSMA/CA** (Carrier Sense Multiple Access with Collision Avoidance).
* **Practical Task (Inspect Wireless Adapter, Channel, Band & Signal):**
  * **Windows (CMD):**
    ```cmd
    netsh wlan show interfaces
    netsh wlan show networks mode=bssid
    ```
  * **Linux:**
    ```bash
    nmcli dev wifi list
    iw dev wlan0 link 2>/dev/null || iwconfig
    ```

---

### 24. Wi-Fi Security
* **Concept:** Securing wireless frames against eavesdropping and Evil Twin / deauthentication attacks:
  * **Legacy/Broken:** WEP, WPA, WPA2-TKIP (vulnerable to cracking).
  * **Secure Personal:** **WPA2-PSK (AES-CCMP)** and **WPA3-SAE** (Simultaneous Authentication of Equals — protects against offline dictionary attacks and adds Protected Management Frames).
  * **Secure Enterprise:** **WPA2/WPA3-Enterprise** using **802.1X** and a **RADIUS** authentication server.
* **Practical Task (Audit Saved Wireless Profiles & Encryption Types):**
  * **Windows (CMD):**
    ```cmd
    netsh wlan show profiles
    netsh wlan show profile name="<YOUR_WIFI_SSID>" key=clear | findstr /i "Authentication Cipher"
    ```
  * **Linux:**
    ```bash
    sudo grep -E "ssid=|key-mgmt=|pairwise=" /etc/NetworkManager/system-connections/* 2>/dev/null
    ```

---

### 25. Network Segmentation
* **Concept:** Dividing a network into isolated security zones (e.g., **DMZ / Screened Subnet** for public-facing web servers, **Internal Corporate LAN**, **Guest Wi-Fi**, and **Restricted PCI/Database VLANs**) to enforce Least Privilege and prevent lateral movement after a breach.
* **Practical Task (Build an Isolated Lab Segment in VirtualBox):**
  1. Open **VirtualBox** $\rightarrow$ Select two VMs (e.g., Ubuntu Server + Kali/Client VM) $\rightarrow$ **Settings** $\rightarrow$ **Network**.
  2. Set **Adapter 1** on both VMs to **Internal Network** and name it `isolated_corp_lan`.
  3. Assign static IPs on the same subnet (`10.50.0.10/24` and `10.50.0.20/24`) with **no default gateway**.
  4. Verify the two VMs can `ping` each other, while neither can reach the public Internet (`8.8.8.8`) or your host machine—simulating a true air-gapped/segmented VLAN.

---

### 26. Firewalls
* **Concept:** Enforces access control policies between network zones:
  * **Stateless Packet Filter:** Inspects individual packet headers (Source/Dest IP, Port, Protocol) without tracking session state.
  * **Stateful Inspection Firewall:** Tracks active TCP/UDP sessions in a state table and automatically permits return traffic for approved outbound connections.
  * **NGFW (Next-Generation Firewall):** Inspects Layer 7 applications, integrates IPS, and performs TLS decryption.
* **Practical Task (Configure Stateful Rules & Test Implicit Deny):**
  * **Linux (`ufw`):**
    ```bash
    sudo ufw default deny incoming
    sudo ufw default allow outgoing
    sudo ufw allow from 192.168.1.0/24 to any port 22 proto tcp
    sudo ufw deny 23/tcp
    sudo ufw status verbose
    ```
  * **Windows (PowerShell):**
    ```powershell
    New-NetFirewallRule -DisplayName "Lab-Block-Telnet" -Direction Inbound -LocalPort 23 -Protocol TCP -Action Block
    Get-NetFirewallRule -DisplayName "Lab-Block-Telnet" | Select-Object DisplayName, Enabled, Action
    # Cleanup rule after testing:
    Remove-NetFirewallRule -DisplayName "Lab-Block-Telnet"
    ```

---

### 27. Proxies
* **Concept:** An intermediary server separating endpoints from destinations:
  * **Forward Proxy:** Sits in front of internal clients; filters outbound web browsing, blocks malicious domains, caches content, and hides client IPs.
  * **Reverse Proxy:** Sits in front of backend web servers (e.g., Nginx, Cloudflare); provides load balancing, WAF filtering, and SSL/TLS termination.
* **Practical Task (Inspect Proxy Settings & Trace HTTP Headers):**
  1. Check if a system proxy is configured:
     * **Linux/macOS:** `env | grep -i "_proxy"`
     * **Windows (CMD):** `netsh winhttp show proxy`
  2. Send an HTTP request and inspect server/reverse-proxy headers (`Server`, `Via`, `X-Cache`, `CF-Ray`):
     ```bash
     curl -sI https://cloudflare.com | grep -iE "server:|cf-ray:|cache"
     ```

---

### 28. VPNs (Virtual Private Networks)
* **Concept:** Establishes an encrypted tunnel across an untrusted network (such as public Wi-Fi or the Internet) to protect **Confidentiality** and **Integrity**:
  * **IPsec (IKEv2 / ESP):** Operates at Layer 3; used heavily for Site-to-Site and Remote Access VPNs.
  * **TLS/SSL VPN (OpenVPN) & WireGuard:** Operates over standard UDP/TCP ports (`443` or `51820`), making it easy to traverse restrictive firewalls.
  * **Split Tunneling vs. Full Tunneling:** Split tunneling routes only corporate traffic through the VPN; full tunneling routes *all* traffic through the VPN for maximum security inspection.
* **Practical Task (Inspect Virtual Tunnel Interfaces & Routing Changes):**
  1. When connected to any VPN client (or WireGuard/OpenVPN lab), compare your routing table and interfaces before and after connecting:
     * **Linux:**
       ```bash
       ip addr show | grep -E "tun|wg|ppp"
       ip route show
       ```
     * **Windows (PowerShell):**
       ```powershell
       Get-NetAdapter | Where-Object {\$_.InterfaceDescription -match "TAP|TUN|WireGuard|VPN"}
       ```

---

### 29. Network Troubleshooting
* **Concept:** Resolving network outages methodically from **Layer 1 (Physical)** up to **Layer 7 (Application)** rather than guessing.
* **Practical Task (Execute the 6-Layer Diagnostic Runbook):**
  Run this exact sequence whenever diagnosing a broken network connection:
  ```bash
  # 1. Layer 1/2 - Is the network interface UP with a valid MAC & link?
  ip link show                     # Windows: netsh interface show interface

  # 2. Layer 3 (Local) - Does the host have a valid IP (not 169.254.x.x APIPA)?
  ip -4 addr show                  # Windows: ipconfig

  # 3. Layer 3 (Gateway) - Can we reach the Default Gateway?
  ping -c 2 <DEFAULT_GATEWAY_IP>

  # 4. Layer 3 (WAN) - Can we route outside our LAN to the Internet?
  ping -c 2 1.1.1.1

  # 5. Layer 7 (DNS) - Is name resolution working?
  nslookup comptia.org 1.1.1.1

  # 6. Layer 4/7 (Port/Service) - Is the target application port open and not blocked by a firewall?
  nc -zv comptia.org 443           # Windows PowerShell: Test-NetConnection comptia.org -Port 443
  ```

---

### 30. Packet Analysis
* **Concept:** Capturing raw frames off a NIC in **promiscuous mode** using **Wireshark** or **`tcpdump`** to analyze protocol handshakes, spot cleartext credentials (HTTP/FTP/Telnet), detect ARP spoofing, and investigate malware Command-and-Control (C2) traffic.
* **Practical Task 1 (CLI Packet Capture with `tcpdump`):**
  Capture 25 packets of DNS (`port 53`) and ICMP traffic without resolving hostnames (`-nn`), and save to a `.pcap` file for Wireshark analysis:
  ```bash
  sudo tcpdump -i any -nn -c 25 "icmp or port 53" -w module3_lab.pcap
  ```
* **Practical Task 2 (Wireshark Display Filter & Stream Reconstruction):**
  1. Open `module3_lab.pcap` in **Wireshark** (or start a live capture on your active interface).
  2. Test these essential Security+ Wireshark Display Filters:
     * `tcp.flags.syn == 1 && tcp.flags.ack == 0` $\rightarrow$ Finds new TCP connection initiations (useful for spotting SYN port scans).
     * `dns.qry.name contains "google"` $\rightarrow$ Filters specific DNS domain lookups.
     * `http.request.method == "POST"` $\rightarrow$ Isolates HTTP form submissions (reveals cleartext passwords on unencrypted sites).
     * `arp.duplicate-address-detected` $\rightarrow$ Detects potential ARP spoofing / IP conflicts.
  3. Right-click any TCP packet $\rightarrow$ **Follow** $\rightarrow$ **TCP Stream** to reconstruct the human-readable conversation between client and server.

---

### Module 3 Completion Checklist
- [ ] Audited open TCP/UDP ports (`ss -tulnp` / `netstat -abno`) and verified service banners.
- [ ] Inspected wireless interface radio bands, channels, and WPA2/WPA3 security profiles.
- [ ] Built an isolated **Internal Network** segment in VirtualBox to test network segmentation.
- [ ] Configured and verified stateful host firewall rules (`ufw` / Windows Defender Firewall).
- [ ] Executed the 6-layer network troubleshooting runbook from physical link to DNS/port check.
- [ ] Captured a `.pcap` file with `tcpdump` and inspected TCP streams in **Wireshark**.
