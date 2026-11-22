## Layer 5: Session Layer (Dialog Control & State Management)

The Session Layer establishes, manages, synchronizes, and terminates communication **sessions** (dialogs) between local and remote applications. In modern TCP/IP networks, Layer 5 functions are often blended into application protocols, RPC frameworks, and authentication state mechanisms.

### Environment Differences: Ubuntu vs. Termux
* **Ubuntu:** Full support for SMB/NetBIOS enumeration suites (`enum4linux-ng`, `impacket`, `smbclient`), RPC dumping (`rpcclient`, `rpcinfo`), and automated session replay/hijacking tools.
* **Termux:** Python-based tools like `impacket` (`smbclient.py`, `rpcdump.py`), `nmap` NSE scripts, and `curl` work natively without root. Kernel-level SMB mounting (`mount.cifs`) requires root.

---

### Core Layer 5 Protocols & Testing Tools

| Protocol / Standard | Full Name & Role | Security Auditing Focus | Testing Tools (Ubuntu & Termux) |
| :--- | :--- | :--- | :--- |
| **NetBIOS (NBNS / SMB Sessions)** | Network Basic Input/Output System (name resolution & session establishment over TCP 139/445). | Null sessions (unauthenticated enumeration), LLMNR/NBNS poisoning (credential relay), and anonymous share listing. | `enum4linux-ng`, `smbclient`, `smbmap`, `responder`, `nbtscan` |
| **RPC (ONC RPC / MSRPC)** | Remote Procedure Call (allows a program to execute procedures on a remote host). | Unauthenticated endpoint mapping (`portmapper` TCP/UDP 111, MSRPC TCP 135), exposed NFS exports, and Active Directory enumeration. | `rpcinfo`, `rpcclient`, `impacket-rpcdump`, `nmap --script rpcinfo` |
| **PPTP / L2TP** | Point-to-Point Tunneling Protocol / Layer 2 Tunneling Protocol (VPN session control). | Weak MS-CHAPv2 authentication in PPTP (crackable NTLMv1 challenge/response) and unencrypted L2TP sessions lacking IPsec. | `thc-pptp-bruter`, `asleap`, `nmap -sV -p 1723,1701`, `wireshark` |
| **SOCKS (SOCKS4 / SOCKS5)** | Socket Secure (session-layer proxy protocol routing TCP/UDP traffic through an intermediary). | Open/unauthenticated SOCKS proxies allowing internal network pivoting, SSRF chaining, or anonymous traffic relay. | `proxychains4`, `curl --socks5`, `nmap --script socks-open-proxy` |
| **SIP (Session Initiation Protocol)** | VoIP signaling protocol that initiates, maintains, and terminates voice/video sessions. | Extension enumeration, SIP registration hijacking, toll fraud via unauthenticated INVITEs, and digest credential brute-forcing. | `sipvicious` (`svmap`, `svwar`, `svcrack`), `nmap --script sip-methods` |
| **WebSockets (`ws://` / `wss://`)** | Persistent, full-duplex stateful session channel upgraded over an initial HTTP handshake. | Cross-Site WebSocket Hijacking (CSWSH) due to missing `Origin` validation, unencrypted `ws://` session interception, and broken message-level auth. | `wscat`, `websocat`, `burpsuite`, `owasp-zap` |

---

### Practical Layer 5 Auditing Commands (Ubuntu & Termux)

```bash
# 1. Enumerate SMB sessions, shares, and users via null session (Ubuntu & Termux)
smbclient -N -L //<target-ip>

# 2. Dump exposed ONC RPC services on port 111 (Ubuntu & Termux)
rpcinfo -p <target-ip>

# 3. Query MSRPC endpoints over TCP 135 using Impacket (Ubuntu & Termux)
impacket-rpcdump @<target-ip>

# 4. Test an open SOCKS5 proxy for unauthenticated internal pivoting (Ubuntu & Termux)
curl -v --socks5 <target-ip>:1080 http://example.com

# 5. Connect to a WebSocket endpoint to test session origin checks and message handling
websocat -H="Origin: https://example.com" wss://://example.com
```

---

### Layer 5 -> Web Security Connection
* **HTTP Session Management (`Cookies`, `JWT`, `SessionID`):** Although HTTP is stateless at Layer 7, applications recreate Layer 5 state using session tokens—making **Session Fixation**, **Session Hijacking** (missing `HttpOnly`/`Secure` flags), and **JWT signature/expiration flaws** primary web attack vectors.
* **Cross-Site WebSocket Hijacking (CSWSH):** When a web server upgrades an HTTP connection to a persistent Layer 5 WebSocket session using ambient cookies without checking the `Origin` header or a CSRF token, malicious sites can hijack the real-time session.
* **SMB Relay to Web / NTLM Authentication:** Capturing Layer 5 NetBIOS/SMB session handshakes on an internal network allows attackers to relay NTLM authentication directly to internal web applications (e.g., ADCS web enrollment or Exchange OWA).
