---

### 2. Security Auditing & Web Vulnerabilities (Section 6: Network Management & Monitoring)

In authorized penetration testing and bug bounty hunting, network management protocols often expose entire infrastructure topologies, plaintext credentials, or XML parsing flaws that tie directly into web-based monitoring dashboards.

#### Environment Differences: Ubuntu vs. Termux

* **Ubuntu:** Supports raw UDP scanning (`nmap -sU` for SNMP/Syslog) and full SNMP MIB translation suites (`snmp`, `snmp-mibs-downloader`).
* **Termux:** UDP Nmap scans require root, so auditors use user-space Python/CLI utilities (`onesixtyone`, `snmpwalk` via `net-snmp`, `nc`, `ssh`) to query SNMP, Syslog, and NETCONF over TCP/UDP sockets without root.

#### Protocol-by-Protocol Breakdown

##### 1. SNMP (Ports 161, 162 - UDP)

* **How it is audited (Ubuntu & Termux):**
  * **Community String Brute-Forcing & OID Walking:** Testing SNMPv1/v2c for default community strings (`public`, `private`, `manager`) and walking the Management Information Base (MIB) tree to extract running processes, network interfaces, and routing tables.
  * **Additional Auditing Commands:**
    ```bash
    # Scan UDP port 161 and enumerate system info/processes on Ubuntu (requires root)
    sudo nmap -sU -p 161 --script snmp-info,snmp-processes,snmp-netstat <target>

    # Brute-force SNMP community strings (works on Ubuntu & Termux)
    onesixtyone -c /usr/share/seclists/Discovery/SNMP/common-snmp-community-strings.txt <target>

    # Walk the entire SNMPv2c OID tree using the 'public' community string
    snmpwalk -v2c -c public <target>

    # Query specific OIDs (e.g., running software/processes)
    snmpwalk -v2c -c public <target> 1.3.6.1.2.1.25.4.2.1.2
    ```
* **Web Bugs Found:**
  * **Plaintext Web Admin Credentials & API Keys:** Network routers, printers, and servers frequently store web UI passwords, database connection strings, and internal API URLs inside SNMP OID variables or process arguments (`hrSWRunParameters`).

##### 2. Syslog (Port 514 - UDP/TCP)

* **How it is audited (Ubuntu & Termux):**
  * **Unauthenticated Log Injection Checks:** Verifying whether port 514 accepts arbitrary log messages from external or untrusted IP addresses without TLS or source filtering.
  * **Additional Auditing Commands:**
    ```bash
    # Probe TCP port 514 for exposed Syslog listeners
    nmap -sT -p 514 <target>

    # Send a test Syslog message over UDP using Netcat (Ubuntu & Termux)
    echo "<14>Test audit log entry" | nc -u -w1 <target> 514

    # Send a test Syslog message over TCP
    echo "<14>Test audit log entry" | nc -w1 <target> 514
    ```
* **Web Bugs Found:**
  * **Stored XSS / Log Injection in Web SIEM Dashboards:** Injecting HTML/JavaScript payloads or CRLF characters into Syslog messages that later execute in an administrator's browser when viewed inside a web-based log viewer (e.g., Splunk, Kibana, Graylog).

##### 3. NETCONF (Port 830)

* **How it is audited (Ubuntu & Termux):**
  * **Subsystem & XML Capability Checks:** Connecting to the NETCONF SSH subsystem on port 830 to inspect supported YANG data models and XML RPC handling.
  * **Additional Auditing Commands:**
    ```bash
    # Check if NETCONF port 830 is open and inspect SSH banner
    nmap -sT -sV -p 830 <target>

    # Connect to the NETCONF SSH subsystem manually (Ubuntu & Termux)
    ssh -s user@<target> -p 830 netconf
    ```
* **Web Bugs Found:**
  * **XXE (XML External Entity) Injection:** Web-based network orchestrators and SDN dashboards that translate user input into backend NETCONF XML RPC payloads without disabling external entity resolution.

---

### 2. Security Auditing & Web Vulnerabilities (Section 7: Voice, Video & Real-Time Media)

In authorized penetration testing and bug bounty hunting, media and VoIP protocols frequently expose unauthenticated camera feeds, internal IP addresses, and web-based PBX management panels.

#### Environment Differences: Ubuntu vs. Termux

* **Ubuntu:** Full support for VoIP auditing suites (`sipvicious`), media stream inspection (`ffplay`, `ffmpeg`), and browser WebRTC debugging.
* **Termux:** Python-based SIP tools (`sipvicious`), `curl`, `nmap`, and `ffmpeg` run natively without root.

#### Protocol-by-Protocol Breakdown

##### 1. SIP (Ports 5060, 5061)

* **How it is audited (Ubuntu & Termux):**
  * **Extension Enumeration & Registration Checks:** Probing SIP servers (`OPTIONS`, `REGISTER`, `INVITE`) to identify PBX software versions (Asterisk, FreePBX) and enumerate valid internal phone extensions.
  * **Additional Auditing Commands:**
    ```bash
    # Probe SIP options and server banner via Nmap
    nmap -sT -sV -p 5060,5061 --script sip-methods,sip-enum-users <target>

    # Scan for SIP devices and enumerate extensions using SIPVicious (Ubuntu & Termux)
    svmap <target>
    svwar -e 100-500 <target>

    # Send a raw SIP OPTIONS request over TCP via Netcat
    printf "OPTIONS sip:<target> SIP/2.0\r\nVia: SIP/2.0/TCP 127.0.0.1:5060\r\nFrom: <sip:audit@127.0.0.1>\r\nTo: <sip:audit@<target>>\r\nCall-ID: 12345@127.0.0.1\r\nCSeq: 1 OPTIONS\r\nContent-Length: 0\r\n\r\n" | nc -nv <target> 5060
    ```
* **Web Bugs Found:**
  * **Exposed Web PBX Admin Panels:** Discovering SIP servers often leads directly to co-hosted web interfaces (FreePBX, 3CX, Elastix) vulnerable to default credentials, SQLi, or RCE.
  * **SIP Header Injection via Click-to-Call:** Web applications offering "Click-to-Call" forms that pass unvalidated phone numbers into backend SIP `INVITE` headers.

##### 2. RTP (Dynamic 16384–32767) & RTSP (Port 554)

* **How it is audited (Ubuntu & Termux):**
  * **Unauthenticated Stream Discovery:** Testing RTSP endpoints for default stream paths (`/live.sdp`, `/h264`, `/stream1`) that allow viewing live feeds without credentials.
  * **Additional Auditing Commands:**
    ```bash
    # Brute-force common RTSP stream URLs and check methods via Nmap
    nmap -sT -p 554 --script rtsp-methods,rtsp-url-brute <target>

    # Test an RTSP stream endpoint using curl DESCRIBE request (Ubuntu & Termux)
    curl -i -X DESCRIBE rtsp://<target>:554/stream1

    # Capture a single frame from an unauthenticated RTSP stream using ffmpeg
    ffmpeg -i rtsp://<target>:554/stream1 -frames:v 1 frame_audit.jpg
    ```
* **Web Bugs Found:**
  * **Unauthenticated IP Camera Feeds & Path Traversal:** Web-based surveillance portals exposing raw RTSP URLs in frontend HTML/JS source code without token authentication, or web servers vulnerable to path traversal on `/stream/` endpoints.

##### 3. WebRTC (Dynamic)

* **How it is audited (Ubuntu & Termux):**
  * **STUN/TURN Configuration & SDP Inspection:** Analyzing Session Description Protocol (SDP) offers/answers and TURN server credentials embedded in web application JavaScript.
  * **Additional Auditing Commands:**
    ```bash
    # Check exposed STUN/TURN ports (3478, 5349) via Nmap
    nmap -sT -sV -p 3478,5349 --script stun-info <target>
    ```
* **Web Bugs Found:**
  * **TURN Server SSRF / Internal Network Pivoting:** Misconfigured TURN relay servers that allow authenticated (or anonymous) web users to relay traffic to `127.0.0.1` or internal cloud metadata IPs (`169.254.169.254`).
  * **Hardcoded TURN Credentials in Frontend JS:** Leaking static `username` and `credential` strings for TURN servers inside client-side WebRTC JavaScript bundles.

---

### 2. Security Auditing & Web Vulnerabilities (Section 8: IoT & Industrial Protocols)

In authorized penetration testing and bug bounty hunting, IoT and message-queuing protocols frequently back modern web dashboards, mobile apps, and microservices.

#### Environment Differences: Ubuntu vs. Termux

* **Ubuntu:** Full support for `mosquitto-clients`, `libcoap` (`coap-client`), Python `pika`/`aiocoap`, and `nmap` IoT NSE scripts.
* **Termux:** `mosquitto` (includes `mosquitto_sub`/`mosquitto_pub`), Python `aiocoap`, `pika`, and `curl` install natively via `pkg` and `pip` without root.

#### Protocol-by-Protocol Breakdown

##### 1. MQTT (Ports 1883, 8883)

* **How it is audited (Ubuntu & Termux):**
  * **Anonymous Broker Access & Wildcard Subscription:** Connecting to port 1883 without credentials and subscribing to `#` (all topics) to monitor live telemetry and command messages.
  * **Additional Auditing Commands:**
    ```bash
    # Check if MQTT broker allows unauthenticated connections via Nmap
    nmap -sT -p 1883,8883 --script mqtt-subscribe <target>

    # Subscribe to all topics (#) anonymously using mosquitto_sub (Ubuntu & Termux)
    mosquitto_sub -h <target> -p 1883 -t '#' -v

    # Test publishing a benign audit message to a topic
    mosquitto_pub -h <target> -p 1883 -t 'test/audit' -m 'ping'
    ```
* **Web Bugs Found:**
  * **MQTT-over-WebSockets Exposure & Stored XSS:** Many IoT web dashboards connect to MQTT over WebSockets (commonly port `8083` or `9001`). Subscribing anonymously often leaks user session tokens, GPS locations, or device API keys, while publishing crafted payloads can trigger Stored XSS in admin web panels.

##### 2. CoAP (Port 5683 - UDP)

* **How it is audited (Ubuntu & Termux):**
  * **Resource Discovery (`.well-known/core`):** Querying the standard CoAP discovery endpoint to list all exposed sensor routes and supported methods (`GET`, `PUT`, `POST`).
  * **Additional Auditing Commands:**
    ```bash
    # Query available CoAP endpoints on Ubuntu (requires root for UDP Nmap)
    sudo nmap -sU -p 5683 --script coap-resources <target>

    # Query .well-known/core using Python aiocoap-client (works on Ubuntu & Termux)
    aiocoap-client coap://<target>:5683/.well-known/core

    # Query using libcoap coap-client (Ubuntu)
    coap-client -m get coap://<target>:5683/.well-known/core
    ```
* **Web Bugs Found:**
  * **HTTP-to-CoAP Proxy SSRF:** Web gateways that translate incoming HTTP REST requests into backend CoAP UDP packets without validating target URIs, allowing attackers to scan or control internal constrained devices.

##### 3. AMQP (Port 5672)

* **How it is audited (Ubuntu & Termux):**
  * **Default Credentials & Management UI Checks:** Testing for default `guest:guest` credentials on port 5672 and checking for exposed RabbitMQ HTTP management plugins on port `15672`.
  * **Additional Auditing Commands:**
    ```bash
    # Enumerate AMQP server properties and authentication mechanisms via Nmap
    nmap -sT -sV -p 5672 --script amqp-info <target>

    # Probe the RabbitMQ Web Management API on port 15672 using default credentials
    curl -i -u guest:guest http://<target>:15672/api/overview
    ```
* **Web Bugs Found:**
  * **Exposed RabbitMQ Web Management Dashboard (`15672`):** Finding an internet-facing RabbitMQ web UI with default or weak credentials grants full visibility into queued web application background jobs (password reset tokens, payment webhooks, internal API secrets) and often allows arbitrary message injection.

