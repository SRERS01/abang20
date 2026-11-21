# Offensive Security Tools & Usage Across the 7 OSI Layers (Ubuntu)

> **Disclaimer:** Network protocols are communication rules rather than standalone software, so you install offensive tools designed to interact with each layer. Only use these tools on networks and systems you own or have explicit written permission to test.

---

## Quick Reference Summary

| OSI Layer | Primary Offensive Goal | Key Ubuntu Packages |
| :--- | :--- | :--- |
| **7. Application** | Service & web exploitation, brute-forcing | `nmap`, `gobuster`, `hydra`, `sqlmap` |
| **6. Presentation** | TLS/SSL auditing, cipher & encoding checks | `sslscan`, `testssl.sh`, `openssl` |
| **5. Session** | SMB/RPC enumeration, hash relaying | `python3-impacket`, `responder`, `smbclient` |
| **4. Transport** | Port scanning, firewall evasion, raw sockets | `nmap`, `masscan`, `hping3`, `netcat` |
| **3. Network** | Packet crafting, sniffing, route analysis | `python3-scapy`, `tcpdump`, `traceroute` |
| **2. Data Link** | ARP spoofing, VLAN hopping, Wi-Fi attacks | `bettercap`, `dsniff`, `aircrack-ng`, `yersinia` |
| **1. Physical** | RF sniffing, Bluetooth scanning, UART access | `gnuradio`, `gqrx-sdr`, `bluez`, `screen` |

---

## Layer 7: Application Layer (HTTP, DNS, SMB, SSH, FTP)
*Focuses on web exploitation, service enumeration, and credential brute-forcing.*

* **Installation:**
  ```bash
  sudo apt update && sudo apt install -y nmap gobuster hydra sqlmap smbclient
  ```
* **Basic Usage:**
  * **Enumerate web directories (HTTP/HTTPS):**
    ```bash
    gobuster dir -u http://192.168.1.10 -w /usr/share/wordlists/dirb/common.txt
    ```
  * **Test SSH login credentials:**
    ```bash
    hydra -l admin -P /path/to/wordlist.txt ssh://192.168.1.10
    ```

---

## Layer 6: Presentation Layer (SSL/TLS, Encoding, Encryption)
*Focuses on auditing cryptographic implementations, weak ciphers, and certificate configurations.*

* **Installation:**
  ```bash
  sudo apt install -y sslscan testssl.sh openssl
  ```
* **Basic Usage:**
  * **Audit SSL/TLS ciphers and known vulnerabilities:**
    ```bash
    sslscan 192.168.1.10:443
    ```
  * **Inspect a remote TLS certificate:**
    ```bash
    openssl s_client -connect 192.168.1.10:443
    ```

---

## Layer 5: Session Layer (SMB Sessions, RPC, NetBIOS, SIP)
*Focuses on session hijacking, null-session enumeration, and NTLM hash relaying.*

* **Installation:**
  ```bash
  sudo apt install -y python3-impacket smbclient responder
  ```
* **Basic Usage:**
  * **Enumerate users/shares via an anonymous RPC null session:**
    ```bash
    rpcclient -U "" -N 192.168.1.10
    ```
  * **Capture NetNTLMv2 hashes via local broadcast poisoning:**
    ```bash
    sudo responder -I eth0
    ```

---

## Layer 4: Transport Layer (TCP, UDP, SCTP)
*Focuses on port discovery, firewall rule mapping, and custom TCP/UDP packet crafting.*

* **Installation:**
  ```bash
  sudo apt install -y nmap masscan hping3 netcat-traditional
  ```
* **Basic Usage:**
  * **Perform a TCP SYN (stealth) port scan:**
    ```bash
    sudo nmap -sS -p- 192.168.1.10
    ```
  * **Craft custom TCP packets with specific flags (e.g., SYN to port 80):**
    ```bash
    sudo hping3 -S -p 80 192.168.1.10
    ```

---

## Layer 3: Network Layer (IPv4, IPv6, ICMP, OSPF, BGP)
*Focuses on host discovery, route mapping, traffic sniffing, and custom IP header crafting.*

* **Installation:**
  ```bash
  sudo apt install -y python3-scapy traceroute tcpdump
  ```
* **Basic Usage:**
  * **Craft and send a custom ICMP echo packet using Scapy:**
    ```bash
    sudo scapy
    >>> send(IP(dst="192.168.1.10")/ICMP()/"Payload")
    ```
  * **Capture live IP traffic on a specific interface:**
    ```bash
    sudo tcpdump -i eth0 host 192.168.1.10
    ```

---

## Layer 2: Data Link Layer (Ethernet, ARP, Wi-Fi 802.11, VLAN, STP)
*Focuses on local LAN attacks such as ARP spoofing, MAC spoofing, VLAN hopping, and wireless auditing.*

* **Installation:**
  ```bash
  sudo apt install -y bettercap dsniff macchanger aircrack-ng yersinia
  ```
* **Basic Usage:**
  * **Spoof your MAC address:**
    ```bash
    sudo ip link set eth0 down
    sudo macchanger -r eth0
    sudo ip link set eth0 up
    ```
  * **Perform an ARP spoofing MITM attack between a target and gateway:**
    ```bash
    sudo arpspoof -i eth0 -t 192.168.1.10 192.168.1.1
    ```
  * **Put a wireless interface into monitor mode for 802.11 capture:**
    ```bash
    sudo airmon-ng start wlan0
    ```

---

## Layer 1: Physical Layer (RF, Bluetooth, USB, Serial/UART)
*Focuses on hardware interfaces and physical signals (requires compatible hardware such as an SDR, Bluetooth adapter, or USB-to-TTL cable).*

* **Installation:**
  ```bash
  sudo apt install -y gqrx-sdr gnuradio bluez minicom screen
  ```
* **Basic Usage:**
  * **Scan for nearby Bluetooth devices:**
    ```bash
    hcitool scan
    ```
  * **Connect to an embedded device's physical UART/Serial debug port:**
    ```bash
    sudo screen /dev/ttyUSB0 115200
    ```
