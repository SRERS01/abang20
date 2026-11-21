# Complete Termux Setup Guide: Networking, Programming & Security Research

If you install Termux fresh from F-Droid, it is best to set it up in one organized installation rather than installing packages individually.

This guide configures Termux as a Linux networking, programming, SSH, and authorized offensive-security research environment.

### What This Setup Includes
* Linux command-line utilities
* Networking and port investigation
* SSH client and server
* DNS and web diagnostics
* Python development (isolated with `venv`)
* Git and source-code analysis
* Termux Android API integration
* System and process diagnostics

> **Important Note:** Termux is an Android-based Linux environment, not a complete Ubuntu installation. Some kernel and network operations remain restricted without root.

---

### 1. Prepare Fresh Termux

Open your newly installed Termux and run:

```bash
pkg update
pkg upgrade -y
```

If the mirror selection screen appears, select a working mirror for the Main repository. You can change it later with:

```bash
termux-change-repo
```

*Tip: The official Termux documentation recommends changing mirrors if the current repository is unavailable or under maintenance.*

---

### 2. Install the Complete Networking and Linux Toolkit

Copy and run this entire command:

```bash
pkg install -y \
openssh \
nmap \
net-tools \
iproute2 \
inetutils \
dnsutils \
curl \
wget \
netcat-openbsd \
lsof \
procps \
termux-api \
git \
python \
clang \
make \
cmake \
pkg-config \
openssl-tool \
termux-tools \
nano \
vim \
man \
zip \
unzip \
tar \
rsync \
jq \
coreutils \
findutils \
grep \
sed \
gawk \
less \
tree \
htop
```

#### Installed Toolkit Breakdown

| Area | Tools |
| :--- | :--- |
| **Remote access** | SSH, SSHD |
| **Port scanning** | Nmap, Netcat |
| **Network diagnostics** | IProute2, Net-tools, Inetutils |
| **DNS** | Dig, Nslookup |
| **Web investigation** | Curl, Wget |
| **Process investigation** | PS, Lsof, Htop |
| **Programming** | Python, Clang, Make, CMake |
| **Source-code management** | Git |
| **Encryption** | OpenSSL |
| **File investigation** | Find, Grep, Sed, JQ |
| **File management** | Tar, Zip, Unzip, Rsync |
| **Android integration** | Termux:API |

> **About `iputils`:** Do not include `iputils` in this installation. Termux repositories do not provide it as a standard standalone package; `inetutils` provides an alternative `ping` implementation.

---

### 3. Set Up Python & Virtual Environment (`myvenv`)

Verify your Python installation:

```bash
python --version
```

Create a virtual environment named `myvenv` and activate it:

```bash
python -m venv myvenv
source myvenv/bin/activate
```

*(Your terminal prompt should now show `(myvenv)` at the beginning. Whenever you open a new Termux session, run `source ~/myvenv/bin/activate` to re-enter it.)*

Upgrade `pip` inside `myvenv` and install the security research libraries:

```bash
pip install --upgrade pip
pip install requests beautifulsoup4 dnspython rich ipython
```

#### What These Libraries Support
* **`requests`**: HTTP requests and web traffic analysis
* **`beautifulsoup4`**: HTML parsing and inspection
* **`dnspython`**: Advanced DNS investigation and record querying
* **`rich`**: Clean terminal output formatting and tables
* **`ipython`**: Interactive Python shell for rapid testing

*(To exit the virtual environment at any time, simply run `deactivate`.)*

---

### 4. Configure SSH

Generate an Ed25519 SSH key pair:

```bash
ssh-keygen -t ed25519
```

Set your Termux user password:

```bash
passwd
```

Start the SSH daemon (server):

```bash
sshd
```

Verify that `sshd` is running:

```bash
pgrep -a sshd
```

Test the local SSH port (`8022` is the default in Termux):

```bash
nc -zv 127.0.0.1 8022
```

---

### 5. Install the Termux:API Android Application

Installing the `termux-api` package inside the terminal is not enough on its own. You must also install the companion Android app:

* **App:** Termux:API (Android companion application)
* **Download:** [Get Termux:API from F-Droid](https://f-droid.org/packages/com.termux.api/)

> **Warning:** Install Termux:API from the **exact same source** as your main Termux app (e.g., F-Droid). Do not mix F-Droid and GitHub versions because their APK signing keys differ, which will prevent them from working together.

Once installed, grant storage access and test the API:

```bash
termux-setup-storage
termux-wifi-connectioninfo
```

Grant the requested Android permissions when prompted.

---

### 6. Verify Your Complete Installation

Run this diagnostic script to verify all core tools and paths:

```bash
echo "===== SYSTEM ====="
uname -a

echo "===== PYTHON ====="
python --version

echo "===== NETWORK TOOLS ====="
for tool in ssh sshd nmap nc ip ss \
netstat ifconfig ping dig curl wget \
lsof ps git openssl; do
    printf "%-12s" "\$tool"
    command -v "\$tool" || echo "NOT FOUND"
done

echo "===== SSH SERVER ====="
pgrep -a sshd

echo "===== STORAGE ====="
echo "\$HOME"

echo "===== TERMUX PREFIX ====="
echo "\$PREFIX"
```

---

### 7. Understand Termux Limitations

Even with a complete setup, Android enforces strict sandboxing on non-rooted devices:

| Capability | Normal (Unrooted) Termux |
| :--- | :--- |
| **SSH connections** | Yes |
| **TCP port scanning** | Yes (subject to Android restrictions) |
| **DNS investigation** | Yes |
| **HTTP/HTTPS testing** | Yes |
| **Python programming** | Yes |
| **Source-code analysis** | Yes |
| **Network interface inspection** | Partially restricted |
| **Raw packet capture (e.g., SYN scans)** | Restricted |
| **Changing Android firewall rules** | Generally requires root |
| **Kernel manipulation** | Requires root privileges |

---

### 8. Official Resources

* [Termux Official Website](https://termux.dev/)
* [Termux Package Repository (GitHub)](https://github.com/termux/termux-packages)
* [Termux Application Documentation (GitHub)](https://github.com/termux/termux-app)
* [Termux Wiki](https://wiki.termux.com/)

---

### Summary Recommendation
Start with this clean, well-structured baseline before adding specialized security tools. A properly configured environment with isolated dependencies (`myvenv`) is far more reliable than installing dozens of tools without understanding their system limitations. With this setup, your Android device serves as a portable Linux development and research workstation alongside a full desktop Linux environment like Ubuntu.
---

### 9. Appendix: How to Install F-Droid

Because the Google Play Store version of Termux is outdated and no longer receives updates due to Play Store policy restrictions, you should install both **Termux** and **Termux:API** through **F-Droid** (an open-source app repository for Android).

#### Step 1: Download the F-Droid APK
1. Open the web browser on your Android device (e.g., Chrome, Firefox, or Brave).
2. Go to the official F-Droid website: [https://f-droid.org](https://f-droid.org)
3. Tap the **"Download F-Droid"** button to download the `F-Droid.apk` installer file.

#### Step 2: Allow Installing Unknown Apps
Android blocks APK installations from web browsers by default for security:
1. Open the downloaded `F-Droid.apk` file from your browser's **Downloads** menu or your phone's **Files** app.
2. When prompted with *"For your security, your phone currently isn't allowed to install unknown apps from this source"*, tap **Settings**.
3. Toggle on **"Allow from this source"** (or *"Install unknown apps"*), then press the **Back** button.

#### Step 3: Install and Update Repositories
1. Tap **Install** to complete the F-Droid installation.
2. Open the **F-Droid** app from your app drawer.
3. Wait a moment on the main screen (or pull down to refresh) while F-Droid updates its package repositories.

#### Step 4: Install Termux & Termux:API
1. Tap the **Search** icon in the bottom-right corner of F-Droid.
2. Search for **Termux** (by Fredrik Fornwall) and tap **Install** *(you will need to allow F-Droid to install unknown apps the first time, just like in Step 2)*.
3. Search for **Termux:API** and tap **Install**.

> **Tip:** Open F-Droid periodically and check the **Updates** tab to keep both Termux and Termux:API up to date with the same matching cryptographic signatures.
