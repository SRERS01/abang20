## Layer 4: Transport Layer (Segments, Datagrams & Ports)

The Transport Layer provides end-to-end communication, process-to-process delivery via **port numbers (0–65535)**, flow control, and error recovery. It breaks Layer 5–7 data into **TCP segments** (connection-oriented, reliable) or **UDP datagrams** (connectionless, low-latency).

### Environment Differences: Ubuntu vs. Termux
* **Ubuntu:** Full support for raw TCP/UDP packet crafting (`sudo`), half-open SYN scans (`nmap -sS`), ACK/FIN/Xmas firewall mapping, and high-speed asynchronous scanning (`masscan`, `rustscan`).
* **Termux:** Non-rooted Android restricts raw socket packet crafting, meaning `nmap` defaults to full TCP 3-way handshake connect scans (`-sT`) and UDP scans (`-sU`) require root. Tools like `nc` (netcat), `socat`, `ss`, and `curl` work natively without root.

---

### Core Layer 4 Protocols & Testing Tools

| Protocol / Standard | Full Name & Role | Security Auditing Focus | Testing Tools (Ubuntu & Termux) |
| :--- | :--- | :--- | :--- |
| **TCP** | Transmission Control Protocol (reliable, stateful 3-way handshake: `SYN`, `SYN-ACK`, `ACK`). | Port enumeration, SYN flood DoS, TCP sequence number prediction, session hijacking, and stateful firewall/IDS rule mapping (`FIN`, `NULL`, `Xmas`, `ACK` scans). | `nmap`, `masscan`, `rustscan`, `hping3`, `scapy`, `ss` |
| **UDP** | User Datagram Protocol (connectionless, stateless datagram delivery). | Amplification/reflection DDoS vectors (DNS, NTP, SNMP, SSDP, Memcached), unauthenticated management services, and firewall bypasses via stateless UDP ports. | `nmap -sU`, `udp-proto-scanner`, `nc -u`, `hping3`, `onesixtyone` |
| **SCTP** | Stream Control Transmission Protocol (multi-homed, message-oriented telecom & signaling transport). | Exposed telecom/5G/SS7/Diameter signaling interfaces, SCTP INIT/COOKIE-ECHO port scanning, and multihoming firewall evasion. | `nmap -sY / -sZ`, `scapy`, `ncat --sctp`, `wireshark` |
| **QUIC** | Quick UDP Internet Connections (encrypted, multiplexed transport over UDP; underpins HTTP/3). | Firewall/DLP bypasses where UDP port 443 is unfiltered or uninspected compared to traditional TCP port 443 inspection. | `curl --http3`, `wireshark`, `nmap`, `quic-go` |
| **TLS (Transport Wrapper)** | Transport Layer Security (cryptographic wrapper bridging Layer 4 TCP/UDP and Layer 7). | Weak cipher suites, deprecated protocols (SSLv3, TLS 1.0/1.1), Heartbleed/POODLE/ROBOT vulnerabilities, and expired or self-signed certificates. | `testssl.sh`, `sslscan`, `openssl s_client`, `nmap --script ssl-enum-ciphers` |

---

### Practical Layer 4 Auditing Commands (Ubuntu & Termux)

```bash
# 1. Inspect active listening TCP/UDP ports and owning processes (Ubuntu & Termux)
ss -tulnp

# 2. Fast TCP SYN scan with service/version detection (Ubuntu root; use -sT on non-rooted Termux)
sudo nmap -sS -sV -p- --min-rate 1000 <target-ip>

# 3. Map stateful firewall rules using a TCP ACK scan (Ubuntu root)
sudo nmap -sA -p 22,80,443,3389 <target-ip>

# 4. Scan top 100 UDP ports for exposed stateless services (Ubuntu root)
sudo nmap -sU --top-ports 100 <target-ip>

# 5. Manually grab a TCP service banner or test raw port connectivity (Ubuntu & Termux)
nc -nv <target-ip> 80

# 6. Audit TLS ciphers and certificate configuration on port 443 (Ubuntu & Termux)
openssl s_client -connect example.com:443 -servername example.com
```

---

### Layer 4 -> Web Security Connection
* **HTTP Request Smuggling (CL.TE / TE.CL):** Exploits discrepancies in how front-end reverse proxies and back-end web servers reuse persistent Layer 4 **TCP keep-alive connections** and parse `Content-Length` vs. `Transfer-Encoding` boundaries.
* **Slowloris & Connection Exhaustion:** Holds hundreds of Layer 4 TCP sockets open by sending partial HTTP headers slowly, starving the web server's concurrent connection pool without needing high bandwidth.
* **Firewalled Admin Ports & Non-Standard HTTP:** Full TCP port sweeps (`-p-`) frequently uncover hidden web applications, staging servers, or container APIs running on high ports (`8080`, `8443`, `9000`, `2375`) that bypass edge CDN/WAF protections.
