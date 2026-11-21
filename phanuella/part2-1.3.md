# CompTIA Security+ (SY0-701) – Practical Lab Guide
## Domain 1: General Security Concepts
### Objective 1.3: Cryptographic Solutions

> **Objective:** Implement and verify Public Key Infrastructure (PKI), symmetric/asymmetric encryption, data-at-rest and data-in-transit protections, hashing, salting, digital signatures, and key management practices.  
> **Recommended Lab Tools:** OpenSSL CLI (`openssl`), Python 3 (`hashlib`, `secrets`, `base64`), `gpg` (GnuPG), Linux Terminal / Windows PowerShell.

---

## Part A: Public Key Infrastructure (PKI)

### 1. Public Keys & 2. Private Keys
* **Concept:** Asymmetric cryptography uses a mathematically linked key pair:
  * **Public Key:** Shared openly with anyone; used to **encrypt** data sent to the key owner or **verify** the owner's digital signatures.
  * **Private Key:** Kept strictly secret by the owner; used to **decrypt** data encrypted with the public key or **create** digital signatures.
* **Practical Task (Generate an RSA-2048 Key Pair & Extract Public Key):**
  ```bash
  mkdir -p ~/secplus_crypto_lab && cd ~/secplus_crypto_lab

  # Generate a 2048-bit RSA Private Key
  openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
  chmod 600 private_key.pem

  # Derive the matching Public Key
  openssl rsa -pubout -in private_key.pem -out public_key.pem
  head -n 5 public_key.pem
  ```

### 3. Key Escrow
* **Concept:** Securely storing a copy of cryptographic decryption keys with an authorized trusted third party or corporate recovery agent (e.g., Active Directory BitLocker recovery keys) so encrypted business data can be recovered if an employee leaves or loses their key.
* **Practical Task (Simulate Split-Knowledge Key Escrow in Python):**
  ```python
  import secrets

  # Generate a 256-bit (32-byte) master recovery key and split it across two escrow officers (XOR split)
  master_key = secrets.token_bytes(32)
  officer_a_share = secrets.token_bytes(32)
  officer_b_share = bytes(a ^ b for a, b in zip(master_key, officer_a_share))

  # Reconstruct master key only when both escrow officers combine shares
  recovered_key = bytes(a ^ b for a, b in zip(officer_a_share, officer_b_share))
  print("Key Escrow Recovery Match:", master_key == recovered_key)
  ```

### 4. Certificate Authorities (CAs) & 9. Root of Trust
* **Concept:**
  * **Certificate Authority (CA):** A trusted entity (e.g., DigiCert, Let's Encrypt, or an internal Enterprise Root CA) that verifies identities and digitally signs X.509 certificates binding a public key to a domain/entity.
  * **Root of Trust:** The pre-installed, self-signed **Root CA certificates** embedded inside your OS and web browser trust stores. If a certificate chains up to a trusted Root CA, your system trusts it.
* **Practical Task (Build Your Own Mini Root CA & Inspect OS Root Trust Store):**
  ```bash
  # Create a self-signed Root CA key and certificate valid for 3650 days
  openssl req -x509 -new -nodes -key private_key.pem -sha256 -days 3650 \
    -subj "/C=CM/ST=Southwest/O=SecPlusLab Root CA/CN=SecPlusRootCA" \
    -out rootCA.crt

  # Inspect the Root CA certificate fields (Issuer == Subject proves it is a Root CA)
  openssl x509 -in rootCA.crt -noout -subject -issuer -dates

  # View your Linux system's built-in trusted Root CAs
  ls /etc/ssl/certs | head -n 10
  ```

### 5. Certificate Revocation Lists (CRLs) & 6. OCSP
* **Concept:** Mechanisms to invalidate compromised or expired certificates *before* their scheduled expiration date:
  * **CRL:** A periodically published, CA-signed list of revoked certificate serial numbers downloaded by clients (high bandwidth/latency).
  * **OCSP (Online Certificate Status Protocol):** Real-time query asking the CA whether a single certificate serial number is `Good`, `Revoked`, or `Unknown` (faster; **OCSP Stapling** lets the web server attach the CA's timestamped OCSP response directly to the TLS handshake).
* **Practical Task (Inspect a Live Website's CRL & OCSP Endpoints):**
  ```bash
  echo | openssl s_client -connect google.com:443 2>/dev/null | \
    openssl x509 -noout -ext crlDistributionPoints,authorityInfoAccess
  ```

### 7. Self-Signed Certificates vs. 8. Third-Party Certificates
* **Concept:**
  * **Self-Signed Certificate:** Signed by its own private key rather than a trusted CA. Free and fast for internal labs/testing, but triggers browser trust warnings on public websites because no external CA vouches for it.
  * **Third-Party Certificate:** Issued and signed by a publicly trusted commercial/public CA (e.g., Let's Encrypt, Sectigo) after domain validation (DV), organization validation (OV), or extended validation (EV).
* **Practical Task:**
  1. Compare `rootCA.crt` (created above, where `Issuer` and `Subject` are identical) against a live third-party certificate (`openssl s_client -connect wikipedia.org:443 </dev/null 2>/dev/null | openssl x509 -noout -subject -issuer`).

### 10. Certificate Signing Requests (CSRs)
* **Concept:** An encoded file (PKCS#10) generated on a server containing its **Public Key** and **Distinguished Name** (`CN`, `O`, `C`) sent to a CA to request a signed digital certificate. *(The server's Private Key never leaves the server).*
* **Practical Task (Generate a Server Key, Create a CSR, and Sign It with Your Root CA):**
  ```bash
  # 1. Generate web server private key & CSR
  openssl genpkey -algorithm RSA -out web_server.key -pkeyopt rsa_keygen_bits:2048
  openssl req -new -key web_server.key \
    -subj "/C=CM/O=SecPlusLab/CN=app.secplus.local" \
    -out web_server.csr

  # 2. Sign the CSR using your Root CA to issue a valid X.509 server certificate
  openssl x509 -req -in web_server.csr -CA rootCA.crt -CAkey private_key.pem \
    -CAcreateserial -out web_server.crt -days 365 -sha256

  # 3. Verify the certificate chain against your Root CA
  openssl verify -CAfile rootCA.crt web_server.crt
  ```

### 11. Wildcard Certificates
* **Concept:** A single TLS certificate using an asterisk (`*.example.com`) in the Common Name / Subject Alternative Name (SAN) to secure unlimited first-level subdomains (`://example.com`, `://example.com`, `://example.com`). *(Trade-off: If the private key is compromised, all subdomains are exposed).*
* **Practical Task (Inspect Subject Alternative Names & Wildcard Entries on a Live Site):**
  ```bash
  echo | openssl s_client -connect github.com:443 2>/dev/null | \
    openssl x509 -noout -ext subjectAltName
  ```

---

## Part B: Encryption (At-Rest, In-Transit, Algorithms & Key Lengths)

### 12. Symmetric Encryption vs. 13. Asymmetric Encryption
* **Concept:**
  * **Symmetric:** Uses the **same shared secret key** to encrypt and decrypt (e.g., **AES-256**, **ChaCha20**). Extremely fast; ideal for bulk data encryption, but suffers from the secure key-distribution problem.
  * **Asymmetric:** Uses a **Public/Private key pair** (e.g., **RSA**, **ECC / ECDSA**). Computationally slow; used for key exchange, digital signatures, and encrypting small payloads.
* **Practical Task (Hybrid Encryption Demo — Asymmetric RSA Protecting a Symmetric AES Key):**
  ```bash
  # 1. Generate a random 32-byte symmetric session key
  openssl rand -hex 32 > session.key

  # 2. Encrypt bulk data quickly with Symmetric AES-256-CBC
  echo "Confidential Database Dump" | openssl enc -aes-256-cbc -pbkdf2 -pass file:session.key -out data.enc

  # 3. Encrypt the Symmetric Session Key with the recipient's Asymmetric Public Key
  openssl pkeyutl -encrypt -inkey public_key.pem -pubin -in session.key -out session.key.enc
  ls -lh data.enc session.key.enc
  ```

### 14. Full-Disk, 15. Partition, 16. File, and 17. Volume Encryption
* **Concept:** Data-at-rest storage encryption layers:
  * **Full-Disk Encryption (FDE):** Encrypts the entire physical drive including the OS and boot sectors (e.g., **BitLocker** on Windows, **FileVault** on macOS, **LUKS** on Linux) using a **TPM (Trusted Platform Module)**.
  * **Partition / Volume Encryption:** Encrypts a specific disk partition or virtual container file (e.g., **VeraCrypt** volume, encrypted cloud EBS volume).
  * **File Encryption:** Encrypts individual files or folders (e.g., **EFS**, **GPG**, **7-Zip AES-256**).
* **Practical Task (Check OS Disk Encryption Status & Perform File Encryption with GPG):**
  * **Linux:** `lsblk -o NAME,FSTYPE,MOUNTPOINT` (look for `crypto_LUKS`)
  * **Windows (PowerShell):** `Get-BitLockerVolume | Select-Object MountPoint, EncryptionMethod, VolumeStatus`
  * **File Encryption (`openssl` / `gpg`):**
    ```bash
    echo "Top Secret Incident Report" > incident_report.txt
    gpg --batch --yes --passphrase "LabPassphrase2026!" -c incident_report.txt
    file incident_report.txt.gpg
    ```

### 18. Database Encryption & 19. Record-Level Encryption
### 18. Database Encryption & 19. Record-Level Encryption
* **Concept:**
  * **Database Encryption (TDE — Transparent Data Encryption):** Encrypts the entire physical database storage engine (data files, transaction logs, and backups) on disk at rest. Protects against physical disk theft, though authorized database users querying the DB still see plaintext.
  * **Record-Level (Column / Field-Level) Encryption:** Encrypts specific sensitive columns or individual rows (e.g., National ID numbers, credit card PANs, medical records) inside the application layer *before* writing to the database. Even a Database Administrator (DBA) running `SELECT *` sees only encrypted ciphertext.
* **Practical Task (Implement Column/Record-Level Encryption in Python):**
  ```python
  import os
  import base64
  import hashlib

  # Simulate storing a customer record where 'national_id' is encrypted at the record level
  # while non-sensitive metadata remains queryable in plaintext.
  def protect_field(plaintext_value, app_secret_key):
      nonce = os.urandom(12)
      keystream = hashlib.sha256(app_secret_key + nonce).digest()
      ciphertext = bytes(p ^ k for p, k in zip(plaintext_value.encode(), keystream))
      return base64.b64encode(nonce + ciphertext).decode("utf-8")

  master_app_key = os.urandom(32)
  db_row = {
      "customer_id": 501,
      "full_name": "Ambe Fon",
      "national_id_encrypted": protect_field("CM-1998-88412", master_app_key)
  }

  print("Database Row Stored on Disk:")
  for col, val in db_row.items():
      print(f"  {col:<22}: {val}")
  ```

---

### 20. Transport Encryption & 23. Secure Communication Protocols
* **Concept:** Protecting **Data in Transit** across untrusted networks against passive eavesdropping and active Man-in-the-Middle (MitM) modification:
  * **TLS 1.2 / TLS 1.3:** Secures web traffic (**HTTPS**), email (**SMTPS / IMAPS**), directory lookups (**LDAPS**), and APIs.
  * **SSH / SFTP / SCP:** Replaces insecure Telnet and FTP for encrypted remote terminal administration and file transfers.
  * **IPsec & WireGuard:** Network-layer VPN protocols encrypting IP packets across site-to-site or remote-access tunnels.
* **Practical Task (Inspect Live TLS 1.3 Negotiation, Certificate Chain & Key Exchange):**
  ```bash
  # Connect to a live HTTPS endpoint using TLS 1.3 and inspect negotiated security parameters
  openssl s_client -connect cloudflare.com:443 -tls1_3 </dev/null 2>/dev/null | \
    grep -E "Protocol|Cipher|Server Temp Key|Verification:"
  ```

---

### 21. Key Exchange
* **Concept:** Cryptographic protocols enabling two parties to establish a shared symmetric session key over an open, eavesdropped network without ever transmitting the secret key itself:
  * **Diffie-Hellman (DH) & ECDHE (Elliptic Curve Diffie-Hellman Ephemeral):** **ECDHE** generates temporary (ephemeral) per-session keys, guaranteeing **Perfect Forward Secrecy (PFS)**—meaning if an attacker steals the server's long-term RSA/ECDSA private key years later, they still cannot decrypt previously captured TLS traffic.
* **Practical Task (Simulate Diffie-Hellman Key Agreement in Python):**
  ```python
  # Publicly visible parameters agreed over the open network
  prime_p = 23
  generator_g = 5

  # Private secrets kept strictly local on each host
  client_private = 6
  server_private = 15

  # Public values sent across the network (safe for attackers to see)
  client_public = pow(generator_g, client_private, prime_p)
  server_public = pow(generator_g, server_private, prime_p)

  # Independent calculation of the shared symmetric secret
  client_shared_secret = pow(server_public, client_private, prime_p)
  server_shared_secret = pow(client_public, server_private, prime_p)

  print(f"Public Exchange -> Client sends: {client_public}, Server sends: {server_public}")
  print(f"Shared Secret   -> Client: {client_shared_secret} == Server: {server_shared_secret}")
  ```

---

### 22. Cryptographic Algorithms & Key Lengths
* **Concept:** CompTIA Security+ requires distinguishing modern, approved cryptographic algorithms and minimum bit lengths from broken/deprecated legacy algorithms:

| Cryptographic Function | Approved Modern Algorithms & Key Lengths | Deprecated / Insecure (Never Use) |
| :--- | :--- | :--- |
| **Symmetric Block/Stream** | **AES** (`128`, `192`, `256`-bit), **ChaCha20-Poly1305** (`256`-bit) | DES (`56`-bit), 3DES (`168`-bit), RC4, Blowfish |
| **Asymmetric Encryption / Sign** | **RSA** (`2048`-bit min, `4096`-bit), **ECC / Ed25519 / ECDSA** (`256`-bit) | RSA `1024`-bit, DSA, Diffie-Hellman `1024`-bit |
| **Cryptographic Hashing** | **SHA-256**, **SHA-384**, **SHA-512**, **SHA-3** | MD5 (`128`-bit), SHA-1 (`160`-bit) |
| **Password Hashing (KDFs)** | **Argon2id**, **bcrypt**, **PBKDF2**, **scrypt** | Unsalted MD5, Unsalted SHA-1 / SHA-256 |

* **Practical Task (Benchmark & Compare Hash Digest Bit-Lengths in Python):**
  ```python
  import hashlib

  sample = b"SecurityPlus_SY0-701"
  for algo in ["md5", "sha1", "sha256", "sha512"]:
      digest = hashlib.new(algo, sample).hexdigest()
      status = "DEPRECATED [!]" if algo in ["md5", "sha1"] else "APPROVED [OK]"
      print(f"{algo.upper():<8} ({len(digest)*4:>3}-bit) | {status} | {digest[:32]}...")
  ```

---

## Part C: Other Cryptographic Concepts

### 24. Digital Signatures
* **Concept:** Guarantees **Integrity**, **Authenticity**, and **Non-Repudiation** for software binaries, emails (S/MIME), and legal contracts:
  * **Signing:** Hash the message $\rightarrow$ Encrypt the hash digest with the **Sender's Private Key**.
  * **Verification:** Decrypt the signature with the **Sender's Public Key** $\rightarrow$ Hash the received message $\rightarrow$ Confirm both hashes match identically.
* **Practical Task (Sign a Software Release & Verify Tamper Detection with OpenSSL):**
  ```bash
  mkdir -p ~/secplus_crypto_lab && cd ~/secplus_crypto_lab

  # 1. Generate signing keypair
  openssl genpkey -algorithm RSA -out release_priv.pem -pkeyopt rsa_keygen_bits:2048 2>/dev/null
  openssl rsa -pubout -in release_priv.pem -out release_pub.pem 2>/dev/null

  # 2. Sign a deployment script
  echo "echo 'Deploying verified security patch v3.4'" > deploy.sh
  openssl dgst -sha256 -sign release_priv.pem -out deploy.sh.sig deploy.sh

  # 3. Verify valid signature (Outputs: Verified OK)
  openssl dgst -sha256 -verify release_pub.pem -signature deploy.sh.sig deploy.sh

  # 4. Tamper with 1 byte of the script and re-verify (Outputs: Verification Failure)
  echo "# backdoor" >> deploy.sh
  openssl dgst -sha256 -verify release_pub.pem -signature deploy.sh.sig deploy.sh
  ```

---

### 25. Salting & 26. Hashing Algorithms
* **Concept:**
  * **Hashing Algorithms:** One-way mathematical functions converting variable-length input into a fixed-length digest. **Deterministic** (same input = same output), **irreversible** (pre-image resistant), and **avalanche-sensitive** (1-bit input change alters ~50% of output bits).
  * **Salting:** Adding a unique, cryptographically random value (salt) to every user's password *before* hashing. Prevents **Rainbow Table** attacks and ensures two users with the exact same password have completely different database hashes.
  * **Key Stretching:** Slowing down password hashing intentionally (e.g., 100,000+ iterations in PBKDF2 or memory-hard Argon2id) to defeat high-speed GPU brute-force cracking.
* **Practical Task (Demonstrate Avalanche Effect & Salted PBKDF2 Password Storage):**
  ```python
  import hashlib
  import os

  # 1. Avalanche Effect: 1-character difference completely transforms SHA-256
  h1 = hashlib.sha256(b"Transfer $100").hexdigest()
  h2 = hashlib.sha256(b"Transfer $101").hexdigest()
  print("Hash 1:", h1)
  print("Hash 2:", h2)

  # 2. Salted + Stretched Password Hashing (two users sharing the same password)
  shared_password = b"P@ssw0rd2026!"
  user_a_salt = os.urandom(16)
  user_b_salt = os.urandom(16)

  user_a_hash = hashlib.pbkdf2_hmac("sha256", shared_password, user_a_salt, 200_000).hex()
  user_b_hash = hashlib.pbkdf2_hmac("sha256", shared_password, user_b_salt, 200_000).hex()

  print("\nUser A Stored Hash:", user_a_hash)
  print("User B Stored Hash:", user_b_hash)
  ```

---

### 27. Obfuscation
* **Concept:** Techniques that disguise data, source code, or payloads to hinder casual human inspection or basic signature detection—**without providing cryptographic confidentiality** (since no secret key is required to reverse it):
  * **Encoding (Base64 / Hex / URL encoding):** Standardized data representation, easily decoded by anyone.
  * **Code Minification / Packing / Variable Renaming:** Used legitimately to protect intellectual property or maliciously by malware authors to evade static AV signatures.
  * **Steganography:** Hiding secret messages or payloads inside ordinary carrier files (e.g., `.png` images, `.wav` audio files).
* **Practical Task (Demonstrate Steganography-Style File Appending & Base64 Decoding):**
  ```bash
  # 1. Base64 is obfuscation/encoding, NOT encryption:
  encoded_str=$(echo -n "DB_PASS=Admin12345" | base64)
  echo "Encoded: $encoded_str"
  echo "Decoded without any key: $(echo "$encoded_str" | base64 -d)"

  # 2. Simple EOF Steganography demo: hide secret text after an image's end-of-file bytes
  printf "\x89PNG\r\n\x1a\nFAKE_IMAGE_DATA" > photo.png
  echo "HIDDEN_C2_SERVER=198.51.100.44" >> photo.png
  strings photo.png | grep "HIDDEN"
  ```

---

### 28. Cryptographic Tools
### 28. Cryptographic Tools
* **Concept:** Standard command-line and enterprise tools used by security engineers to generate keys, inspect certificates, verify file integrity, and encrypt sensitive artifacts:
  * **`openssl`:** Industry-standard CLI toolkit for generating RSA/ECC keys, creating CSRs, signing X.509 certificates, testing TLS handshakes, and performing symmetric/asymmetric encryption.
  * **`gpg` (GNU Privacy Guard):** OpenPGP-compliant tool for encrypting files/emails and verifying signed software packages (`apt`/`rpm` repository keys).
  * **`ssh-keygen`:** Generates modern cryptographic keypairs (**Ed25519** or **RSA-4096**) for passwordless, phishing-resistant SSH authentication and Git commit signing.
  * **`certutil` (Windows) / `sha256sum` (Linux):** Native utilities for computing file hashes (`certutil -hashfile app.exe SHA256`), inspecting certificate stores, and checking CRLs.
* **Practical Task 1 (Generate an Ed25519 SSH Keypair & Sign a Git Commit):**
  ```bash
  mkdir -p ~/secplus_tools_lab && cd ~/secplus_tools_lab

  # 1. Generate a modern Ed25519 keypair (faster and stronger than RSA-2048)
  ssh-keygen -t ed25519 -f ./secplus_ed25519 -N "LabKeyPass2026!" -C "analyst@secplus.local"
  chmod 600 secplus_ed25519
  cat secplus_ed25519.pub

  # 2. Verify key fingerprint (used to prevent SSH Man-in-the-Middle attacks)
  ssh-keygen -lf secplus_ed25519.pub
  ```

* **Practical Task 2 (Symmetric & Asymmetric File Protection with GnuPG & Windows `certutil`):**
  * **Linux / macOS (`gpg`):**
    ```bash
    echo "Incident Response Evidence Log #001" > evidence.log
    gpg --batch --yes --passphrase "VaultPass2026!" --cipher-algo AES256 -c evidence.log
    file evidence.log.gpg
    gpg --batch --yes --passphrase "VaultPass2026!" -d evidence.log.gpg
    ```
  * **Windows (CMD / PowerShell — Built-in `certutil` & `Get-FileHash`):**
    ```powershell
    "Incident Response Evidence Log #001" | Out-File -Encoding utf8 evidence.log
    Get-FileHash .\evidence.log -Algorithm SHA256
    certutil -hashfile .\evidence.log SHA256
    ```

---

### 29. Key Management
* **Concept:** Governing cryptographic keys across their complete lifecycle so keys are never leaked, lost, or used past their safe lifespan (**cryptoperiod**):
  * **1. Generation:** Must use a Cryptographically Secure Pseudo-Random Number Generator (**CSPRNG**—e.g., `/dev/urandom`, hardware RNG, Python `secrets`), never predictable timestamps or standard `random`.
  * **2. Storage:** Store keys inside hardware-backed vaults—**TPM** (Trusted Platform Module on endpoints), **HSM** (Hardware Security Module in data centers), or **Cloud KMS** (AWS KMS, Azure Key Vault)—never hardcoded in source code or `.env` files pushed to Git.
  * **3. Distribution & Exchange:** Never send symmetric keys over plaintext email/chat; use **ECDHE**, **RSA key wrapping**, or **Key Escrow** for authorized recovery.
  * **4. Rotation:** Automatically retiring active keys on a fixed schedule (e.g., every 90 or 365 days) and re-encrypting data encryption keys (envelope encryption) to limit exposure if a key is compromised.
  * **5. Revocation & Destruction (Crypto-Shredding):** Revoking compromised certificates via **CRL/OCSP**, and destroying cryptographic keys (**crypto-shredding**) when decommissioning cloud storage or SSDs so encrypted data becomes permanently mathematically unrecoverable.
* **Practical Task 1 (Scan a Code Directory for Hardcoded Cryptographic Keys / Secrets):**
  Simulate a pre-commit secret scanner in Python to catch leaked private keys or hardcoded AES secrets before they reach Git:
  ```python
  import re

  sample_source_code = '''
  API_URL = "https://corp.local"
  AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
  BEGIN_KEY = "-----BEGIN RSA PRIVATE KEY-----"
  '''

  secret_patterns = {
      "PEM Private Key Header": r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----",
      "Hardcoded Secret Assignment": r"(?i)(secret|api_key|password|private_key)\s*=\s*['\"][A-Za-z0-9/+=]{16,}['\"]"
  }

  for rule_name, pattern in secret_patterns.items():
      if re.search(pattern, sample_source_code):
          print(f"[KEY MGMT VIOLATION] {rule_name} detected in source code! Move to KMS/Vault.")
  ```

* **Practical Task 2 (Simulate Envelope Encryption, Key Rotation & Crypto-Shredding):**
  ```python
  import secrets
  from datetime import datetime

  # Envelope Encryption & Key Lifecycle Simulation:
  # - Key Encryption Key (KEK) lives in Cloud KMS/HSM
  # - Data Encryption Key (DEK) encrypts actual customer records
  kms_keyring = {
      "KEK-2025-Q4": {"state": "CRYPTO_SHREDDED", "key_material": None},
      "KEK-2026-Q3": {"state": "ROTATED_DECRYPT_ONLY", "key_material": secrets.token_hex(32)},
      "KEK-2026-Q4": {"state": "ACTIVE_ENCRYPT_DECRYPT", "key_material": secrets.token_hex(32)}
  }

  print(f"=== KMS Key Lifecycle Audit ({datetime.now().strftime('%Y-%m-%d')}) ===")
  for key_id, info in kms_keyring.items():
      mat = info["key_material"][:16] + "..." if info["key_material"] else "DESTROYED (Unrecoverable)"
      print(f"{key_id:<14} | State: {info['state']:<24} | Key: {mat}")
  ```

---

### Objective 1.3 Completion Checklist
- [ ] Generated RSA & Ed25519 keypairs, created a **CSR**, signed an **X.509 certificate** with a custom **Root CA**, and verified the chain (`openssl verify`).
- [ ] Inspected live **CRL**, **OCSP**, **SAN/Wildcard**, and **TLS 1.3 ECDHE** cipher suites using `openssl s_client`.
- [ ] Practiced **Symmetric (AES-256)**, **Asymmetric (RSA)**, **Record-Level**, and **GPG** file encryption.
- [ ] Verified **Digital Signatures** (`openssl dgst`) and demonstrated **Salted PBKDF2** hashing vs. **Base64 / Steganography obfuscation**.
- [ ] Built a **secret-leak scanner** and simulated **KMS Key Rotation & Crypto-Shredding**.

