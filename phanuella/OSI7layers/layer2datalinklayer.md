## Layer 2: Data Link Layer (Frames & MAC Addresses)

The Data Link Layer handles node-to-node data transfer across a single local network segment (LAN). It packages raw bits from Layer 1 into **frames**, uses **MAC (Media Access Control) addresses** for hardware identification, and detects physical transmission errors.

### Environment Differences: Ubuntu vs. Termux
* **Ubuntu:** Full access to Layer 2 raw sockets (`sudo`), enabling ARP scanning, MAC spoofing, VLAN tagging, and packet injection.
* **Termux:** Non-rooted Android blocks raw Layer 2 frame crafting and promiscuous mode (`AF_PACKET`). You can view your local ARP cache (`ip neigh`) and capture packets only if the device is rooted.

---

### Core Layer 2 Protocols & Testing Tools

| Protocol / Standard | Full Name & Role | Security Auditing Focus | Testing Tools (Ubuntu & Termux) |
| :--- | :--- | :--- | :--- |
| **Ethernet (IEEE 802.3)** | Wired LAN framing standard using 48-bit MAC addresses. | MAC flooding (CAM table overflow), MAC spoofing to bypass port security, and sniffing cleartext LAN traffic. | `tcpdump`, `wireshark`, `macchanger` (Ubuntu root), `ip link` |
| **Wi-Fi (IEEE 802.11)** | Wireless LAN framing, association, and encryption (WPA2/WPA3). | Evil Twin APs, deauthentication frames, weak WPA2 handshakes, and WPS PIN vulnerabilities. | `aircrack-ng`, `iw`, `iwconfig`, `kismet` (Ubuntu with monitor-mode adapter) |
| **ARP** | Address Resolution Protocol (maps IPv4 addresses to MAC addresses). | **ARP Spoofing / Poisoning** (Man-in-the-Middle) due to ARP's stateless, unauthenticated trust model. | `arp-scan`, `arpspoof` (`dsniff`), `bettercap`, `ip neigh` |
| **STP** | Spanning Tree Protocol (IEEE 802.1D) — prevents switching loops. | **STP Root Bridge Hijacking**—sending spoofed BPDUs to become the root bridge and intercept switch traffic. | `yersinia`, `wireshark`, `scapy` (Ubuntu root) |
| **VLAN (IEEE 802.1Q)** | Virtual LAN tagging — isolates broadcast domains on switches. | **VLAN Hopping** (Switch Spoofing via DTP or Double Tagging) to pivot between isolated network segments. | `yersinia`, `scapy`, `vconfig` / `ip link` (Ubuntu root) |
| **CDP / LLDP** | Cisco Discovery Protocol / Link Layer Discovery Protocol. | **Information Disclosure**—switches broadcast device models, firmware versions, management IPs, and native VLAN IDs in cleartext. | `tcpdump`, `wireshark`, `cdpr`, `lldpctl` |
| **PPP / PPPoE** | Point-to-Point Protocol (over Ethernet) — direct link encapsulation. | Weak authentication protocols (PAP cleartext passwords or MS-CHAPv2 cracking) on ISP/DSL links. | `pppoe-discovery`, `wireshark`, `asleap` |

---

### Practical Layer 2 Auditing Commands (Ubuntu)

```bash
# 1. Discover all active hosts and MAC addresses on the local subnet via ARP
sudo arp-scan --localnet

# 2. View the local ARP neighbor table (works on both Ubuntu & non-rooted Termux)
ip neigh show

# 3. Sniff CDP and LLDP discovery broadcasts to leak switch models, IPs, and VLANs
sudo tcpdump -nn -v -i eth0 -s 1500 'ether[20:2] == 0x2000 or ether proto 0x88cc'

# 4. Inspect or spoof a MAC address on Ubuntu (requires root)
sudo ip link set dev eth0 down
sudo macchanger -r eth0
sudo ip link set dev eth0 up

# 5. Capture raw Layer 2 Ethernet frames with MAC headers visible
sudo tcpdump -e -i eth0 -c 20
```

---

### Layer 2 -> Web Security Connection
* **ARP & WPAD MITM:** Poisoning Layer 2 ARP tables on a local network allows an auditor to intercept unencrypted HTTP traffic, perform SSL stripping, or inject malicious JavaScript into web pages loaded by local victims.
* **CDP/LLDP Switch Leaks:** Capturing Layer 2 discovery frames often reveals the exact IP address and firmware version of the switch's **web management interface** (`http://<switch-mgmt-ip>`).
