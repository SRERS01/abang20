## Layer 3: Network Layer (Packets & Logical IP Addressing)

The Network Layer handles logical addressing, packet routing, and path determination across multiple interconnected networks (WANs and the Internet). It packages Layer 4 segments into **packets** and uses **IPv4/IPv6 addresses** to route data from source to destination across routers.

### Environment Differences: Ubuntu vs. Termux
* **Ubuntu:** Full raw socket access (`SOCK_RAW` with `sudo`), custom IP/ICMP packet crafting (`scapy`, `hping3`), route table modification (`ip route`), and full `nmap` scan types (`-sS`, `-O`, `-sO`).
* **Termux:** Non-rooted Android blocks raw IP packet crafting (`SOCK_RAW`). Standard `ping`, `traceroute`, `ip route`, and unprivileged TCP connect scans (`nmap -sT`) work out of the box, while SYN scans and OS detection require root.

---

### Core Layer 3 Protocols & Testing Tools

| Protocol / Standard | Full Name & Role | Security Auditing Focus | Testing Tools (Ubuntu & Termux) |
| :--- | :--- | :--- | :--- |
| **IPv4** | Internet Protocol version 4 (32-bit logical addressing & fragmentation). | IP spoofing, source routing abuse, IP fragmentation evasion (overlapping fragments), and subnet enumeration. | `nmap`, `hping3`, `scapy`, `ip addr`, `ip route` |
| **IPv6** | Internet Protocol version 6 (128-bit addressing & Neighbor Discovery). | **SLAAC / Rogue Router Advertisements (RA)** MITM, DHCPv6 spoofing, and dual-stack firewall bypasses (unmonitored IPv6 interfaces). | `thc-ipv6` (`atk6-*`), `mitm6`, `scapy`, `ndisc6` |
| **ICMP / ICMPv6** | Internet Control Message Protocol (diagnostics & error reporting). | Host discovery sweeps, firewall ACL mapping, ICMP redirect MITM attacks, and covert data tunneling. | `ping`, `traceroute`, `mtr`, `hping3`, `ptunnel`, `icmpsh` |
| **IPsec (AH / ESP)** | Internet Protocol Security (network-layer authentication & encryption). | Aggressive Mode IKEv1 PSK hash capture/cracking, weak ciphers (DES/3DES/MD5), and misconfigured VPN split-tunneling. | `ike-scan`, `psk-crack`, `strongswan`, `wireshark` |
| **OSPF / EIGRP / RIP** | Interior Gateway Routing Protocols (dynamic route exchange within an AS). | **Route Injection / Poisoning** via unauthenticated or weak MD5-authenticated routing updates to blackhole or reroute traffic. | `yersinia`, `scapy`, `frr` (FRRouting), `loki` |
| **BGP** | Border Gateway Protocol (inter-domain Internet routing between ASNs). | BGP route hijacking, ASN enumeration, and prefix leak verification during external perimeter assessments. | `bgpq4`, `whois`, `traceroute`, `scapy` |
| **GRE** | Generic Routing Encapsulation (point-to-point virtual tunneling). | Unencrypted tunnel traffic sniffing and cleartext credential exposure if not wrapped inside IPsec. | `tcpdump`, `wireshark`, `ip tunnel` |

---

### Practical Layer 3 Auditing Commands (Ubuntu & Termux)

```bash
# 1. Inspect local IP addresses and subnet masks (Ubuntu & Termux)
ip -br addr show

# 2. View the kernel routing table and default gateway (Ubuntu & Termux)
ip route show

# 3. Perform an ICMP echo sweep to discover live hosts on a subnet
nmap -sn -PE 192.168.1.0/24

# 4. Trace the Layer 3 router hops to a target with packet loss stats (Ubuntu & Termux)
mtr -rwzbc 10 example.com

# 5. Fingerprint an IPsec VPN gateway for IKEv1 Aggressive Mode vulnerabilities (Ubuntu root)
sudo ike-scan -M -A <target-vpn-ip>

# 6. Send custom fragmented IP packets with hping3 to test firewall/IDS evasion (Ubuntu root)
sudo hping3 -S -p 80 -f <target-ip>
```

---

### Layer 3 -> Web Security Connection
* **SSRF & Internal IP Pivoting:** Server-Side Request Forgery (SSRF) vulnerabilities allow attackers to force a web server to send Layer 3 requests to internal RFC 1918 subnets (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`) or cloud metadata endpoints (`169.254.169.254`).
* **IPv6 Dual-Stack Blind Spots:** Many organizations harden firewall rules and WAFs for their public IPv4 web servers while leaving the server's native IPv6 address exposed directly to the Internet without rate limiting or ACLs.
* **IP-Based Access Control Bypasses:** Web applications relying on Layer 3 source IPs (or spoofable headers like `X-Forwarded-For`) for admin panel allowlisting can be bypassed via internal subnet pivoting or misconfigured reverse proxies.
