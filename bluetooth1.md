# Practical Security+ Lab: Bluetooth Discovery, Pairing, File Sharing & Hardening
**Target System:** Ubuntu Linux (`user-Latitude-3380` | Controller `74:40:BB:43:CF:EE`)  
**Syllabus Alignment:** Domain 2 (Objective 2.4 – Low-Powered Communication & Wireless Threats: Bluesnarfing, Bluejacking, Bluebugging, MITM Pairing) & Domain 4 (Objective 4.1 – System Hardening & Attack Surface Reduction)

---

## Phase 1: Enable & Power On the Bluetooth Controller
Unblock the kernel radio kill switch (`rfkill`), start the `bluez` daemon, and power on `hci0`:

```bash
# 1. Check radio block status
rfkill list

# 2. Unblock Bluetooth radio and start the systemd service
sudo rfkill unblock bluetooth
sudo systemctl start bluetooth

# 3. Power on the local HCI controller
bluetoothctl power on
```

---

## Phase 2: Why Non-Interactive Scans Purge Unpaired BLE Devices
When you run `bluetoothctl --timeout 10 scan on`, `bluez` discovers nearby devices during the 10-second window, **but automatically purges unpaired temporary BLE devices from its cache the instant the scan exits**:

```text
[CHG] Controller 74:40:BB:43:CF:EE Discovering: yes
[NEW] Device 54:09:8A:7E:B6:31 54-09-8A-7E:B6:31
[NEW] Device 4F:2A:37:08:68:83 4F:2A:37:08:68:83
# Once --timeout 10 finishes, running `bluetoothctl info <MAC>` returns "not available"
```

* **Security Insight:** Modern phones and wearables broadcast **Resolvable Private Addresses (RPAs)**—randomized BLE MAC addresses that rotate roughly every 15 minutes to prevent physical tracking. To inspect or pair with a device, you must interact with it **inside an active `bluetoothctl` session while scanning is running** (and set the target phone/device to visible/discoverable in its Bluetooth settings).

---

## Phase 3: Interactive Discovery, Secure Pairing & Trust Bonding
To share files or exchange data between your Latitude 3380 and an authorized test phone/device, establish a **Secure Simple Pairing (SSP)** bond inside `bluetoothctl`:

### 1. Open `bluetoothctl` and Start Discovery
```bash
bluetoothctl
```
Inside the `[bluetooth]#` prompt, enable the pairing agent and scan:
```text
agent on
default-agent
scan on
```
*(Ensure your test phone's Bluetooth settings screen is open so it broadcasts its Classic/BR-EDR MAC address).*

### 2. Inspect, Pair, Trust & Connect While Scanning
Once your test device appears (`[NEW] Device <TARGET_MAC> <Device_Name>`), inspect its profiles and initiate pairing:
```text
devices
info <TARGET_MAC>
pair <TARGET_MAC>
```
* **Security Verification (Numeric Comparison):** Both your Ubuntu terminal (`Confirm passkey 123456 (yes/no):`) and your phone screen will display a **6-digit passkey**. Verify the numbers match identically before typing `yes` (this prevents Man-in-the-Middle pairing attacks).

### 3. Mark Device as Trusted, Connect & Stop Scanning
```text
trust <TARGET_MAC>
connect <TARGET_MAC>
scan off
exit
```

---

## Phase 4: Sharing Information Over Bluetooth (OBEX File Transfer & BLE GATT)

Once two devices are paired and connected, they share data over specific Bluetooth profiles:

### Method A: Classic Bluetooth File Sharing via OBEX (`obexftp` / `bluetooth-sendto`)
**OBEX (Object Exchange)** is the standard protocol used to push/receive files between paired computers and smartphones:

```bash
# 1. Install OBEX tools if not already present
sudo apt update && sudo apt install -y obexftp bluez-obexd

# 2. Create a sample test file to share
echo "SecPlus Lab Verified Bluetooth Transfer - $(date)" > ~/bluetooth_test_note.txt

# 3. Send the file to your paired device via GUI/OBEX prompt
bluetooth-sendto --device=<TARGET_MAC> ~/bluetooth_test_note.txt
```
*(Accept the incoming file transfer prompt on your paired device to complete the encrypted RFCOMM/OBEX transfer).*

### Method B: Inspecting Shared BLE GATT Characteristics (Low-Energy Sensors/IoT)
For Bluetooth Low Energy (**BLE**) devices (smartwatches, fitness trackers, IoT beacons), data is shared via **GATT (Generic Attribute Profile)** Services and Characteristics rather than OBEX files:

```bash
bluetoothctl
```
Inside `[bluetooth]#` while connected to a BLE peripheral:
```text
menu gatt
list-attributes <TARGET_MAC>
# Example: Read a specific characteristic UUID (e.g., Battery Level 00002a19-...)
# select-attribute /org/bluez/hci0/dev_XX_XX_XX_XX_XX_XX/service0010/char0011
# read
back
exit
```

---

## Phase 5: Security Audit of Paired Bonds & Post-Lab Hardening

Unmonitored Bluetooth bonds and active radios expose systems to **Bluejacking** (unsolicited messages), **Bluesnarfing** (unauthorized data theft via OBEX), and **Bluebugging** (unauthorized AT/command execution).

### 1. Audit & Remove Temporary Lab Bonds
Never leave test pairings stored permanently on a workstation:
```bash
bluetoothctl paired-devices
bluetoothctl remove <TARGET_MAC>
```

### 2. Disable Discovery/Pairing, Power Off & Re-Block Radio
```bash
# Disable discoverable/pairable flags and power off controller
bluetoothctl discoverable off
bluetoothctl pairable off
bluetoothctl power off

# Re-apply kernel-level rfkill soft block
sudo rfkill block bluetooth

# Verify hardened state (Soft blocked: yes)
rfkill list | grep -A 2 -i bluetooth
```

---

## Lab Completion Checklist
- [ ] Unblocked `hci0` (`sudo rfkill unblock bluetooth`) and started `bluetoothd`.
- [ ] Discovered and inspected live devices inside an interactive `bluetoothctl` session (`scan on` $\rightarrow$ `info <MAC>`).
- [ ] Completed **Secure Simple Pairing (SSP)** with 6-digit passkey verification (`pair` $\rightarrow$ `trust` $\rightarrow$ `connect`).
- [ ] Successfully shared data via **OBEX (`bluetooth-sendto`)** and reviewed **BLE GATT** attribute inspection.
- [ ] Removed the test pairing (`bluetoothctl remove`), powered off `hci0`, and re-blocked Bluetooth (`sudo rfkill block bluetooth`).
