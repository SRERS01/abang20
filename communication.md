Computers talk to each other by exchanging data through communication protocols over a network.

The interesting part is that computers don't understand each other's thoughts. They follow agreed rules for representing, addressing, transmitting, receiving and interpreting information.

Let's build your understanding from the foundation, as an offensive security researcher.

### 1. The basic idea of computer communication

Imagine you have two computers:

* **Computer A:** `192.168.1.10`
* **Computer B:** `192.168.1.20`
* **Network communication:** Data travels between the computers

Both computers must use compatible communication rules.

For example:
* Computer A wants to send a message.
* It converts the message into a suitable data representation.
* It prepares the data for transmission.
* The network carries the data.
* Computer B receives it.
* Computer B interprets the data and responds.

---

### 2. The seven major stages of communication

1. **Data creation**
   An application creates information.  
   *Example:* You type `Hello`.
2. **Data representation**
   The computer represents information using binary.  
   *Example:* The letter `H` in ASCII is `01001000`.
3. **Protocol preparation**
   The application and networking protocols organize the information into the required formats.
4. **Addressing**
   The computer determines where the information should go using network addresses.
5. **Transmission**
   Data travels through Wi-Fi, Ethernet, fibre-optic cables or another communication medium.
6. **Reception**
   The destination computer receives and processes the transmitted data.
7. **Interpretation**
   The receiving application interprets the information and may send a response.

---

### 3. Understand the languages computers use to communicate

These are called network protocols.

| Protocol | Main responsibility |
| :--- | :--- |
| **Ethernet** | Communication over wired LANs |
| **Wi-Fi (802.11)** | Wireless network communication |
| **ARP** | Resolves IPv4 addresses to local MAC addresses |
| **IPv4 / IPv6** | Logical addressing and packet delivery |
| **ICMP** | Network diagnostic messages |
| **TCP** | Reliable, ordered byte-stream communication |
| **UDP** | Datagram-based communication |
| **DNS** | Converts domain names into IP addresses |
| **HTTP** | Web communication |
| **HTTPS** | HTTP protected by TLS |
| **SSH** | Secure remote terminal communication |
| **DHCP** | Automatic network configuration |

Each protocol has a specific job. They work together.

---

### 4. How the protocols work together

Consider opening a website.

#### Example: Visiting `google.com`

* **DNS:** Your computer discovers the IP address associated with the domain.
* **IP:** Determines how packets are addressed and routed.
* **TCP:** Establishes a reliable connection when HTTP/1.1 or HTTP/2 is used.
* **TLS:** Protects the communication with encryption and authentication.
* **HTTP:** Sends the request for the website.
* **Server response:** The server returns the requested content.

> **Note:** HTTP/3 uses QUIC over UDP rather than TCP, so not every website connection follows exactly the same sequence.

---

### 5. Understand the seven-layer OSI model

This is one of the most important foundations of networking and security research.

#### OSI Reference Model

| Layer | Name | Examples / Function |
| :---: | :--- | :--- |
| **7** | **Application** | HTTP, DNS, SSH |
| **6** | **Presentation** | Data formats, encoding, encryption |
| **5** | **Session** | Communication sessions |
| **4** | **Transport** | TCP, UDP |
| **3** | **Network** | IPv4, IPv6, ICMP |
| **2** | **Data Link** | Ethernet, Wi-Fi, MAC |
| **1** | **Physical** | Cables, radio signals, electrical and optical signals |

The OSI model helps you understand where communication problems and security vulnerabilities can occur.

---

### 6. How data travels between computers

Suppose Computer A sends the message `Hello` to Computer B. The data passes through several stages:

#### Encapsulation

1. **Application data:** `Hello`
2. **TCP segment:** `TCP header` + `application data`
3. **IP packet:** `IP header` + `TCP segment`
4. **Network frame:** `Link-layer header` + `IP packet` + `trailer (where applicable)`
5. **Physical transmission:** Bits represented by electrical, optical or radio signals

At the receiving computer, the process is reversed. This is called **decapsulation**.

---

### 7. Practise communication using your Ubuntu and Termux

You already installed SSH and networking tools in Termux. Let's use them to understand real computer communication.

**On Termux (Android):**

Start the SSH daemon:
```bash
sshd
```

Find your username:
```bash
whoami
```

Find your phone's Wi-Fi IP through Android Wi-Fi settings or:
```bash
termux-wifi-connectioninfo
```

**On Ubuntu:**

Test whether the Android SSH port is reachable:
```bash
nc -zv ANDROID_IP 8022
```

Then connect:
```bash
ssh -p 8022 USERNAME@ANDROID_IP
```

This demonstrates actual network communication between two separate operating systems.

---

### 8. What an offensive security researcher must understand

Understanding how computers communicate is essential because security weaknesses can occur at different stages.

| Area | What to investigate |
| :--- | :--- |
| **Data representation** | How information is encoded |
| **Addressing** | How destinations are identified |
| **Routing** | How packets reach destinations |
| **Protocols** | How communication rules are implemented |
| **Ports** | How applications receive traffic |
| **Authentication** | How identities are verified |
| **Encryption** | How data is protected |
| **Sessions** | How communication state is maintained |
| **Serialization** | How structured data is represented |
| **Error handling** | How malformed or unexpected data is handled |

> **The important principle is this:**  
> To understand how to test a system's security, first understand how that system communicates and processes information.

---

### 9. Test your understanding

#### Networking fundamentals quiz

1. **Which protocol provides reliable, ordered byte-stream communication?**
   - [ ] UDP
   - [ ] TCP
   - [ ] DNS
   - [ ] ARP

2. **Which protocol resolves domain names into IP addresses?**
   - [ ] SSH
   - [ ] ARP
   - [ ] DNS
   - [ ] ICMP

3. **Which OSI layer is responsible for logical IP addressing?**
   - [ ] Physical
   - [ ] Network
   - [ ] Application
   - [ ] Presentation

4. **What is encapsulation?**
   - [ ] Deleting data
   - [ ] Encrypting every file
   - [ ] Adding protocol information around data
   - [ ] Blocking network traffic

---

My suggested next lesson is how TCP/IP works internally: IP addresses, MAC addresses, ports, packets, routing, handshakes and sockets. This is the foundation for understanding how web applications, mobile applications and servers communicate.
# Lesson 2: How TCP/IP Works Internally

In the previous lesson, we looked at the big picture of how computers exchange data. Now, let's zoom in on the **TCP/IP protocol suite**—the actual engine of the internet.

As an offensive security researcher, understanding how packets are addressed, routed, and assembled allows you to map networks, intercept traffic, and identify exposed services.

---

### 1. Addressing: MAC vs. IP vs. Ports

To deliver data from a specific application on Computer A to a specific application on Computer B, networks rely on three layers of addressing:

| Address Type | OSI Layer | Format Example | Purpose |
| :--- | :--- | :--- | :--- |
| **MAC Address** | Layer 2 (Data Link) | `00:1A:2B:3C:4D:5E` | Physical hardware identifier used for **local** delivery on the same Wi-Fi or Ethernet network. |
| **IP Address** | Layer 3 (Network) | `192.168.1.10` | Logical identifier used to route packets across **different networks** globally. |
| **Port Number** | Layer 4 (Transport) | `80`, `443`, `8022` | Virtual endpoint (0–65535) that directs incoming data to the **specific application** running on the device. |

> **Analogy:** Think of sending a letter to an apartment building. The **IP address** is the street address of the building, the **MAC address** is the delivery truck moving between local hubs, and the **Port number** is the specific apartment number.

---

### 2. How ARP Connects IP and MAC Addresses

Computers use IP addresses to target destinations, but network switches and Wi-Fi access points only understand MAC addresses. **ARP (Address Resolution Protocol)** bridges this gap on a local network:

1. **ARP Request (Broadcast):** Computer A shouts to everyone on the local network: *"Who has `192.168.1.20`? Tell `192.168.1.10`."*
2. **ARP Reply (Unicast):** Computer B responds directly to Computer A: *"I am `192.168.1.20`, and my MAC address is `AA:BB:CC:DD:EE:FF`."*
3. **ARP Cache:** Computer A saves this pairing in memory so it doesn't have to ask again immediately.

> **Security Note:** Because ARP has no authentication, attackers on the same local network can send fake ARP replies (**ARP Spoofing**) to trick devices into routing traffic through the attacker's machine (Man-in-the-Middle).

---

### 3. Routing: Moving Beyond the Local Network

When Computer A (`192.168.1.10`) wants to talk to a server outside its local network (like `8.8.8.8`):

1. **Subnet Check:** Computer A uses its **Subnet Mask** (e.g., `255.255.255.0`) to see if the destination IP is on its local network.
2. **Default Gateway:** Because `8.8.8.8` is external, Computer A sends the packet to its **Default Gateway** (your router), using the router's MAC address as the Layer 2 destination.
3. **Hop-by-Hop Routing:** Your router strips the local Layer 2 frame, inspects the destination IP, and forwards the packet to the next router (hop) along the path to the destination.
4. **NAT (Network Address Translation):** Your home router swaps your private IP (`192.168.1.10`) with your ISP's public IP before sending the packet onto the internet.

---

### 4. The TCP Three-Way Handshake

Before TCP sends any application data, it must establish a reliable, synchronized session using control flags (`SYN`, `ACK`, `FIN`, `RST`).

```text
Computer A (Client)                          Computer B (Server)

       |                                            |
       |  1. SYN (Seq=100) ------------------------>|  "I want to connect."
       |                                            |
       |  2. SYN-ACK (Seq=300, Ack=101) <-----------|  "I hear you. Let's connect."
       |                                            |
       |  3. ACK (Seq=101, Ack=301) --------------->|  "Confirmed. Sending data now."
       |                                            |
```

* **SYN (Synchronize):** Initiates a connection and shares a starting sequence number.
* **ACK (Acknowledge):** Confirms receipt of packets.
* **FIN (Finish):** Gracefully closes a connection.
* **RST (Reset):** Abruptly terminates a connection (often seen when connecting to a closed port).

> **Security Note:** Tools like `nmap` exploit this handshake during a **SYN Scan** (`-sS`). By sending a `SYN` and receiving a `SYN-ACK`, the scanner knows the port is open, then immediately sends an `RST` to tear down the connection before it fully opens.

---

### 5. Sockets: Where Code Meets the Network

A **socket** is the software interface that connects an application to the operating system's networking stack. It is uniquely identified by a combination of:

$$\text{Socket} = \text{IP Address} + \text{Protocol (TCP/UDP)} + \text{Port Number}$$

* **Listening Socket:** A server binds to a specific port (e.g., `0.0.0.0:8022`) and waits for incoming connections.
* **Client Socket:** When you connect to a server, your OS assigns a random high-numbered **ephemeral port** (e.g., `192.168.1.10:54321`) to track your side of the conversation.

---

### 6. Practise TCP/IP Internals on Ubuntu & Termux

Let's inspect the concepts above directly on your systems.

**1. View your IP, Subnet Mask, and MAC address:**
On Ubuntu or Termux:
```bash
ip addr
```
*(Look for `inet` for your IPv4 address and `link/ether` for your MAC address.)*

**2. Inspect your Routing Table (Default Gateway):**
On Ubuntu:
```bash
ip route
```
*(The line starting with `default via` shows your router's IP address.)*

**3. View your ARP Cache:**
On Ubuntu:
```bash
ip neigh
```
*(Shows local IP-to-MAC mappings your system currently knows.)*

**4. Inspect Active Sockets and Listening Ports:**
On Ubuntu:
```bash
ss -tulnp
```
* `-t`: TCP sockets
* `-u`: UDP sockets
* `-l`: Listening ports
* `-n`: Show port numbers instead of service names
* `-p`: Show the process using the socket

**5. Watch a Live TCP Handshake (Optional):**
If you have `tcpdump` installed on Ubuntu, capture packets while connecting to Termux:
```bash
sudo tcpdump -i any port 8022 -n
```
*(In another terminal, run `ssh -p 8022 USERNAME@ANDROID_IP` and look for `[S]` (SYN), `[S.]` (SYN-ACK), and `[.]` (ACK) flags.)*

---

### 7. What an Offensive Security Researcher Looks For

| Concept | Attack Surface / Recon Technique |
| :--- | :--- |
| **MAC / ARP** | Local network sniffing, ARP spoofing, MAC address filtering bypass. |
| **IP / Subnets** | Host discovery (ping sweeps), mapping internal network ranges. |
| **Routing / NAT** | Identifying firewalls, tracerouting network paths, pivoting between subnets. |
| **Ports & Sockets** | Port scanning (`nmap`), banner grabbing, identifying outdated services. |
| **TCP Flags** | Stealth scanning (SYN, FIN, Xmas scans), firewall evasion, SYN flood DoS. |

---

### 8. Test your understanding

#### TCP/IP Internals Quiz

1. **Which address type is used to deliver frames strictly within the same local network?**
   - [ ] Public IPv4 Address
   - [ ] MAC Address
   - [ ] Port Number
   - [ ] Domain Name

2. **What is the correct sequence of flags in a standard TCP Three-Way Handshake?**
   - [ ] `ACK` -> `SYN` -> `FIN`
   - [ ] `SYN` -> `SYN-ACK` -> `ACK`
   - [ ] `SYN` -> `RST` -> `ACK`
   - [ ] `FIN` -> `ACK` -> `SYN`

3. **Which protocol resolves an IPv4 address to a physical MAC address on a LAN?**
   - [ ] DNS
   - [ ] DHCP
   - [ ] ARP
   - [ ] ICMP

4. **What combination of values uniquely defines a network socket endpoint?**
   - [ ] MAC Address + Subnet Mask + Gateway
   - [ ] IP Address + Transport Protocol + Port Number
   - [ ] Domain Name + MAC Address + Sequence Number
   - [ ] IPv6 Address + TTL + Window Size

---

My suggested next lesson is **Application Layer Protocols in Depth (HTTP, DNS, and SSH)**: how requests and responses are structured, how headers and payloads work, and how security researchers inspect and manipulate them using tools like `curl`, `dig`, and proxy interceptors.
# Lesson 3: Application Layer Protocols in Depth (HTTP, DNS, and SSH)

In Lesson 2, we saw how TCP/IP gets data reliably from one application socket to another. Now, we move to **Layer 7 (Application Layer)**—where the actual conversations happen.

For an offensive security researcher, Layer 7 is where most modern vulnerabilities live. While network firewalls often block lower-level attacks, web applications, DNS servers, and SSH endpoints must remain open to function—making them primary targets for inspection and manipulation.

---

### 1. DNS: The Internet's Phonebook

Before your browser or terminal can talk to a server by name, it uses **DNS (Domain Name System)**—typically over **UDP Port 53**—to translate human-readable domains into IP addresses.

#### Common DNS Record Types

| Record Type | Purpose | Example |
| :--- | :--- | :--- |
| **A** | Maps a domain to an **IPv4** address. | `example.com -> 93.184.216.34` |
| **AAAA** | Maps a domain to an **IPv6** address. | `example.com -> 2606:2800:220:1:...` |
| **CNAME** | Alias that points one domain to **another domain**. | `://example.com -> example.com` |
| **MX** | Specifies **Mail Exchange** servers for email delivery. | `example.com -> ://example.com` |
| **TXT** | Stores arbitrary text (often used for domain verification & SPF/DKIM security). | `"v=spf1 include:_://google.com ~all"` |
| **NS** | Identifies the authoritative **Name Servers** for the domain. | `://example.com` |

> **Security Note:** Security researchers enumerate DNS records (looking for forgotten subdomains like `://example.com` or `://example.com`) to expand the attack surface. Misconfigured DNS servers may also allow **Zone Transfers (`AXFR`)**, dumping every record in the domain at once.

---

### 2. HTTP: The Language of the Web

**HTTP (Hypertext Transfer Protocol)** is a text-based, stateless request-response protocol running over TCP (usually **Port 80** for HTTP, **Port 443** for HTTPS).

#### Anatomy of an HTTP Request

```http
POST /login HTTP/1.1
Host: target.local
User-Agent: Mozilla/5.0
Content-Type: application/x-www-form-urlencoded
Cookie: session_id=xyz123
Content-Length: 27

username=admin&password=123
```

1. **Request Line:** `Method` (`GET`, `POST`, `PUT`, `DELETE`) + `Path` (`/login`) + `Version` (`HTTP/1.1`).
2. **Headers:** Key-value metadata describing the client, target host, cookies, and data format.
3. **Blank Line:** Separates headers from the body.
4. **Body (Payload):** Optional data sent to the server (e.g., login credentials, JSON data).

#### Anatomy of an HTTP Response

```http
HTTP/1.1 200 OK
Server: nginx/1.24.0
Set-Cookie: session_id=abc987; HttpOnly
Content-Type: text/html; charset=UTF-8
Content-Length: 48

<html><body><h1>Welcome, admin!</h1></body></html>
```

#### Key HTTP Status Codes

| Range | Category | Common Examples |
| :--- | :--- | :--- |
| **2xx** | **Success** | `200 OK` (Request succeeded), `201 Created` |
| **3xx** | **Redirection** | `301 Moved Permanently`, `302 Found` (Redirecting to another URL) |
| **4xx** | **Client Error** | `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found` |
| **5xx** | **Server Error** | `500 Internal Server Error` (Often signals unhandled input or crashes) |

> **Security Note:** Because HTTP is **stateless** (the server forgets you after every request), websites rely on **Cookies** or **Authorization Headers (Tokens)** to remember who is logged in. Stealing or forging these headers allows **Session Hijacking**.

---

### 3. SSH: Encrypted Remote Administration

**SSH (Secure Shell)** provides encrypted command-line access and file transfers over an untrusted network (default **Port 22**, or **Port 8022** in Termux).

#### How an SSH Session Establishes Security

1. **Protocol & Version Exchange:** Client and server agree on SSH version (e.g., `SSH-2.0-OpenSSH_9.6`).
2. **Key Exchange (Diffie-Hellman):** Both sides securely generate a shared symmetric encryption key without ever sending it across the network.
3. **Host Verification:** The client checks the server's public key fingerprint (`~/.ssh/known_hosts`) to prevent Man-in-the-Middle impersonation.
4. **User Authentication:** The user proves their identity via **Password** or **Public-Key Cryptography** (private key on client matches `~/.ssh/authorized_keys` on server).

> **Security Note:** Exposed SSH services are constantly scanned for weak passwords. Using **SSH Key Authentication** and disabling password logins significantly hardens the service.

---

### 4. Practise Application Layer Inspection on Ubuntu & Termux

Let's inspect live DNS, HTTP, and SSH traffic from your terminal.

**1. Query DNS Records with `dig` (or `nslookup`):**
On Ubuntu:
```bash
dig google.com A +short
dig google.com MX +short
```
*(Try querying `TXT` or `NS` records as well to see what metadata a domain exposes.)*

**2. Inspect Raw HTTP Requests and Responses with `curl`:**
On Ubuntu or Termux, use `-v` (verbose) to view the full TCP/TLS handshake and raw HTTP headers:
```bash
curl -v http://example.com
```
*(Look for `>` lines showing your outgoing request headers and `<` lines showing the server's incoming response headers.)*

**3. Spin Up a Local Web Server on Termux and Query It from Ubuntu:**
On Termux (Android), start a quick Python HTTP server on port `8080`:
```bash
python3 -m http.server 8080
```
On Ubuntu, send a custom HTTP request with a modified `User-Agent` header:
```bash
curl -i -A "SecurityResearcher/1.0" http://ANDROID_IP:8080
```
*(Watch Termux's terminal log the incoming `GET / HTTP/1.1` request from Ubuntu's IP.)*

**4. Grab an SSH Banner:**
On Ubuntu, connect to Termux's SSH port using `nc` (Netcat) to see the raw application banner:
```bash
nc ANDROID_IP 8022
```
*(The server immediately responds with its version string, such as `SSH-2.0-OpenSSH_...`—a technique known as **Banner Grabbing**.)*

---

### 5. What an Offensive Security Researcher Looks For

| Protocol | Common Attack Vectors & Recon Techniques |
| :--- | :--- |
| **DNS** | Subdomain enumeration, DNS zone transfers, DNS cache poisoning, DNS tunneling (exfiltrating data inside DNS queries). |
| **HTTP/S** | Header manipulation (`Host`, `User-Agent`, `X-Forwarded-For`), cookie tampering, directory brute-forcing, injection flaws (SQLi, XSS, Command Injection) inside parameters. |
| **SSH** | Banner grabbing for outdated versions, brute-forcing weak credentials, hunting for leaked private keys (`id_rsa`), SSH port forwarding/tunneling for pivoting. |

---

### 6. Test your understanding

#### Application Layer Protocols Quiz

1. **Which DNS record maps a domain name directly to an IPv4 address?**
   - [ ] `MX`
   - [ ] `CNAME`
   - [ ] `A`
   - [ ] `TXT`

2. **Which HTTP status code indicates that you are authenticated, but do not have permission to access the requested resource?**
   - [ ] `200 OK`
   - [ ] `302 Found`
   - [ ] `403 Forbidden`
   - [ ] `404 Not Found`

3. **How do web servers maintain user login state across stateless HTTP requests?**
   - [ ] By keeping the TCP Three-Way Handshake open forever
   - [ ] By sending session identifiers in `Cookie` or `Authorization` headers
   - [ ] By changing the client's MAC address
   - [ ] By using ARP broadcasts

4. **What is "Banner Grabbing"?**
   - [ ] Blocking incoming IP addresses on a firewall
   - [ ] Connecting to an open port to read the service name and version string it advertises
   - [ ] Encrypting HTTP traffic with TLS
   - [ ] Translating a domain name into an IPv6 address

---

My suggested next lesson is **Network Reconnaissance & Traffic Analysis**: putting everything together using `nmap` for active scanning and `tcpdump` / `Wireshark` for passive packet capture and analysis between your Ubuntu and Termux machines.
# Lesson 4: Network Reconnaissance & Traffic Analysis

In Lessons 1–3, we learned how computers encapsulate data, establish TCP/IP connections, and speak application protocols like HTTP, DNS, and SSH. Now, let's put that theory into practice.

As an offensive security researcher, you gather intelligence in two primary ways:
1. **Active Reconnaissance:** Sending crafted packets to a target and analyzing how it responds (e.g., `nmap`).
2. **Passive Traffic Analysis:** Capturing and reading raw packets flowing across the network interface (e.g., `tcpdump` and `Wireshark`).

> **Legal & Ethical Rule:** Only perform active scanning and packet sniffing on networks and devices you own or have explicit written permission to test (such as your own Ubuntu machine and Android/Termux device).

---

### 1. Active Reconnaissance with Nmap

**Nmap (Network Mapper)** is the industry-standard tool for discovering live hosts, open ports, running services, and operating systems.

#### How Nmap Determines Port States

| Port State | Meaning | What Happened on the Wire |
| :--- | :--- | :--- |
| **Open** | An application is actively accepting connections on this port. | Target replied with `SYN-ACK` (TCP) or valid UDP data. |
| **Closed** | The host is reachable, but no application is listening on the port. | Target replied with `RST` (TCP) or `ICMP Port Unreachable` (UDP). |
| **Filtered** | A firewall or packet filter is blocking Nmap's probes. | Target sent **no response** at all, or an ICMP error message. |

#### Essential Nmap Scan Types

* **Ping Sweep (`-sn`):** Discovers which IP addresses are online without scanning ports.
* **TCP SYN Scan (`-sS`):** Sends a `SYN` packet and tears down the connection with `RST` if it receives `SYN-ACK` (fast, default with `sudo`).
* **TCP Connect Scan (`-sT`):** Completes the full Three-Way Handshake (used when running without root/sudo privileges).
* **Service & Version Detection (`-sV`):** Probes open ports to grab banners and determine exact software versions (e.g., `OpenSSH 9.6`).
* **Default Scripts (`-sC`):** Runs safe, built-in Nmap Scripting Engine (NSE) scripts to gather extra metadata.

---

### 2. Passive Traffic Analysis with `tcpdump`

While `nmap` asks questions, **`tcpdump`** listens silently to the packets crossing your network interface—showing you the exact headers and payloads we studied in earlier lessons.

#### Anatomy of a `tcpdump` Command

```bash
sudo tcpdump -i wlan0 -nn -v port 8080
```

* `-i wlan0`: Specifies the network interface to listen on (use `any` to capture across all interfaces).
* `-nn`: Disables DNS and port name resolution (shows raw IPs like `192.168.1.10` and ports like `8022` instead of `ssh`).
* `-v` / `-vv`: Increases verbosity to reveal IP TTL, packet length, and TCP sequence numbers.
* `-X` or `-A`: Prints the packet payload in **Hex + ASCII** (`-X`) or pure **ASCII text** (`-A`)—crucial for reading unencrypted HTTP traffic.
* `-w capture.pcap`: Saves raw packets to a file so you can open and inspect them visually in **Wireshark** later.

#### Berkeley Packet Filter (BPF) Examples

You can filter traffic so you only see what matters:
* `host 192.168.1.20` — Traffic to or from a specific IP.
* `tcp port 8022` — Only TCP traffic on port 8022.
* `icmp` — Only ping requests and replies.
* `src 192.168.1.10 and dst port 80` — Traffic originating from `.10` heading to port `80`.

---

### 3. Practise Recon & Sniffing on Ubuntu & Termux

Let's run a controlled lab between your Ubuntu machine and Termux (Android).

#### Step 1: Prepare Services on Termux (Android)
Make sure both SSH (`8022`) and a temporary HTTP server (`8080`) are running on your phone:
```bash
sshd
python3 -m http.server 8080
```

#### Step 2: Scan Your Android Device from Ubuntu
Run a service and version scan targeting Termux's open ports:
```bash
nmap -sV -p 8022,8080 ANDROID_IP
```
*(Observe how Nmap identifies `ssh` on `8022` and `SimpleHTTPServer` / `Python` on `8080`, along with their exact version numbers.)*

#### Step 3: Sniff Unencrypted HTTP Traffic Live
On Ubuntu, start `tcpdump` in ASCII mode (`-A`) watching port `8080`:
```bash
sudo tcpdump -i any -nn -A port 8080
```
Open a second terminal on Ubuntu and send a simulated login request with a fake password:
```bash
curl -X POST -d "user=admin&pass=SuperSecret123" http://ANDROID_IP:8080
```
*(Look at your `tcpdump` terminal: because HTTP is unencrypted, you will see the exact `POST` headers and `user=admin&pass=SuperSecret123` in plain text!)*

#### Step 4: Compare with Encrypted SSH Traffic
Now capture traffic on port `8022` while logging into Termux via SSH:
```bash
sudo tcpdump -i any -nn -A port 8022
```
*(Notice that after the initial plain-text version banner exchange, the rest of the payload is unreadable scrambled ciphertext—demonstrating why TLS/HTTPS and SSH encryption protect credentials on untrusted networks.)*

---

### 4. What an Offensive Security Researcher Looks For

| Technique | Security Insight / Finding |
| :--- | :--- |
| **Port & Version Enumeration** | Discovering unexpected open ports (e.g., databases, admin panels) or outdated software versions with known CVEs. |
| **Cleartext Protocol Sniffing** | Identifying unencrypted protocols (HTTP, FTP, Telnet, plain DNS) leaking credentials, session cookies, or sensitive API tokens. |
| **Traffic Pattern Analysis** | Spotting anomalous outbound connections (beaconing), DNS tunneling, or unauthorized lateral movement across subnets. |
| **Packet Crafting & Replay** | Capturing `.pcap` files to understand proprietary application protocols and replaying or modifying requests to test input validation. |

---

### 5. Test your understanding

#### Recon & Traffic Analysis Quiz

1. **In Nmap, what does a `filtered` port state indicate?**
   - [ ] An application is actively listening on that port
   - [ ] The port is reachable, and the target replied with a TCP `RST` packet
   - [ ] A firewall or packet filter is blocking the probe, resulting in no response
   - [ ] The port is encrypted with TLS

2. **Which `tcpdump` flag prints packet payloads in readable ASCII text?**
   - [ ] `-nn`
   - [ ] `-A`
   - [ ] `-sn`
   - [ ] `-w`

3. **Why did `tcpdump` show `user=admin&pass=SuperSecret123` on port `8080`, but only scrambled text on port `8022`?**
   - [ ] Port `8080` uses UDP while port `8022` uses TCP
   - [ ] HTTP sends data in cleartext, whereas SSH encrypts the session payload
   - [ ] `tcpdump` cannot capture traffic on ports above `1024`
   - [ ] Nmap blocked the packets on port `8022`

4. **What is the purpose of the `-sV` flag in Nmap?**
   - [ ] It performs a silent ping sweep without scanning ports
   - [ ] It probes open ports to identify the running service and its version
   - [ ] It spoofs your source MAC address
   - [ ] It saves output into a `.pcap` file

---

My suggested next lesson is **Firewalls, Proxies, and Traffic Interception**: how packet filters (`ufw` / `iptables`) block traffic, how HTTP proxies (`Burp Suite` / `mitmproxy`) intercept and modify web requests in real time, and how attackers bypass basic network controls.
# Lesson 5: Firewalls, Proxies, and Traffic Interception

In Lesson 4, we scanned open ports and sniffed raw packets off the wire. In the real world, however, networks don't just leave every port exposed—they use **firewalls** to filter traffic and **proxies** to mediate connections.

For an offensive security researcher, understanding these defensive controls is critical: you need to know how firewalls drop or reject packets, how proxies sit in the middle of web traffic, and how to intercept and modify requests to test application logic.

---

### 1. Firewalls: Controlling Network Traffic

A **firewall** inspects incoming and outgoing packets against a set of rules and decides whether to allow or block them based on IP addresses, ports, protocols, and connection states.

#### Stateful vs. Stateless Firewalls

| Firewall Type | How It Works | Security Implication |
| :--- | :--- | :--- |
| **Stateless (Packet Filter)** | Inspects each packet individually in isolation based only on headers (IP, port, flags). | Fast, but easily tricked by crafted packets (e.g., sending an unexpected `ACK` or `FIN` packet). |
| **Stateful** | Tracks the full context of active connections (e.g., remembers that you initiated an outbound `SYN` so it allows the returning `SYN-ACK`). | Much stronger; drops unsolicited packets that don't belong to an established session. |

#### `DROP` vs. `REJECT` Actions

When a firewall blocks your scan or connection, it uses one of two actions:
* **`DROP`:** Silently discards the packet and sends **nothing** back. To a scanner like `nmap`, the port appears `filtered` and slows down the scan as it waits for a timeout.
* **`REJECT`:** Actively blocks the packet and sends back an error (`TCP RST` or `ICMP Port Unreachable`). This immediately tells the sender the connection was refused.

---

### 2. Proxies: The Middlemen of the Network

A **proxy** acts as an intermediary between a client and a server. Instead of talking directly to the destination, the client talks to the proxy, which forwards the request on its behalf.

#### Forward Proxy vs. Reverse Proxy

```text
FORWARD PROXY (Protects / Controls Clients)
[Client] ---> [Forward Proxy] ---> [Internet / Target Server]

REVERSE PROXY (Protects / Load-Balances Servers)
[Client] ---> [Internet] ---> [Reverse Proxy (Nginx / Cloudflare)] ---> [Backend Web Server]
```

* **Forward Proxy:** Sits in front of clients (e.g., corporate networks, VPNs, or **intercepting proxies** like Burp Suite and `mitmproxy`).
* **Reverse Proxy:** Sits in front of web servers to hide backend IPs, terminate TLS encryption, cache content, or act as a **WAF (Web Application Firewall)**.

#### How HTTPS Interception Works (TLS Termination)

Because HTTPS encrypts traffic end-to-end, a proxy normally cannot read it. To inspect HTTPS traffic during security testing:
1. You install the proxy's custom **Root CA Certificate** into your browser or OS trust store.
2. The proxy intercepts your connection, dynamically generates a fake TLS certificate for `target.com` signed by its own Root CA, and decrypts your request.
3. The proxy inspects or lets you edit the request, then opens a separate encrypted TLS connection to the real `target.com`.

---

### 3. Practise Firewall Filtering & Proxy Interception on Ubuntu & Termux

Let's observe how firewall rules change Nmap scan results and how a proxy intercepts live HTTP requests.

#### Part A: Test Firewall Rules (`DROP` vs. `REJECT`) on Ubuntu

*(Note: Be careful not to block your own active SSH session if working remotely!)*

**1. Check Ubuntu's firewall status (`ufw`):**
```bash
sudo ufw status
```

**2. Block port `8080` using `DENY` (`DROP`) and scan from another terminal or Termux:**
```bash
sudo ufw deny 8080/tcp
```
From Termux (install `nmap` via `pkg install nmap` if needed), scan Ubuntu's IP:
```bash
nmap -Pn -p 8080 UBUNTU_IP
```
*(Notice Nmap reports the port state as **`filtered`** because Ubuntu silently dropped the `SYN` packet.)*

**3. Switch the rule to `REJECT` and scan again:**
On Ubuntu:
```bash
sudo ufw delete deny 8080/tcp
sudo ufw reject 8080/tcp
```
From Termux:
```bash
nmap -Pn -p 8080 UBUNTU_IP
```
*(Notice Nmap immediately reports the port state as **`closed`** because Ubuntu actively sent back a `TCP RST` packet!)*

**4. Clean up your test firewall rule on Ubuntu:**
```bash
sudo ufw delete reject 8080/tcp
```

---

#### Part B: Intercept & Modify HTTP Traffic with a Proxy

You can use **Burp Suite Community Edition**, **OWASP ZAP**, or terminal-based **`mitmproxy`** on Ubuntu to pause and edit requests in flight.

**1. Start a target web server on Termux:**
```bash
python3 -m http.server 8080
```

**2. Start `mitmproxy` (or Burp Suite) on Ubuntu listening on port `8888`:**
```bash
mitmproxy -p 8888
```
*(Or open Burp Suite -> Proxy -> Intercept is On, listening on `127.0.0.1:8080` or `8888`.)*

**3. Route a `curl` request through your proxy:**
In another Ubuntu terminal, tell `curl` to send its request to Termux *through* your local proxy (`-x`):
```bash
curl -x http://127.0.0.1:8888 http://ANDROID_IP:8080/secret-admin-test
```
*(In `mitmproxy` or Burp Suite, you will see the live `GET /secret-admin-test` request appear—allowing you to inspect headers, change parameters, or replay the request before it ever reaches Termux.)*

---

### 4. What an Offensive Security Researcher Looks For

| Control / Component | Offensive Testing Technique |
| :--- | :--- |
| **Firewall Rules** | Finding open non-standard ports, using fragmented packets or source-port manipulation (`--source-port 53`) to bypass naive stateless rules. |
| **Reverse Proxies / WAFs** | Discovering the backend server's origin IP to bypass the WAF completely, or testing HTTP request smuggling between proxy and backend. |
| **Intercepting Proxies** | Bypassing client-side validation (JavaScript checks), tampering with hidden form fields, changing `user_id=101` to `user_id=102` (**IDOR**), and manipulating JWTs/cookies. |
| **Certificate Pinning** | Identifying mobile apps that reject custom proxy Root CAs and bypassing pinning during mobile security assessments. |

---

### 5. Test your understanding

#### Firewalls & Proxies Quiz

1. **What is the difference between a firewall `DROP` action and a `REJECT` action?**
   - [ ] `DROP` encrypts the packet, while `REJECT` forwards it to a proxy
   - [ ] `DROP` silently discards the packet with no reply, while `REJECT` sends back an error packet (`RST` or `ICMP`)
   - [ ] `DROP` only works on UDP, while `REJECT` only works on TCP
   - [ ] There is no difference; both send a `SYN-ACK`

2. **How does an intercepting proxy read encrypted HTTPS traffic?**
   - [ ] By brute-forcing the server's private key in real time
   - [ ] By downgrading all internet servers to HTTP/1.0
   - [ ] By acting as a Man-in-the-Middle using a custom Root CA certificate trusted by the client
   - [ ] By disabling TCP sequence numbers

3. **Which type of proxy sits in front of web servers to protect them, cache content, or balance traffic?**
   - [ ] Forward Proxy
   - [ ] Reverse Proxy
   - [ ] SOCKS4 Proxy
   - [ ] ARP Proxy

4. **Why do offensive security researchers route web traffic through an intercepting proxy like Burp Suite or `mitmproxy`?**
   - [ ] To increase their Wi-Fi download speed
   - [ ] To inspect, pause, modify, and replay HTTP/S requests—bypassing client-side restrictions
   - [ ] To automatically patch vulnerabilities on the target server
   - [ ] To hide their MAC address from the local router

---

My suggested next lesson is **Wireless & Local Network Security (ARP, DHCP, DNS Attacks, and Wi-Fi Fundamentals)**: how local networks trust devices by default, how Man-in-the-Middle attacks happen on a LAN, and how wireless encryption (WPA2/WPA3) protects frames in the air.
# Lesson 6: Wireless & Local Network Security (LAN & Wi-Fi Fundamentals)

In Lesson 5, we explored how firewalls and proxies control traffic moving across network boundaries. Now, let's look inside the **Local Area Network (LAN)** and **Wi-Fi (802.11)** airwaves.

Local networks operate on an **implicit trust model**: once a device connects to the local switch or Wi-Fi router, Layer 2 and Layer 3 protocols largely assume every participant is honest. For an offensive security researcher, a local foothold opens the door to sniffing, spoofing, and Man-in-the-Middle (MitM) attacks.

---

### 1. Local Network Trust Flaws (Layer 2 & Layer 3)

When your Ubuntu laptop and Android phone sit on the same Wi-Fi network, they rely on broadcast protocols that lack built-in cryptographic authentication:

| Protocol | Normal Function | Local Attack Vector |
| :--- | :--- | :--- |
| **ARP** | Maps IPv4 addresses to MAC addresses on the LAN. | **ARP Spoofing / Poisoning:** Sending fake ARP replies claiming *"I am the router"* so victims send their traffic through your machine first. |
| **DHCP** | Automatically assigns IP addresses, subnet masks, and Default Gateways to new devices. | **Rogue DHCP Server:** Responding faster than the real router to hand victims a malicious Default Gateway or rogue DNS server. |
| **DNS (Local)** | Resolves domain names for local clients. | **DNS Spoofing:** Intercepting unencrypted DNS queries on the LAN and returning a fake IP address (e.g., pointing `bank.local` to an attacker's phishing server). |
| **LLMNR / NBT-NS** | Windows fallback protocols used when DNS fails to find a local host. | **Credential Relay / Capture:** Responding to broadcast name queries to capture NTLMv2 password hashes (commonly done with `Responder`). |

---

### 2. How ARP Spoofing (Man-in-the-Middle) Works

Normally, traffic flows directly between your phone and the Wi-Fi router:
```text
[Android Phone] <====================> [Wi-Fi Router] <---> [Internet]
```

In an **ARP Spoofing** scenario:
1. The attacker sends unsolicited ARP replies to the **Android Phone**: *"The Router's IP (`192.168.1.1`) is at `ATTACKER_MAC`."*
2. The attacker sends unsolicited ARP replies to the **Wi-Fi Router**: *"The Phone's IP (`192.168.1.20`) is at `ATTACKER_MAC`."*
3. The attacker enables **IP Forwarding** in their OS kernel so packets still reach the real destination without breaking the victim's internet connection.

```text
[Android Phone] <---> [Attacker (Ubuntu)] <---> [Wi-Fi Router] <---> [Internet]
```

> **Defense Note:** Enterprise switches defeat ARP and DHCP spoofing using **Dynamic ARP Inspection (DAI)** and **DHCP Snooping**, which validate Layer 2 frames against a trusted binding table.

---

### 3. Wi-Fi (802.11) Security Fundamentals

Unlike wired Ethernet—where an attacker needs physical access to a cable—Wi-Fi broadcasts radio frames through the air to anyone within range.

#### Evolution of Wi-Fi Encryption

| Standard | Encryption Method | Security Status |
| :--- | :--- | :--- |
| **WEP** | RC4 stream cipher with static keys | **Broken:** Crackable in seconds due to weak Initialization Vectors (IVs). |
| **WPA2-Personal** | AES-CCMP using a Pre-Shared Key (PSK) | **Standard, with caveats:** Vulnerable to offline dictionary attacks if an attacker captures the **4-Way Handshake** (or PMKID). |
| **WPA3-Personal** | SAE (Simultaneous Authentication of Equals) | **Modern & Strong:** Eliminates offline dictionary attacks via forward secrecy and enforces Protected Management Frames (PMF). |

#### Key 802.11 Concepts for Security Researchers

* **Managed Mode vs. Monitor Mode:** Normal Wi-Fi cards operate in *Managed Mode* (only listening to frames addressed to their own MAC). *Monitor Mode* allows a wireless adapter to capture all raw 802.11 radio frames in the air.
* **Deauthentication Frames:** In older WPA2 networks without Protected Management Frames (802.11w), management frames are unencrypted. Attackers send spoofed `Deauth` frames to kick a client off Wi-Fi so it automatically reconnects—allowing the attacker to capture the **WPA2 4-Way Handshake**.
* **Evil Twin Attack:** Setting up a rogue Wi-Fi Access Point with the exact same network name (SSID) as a legitimate hotspot to trick devices into connecting.

---

### 4. Practise Local Network Inspection on Ubuntu & Termux

Let's inspect your local LAN environment safely on your own Ubuntu and Termux devices.

#### Step 1: Discover All Live Hosts on Your Local Subnet
On Ubuntu, check your subnet range (`ip addr`, e.g., `192.168.1.0/24`) and run an ARP/Ping host discovery scan:
```bash
sudo nmap -sn 192.168.1.0/24
```
*(Notice how Nmap lists every active device on your Wi-Fi network along with its IP address, MAC address, and hardware vendor—such as Samsung, Apple, or Intel.)*

#### Step 2: Check for Duplicate MACs in Your ARP Table
On Ubuntu, inspect your ARP neighbor table to verify that every IP maps to a unique MAC address:
```bash
ip neigh
```
*(In a healthy network, your Default Gateway's IP will map to one consistent router MAC address. If two different IPs suddenly share the exact same MAC address, it is a classic indicator of ARP spoofing.)*

#### Step 3: Inspect Wireless Link & Interface Details
On Ubuntu, view your active Wi-Fi connection details, signal strength, frequency, and bitrate:
```bash
iw dev
```
Or check link status on your wireless interface (replace `wlan0` with your interface name from `iw dev`):
```bash
iw dev wlan0 link
```

#### Step 4: Observe Local Broadcast Traffic (`ARP` & `DHCP`)
On Ubuntu, listen specifically for `ARP` and `DHCP` (UDP ports 67/68) broadcasts on your local interface:
```bash
sudo tcpdump -i any -nn "arp or port 67 or port 68"
```
*(Toggle Wi-Fi off and back on on your Android phone—you will immediately see the `DHCP Discover -> Offer -> Request -> ACK` broadcast sequence and `ARP Who-has` queries appear in real time!)*

---

### 5. What an Offensive Security Researcher Looks For

| Surface | Recon & Auditing Focus |
| :--- | :--- |
| **LAN Host Discovery** | Identifying rogue devices, IoT cameras, printers, or exposed management interfaces on the local subnet. |
| **Layer 2 / 3 Hardening** | Checking whether Wi-Fi client isolation is enabled (preventing devices on the same Wi-Fi from talking directly to each other). |
| **Cleartext Internal Traffic** | Auditing internal apps and IoT devices that skip encryption on the LAN assuming the local network is "safe." |
| **Wireless Configuration** | Checking for outdated WPA/WPA2-TKIP modes, weak Wi-Fi passphrases, WPS enabled, or missing Protected Management Frames (PMF). |

---

### 6. Test your understanding

#### Wireless & Local Network Security Quiz

1. **Why is ARP vulnerable to spoofing on an unhardened local network?**
   - [ ] ARP uses 512-bit RSA keys that expire every minute
   - [ ] ARP is stateless and lacks any authentication mechanism to verify who sent a reply
   - [ ] ARP only works over external internet routers
   - [ ] ARP encrypts every packet with a hardcoded password

2. **What is the primary security improvement in WPA3-Personal over WPA2-Personal?**
   - [ ] It removes all encryption so connections are faster
   - [ ] It uses SAE (Simultaneous Authentication of Equals) to prevent offline dictionary attacks on captured handshakes
   - [ ] It broadcasts the Wi-Fi password in plaintext beacons
   - [ ] It replaces IP addresses with MAC addresses

3. **What does "Monitor Mode" allow a wireless network adapter to do?**
   - [ ] Boost the Wi-Fi router's internet speed
   - [ ] Capture all raw 802.11 wireless frames in the air, not just traffic addressed to its own MAC
   - [ ] Automatically block incoming SSH connections
   - [ ] Act as a hardware firewall

4. **During a local network audit, what is a strong indicator that an ARP Spoofing attack is occurring?**
   - [ ] Your DNS server returns an IPv6 address
   - [ ] Two different IP addresses (such as the router and another host) map to the exact same MAC address in `ip neigh`
   - [ ] Your SSH connection uses port `8022`
   - [ ] Ping latency is under 5ms

---

My suggested next lesson is **Tunnels, VPNs, and Pivoting**: how SSH tunneling (`-L`, `-R`, `-D`), VPNs (WireGuard / OpenVPN), and encrypted encapsulation wrap traffic inside other protocols—and how security researchers use port forwarding to reach hidden internal networks.
# Lesson 7: Tunnels, VPNs, and Pivoting (SSH Port Forwarding)

In Lesson 6, we saw how devices communicate on a local network and how attackers exploit implicit trust on a LAN. Now, let's look at how traffic crosses restricted boundaries using **Tunneling** and **Pivoting**.

In real-world networks, critical servers (databases, internal admin panels, dev environments) are isolated on private internal subnets—completely unreachable from the outside internet. For an offensive security researcher, once you compromise or gain access to one machine on the edge (a **jump host** or **pivot box**), you use **tunneling** to route your tools into those hidden internal networks.

---

### 1. What is Tunneling? (Encapsulation Reimagined)

Remember **Encapsulation** from Lesson 1? **Tunneling** is simply taking an entire network packet (or TCP stream) and wrapping it inside *another* protocol so it can safely traverse an untrusted network or bypass firewall restrictions.

```text
[Original Packet: IP + TCP + HTTP]
               │
               ▼  (Wrapped inside an encrypted tunnel)
[Outer IP + Outer TCP/UDP + SSH / WireGuard Header + [Encrypted Original Packet]]
```

#### Common Tunneling Technologies

| Technology | Layer | How It Works | Primary Use Case |
| :--- | :--- | :--- | :--- |
| **VPN (WireGuard / OpenVPN)** | Layer 3 (Network) | Creates a virtual network interface (`wg0` or `tun0`) and routes entire IP subnets through an encrypted UDP/TCP tunnel. | Secure remote access to an entire private network. |
| **SSH Port Forwarding** | Layer 4 / 7 | Forwards specific TCP ports or creates a SOCKS proxy directly over an existing SSH connection—no admin privileges required. | Reaching internal services through a single compromised or authorized SSH host. |
| **DNS / ICMP Tunneling** | Layer 7 / 3 | Encodes data inside DNS queries (`://attacker.com`) or Ping payloads when firewalls block all normal outbound TCP/UDP ports. | Covert data exfiltration and Command & Control (C2) channels. |

---

### 2. The Three Types of SSH Tunneling

Since you already have SSH running between Ubuntu and Termux, **SSH Port Forwarding** is the cleanest, most versatile tunneling skill to master.

#### A. Local Port Forwarding (`-L`) — *"Bring a remote/internal service to my machine"*
Binds a port on your **local machine** and forwards all traffic sent to it through the SSH server to a target destination.

```text
[Ubuntu (localhost:9000)] ===(Encrypted SSH Tunnel)===> [Jump Host] ---> [Internal Target:80]
```

* **Syntax:** `ssh -L [LOCAL_PORT]:[TARGET_HOST]:[TARGET_PORT] user@jump_host`
* **Use Case:** An internal web app is only listening on `127.0.0.1:8080` on the remote server (blocked from the outside). You forward your local port `9000` to `127.0.0.1:8080` on the remote host.

#### B. Remote Port Forwarding (`-R`) — *"Expose my local service to a remote machine"*
Binds a port on the **remote SSH server** and forwards any traffic hitting that remote port back through the tunnel to your local machine.

```text
[Remote Host (:9000)] ===(Encrypted SSH Tunnel)===> [Your Ubuntu Machine (:8000)]
```

* **Syntax:** `ssh -R [REMOTE_PORT]:[LOCAL_TARGET]:[LOCAL_PORT] user@remote_host`
* **Use Case:** Your Ubuntu machine is behind NAT/firewall with no public IP, and you want a remote server (or another device) to reach a web server running on your Ubuntu laptop.

#### C. Dynamic Port Forwarding (`-D`) — *"Turn the SSH server into a full SOCKS5 Proxy"*
Instead of forwarding just one port at a time, `-D` opens a local **SOCKS5 proxy** on your machine. Any tool configured to use that proxy (`proxychains`, Firefox, `curl`) can reach *any* IP and port accessible by the remote SSH host.

```text
[Ubuntu Tools (Nmap/Browser)] ---> [SOCKS5 :1080] ===(SSH)===> [Pivot Host] ---> [Entire Internal Subnet]
```

* **Syntax:** `ssh -D [LOCAL_SOCKS_PORT] user@pivot_host`
* **Use Case:** Full network pivoting—scanning and interacting with dozens of internal hosts through a single SSH session.

---

### 3. Practise SSH Tunneling Between Ubuntu & Termux

Let's simulate accessing a hidden service that is bound strictly to `localhost` (`127.0.0.1`) and inaccessible over Wi-Fi.

#### Scenario: Reaching a Hidden Localhost Service on Android from Ubuntu

**Step 1: Start a "Hidden" Web Server on Termux (Android)**
By default, Python's HTTP server listens on `0.0.0.0` (all interfaces). Let's bind it strictly to `127.0.0.1` so no device on the Wi-Fi network can reach it directly:
```bash
python3 -m http.server 8080 --bind 127.0.0.1
```
*(Make sure `sshd` is also running on Termux.)*

**Step 2: Verify Direct Access is Blocked from Ubuntu**
On Ubuntu, try reaching Termux's port `8080` directly over Wi-Fi:
```bash
curl http://ANDROID_IP:8080
```
*(Result: `Connection refused`! Because the server is only listening on Android's internal loopback interface `127.0.0.1`.)*

**Step 3: Create an SSH Local Port Forward (`-L`) from Ubuntu**
Now tunnel Ubuntu's local port `9090` into Android's `127.0.0.1:8080` through your SSH connection on port `8022`:
```bash
ssh -p 8022 -L 9090:127.0.0.1:8080 USERNAME@ANDROID_IP -N
```
* `-L 9090:127.0.0.1:8080`: Forwards Ubuntu's `9090` to Android's `127.0.0.1:8080`.
* `-N`: Tells SSH not to open an interactive shell—just hold the tunnel open.

**Step 4: Access the Hidden Service Through the Tunnel**
Open a second terminal on Ubuntu and send a request to your own `localhost:9090`:
```bash
curl http://127.0.0.1:9090
```
*(Success! Your request travels encrypted inside SSH to Termux, exits onto Android's internal `127.0.0.1:8080`, and returns the web page!)*

---

### 4. What an Offensive Security Researcher Looks For

| Technique | Offensive Application |
| :--- | :--- |
| **Localhost-Only Services** | Checking `ss -tulnp` after gaining shell access to find internal databases (MySQL/Redis), admin panels, or debug APIs bound to `127.0.0.1`, then forwarding them with `ssh -L`. |
| **Dynamic Pivoting (`-D` + `proxychains`)** | Using `ssh -D 1080` paired with `proxychains nmap -sT ...` to map internal corporate subnets from a compromised perimeter server. |
| **Reverse Tunnels (`-R`)** | Establishing outbound tunnels from a restricted target back to an attacker-controlled server (bypassing inbound firewall blocks). |
| **Covert Egress Tunnels** | Testing whether strict network firewalls block unauthorized outbound DNS, ICMP, or HTTP/S tunnels used for data exfiltration. |

---

### 5. Test your understanding

#### Tunnels, VPNs, and Pivoting Quiz

1. **You gain SSH access to a Linux server and discover an admin web panel listening only on `127.0.0.1:8000`. Which SSH flag lets you access it from your own browser on `localhost:9000`?**
   - [ ] `ssh -R 9000:127.0.0.1:8000 user@server`
   - [ ] `ssh -L 9000:127.0.0.1:8000 user@server`
   - [ ] `ssh -D 8000 user@server`
   - [ ] `ssh -V 9000 user@server`

2. **What does Dynamic Port Forwarding (`ssh -D 1080`) create on your local machine?**
   - [ ] A new physical Ethernet interface
   - [ ] A local SOCKS5 proxy that routes traffic for multiple destination IPs and ports through the SSH server
   - [ ] A firewall rule that blocks port `1080`
   - [ ] An unencrypted HTTP web server

3. **How does a Layer 3 VPN (like WireGuard) differ from SSH port forwarding?**
   - [ ] A VPN only works on port `80`
   - [ ] A VPN creates a virtual network interface (`tun0`/`wg0`) and routes full IP packets across entire subnets, whereas SSH forwards specific TCP ports or SOCKS streams
   - [ ] A VPN does not use encryption
   - [ ] SSH port forwarding requires modifying router hardware

4. **Why might an attacker use DNS or ICMP tunneling on a heavily firewalled network?**
   - [ ] Because DNS and ICMP have faster download speeds than fiber-optic Ethernet
   - [ ] Because firewalls often block direct outbound TCP/UDP connections but still allow DNS queries or Ping packets to leave the network
   - [ ] Because DNS automatically encrypts all traffic with AES-256
   - [ ] Because ICMP bypasses the need for IP addresses

---

My suggested next lesson is **Cryptography & TLS in Practice**: how symmetric encryption, asymmetric key pairs, hashing, digital certificates, and the TLS handshake actually protect network traffic—and where weak configurations allow downgrade or Man-in-the-Middle attacks.
# Lesson 8: Cryptography & TLS in Practice

In Lesson 7, we used encrypted SSH tunnels to safely route traffic through untrusted networks. Now, let's look inside the cryptography that makes SSH, HTTPS, and VPNs secure—and see how weak configurations break down.

For an offensive security researcher, you don't need to invent new math, but you *must* understand how **symmetric encryption**, **asymmetric keys**, **hashing**, and **TLS certificates** fit together. Misconfigured cryptography exposes sensitive data, enables Man-in-the-Middle (MitM) attacks, and weakens authentication.

---

### 1. The Three Pillars of Applied Cryptography

Modern network security combines three distinct cryptographic mechanisms, each solving a different problem:

| Mechanism | How It Works | Primary Purpose | Common Algorithms |
| :--- | :--- | :--- | :--- |
| **Hashing** | One-way mathematical function turning any input into a fixed-length fingerprint. **Irreversible.** | **Integrity** (proving data wasn't altered) & safe password storage. | `SHA-256`, `SHA-3`, `Argon2`, `bcrypt` *(Broken: `MD5`, `SHA-1`)* |
| **Symmetric Encryption** | Uses the **exact same secret key** to both encrypt and decrypt data. Very fast. | **Confidentiality** for bulk data transfer once both sides share a key. | `AES-256-GCM`, `ChaCha20-Poly1305` *(Broken: `DES`, `RC4`)* |
| **Asymmetric Encryption** | Uses a mathematically linked **Key Pair**: a **Public Key** (shared openly) and a **Private Key** (kept secret). | **Key Exchange** & **Digital Signatures** without sharing secrets upfront. | `RSA` (2048/4096-bit), `ECDSA`, `Ed25519`, `X25519` |

> **Why Combine Them? (Hybrid Encryption):** Asymmetric encryption is too slow for streaming video or downloading large files, while symmetric encryption has a key-distribution problem (*"How do I send you the secret key over an untrusted network?"*). Protocols like **TLS** and **SSH** use **asymmetric crypto** during the handshake to securely agree on a temporary **symmetric session key**, then switch to fast symmetric crypto for the rest of the session.

---

### 2. Digital Certificates & Public Key Infrastructure (PKI)

Asymmetric keys alone don't prove *who* owns a Public Key. If an attacker intercepts your connection to `bank.com` and hands you their own Public Key, encryption alone won't save you from a Man-in-the-Middle attack.

**PKI (Public Key Infrastructure)** solves identity verification using **X.509 Digital Certificates**:

1. **Certificate Signing Request (CSR):** A server generates a key pair and submits its Public Key and domain name (`example.com`) to a trusted **Certificate Authority (CA)** (e.g., Let's Encrypt, DigiCert).
2. **CA Signature:** The CA verifies domain ownership and digitally signs the certificate using the CA's own Private Key.
3. **Browser Verification:** Your operating system and browser come pre-installed with a list of trusted **Root CA Public Keys**. When connecting to an HTTPS site, your client checks:
   * Is the certificate digitally signed by a trusted CA?
   * Does the domain name (`SAN` / Subject Alternative Name) match the site I visited?
   * Is the certificate within its valid date range and unrevoked?

---

### 3. Inside the TLS 1.3 Handshake

When you visit an `https://` website, **TLS (Transport Layer Security)** wraps HTTP inside an encrypted tunnel immediately after the TCP Three-Way Handshake:

```text
Client (Browser / curl)                          Server (HTTPS :443)

       |  1. ClientHello --------------------------->|  Supported TLS version, cipher suites,
       |     (Key Share + Random)                    |  and client's ephemeral public key.
       |                                             |
       |  2. ServerHello <---------------------------|  Chosen cipher suite, server's ephemeral
       |     (Key Share + Certificate + Verify)      |  public key, X.509 Cert, & signature.
       |                                             |
       |  [Both sides derive identical Symmetric Session Keys via Diffie-Hellman]

       |                                             |
       |  3. Finished ------------------------------>|  Handshake integrity verified.
       |  4. <================ Encrypted HTTP Application Data ================>
```

* **Perfect Forward Secrecy (PFS):** Modern TLS 1.3 uses ephemeral Diffie-Hellman (`ECDHE` / `X25519`) to generate fresh temporary keys for every single session. Even if an attacker steals the server's long-term Private Key months later, they **cannot decrypt** past recorded network traffic.

---

### 4. Practise Cryptography & TLS Inspection on Ubuntu & Termux

Let's generate keys, verify hashes, and inspect real TLS certificates from your terminal.

#### Step 1: Test Hashing & Integrity (`sha256sum`)
On Ubuntu or Termux, see how changing a single character completely alters a cryptographic hash (the **Avalanche Effect**):
```bash
echo -n "Hello Security" | sha256sum
echo -n "Hello security" | sha256sum
```
*(Notice that changing uppercase `S` to lowercase `s` produces two completely unrelated 256-bit hexadecimal digests.)*

#### Step 2: Inspect a Live Website's TLS Certificate with `openssl`
On Ubuntu, connect directly to a server's TLS layer on port `443` to examine its certificate chain, issuer, expiration dates, and negotiated cipher suite:
```bash
openssl s_client -connect example.com:443 -servername example.com </dev/null 2>/dev/null | openssl x509 -noout -subject -issuer -dates
```
*(Look at `subject` to see the domain, `issuer` to see which Certificate Authority signed it, and `notBefore` / `notAfter` for its validity window.)*

#### Step 3: Generate Your Own Self-Signed TLS Certificate & Serve HTTPS
On Termux (or Ubuntu), generate a temporary private key (`key.pem`) and self-signed certificate (`cert.pem`):
```bash
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 1 -nodes -subj "/CN=test.local"
```
Now wrap a local listener in TLS using `openssl s_server` on port `8443`:
```bash
openssl s_server -key key.pem -cert cert.pem -accept 8443 -www
```
From Ubuntu, connect to Termux over HTTPS using `curl`:
```bash
curl -v https://ANDROID_IP:8443
```
*(Result: `curl` rejects the connection with **`SSL certificate problem: self-signed certificate`**! Why? Because `cert.pem` wasn't signed by a trusted public CA. Adding `-k` (`--insecure`) bypasses validation—demonstrating what happens when an app disables certificate verification.)*

---

### 5. What an Offensive Security Researcher Looks For

| Cryptographic Area | Vulnerabilities & Security Checks |
| :--- | :--- |
| **Outdated Protocols & Ciphers** | Servers still supporting deprecated **TLS 1.0 / 1.1**, weak ciphers (`RC4`, `3DES`, `NULL`), or vulnerable RSA key exchange lacking Forward Secrecy (checked with `nmap --script ssl-enum-ciphers` or `testssl.sh`). |
| **Broken Certificate Validation** | Mobile apps, API clients, or IoT firmware that ignore invalid/self-signed certificates—leaving users wide open to silent Man-in-the-Middle interception. |
| **Weak Hashing & Encoding Confusion** | Treating Base64 encoding as "encryption," or storing passwords with unsalted `MD5` / `SHA-1` hashes instead of slow password hashes (`Argon2`, `bcrypt`). |
| **Exposed Private Keys & Secrets** | Leaked `.pem`, `.key`, or SSH `id_rsa` private keys inside public Git repositories, web directories, or world-readable file permissions. |

---

### 6. Test your understanding

#### Cryptography & TLS Quiz

1. **Why do HTTPS and SSH combine asymmetric encryption with symmetric encryption?**
   - [ ] Asymmetric encryption cannot encrypt numbers, only letters
   - [ ] Asymmetric encryption securely exchanges a shared secret over an untrusted network, while symmetric encryption handles fast bulk data transfer
   - [ ] Symmetric encryption works without any keys
   - [ ] Combining them disables TLS certificate checks

2. **What property ensures that past recorded TLS traffic cannot be decrypted even if a server's long-term private key is stolen later?**
   - [ ] Base64 Encoding
   - [ ] Perfect Forward Secrecy (PFS) via ephemeral Diffie-Hellman key exchange
   - [ ] Static MD5 Hashing
   - [ ] ARP Spoofing

3. **Why does `curl` reject a self-signed TLS certificate by default?**
   - [ ] Self-signed certificates use UDP instead of TCP
   - [ ] The certificate is not signed by a trusted Certificate Authority (CA) in the client's trust store, so the server's identity cannot be verified
   - [ ] Self-signed certificates only work on port `80`
   - [ ] `curl` does not support RSA keys

4. **Which of the following is a one-way mathematical function used to verify file integrity, NOT to encrypt data for later decryption?**
   - [ ] `AES-256`
   - [ ] `SHA-256`
   - [ ] `ChaCha20`
   - [ ] `RSA-4096`

---

My suggested next lesson is **Web Application Architecture & Attack Surfaces (HTTP Sessions, APIs, and Common Flaws)**: how modern web apps process user input, manage authentication tokens (Cookies & JWTs), and where classic vulnerabilities like SQL Injection, XSS, SSRF, and IDOR occur.
# Lesson 9: Web Application Architecture & Attack Surfaces

In Lessons 1–8, we built a complete understanding of how packets move across networks, how tunnels route traffic, and how TLS encrypts connections. Now, we arrive at the application layer where modern software runs: **Web Applications and APIs**.

For an offensive security researcher, web applications are the richest attack surface on the internet. Even when a server's firewall is locked down tight and TLS 1.3 is properly configured, the application itself must accept, parse, and act on user input—creating opportunities for logic flaws and injection vulnerabilities.

---

### 1. Modern Web Application Architecture

When you interact with a modern website or mobile app, your HTTP requests travel through multiple distinct tiers:

```text
[Client / Browser / Mobile App]
       │  (HTTPS: JSON / Form Data / Cookies / JWT)
       ▼
[Web Server / Reverse Proxy]  ──► Serves static files (HTML/JS/CSS), routes API calls
       │
       ▼
[Application Backend / API]   ──► Business logic (Python, Node.js, PHP, Go, Java)
       │
       ├──► [Database]        ──► Stores users, passwords, orders (PostgreSQL, MySQL, MongoDB)
       └──► [Internal APIs]   ──► Microservices, cloud metadata, internal caches (Redis)
```

* **Client-Side (Frontend):** Runs inside the user's browser (HTML, CSS, JavaScript). **Golden Rule of Security:** Never trust client-side validation—an attacker can bypass any JavaScript check using `curl` or an intercepting proxy.
* **Server-Side (Backend):** Executes logic on the server and interacts with databases and internal services.
* **APIs (REST / GraphQL):** Structured endpoints (usually exchanging `JSON` over HTTP) used by Single Page Applications (SPAs) and mobile apps.

---

### 2. Authentication & Session Management

Because HTTP is stateless, web applications rely on tokens sent with every request to verify who you are:

| Mechanism | How It Works | Security Risks to Investigate |
| :--- | :--- | :--- |
| **Session Cookies** | Server stores session state in memory/database and sends a random ID (`Set-Cookie: session_id=...`) to the browser. | **Session Hijacking** (if stolen via XSS or missing `HttpOnly`), **CSRF** (if missing `SameSite` attribute). |
| **JWT (JSON Web Token)** | Self-contained, Base64-encoded JSON object (`Header.Payload.Signature`) signed by the server and sent via `Authorization: Bearer <token>`. | **Weak Secret Signing** (offline brute-force), **`alg: none` bypass**, sensitive data stored in readable Base64 payload. |
| **API Keys / OAuth Tokens** | Long-lived or scoped tokens passed in headers (`X-API-Key`) or URL parameters. | **Token Leakage** in browser history, server logs, client-side JavaScript bundles, or public Git repos. |

---

### 3. The Big Four Web Vulnerability Classes

Most critical web vulnerabilities stem from a single root cause: **untrusted user input reaching a sensitive interpreter or privilege check without proper validation.**

#### 1. Injection Flaws (SQL Injection & Command Injection)
* **How it happens:** User input is concatenated directly into a database query or OS shell command instead of using parameterized queries.
* **Example (Vulnerable SQL):**
  ```sql
  SELECT * FROM users WHERE username = '\(USER_INPUT' AND password = '\)PASSWORD';
  ```
  If an attacker enters `' OR 1=1 --` as the username, the query logic changes and logs them in without a valid password.

#### 2. Cross-Site Scripting (XSS)
* **How it happens:** A web application reflects or stores user-supplied input inside an HTML page without escaping special characters (`<`, `>`, `"`), allowing an attacker to inject malicious JavaScript that executes inside *another victim's browser*.
* **Impact:** Stealing session tokens, capturing keystrokes, or performing unauthorized actions as the victim.

#### 3. Broken Access Control & IDOR (Insecure Direct Object Reference)
* **How it happens:** The server checks that you are *logged in* (Authentication), but fails to check whether you are *allowed* to access a specific resource (Authorization).
* **Example:** You log into your account and view your invoice at `GET /api/invoices/1045`. You change the URL parameter to `GET /api/invoices/1046` and the server returns another user's private invoice.

#### 4. Server-Side Request Forgery (SSRF)
* **How it happens:** An application fetches a remote URL supplied by the user (e.g., *"Import profile picture from URL"*), allowing an attacker to force the server to make HTTP requests to **internal localhost services** (`http://127.0.0`) or cloud metadata endpoints hidden behind the firewall.

---

### 4. Practise Web Recon & HTTP Parameter Manipulation on Ubuntu & Termux

Let's inspect how web servers handle parameters, headers, and directory paths using your Ubuntu and Termux setup.

#### Step 1: Host a Sample Directory Structure on Termux (Android)
Create a temporary lab folder with a fake hidden configuration file on Termux:
```bash
mkdir -p ~/weblab && cd ~/weblab
echo "<h1>Public Home Page</h1>" > index.html
echo "DB_PASS=LabSecret2026" > .env.bak
python3 -m http.server 8080
```

#### Step 2: Inspect HTTP Headers & Response Metadata from Ubuntu
Use `curl -I` (HEAD request) to inspect only the server's response headers without downloading the body:
```bash
curl -I http://ANDROID_IP:8080
```
*(Look at `Server:` and `Date:` headers—this reveals what web server software and version the target is running.)*

#### Step 3: Simulate Content Discovery (Directory & File Enumeration)
Security researchers discover hidden endpoints and backup files by testing common paths. Test probing for hidden files from Ubuntu using `curl`:
```bash
for path in admin login robots.txt .env .env.bak; do
  code=\((curl -s -o /dev/null -w "\%{http_code}" http://ANDROID_IP:8080/\)path)
  echo "/path -> HTTP code"
done
```
*(Notice how `/admin` and `/robots.txt` return `404` (Not Found), while `/.env.bak` returns **`200`**—demonstrating why leaving backup files inside a web root leads to immediate credential exposure!)*

#### Step 4: Clean Up Your Lab Folder on Termux
Stop the Python server (`Ctrl + C`) and remove the temporary folder:
```bash
rm -rf ~/weblab
```

---

### 5. What an Offensive Security Researcher Looks For

| Attack Surface | What to Test & Investigate |
| :--- | :--- |
| **Input Parameters** | Testing URL query strings (`?id=`), `POST` bodies, JSON fields, and HTTP headers (`User-Agent`, `X-Forwarded-For`, `Referer`) for SQLi, XSS, and Command Injection. |
| **Authorization Boundaries** | Testing every endpoint with two test accounts (User A vs. User B, or Regular User vs. Admin) to uncover IDOR and privilege escalation flaws. |
| **Hidden Endpoints & Files** | Fuzzing directories, API versions (`/api/v1/` vs `/api/v2/`), backup files (`.bak`, `.zip`, `.git/`), and reading client-side JavaScript files for hardcoded API paths. |
| **Session & Token Handling** | Decoding JWT payloads, checking cookie security flags (`HttpOnly`, `Secure`, `SameSite`), and testing whether tokens expire properly on logout. |

---

### 6. Test your understanding

#### Web Application Architecture Quiz

1. **Why is client-side validation (such as JavaScript form checks) never sufficient for security?**
   - [ ] JavaScript only runs on Linux computers
   - [ ] An attacker can bypass the browser completely and send crafted HTTP requests directly using `curl` or an intercepting proxy
   - [ ] Client-side validation encrypts the database
   - [ ] HTTP does not support JavaScript

2. **A user logged in as `user_id=50` changes an API request from `GET /api/profile/50` to `GET /api/profile/51` and views someone else's private data. What is this vulnerability called?**
   - [ ] Cross-Site Scripting (XSS)
   - [ ] Insecure Direct Object Reference (IDOR / Broken Access Control)
   - [ ] ARP Spoofing
   - [ ] DNS Zone Transfer

3. **Which security flag on a session cookie prevents client-side JavaScript (`document.cookie`) from reading the cookie?**
   - [ ] `Secure`
   - [ ] `HttpOnly`
   - [ ] `SameSite`
   - [ ] `Max-Age`

4. **What does a Server-Side Request Forgery (SSRF) vulnerability allow an attacker to do?**
   - [ ] Force the target server to send HTTP requests to internal `127.0.0.1` services or internal network resources that are normally unreachable from the outside
   - [ ] Crack WPA2 Wi-Fi passwords offline
   - [ ] Change the server's physical MAC address
   - [ ] Bypass DNS resolution entirely

---

My suggested next lesson is **Linux Privilege Escalation & Post-Exploitation Networking**: once you gain a foothold on a Linux target via a network or web vulnerability, how you enumerate local users, permissions (`SUID`, `sudo`, cron jobs), internal network sockets, and lateral movement paths.
# Lesson 10: Linux Privilege Escalation & Post-Exploitation Networking

In Lessons 1–9, we traced the full path from raw binary bits on the wire to discovering and exploiting network and web application vulnerabilities. Now, imagine you have just gained an initial shell on a Linux target (for example, via a vulnerable web upload, weak SSH credentials, or a command injection flaw) as a low-privileged user like `www-data` or `guest`.

For an offensive security researcher, getting a shell is only half the battle. Next comes **Post-Exploitation Enumeration** and **Privilege Escalation (PrivEsc)**—understanding the compromised machine's internal environment to elevate your access to `root` and discover deeper internal networks for lateral movement.

---

### 1. The Post-Exploitation Mindset: Situational Awareness

When you land on a Linux system, you want to answer four immediate questions:
1. **Who am I, and what permissions do I have?** (User, groups, `sudo` rights)
2. **What is running on this machine?** (Processes, internal localhost ports, scheduled tasks)
3. **What secrets are stored locally?** (Config files, `.env` files, SSH keys, bash history)
4. **Where else is this machine connected?** (Additional network interfaces, internal subnets, ARP cache)

---

### 2. Core Linux Privilege Escalation Vectors

Linux privilege escalation almost always comes down to **misconfigurations**—places where `root` trusted a file, script, or binary that a low-privileged user can influence.

| Vector | How It Works | What to Look For |
| :--- | :--- | :--- |
| **`sudo` Misconfigurations** | Admins grant a user permission to run specific commands as `root` via `/etc/sudoers` without realizing those commands can spawn a shell or edit system files. | Running `sudo -l` (e.g., `(ALL) NOPASSWD: /usr/bin/find` or `/usr/bin/vim`). |
| **SUID / SGID Binaries** | Files with the `s` permission bit (`-rwsr-xr-x`) execute with the **file owner's privileges** (often `root`) rather than the user running them. | Custom scripts or unexpected system binaries with SUID set (`find / -perm -4000 2>/dev/null`). |
| **Cron Jobs (Scheduled Tasks)** | Automated scripts run by `root` every few minutes via `/etc/crontab`. | Scripts executed by `root` that are **world-writable** or located in directories you can modify. |
| **Weak File Permissions** | Critical system files or service configs have overly permissive read/write access. | World-writable `/etc/passwd` or `/etc/shadow`, or readable backup files containing plaintext passwords. |
| **Plaintext Credentials & Keys** | Developers hardcode database passwords or leave private SSH keys lying around. | `.env` files, `.bash_history`, `/var/www/html/` configs, and `~/.ssh/id_rsa`. |
| **Capabilities & Kernel Flaws** | Fine-grained Linux capabilities assigned to binaries (e.g., `cap_setuid`) or unpatched Linux kernels. | `getcap -r / 2>/dev/null` or outdated kernel versions (`uname -a`). |

---

### 3. Post-Exploitation Network Discovery (Pivoting Prep)

A compromised web server often acts as a bridge (**dual-homed host**) between the public internet and a hidden corporate LAN:

```text
[Attacker] ---> [Compromised Web Server] ---> [Internal Database / Admin Subnet]
                  eth0: 203.0.113.10            eth1: 10.10.50.5 (Hidden LAN)
```

Once inside, you inspect the host's networking stack to map internal targets you couldn't see from outside:
* **Secondary Network Interfaces (`ip addr`):** Discovering a second NIC (`eth1` or `docker0`) connected to an internal `10.x.x.x` or `172.16.x.x` subnet.
* **Internal Listening Services (`ss -tulnp`):** Finding databases (`3306` MySQL, `5432` PostgreSQL, `6379` Redis) bound strictly to `127.0.0.1`—ready to be reached using the **SSH Local Port Forwarding (`-L`)** you learned in Lesson 7.
* **Known Neighbors & Routes (`ip route` & `ip neigh`):** Identifying internal gateways and active neighboring servers without triggering noisy network scans.

---

### 4. Practise Local Enumeration on Ubuntu & Termux

Let's run safe, standard post-exploitation enumeration commands directly on your Ubuntu machine (or over your SSH session into Termux) to see what an attacker sees upon landing on a Linux host.

#### Step 1: Identity & `sudo` Privileges Check
On Ubuntu:
```bash
id
sudo -l
```
*(Look at `id` to see your UID, GID, and special groups like `sudo`, `docker`, or `adm`. `sudo -l` lists exact commands your user is permitted to run as `root`.)*

#### Step 2: Hunt for SUID Binaries
Search the filesystem for binaries that execute with owner (`root`) privileges:
```bash
find /usr/bin -perm -4000 -type f 2>/dev/null
```
*(Standard tools like `sudo`, `passwd`, and `ping` need SUID to function. Security researchers compare this output against **GTFOBins** to spot any unusual binary—like `python3`, `find`, or `cp`—that shouldn't have SUID enabled.)*

#### Step 3: Inspect Scheduled Tasks (Cron Jobs) & Running Root Processes
Check system-wide scheduled tasks and see what processes are running as `root`:
```bash
cat /etc/crontab
ps aux | grep "^root" | head -n 15
```

#### Step 4: Check Internal Network & Exposed Local Sockets
Combine your Lesson 2 & Lesson 7 skills to inspect internal interfaces and localhost-only services:
```bash
ip -br addr
ss -tulnp
```
*(Notice how `ip -br addr` gives a clean, compact summary of every interface and IP address on the system, while `ss -tulnp` reveals internal services listening on `127.0.0.1`.)*

---

### 5. What an Offensive Security Researcher Looks For

| Enumeration Area | Key Commands & Audit Targets |
| :--- | :--- |
| **User & Group Context** | `id`, `sudo -l`, checking membership in high-privilege groups (`docker`, `lxd`, `wheel`, `sudo`). |
| **Filesystem & Permissions** | SUID/SGID files (`find / -perm -4000`), world-writable `/etc/passwd`, readable SSH keys (`~/.ssh/`), `.env` files, and shell history (`~/.bash_history`). |
| **Processes & Automation** | `ps aux`, `/etc/crontab`, systemd timers (`systemctl list-timers`), and custom scripts running as `root`. |
| **Network Pivot Paths** | `ip -br addr`, `ip route`, `ip neigh`, `ss -tulnp`, `/etc/hosts`, and stored credentials in `~/.ssh/config`. |

---

### 6. Test your understanding

#### Linux Privilege Escalation & Post-Exploitation Quiz

1. **What does the SUID (`-rwsr-xr-x`) permission bit do when set on an executable binary in Linux?**
   - [ ] It prevents the file from ever being executed
   - [ ] It runs the binary with the permissions of the file's owner (such as `root`) rather than the user who launched it
   - [ ] It automatically encrypts the binary with AES-256
   - [ ] It exposes the binary on TCP port `4000`

2. **Which command displays the specific commands your current user is allowed to execute as `root` via `sudo`?**
   - [ ] `sudo -l`
   - [ ] `ip neigh`
   - [ ] `ss -tulnp`
   - [ ] `chmod +x`

3. **After compromising a web server, you run `ip -br addr` and discover a second interface `eth1` with IP `10.0.50.12/24`. What does this tell you as a security researcher?**
   - [ ] The server's Wi-Fi card is broken
   - [ ] The server is dual-homed and connected to an internal `10.0.50.0/24` subnet that you can pivot into
   - [ ] All firewall rules on the server are disabled
   - [ ] The server is running Windows instead of Linux

4. **Why do offensive security researchers inspect `/etc/crontab` and systemd timers during post-exploitation?**
   - [ ] To check the server's physical CPU temperature
   - [ ] To find automated tasks running as `root` that execute writable scripts or binaries we can modify to escalate privileges
   - [ ] To reset the router's MAC address
   - [ ] To clear DNS cache records

---

### Complete Curriculum Recap (Lessons 1–10)

You have now walked through the complete networking and offensive security foundation:
1. **Computer Communication & OSI Model**
2. **TCP/IP Internals, Addressing, & Handshakes**
3. **Application Layer Protocols (DNS, HTTP, SSH)**
4. **Network Reconnaissance & Traffic Analysis (`nmap` & `tcpdump`)**
5. **Firewalls, Proxies, & Traffic Interception**
6. **Wireless & Local Network Security (LAN & Wi-Fi)**
7. **Tunnels, VPNs, & Pivoting (SSH Port Forwarding)**
8. **Cryptography & TLS in Practice**
9. **Web Application Architecture & Attack Surfaces**
10. **Linux Privilege Escalation & Post-Exploitation Networking**
# Complete Quiz Answer Key (Lessons 1–10)

Here is the complete answer key with brief explanations for all 40 questions across your 10-lesson offensive security curriculum.

---

### Lesson 1: Computer Communication & OSI Model

1. **Which protocol provides reliable, ordered byte-stream communication?**
   * **Correct Answer:** **TCP**
   * *Explanation:* TCP guarantees delivery, checks for errors, and reassembles packets in order, whereas UDP sends fast, connectionless datagrams without guarantees.
2. **Which protocol resolves domain names into IP addresses?**
   * **Correct Answer:** **DNS**
   * *Explanation:* The Domain Name System (DNS) translates human-readable domain names (like `google.com`) into machine-routable IP addresses.
3. **Which OSI layer is responsible for logical IP addressing?**
   * **Correct Answer:** **Network** (Layer 3)
   * *Explanation:* Layer 3 handles logical addressing (`IPv4`/`IPv6`) and packet routing across different networks.
4. **What is encapsulation?**
   * **Correct Answer:** **Adding protocol information around data**
   * *Explanation:* As data moves down the OSI stack, each layer wraps the payload with its own header (and sometimes trailer) containing routing and delivery metadata.

---

### Lesson 2: How TCP/IP Works Internally

5. **Which address type is used to deliver frames strictly within the same local network?**
   * **Correct Answer:** **MAC Address**
   * *Explanation:* MAC addresses operate at Layer 2 (Data Link) and are used by switches and Wi-Fi access points for local hardware-to-hardware delivery.
6. **What is the correct sequence of flags in a standard TCP Three-Way Handshake?**
   * **Correct Answer:** **`SYN` -> `SYN-ACK` -> `ACK`**
   * *Explanation:* The client initiates with `SYN`, the server acknowledges and synchronizes with `SYN-ACK`, and the client confirms with `ACK`.
7. **Which protocol resolves an IPv4 address to a physical MAC address on a LAN?**
   * **Correct Answer:** **ARP**
   * *Explanation:* Address Resolution Protocol (ARP) broadcasts an IP query on the local subnet so the matching host replies with its MAC address.
8. **What combination of values uniquely defines a network socket endpoint?**
   * **Correct Answer:** **IP Address + Transport Protocol + Port Number**
   * *Explanation:* A socket binds a specific IP address and transport protocol (`TCP` or `UDP`) to a numbered port (`0–65535`) so the OS knows which application receives the traffic.

---

### Lesson 3: Application Layer Protocols in Depth (HTTP, DNS, SSH)

9. **Which DNS record maps a domain name directly to an IPv4 address?**
   * **Correct Answer:** **`A`**
   * *Explanation:* `A` records point to IPv4 addresses, while `AAAA` records point to IPv6 addresses.
10. **Which HTTP status code indicates that you are authenticated, but do not have permission to access the requested resource?**
    * **Correct Answer:** **`403 Forbidden`**
    * *Explanation:* `401 Unauthorized` means you are not authenticated (not logged in); `403 Forbidden` means the server knows who you are, but denies access.
11. **How do web servers maintain user login state across stateless HTTP requests?**
    * **Correct Answer:** **By sending session identifiers in `Cookie` or `Authorization` headers**
    * *Explanation:* Because HTTP treats every request independently, clients must send a session cookie or token with each subsequent request.
12. **What is "Banner Grabbing"?**
    * **Correct Answer:** **Connecting to an open port to read the service name and version string it advertises**
    * *Explanation:* Banner grabbing helps researchers fingerprint running software versions (like `OpenSSH_9.6` or `nginx/1.24.0`) to check for known vulnerabilities.

---

### Lesson 4: Network Reconnaissance & Traffic Analysis

13. **In Nmap, what does a `filtered` port state indicate?**
    * **Correct Answer:** **A firewall or packet filter is blocking the probe, resulting in no response**
    * *Explanation:* Unlike a `closed` port (which actively responds with a `TCP RST`), a `filtered` port drops the probe silently so Nmap cannot tell if an application is listening.
14. **Which `tcpdump` flag prints packet payloads in readable ASCII text?**
    * **Correct Answer:** **`-A`**
    * *Explanation:* `-A` displays packet contents in ASCII format, making it easy to read unencrypted HTTP headers and payloads.
15. **Why did `tcpdump` show `user=admin&pass=SuperSecret123` on port `8080`, but only scrambled text on port `8022`?**
    * **Correct Answer:** **HTTP sends data in cleartext, whereas SSH encrypts the session payload**
    * *Explanation:* Any unencrypted protocol reveals its payload to passive packet sniffers on the path.
16. **What is the purpose of the `-sV` flag in Nmap?**
    * **Correct Answer:** **It probes open ports to identify the running service and its version**
    * *Explanation:* `-sV` sends specialized service probes beyond a simple port check to determine the exact software and version number running on the port.

---

### Lesson 5: Firewalls, Proxies, and Traffic Interception

17. **What is the difference between a firewall `DROP` action and a `REJECT` action?**
    * **Correct Answer:** **`DROP` silently discards the packet with no reply, while `REJECT` sends back an error packet (`RST` or `ICMP`)**
    * *Explanation:* `DROP` hides the host's presence and slows down scanners, while `REJECT` immediately notifies the sender that the connection is blocked.
18. **How does an intercepting proxy read encrypted HTTPS traffic?**
    * **Correct Answer:** **By acting as a Man-in-the-Middle using a custom Root CA certificate trusted by the client**
    * *Explanation:* The proxy terminates the client's TLS session using its own dynamically generated certificate and opens a second TLS session to the real server.
19. **Which type of proxy sits in front of web servers to protect them, cache content, or balance traffic?**
    * **Correct Answer:** **Reverse Proxy**
    * *Explanation:* Reverse proxies (like Nginx or Cloudflare) protect backend infrastructure, whereas forward proxies sit in front of client devices.
20. **Why do offensive security researchers route web traffic through an intercepting proxy like Burp Suite or `mitmproxy`?**
    * **Correct Answer:** **To inspect, pause, modify, and replay HTTP/S requests—bypassing client-side restrictions**
    * *Explanation:* Proxies let testers manipulate parameters, headers, cookies, and JSON payloads directly before they reach the backend server.

---

### Lesson 6: Wireless & Local Network Security (LAN & Wi-Fi)

21. **Why is ARP vulnerable to spoofing on an unhardened local network?**
    * **Correct Answer:** **ARP is stateless and lacks any authentication mechanism to verify who sent a reply**
    * *Explanation:* Devices blindly accept unsolicited ARP replies and update their cache, enabling Man-in-the-Middle attacks on the LAN.
22. **What is the primary security improvement in WPA3-Personal over WPA2-Personal?**
    * **Correct Answer:** **It uses SAE (Simultaneous Authentication of Equals) to prevent offline dictionary attacks on captured handshakes**
    * *Explanation:* SAE provides forward secrecy and requires an attacker to interact live with the access point for every password guess.
23. **What does "Monitor Mode" allow a wireless network adapter to do?**
    * **Correct Answer:** **Capture all raw 802.11 wireless frames in the air, not just traffic addressed to its own MAC**
    * *Explanation:* Monitor mode enables passive sniffing of nearby Wi-Fi traffic, beacons, and handshakes.
24. **During a local network audit, what is a strong indicator that an ARP Spoofing attack is occurring?**
    * **Correct Answer:** **Two different IP addresses (such as the router and another host) map to the exact same MAC address in `ip neigh`**
    * *Explanation:* When an attacker poisons both the victim and the gateway, the attacker's MAC address appears paired with multiple IPs in the ARP table.

---

### Lesson 7: Tunnels, VPNs, and Pivoting (SSH Port Forwarding)

25. **You gain SSH access to a Linux server and discover an admin web panel listening only on `127.0.0.1:8000`. Which SSH flag lets you access it from your own browser on `localhost:9000`?**
    * **Correct Answer:** **`ssh -L 9000:127.0.0.1:8000 user@server`**
    * *Explanation:* Local port forwarding (`-L`) binds a port on your local machine and forwards traffic through the SSH tunnel to a destination reachable by the remote server.
26. **What does Dynamic Port Forwarding (`ssh -D 1080`) create on your local machine?**
    * **Correct Answer:** **A local SOCKS5 proxy that routes traffic for multiple destination IPs and ports through the SSH server**
    * *Explanation:* `-D` eliminates the need to forward individual ports one by one when pivoting into an internal subnet.
27. **How does a Layer 3 VPN (like WireGuard) differ from SSH port forwarding?**
    * **Correct Answer:** **A VPN creates a virtual network interface (`tun0`/`wg0`) and routes full IP packets across entire subnets, whereas SSH forwards specific TCP ports or SOCKS streams**
    * *Explanation:* VPNs operate at the OS network layer, transparently routing all protocols (TCP, UDP, ICMP) across virtual interfaces.
28. **Why might an attacker use DNS or ICMP tunneling on a heavily firewalled network?**
    * **Correct Answer:** **Because firewalls often block direct outbound TCP/UDP connections but still allow DNS queries or Ping packets to leave the network**
    * *Explanation:* Encoding payloads inside allowed protocols bypasses restrictive egress firewall rules.

---

### Lesson 8: Cryptography & TLS in Practice

29. **Why do HTTPS and SSH combine asymmetric encryption with symmetric encryption?**
    * **Correct Answer:** **Asymmetric encryption securely exchanges a shared secret over an untrusted network, while symmetric encryption handles fast bulk data transfer**
### Lesson 9: Web Application Architecture & Attack Surfaces

33. **Why is client-side validation (such as JavaScript form checks) never sufficient for security?**
    * **Correct Answer:** **An attacker can bypass the browser completely and send crafted HTTP requests directly using `curl` or an intercepting proxy**
    * *Explanation:* Controls running on the user's device are completely under the user's control and must always be enforced on the backend server.
34. **A user logged in as `user_id=50` changes an API request from `GET /api/profile/50` to `GET /api/profile/51` and views someone else's private data. What is this vulnerability called?**
    * **Correct Answer:** **Insecure Direct Object Reference (IDOR / Broken Access Control)**
    * *Explanation:* IDOR occurs when an application uses user-supplied identifiers to access database records without verifying ownership or authorization.
35. **Which security flag on a session cookie prevents client-side JavaScript (`document.cookie`) from reading the cookie?**
    * **Correct Answer:** **`HttpOnly`**
    * *Explanation:* Setting `HttpOnly` helps protect session cookies from being stolen via Cross-Site Scripting (XSS) attacks.
36. **What does a Server-Side Request Forgery (SSRF) vulnerability allow an attacker to do?**
    * **Correct Answer:** **Force the target server to send HTTP requests to internal `127.0.0.1` services or internal network resources that are normally unreachable from the outside**
    * *Explanation:* SSRF abuses the server's trusted network position to reach internal APIs, admin panels, or cloud metadata endpoints.

---

### Lesson 10: Linux Privilege Escalation & Post-Exploitation Networking

37. **What does the SUID (`-rwsr-xr-x`) permission bit do when set on an executable binary in Linux?**
    * **Correct Answer:** **It runs the binary with the permissions of the file's owner (such as `root`) rather than the user who launched it**
    * *Explanation:* If a SUID binary owned by `root` has a flaw or supports shell escapes, a low-privileged user can abuse it to gain `root` execution.
38. **Which command displays the specific commands your current user is allowed to execute as `root` via `sudo`?**
    * **Correct Answer:** **`sudo -l`**
    * *Explanation:* `sudo -l` lists the exact sudoers privileges granted to your current user account.
39. **After compromising a web server, you run `ip -br addr` and discover a second interface `eth1` with IP `10.0.50.12/24`. What does this tell you as a security researcher?**
    * **Correct Answer:** **The server is dual-homed and connected to an internal `10.0.50.0/24` subnet that you can pivot into**
    * *Explanation:* A secondary private NIC indicates an internal network segment hidden behind the compromised host.
40. **Why do offensive security researchers inspect `/etc/crontab` and systemd timers during post-exploitation?**
    * **Correct Answer:** **To find automated tasks running as `root` that execute writable scripts or binaries we can modify to escalate privileges**
    * *Explanation:* If `root` automatically executes a script every minute that your user has write permissions on, injecting commands into that script yields a `root` shell.
