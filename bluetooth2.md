# Practical Security+ Lab: Wi-Fi Wireless Security Assessment
**Target System:** Ubuntu Linux (`user-Latitude-3380` | Wireless Radio `phy0`)  
**Syllabus Alignment:** Domain 2 (Objective 2.4 – Wireless & RF Vulnerabilities: Evil Twin, Rogue AP, Weak Encryption, Deauth) & Domain 4 (Objective 4.1 – WIPS, WPA3/SAE, 802.1X, MAC Randomization)  
**Authorization Note:** Passive RF scanning (`nmcli`, `iw`) is completely passive and safe. Never perform active deauthentication attacks against networks you do not own.

---

## Phase 1: Inspect Local Wireless Interface & MAC Randomization Posture

Before scanning surrounding Access Points (APs), verify your wireless interface name, driver status, and whether **MAC Address Randomization** is active to prevent passive physical tracking across Wi-Fi hotspots.

```bash
# 1. Identify your wireless network interface name (e.g., wlp1s0 or wlan0)
nmcli device status | grep wifi

# 2. Check current Wi-Fi radio state and hardware capabilities
nmcli radio wifi
iw dev

# 3. Inspect current MAC address vs. permanent hardware MAC address
WIFI_IFACE=\$(nmcli -t -f DEVICE,TYPE device | awk -F: '\$2=="wifi"{print \$1; exit}')
echo "Active Wi-Fi Interface: \$WIFI_IFACE"
ip link show "\$WIFI_IFACE" | grep "link/ether"
```

### Enable Wi-Fi MAC Randomization During Scanning (Privacy Hardening)
NetworkManager supports automatic MAC randomization while scanning for networks so nearby APs and retail trackers cannot log your permanent hardware OUI:

```bash
# Verify NetworkManager Wi-Fi scan MAC randomization policy
nmcli -f 802-11-wireless.mac-address-randomization connection show "\$(nmcli -t -f NAME connection show --active | head -n 1)" 2>/dev/null || \
  echo "Tip: Set 'wifi.scan-rand-mac-address=yes' in /etc/NetworkManager/NetworkManager.conf"
```

---

## Phase 2: Passive Wireless Discovery (SSID, BSSID, Channel & Signal Audit)

Trigger a fresh passive beacon scan and inspect all nearby Access Points, including hidden networks (`--`), BSSIDs (AP radio MAC addresses), operating bands (`2.4 GHz` vs. `5 GHz`), channels, signal strength, and security protocols:

```bash
# 1. Force a fresh scan of surrounding Wi-Fi beacons
nmcli device wifi rescan

# 2. Display detailed wireless security table
nmcli -f IN-USE,SSID,BSSID,MODE,CHAN,FREQ,RATE,SIGNAL,BARS,SECURITY device wifi list
```

### How to Interpret Each Column as a Security Analyst

| Field | Security & Assessment Meaning |
| :--- | :--- |
| **`SSID`** | Network name broadcast in 802.11 management beacons. Blank/`--` indicates a **Hidden SSID** *(Security through obscurity—still visible in probe requests/responses)*. |
| **`BSSID`** | Unique 48-bit MAC address of the specific Access Point radio. Crucial for spotting **Rogue APs** and **Evil Twins**. |
| **`CHAN` & `FREQ`** | `2.4 GHz` (`Channels 1–14`) travels farther through walls (larger external attack surface); `5 GHz` (`Channels 36–165`) has shorter range and less congestion. |
| **`SIGNAL`** | Percentage/dBm strength. An unexpectedly high signal (`90–100%`) on an unfamiliar BSSID may indicate an attacker sitting physically close with a portable hotspot. |
| **`SECURITY`** | Encryption and authentication suite (`--` / Open, `WEP`, `WPA1`, `WPA2`, `WPA3`, `802.1X`). |

---

## Phase 3: Encryption & Authentication Suite Audit (WPA2 vs. WPA3 vs. Legacy)

Evaluate every discovered Access Point against modern enterprise and home cryptographic standards:

| Security Protocol | Cryptographic Mechanism | Security+ Risk Assessment |
| :--- | :--- | :--- |
| **`--` (Open) / `WEP` / `WPA (TKIP)`** | Cleartext traffic or broken RC4/CRC-32 ciphers. | **CRITICAL:** Passwords cracked in seconds (`WEP`) or traffic sniffed passively in plaintext (`Open` without OWE). |
| **`WPA2-Personal (PSK / AES-CCMP)`** | Pre-Shared Key using 4-Way Handshake + AES-CCMP. | **MODERATE:** Strong encryption *if* passphrase is 16+ chars, **but** vulnerable to offline dictionary cracking of captured 4-Way Handshakes (`PMKID`/EAPOL) and deauth floods. |
| **`WPA2-Enterprise (802.1X / EAP)`** | Individual user/certificate authentication via **RADIUS** server. | **STRONG:** Eliminates shared PSK risk; requires **PEAP** or **EAP-TLS** with strict server certificate validation to prevent Evil Twin credential theft. |
| **`WPA3-Personal (SAE)`** | **Simultaneous Authentication of Equals** (Dragonfly handshake) + mandatory **Protected Management Frames (PMF / 802.11w)**. | **HIGH:** Immune to offline dictionary cracking of captured handshakes, provides **Forward Secrecy**, and blocks unauthenticated deauthentication frames. |
| **`WPA3-Enterprise (192-bit)`** | CNSA-grade 192-bit cryptographic suite + mandatory PMF. | **HIGHEST:** Recommended for government, financial, and high-security enterprise networks. |

---

## Phase 4: Automated Evil Twin & Weak Encryption Audit Script (Python)

An **Evil Twin** attack occurs when an adversary sets up a rogue Access Point broadcasting the **exact same `SSID`** as a legitimate corporate or café network, **but with a different `BSSID` (MAC address)**, often on a different channel or downgraded security mode (`Open` or `WPA2` instead of `WPA3`/`802.1X`), to trick victims into connecting and capturing credentials.

Run this Python script on your Latitude 3380 to parse live `nmcli` scan output and flag **Weak Encryption**, **Open Networks**, and **Duplicate SSIDs (Potential Evil Twins)**:

```bash
mkdir -p ~/wireless_labs && cd ~/wireless_labs

cat << 'EOF' > wifi_security_auditor.py
import subprocess
from collections import defaultdict

# Query live Wi-Fi scan results from NetworkManager in machine-readable terse format
cmd = ["nmcli", "-t", "-f", "SSID,BSSID,CHAN,SIGNAL,SECURITY", "device", "wifi", "list"]
output = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)

ssid_map = defaultdict(list)
weak_aps = []

for line in output.strip().splitlines():
    # Escape escaped colons (\:) inside BSSID MAC addresses before splitting
    parts = line.replace("\\:", "-").split(":")
    if len(parts) < 5:
        continue
    ssid, bssid, chan, signal, security = parts, parts.replace("-", ":"), parts, parts, parts
    display_ssid = ssid if ssid else "<HIDDEN_SSID>"

    if ssid:
        ssid_map[ssid].append({"bssid": bssid, "chan": chan, "signal": signal, "security": security})

    sec_upper = security.upper()
    if not security or security == "--":
        weak_aps.append((display_ssid, bssid, "OPEN / UNENCRYPTED (High Sniffing & MITM Risk)"))
    elif "WEP" in sec_upper or "TKIP" in sec_upper or ("WPA1" in sec_upper and "WPA2" not in sec_upper):
        weak_aps.append((display_ssid, bssid, f"LEGACY WEAK CIPHER ({security})"))

print("=== 1. WEAK / UNENCRYPTED ACCESS POINT AUDIT ===")
if not weak_aps:
    print("  [PASS] No Open, WEP, or TKIP networks detected nearby.")
else:
    for ssid, bssid, issue in weak_aps:
        print(f"  [ALERT] SSID: {ssid:<22} | BSSID: {bssid} | {issue}")

print("\n=== 2. DUPLICATE SSID / EVIL TWIN ANOMALY CHECK ===")
duplicates_found = False
for ssid, aps in ssid_map.items():
    if len(aps) > 1:
        duplicates_found = True
        sec_modes = {ap["security"] for ap in aps}
        flag = " [SECURITY MISMATCH - HIGH EVIL TWIN RISK!]" if len(sec_modes) > 1 else " [Verify Mesh vs. Rogue AP]"
        print(f"  [MULTI-BSSID] SSID '{ssid}' broadcast by {len(aps)} radios:{flag}")
        for ap in aps:
            print(f"     -> BSSID: {ap['bssid']} | Ch: {ap['chan']:<3} | Signal: {ap['signal']}% | Sec: {ap['security']}")

if not duplicates_found:
    print("  [PASS] No duplicate SSIDs detected in current scan window.")
EOF

python3 wifi_security_auditor.py
```

---

## Phase 5: Saved Wireless Profile Audit & Post-Lab Hardening

Attackers also exploit **Preferred Network Lists (PNLs)**—if your laptop previously connected to an open Wi-Fi network (`Free_Airport_WiFi`) with `autoconnect=yes`, your laptop continuously broadcasts probe requests looking for it, allowing an attacker to spin up a matching **Karma / Evil Twin** hotspot anywhere.

### 1. Audit Saved Wi-Fi Profiles & Auto-Connect Settings
```bash
# List all saved Wi-Fi connection profiles
nmcli -f NAME,TYPE,AUTOCONNECT connection show | grep wifi
```

### 2. Harden Saved Profiles (Disable Auto-Connect on Untrusted Networks)
```bash
# Example: Disable auto-connect on any public/untrusted saved profile
# nmcli connection modify "<UNTRUSTED_SSID_NAME>" connection.autoconnect no
```

### 3. Verify Wireless IPS (WIPS) & Enterprise Mitigations
* **Wireless IPS (WIPS):** Enterprise sensors continuously scan `2.4/5/6 GHz` channels to detect unauthorized **Rogue APs** connected to corporate switch ports and automatically contain **Evil Twins**.
* **802.11w (Protected Management Frames — PMF):** Mandatory in **WPA3**; cryptographically signs deauthentication and disassociation frames to defeat Wi-Fi deauth DoS floods.
* **Client VPN + HTTPS:** Always enable a full-tunnel **VPN** when connecting to public or untrusted Wi-Fi networks to protect traffic against on-path sniffing.

---

## Lab Completion Checklist
- [ ] Audited local wireless interface (`nmcli device status`, `iw dev`) and verified MAC randomization settings.
- [ ] Executed a passive beacon scan (`nmcli device wifi list`) analyzing **SSID, BSSID, Channel, Frequency, Signal, and Security**.
- [ ] Contrasted **Open, WEP, WPA2-PSK, WPA2-Enterprise (802.1X), and WPA3-SAE (PMF)** security properties.
- [ ] Ran `wifi_security_auditor.py` to detect weak encryption and multi-BSSID **Evil Twin** anomalies.
- [ ] Audited saved Wi-Fi `autoconnect` profiles to mitigate Karma/Preferred Network List spoofing.
