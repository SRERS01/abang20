Here is Module 1 of your complete 7-Layer OSI Model Security & Protocol Auditing Course, starting from the bottom up (Layer 1: Physical Layer).
We will cover one layer at a time in full copy-pasteable Markdown. Once you review and confirm you are ready, we will move on to Layer 2 (Data Link Layer).
markdown
# Complete 7-Layer OSI Model Course: Protocols & Security Auditing Tools

## Overview of the 7 OSI Layers

| Layer | Name | Data Unit (PDU) | Core Function |
| :--- | :--- | :--- | :--- |
| **7** | Application | Data / Message | End-user network services & web APIs |
| **6** | Presentation | Data | Encryption, encoding, & compression (TLS/SSL) |
| **5** | Session | Data | Session establishment, state, & teardown |
| **4** | Transport | Segment / Datagram | End-to-end delivery & ports (TCP/UDP) |
| **3** | Network | Packet | Logical addressing & routing (IP, ICMP) |
| **2** | Data Link | Frame | Physical MAC addressing & switching (Ethernet, ARP, Wi-Fi) |
| **1** | Physical | Bits (`1`s and `0`s) | Electrical, optical, or radio transmission over hardware |

---

# Module 1: Layer 1 — Physical Layer

### 1. Core Purpose
The Physical Layer transmits raw bitstreams (`1`s and `0`s) over a physical medium—such as copper cables, fiber-optic strands, or radio frequency (RF) waves. It defines voltage levels, physical connectors, pinouts, modulation, and signal timing, without understanding packets, IP addresses, or MAC addresses.

---

### 2. Layer 1 Protocols, Standards & Technologies

| Standard / Protocol | Medium | Purpose & Security Relevance |
| :--- | :--- | :--- |
| **IEEE 802.3 (10BASE-T / 100BASE-TX / 1000BASE-T)** | Copper (Twisted Pair / RJ45) | Defines electrical signaling, duplex modes, and auto-negotiation over Ethernet cables. |
| **IEEE 802.11 PHY (FHSS, DSSS, OFDM)** | Radio Frequency (Wi-Fi) | Defines physical radio modulation, channels (2.4 GHz, 5 GHz, 6 GHz), and signal strength. |
| **IEEE 802.15.1 (Bluetooth PHY)** | Radio Frequency (2.4 GHz) | Short-range wireless frequency-hopping physical transmission. |
| **IEEE 802.15.4 (Zigbee / Thread PHY)** | Radio Frequency | Low-power wireless physical signaling used in IoT and smart home sensors. |
| **RS-232 / UART / SPI / I2C** | Serial Copper Pins | Hardware-level serial interfaces used on routers, IoT boards, and embedded devices. |
| **SONET / SDH / OTN** | Fiber Optic | High-speed optical light-pulse signaling across backbone networks. |
| **DSL / DOCSIS (PHY)** | Telephone / Coaxial Cable | Modulates digital bits over analog phone or cable TV lines. |

---

### 3. Layer 1 Testing & Auditing Tools (Ubuntu & Termux)

Because Layer 1 deals with hardware interfaces, link states, cable speeds, and radio signals, auditing focuses on **link negotiation, hardware detection, RF spectrum/signal strength, and serial hardware interfaces**.

#### Environment Notes: Ubuntu vs. Termux
* **Ubuntu:** Full access to PCIe/USB hardware interfaces (`ethtool`, `iwconfig`, `minicom`, `rtl_433`) with `sudo`.
* **Termux:** Cannot directly manipulate Android's internal Wi-Fi chip or Ethernet PHY without root, though `termux-wifi-scaninfo` (via `Termux:API`) can inspect surrounding RF signal levels (RSSI) and channels.

#### Testing Tools & Commands

| Tool | Target Standard | Auditing Purpose |
| :--- | :--- | :--- |
| **`ethtool`** | IEEE 802.3 (Ethernet) | Inspects physical link status, duplex mode, cable speed, and hardware driver capabilities. |
| **`ip link`** | Physical Interfaces | Checks whether hardware network interfaces are physically connected (`LOWER_UP`). |
| **`iw` / `iwconfig`** | IEEE 802.11 (Wi-Fi PHY) | Audits wireless frequency, channel width, TX power, and physical signal quality (dBm). |
| **`minicom` / `screen`** | UART / RS-232 Serial | Connects to exposed hardware serial pins on routers/IoT devices to access root boot consoles. |
| **`rtl_433` / `gqrx`** | Sub-GHz RF / SDR | Captures and demodulates raw radio signals from wireless sensors, key fobs, and IoT devices. |
| **`termux-wifi-scaninfo`** | Android Wi-Fi PHY | Lists visible RF access points, frequencies, channel widths, and RSSI signal strength in Termux. |

#### Copy-Pasteable Auditing Commands

```bash
# 1. Check physical link state (LOWER_UP means cable/signal is physically connected)
ip link show

# 2. Inspect physical Ethernet speed, duplex, and auto-negotiation (Ubuntu)
sudo ethtool eth0

# 3. Inspect physical Wi-Fi radio frequency, channel, and signal strength (Ubuntu)
iw dev wlan0 link
iw dev wlan0 scan | grep -E "SSID|freq|signal"

# 4. Connect to an exposed hardware UART/Serial debug port via USB-to-TTL adapter (Ubuntu)
sudo screen /dev/ttyUSB0 115200

# 5. Scan physical Wi-Fi RF channels and signal strength on Android (Termux + Termux:API)
termux-wifi-scaninfo
```

---

### 4. Security Vulnerabilities at Layer 1
* **Exposed UART / JTAG Debug Ports:** IoT devices and routers often leave physical serial pins (`TX`, `RX`, `GND`) active on the PCB, granting unauthenticated root shell access during boot.
* **Rogue Physical Connections / Tap Devices:** Unauthorized hardware implants (e.g., LAN Turtle, Packet Squirrel) plugged into exposed Ethernet wall jacks.
* **RF Jamming & Signal Leakage:** Denial-of-service via radio interference or sensitive wireless signals bleeding outside building perimeters.
* **Cable Tapping / Unshielded Crosstalk:** Passive interception of unencrypted signals on poorly shielded copper lines.
Use code with caution.
