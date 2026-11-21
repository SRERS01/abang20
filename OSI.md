# Comprehensive List of Protocols Across the 7 OSI Layers

## Layer 7: Application Layer
*Provides network services directly to end-user applications and software.*
* **Web & File Transfer:** HTTP, HTTPS, FTP, FTPS, SFTP, TFTP, WebDAV, BitTorrent, Gopher
* **Email:** SMTP, POP3, IMAP, X.400
* **Directory & Naming:** DNS, mDNS, LDAP, Active Directory, NIS, WHOIS
* **Network Management & Monitoring:** SNMP, Syslog, NetFlow, IPFIX, RMON, NTP, PTP
* **Remote Access & Terminal:** Telnet, SSH, RDP, VNC, X11
* **Host Configuration:** DHCP, DHCPv6, BOOTP
* **Authentication & Security:** Kerberos, RADIUS, TACACS+, Diameter, OAuth
* **Messaging & Real-Time:** XMPP, IRC, MQTT, AMQP, CoAP, RTSP, RTP, RTCP, NNTP
* **Industrial / IoT / Specialized:** Modbus, BACnet, DNP3, HL7, FIX

---

## Layer 6: Presentation Layer
*Handles data translation, character encoding, compression, and encryption.*
* **Encryption & Security:** SSL, TLS, PGP, S/MIME, X.509 (Certificates)
* **Character Encoding & Syntax:** ASCII, EBCDIC, Unicode (UTF-8, UTF-16), ASN.1, XDR, JSON, XML
* **Data Compression:** GZIP, Brotli, LZW, DEFLATE
* **Multimedia & Formatting Standards:** MIME, JPEG, PNG, GIF, TIFF, MPEG, MP3, MP4, MIDI, QuickTime

---

## Layer 5: Session Layer
*Establishes, synchronizes, manages, and terminates communication sessions.*
* **Session Control & Signaling:** SIP, H.323, H.245, RTCP, SDP
* **Remote Procedure & APIs:** RPC, gRPC, NetBIOS, WinSock, Named Pipes, AppleTalk (ASP, PAP, ZIP)
* **Tunneling & Session Establishment:** PPTP, L2TP, SOCKS, PAP, CHAP, EAP
* **File & Printer Sharing Sessions:** SMB/CIFS, NFS, AFP

---

## Layer 4: Transport Layer
*Manages end-to-end delivery, segmentation, flow control, and error recovery.*
* **Core Internet Protocols:** TCP, UDP
* **Modern & Specialized Transport:** QUIC, SCTP, DCCP, RDP (Reliable Data Protocol)
* **Legacy & Proprietary Transport:** SPX (Novell IPX/SPX), ATP (AppleTalk), NBF (NetBEUI), ISO TP0–TP4, FCP (Fibre Channel Protocol)

---

## Layer 3: Network Layer
*Handles logical addressing, path determination (routing), and packet forwarding.*
* **Routed Protocols (Addressing):** IPv4, IPv6, IPX (Novell), AppleTalk (DDP), CLNP (OSI), X.25 (PLP)
* **Interior Gateway Routing Protocols (IGP):** RIP (v1/v2/ng), OSPF (v2/v3), EIGRP, IGRP, IS-IS
* **Exterior Gateway Routing Protocols (EGP):** BGP, EGP
* **Control, Diagnostic & Multicast:** ICMP, ICMPv6, IGMP, MLD, PIM, DVMRP, MSDP
* **Tunneling, Security & Redundancy:** IPsec (AH & ESP), GRE, MPLS*, VRRP, HSRP, GLBP, NHRP, NAT*

---

## Layer 2: Data Link Layer
*Manages physical (MAC) addressing, framing, media access control, and local error detection.*
* **LAN & Wireless Standards:** Ethernet (IEEE 802.3), Wi-Fi (IEEE 802.11), Token Ring (IEEE 802.5), FDDI, Zigbee (IEEE 802.15.4), Bluetooth (L2CAP/Baseband)
* **WAN & Point-to-Point:** PPP, PPPoE, PPPoA, HDLC, SDLC, Frame Relay, ATM, X.25 (LAPB), ISDN (LAPD), SLIP
* **Switching, VLANs & Loop Prevention:** IEEE 802.1Q (VLAN), STP, RSTP, MSTP, PVST+, VTP, DTP, LACP, PAgP
* **Discovery & Address Resolution:** ARP, RARP, NDP (Neighbor Discovery Protocol), CDP, LLDP, FDP
* **Industrial & Automotive:** CAN bus, Profibus, EtherCAT

---

## Layer 1: Physical Layer
*Defines electrical, optical, and radio specifications for transmitting raw bits.*
* **Wired Ethernet & Copper:** 10BASE-T, 100BASE-TX, 1000BASE-T, 10GBASE-T, Cat5e/Cat6/Cat6a/Cat8, Coaxial
* **Optical Fiber:** SONET, SDH, OTN, 1000BASE-SX/LX, 10GBASE-SR/LR, Fibre Channel (FC-0/FC-1)
* **Wireless & Radio:** IEEE 802.11 PHY (FHSS, DSSS, OFDM), Bluetooth PHY, NFC, RFID, LoRa, LTE/5G NR PHY
* **Serial, Telecom & Broadband:** USB, RS-232, RS-422, RS-485, DSL (ADSL, VDSL), DOCSIS, T1/E1, T3/E3, ISDN (BRI/PRI), IrDA, Thunderbolt, HDMI

---
*\*Note: Some protocols operate across layer boundaries (often called "Layer 2.5" or "Layer 3.5"), such as **MPLS** (Layers 2/3), **ARP** (Layers 2/3), and **TLS** (Layers 5/6/7).*
