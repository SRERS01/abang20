# Part 3 – Practical Security+ Laboratory Syllabus
## Module 5: Cryptography Laboratory

> **Lab Environment:** Linux VM (Ubuntu/Kali) with `openssl`, `gnupg` (`gpg`), `hashcat`, `sha256sum`, and Python 3.  
> **Authorization Warning:** Only run password auditing tools (`hashcat`) against synthetic hashes you create yourself in this lab.

---

### Lab 1: Generate Public/Private Key Pairs (RSA & Elliptic Curve)
* **Objective:** Generate both legacy-compatible **RSA-2048/4096** and modern high-efficiency **ECC (`prime256v1` / `Ed25519`)** asymmetric key pairs, enforce strict `600` file permissions on private keys, and derive the matching public keys.
* **Hands-On Steps:**
  ```bash
  mkdir -p ~/crypto_lab && cd ~/crypto_lab

  # 1. Generate a 2048-bit RSA Private Key and lock down permissions
  openssl genpkey -algorithm RSA -out rsa_private.pem -pkeyopt rsa_keygen_bits:2048
  chmod 600 rsa_private.pem

  # 2. Extract the matching RSA Public Key
  openssl rsa -pubout -in rsa_private.pem -out rsa_public.pem

  # 3. Generate a modern Elliptic Curve (ECC P-256) Private & Public Key Pair
  openssl ecparam -name prime256v1 -genkey -noout -out ecc_private.pem
  chmod 600 ecc_private.pem
  openssl ec -in ecc_private.pem -pubout -out ecc_public.pem

  ls -lh *_private.pem *_public.pem
  ```

---

### Lab 2: Hash Files (`SHA-256`, `SHA-512`, `SHA-3`)
* **Objective:** Compute cryptographic message digests using `sha256sum`, `sha512sum`, and `openssl dgst`, and observe the **avalanche effect** (where changing a single character completely transforms the output digest).
* **Hands-On Steps:**
  ```bash
  cd ~/crypto_lab

  # 1. Create two nearly identical files (differing by 1 character)
  echo "Approve payment of 500,000 XAF to Vendor A" > tx_original.txt
  echo "Approve payment of 500,001 XAF to Vendor A" > tx_altered.txt

  # 2. Compute SHA-256 and SHA-512 hashes via OpenSSL & coreutils
  openssl dgst -sha256 tx_original.txt tx_altered.txt
  sha512sum tx_original.txt | cut -c1-64
  ```

---

### Lab 3: Verify File Integrity (Checksums & GnuPG Detached Signatures)
* **Objective:** Create a signed cryptographic manifest (`SHA256SUMS`) and detect unauthorized file tampering immediately.
* **Hands-On Steps:**
  ```bash
  cd ~/crypto_lab

  # 1. Generate baseline checksum file
  sha256sum tx_original.txt > SHA256SUMS

  # 2. Verify baseline integrity (Expected: tx_original.txt: OK)
  sha256sum -c SHA256SUMS

  # 3. Simulate tampering and re-verify (Expected: FAILED)
  echo "tamper" >> tx_original.txt
  sha256sum -c SHA256SUMS || echo "[INTEGRITY VIOLATION] File tampering detected!"
  ```

---

### Lab 4: Generate Certificates (Root CA, CSR & Signed Server Certificate)
* **Objective:** Build a complete two-tier mini **Public Key Infrastructure (PKI)**—generating a self-signed **Root CA**, creating a **Certificate Signing Request (CSR)** for a web server, and issuing a CA-signed **X.509v3 Server Certificate** with Subject Alternative Names (SANs).
* **Hands-On Steps:**
  ```bash
  cd ~/crypto_lab

  # 1. Generate Root CA Private Key & Self-Signed Root Certificate (valid 10 years)
  openssl genpkey -algorithm RSA -out rootCA.key -pkeyopt rsa_keygen_bits:4096
  chmod 600 rootCA.key
  openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 3650 \
    -subj "/C=CM/ST=Southwest/L=Buea/O=SecPlus Lab PKI/CN=SecPlus Lab Root CA" \
    -out rootCA.crt

  # 2. Generate Web Server Private Key & Certificate Signing Request (CSR)
  openssl genpkey -algorithm RSA -out portal.key -pkeyopt rsa_keygen_bits:2048
  chmod 600 portal.key
  openssl req -new -key portal.key \
    -subj "/C=CM/ST=Southwest/L=Buea/O=SecPlus Corp/CN=portal.secplus.local" \
    -out portal.csr

  # 3. Create X.509v3 extension file for Subject Alternative Names (SAN)
  cat << 'EOF' > san.ext
  authorityKeyIdentifier=keyid,issuer
  basicConstraints=CA:FALSE
  keyUsage = digitalSignature, keyEncipherment
  extendedKeyUsage = serverAuth
  subjectAltName = @alt_names
  [alt_names]
  DNS.1 = portal.secplus.local
  DNS.2 = www.portal.secplus.local
  IP.1  = 127.0.0.1
  EOF

  # 4. Sign the CSR with your Root CA to issue portal.crt (valid 365 days)
  openssl x509 -req -in portal.csr -CA rootCA.crt -CAkey rootCA.key \
    -CAcreateserial -out portal.crt -days 365 -sha256 -extfile san.ext
  ```

---

### Lab 5: Inspect Certificates (X.509 Fields, Extensions, CRL & OCSP)
* **Objective:** Parse X.509 certificate metadata (`Subject`, `Issuer`, `Serial Number`, `Validity Dates`, `Public Key Algorithm`, `SANs`, and `OCSP/CRL` revocation endpoints) using OpenSSL.
* **Hands-On Steps:**
  ```bash
  cd ~/crypto_lab

  # 1. Inspect your newly issued local certificate
  openssl x509 -in portal.crt -noout -subject -issuer -serial -dates -ext subjectAltName

  # 2. Inspect a live production website's certificate & revocation endpoints
  echo | openssl s_client -connect cloudflare.com:443 2>/dev/null | \
    openssl x509 -noout -subject -issuer -dates -ext crlDistributionPoints,authorityInfoAccess
  ```

---

### Lab 6: Test TLS Configurations (Protocol Versions & Cipher Suites)
* **Objective:** Audit an HTTPS server's TLS configuration to confirm deprecated protocols (`TLS 1.0` / `TLS 1.1`) are rejected while modern **TLS 1.3** with **ECDHE Perfect Forward Secrecy** succeeds.
* **Hands-On Steps:**
  ```bash
  # 1. Verify TLS 1.3 handshake succeeds and inspect negotiated AEAD cipher
  openssl s_client -connect google.com:443 -tls1_3 </dev/null 2>/dev/null | \
    grep -E "Protocol|Cipher|Server Temp Key"

  # 2. Test whether deprecated TLS 1.1 is properly rejected (Should fail handshake)
  openssl s_client -connect google.com:443 -tls1_1 </dev/null 2>&1 | \
    grep -iE "Protocol|alert|error|no protocols"
  ```

---

### Lab 7: Understand Digital Signatures (OpenSSL & GnuPG)
* **Objective:** Create and verify cryptographic digital signatures proving **Authenticity**, **Integrity**, and **Non-Repudiation** using both **OpenSSL** and **GnuPG (`gpg`)**.
* **Hands-On Steps:**
  ```bash
  cd ~/crypto_lab

  # 1. Create a deployment script and sign its SHA-256 digest with your RSA Private Key
  echo '#!/bin/bash' > release_patch.sh
  echo 'echo "Applying verified security patch v5.1"' >> release_patch.sh
  openssl dgst -sha256 -sign rsa_private.pem -out release_patch.sh.sig release_patch.sh

  # 2. Verify signature using the matching Public Key (Expected: Verified OK)
  openssl dgst -sha256 -verify rsa_public.pem -signature release_patch.sh.sig release_patch.sh

  # 3. Also test symmetric AES-256 encryption & decryption with GnuPG (gpg)
  gpg --batch --yes --passphrase "VaultPassphrase2026!" --cipher-algo AES256 -c release_patch.sh
  gpg --batch --yes --passphrase "VaultPassphrase2026!" -d release_patch.sh.gpg
  ```

---

### Lab 8: Generate Random Cryptographic Values (CSPRNG)
* **Objective:** Use Cryptographically Secure Pseudo-Random Number Generators (`openssl rand`, `/dev/urandom`, Python `secrets`) to generate high-entropy AES-256 encryption keys, initialization vectors (IVs/nonces), and password salts.
* **Hands-On Steps:**
  ```bash
  # 1. Generate a 256-bit (32-byte) hexadecimal symmetric AES key
  openssl rand -hex 32

  # 2. Generate a 128-bit (16-byte) Base64 random salt/nonce
  openssl rand -base64 16

  # 3. Generate a cryptographically random 24-character passphrase in Python
  python3 -c 'import secrets, string; chars = string.ascii_letters + string.digits + "!@#$%"; print("".join(secrets.choice(chars) for _ in range(24)))'
  ```

---

### Lab 9: Manage Encryption Keys (Envelope Encryption, Rotation & Crypto-Shredding)
* **Objective:** Practice **Envelope Encryption** (encrypting data with a Data Encryption Key [DEK], then wrapping the DEK with a Master Key Encryption Key [KEK]), rotating keys, and performing **Crypto-Shredding** for secure data disposal.
* **Hands-On Steps:**
  ```bash
  cd ~/crypto_lab

  # 1. Generate a 256-bit Data Encryption Key (DEK) and encrypt sensitive data
  openssl rand -hex 32 > dek_v1.key
  echo "Customer_KYC_Records_2026" > kyc_vault.csv
  openssl enc -aes-256-cbc -pbkdf2 -salt -in kyc_vault.csv -out kyc_vault.csv.enc -pass file:dek_v1.key

  # 2. Wrap (encrypt) the DEK using your Asymmetric Public Key (KEK)
  openssl pkeyutl -encrypt -inkey rsa_public.pem -pubin -in dek_v1.key -out dek_v1.key.wrapped

  # 3. Securely shred the plaintext DEK and original CSV
  shred -u dek_v1.key kyc_vault.csv

  # 4. Recover DEK using Private Key when authorized, then decrypt data
  openssl pkeyutl -decrypt -inkey rsa_private.pem -in dek_v1.key.wrapped -out dek_recovered.key
  openssl enc -d -aes-256-cbc -pbkdf2 -in kyc_vault.csv.enc -out kyc_recovered.csv -pass file:dek_recovered.key
  cat kyc_recovered.csv
  ```

---

### Lab 10: Verify Certificate Chains (Root CA $\rightarrow$ Intermediate $\rightarrow$ Leaf)
* **Objective:** Validate X.509 trust chains from leaf server certificate up to the trusted Root CA (`openssl verify`) and inspect multi-tier certificate chains on live HTTPS servers.
* **Hands-On Steps:**
  ```bash
  cd ~/crypto_lab

  # 1. Verify your local server certificate against your custom Root CA (Expected: portal.crt: OK)
  openssl verify -CAfile rootCA.crt portal.crt

  # 2. Inspect the full multi-certificate chain (-showcerts) of a live public HTTPS endpoint
  openssl s_client -connect wikipedia.org:443 -showcerts </dev/null 2>/dev/null | \
    grep -E "s:|i:"
  ```

---

### Lab 11: Authorized Password Auditing with Hashcat
### Lab 11: Authorized Password Auditing with Hashcat
* **Objective:** Understand how GPU/CPU password auditing tools like **Hashcat** evaluate password strength, why legacy unsalted hashes (`MD5` `-m 0`, `SHA-1` `-m 100`, `NTLM` `-m 1000`) fail instantly against dictionary and rule-based attacks, and why **14+ character passphrases** + **salted key-stretching KDFs (`bcrypt` `-m 3200`, `Argon2id`, `PBKDF2`)** are mandatory in enterprise standards.
* **Authorization Rule:** Only execute Hashcat against synthetic hashes you generated yourself in this isolated lab directory.

* **Hands-On Step 1: Dictionary Attack (`-a 0`) & Rule-Based Mutation Attack (`-r`) on a Synthetic Hash:**
  ```bash
  mkdir -p ~/crypto_lab && cd ~/crypto_lab

  # 1. Generate a synthetic weak MD5 hash of a predictable password ("Summer2026!")
  echo -n "Summer2026!" | md5sum | awk '{print \$1}' > synthetic_target.hash
  cat synthetic_target.hash

  # 2. Build a small synthetic lab wordlist
  cat << 'EOF' > lab_wordlist.txt
  admin123
  welcome2026
  Summer2026!
  password123
  EOF

  # 3. Audit the hash using Hashcat (-m 0 = Raw MD5, -a 0 = Straight Dictionary Attack)
  # Note: --force allows execution inside a VirtualBox VM without a dedicated hardware GPU
  hashcat -m 0 -a 0 synthetic_target.hash lab_wordlist.txt --force --quiet 2>/dev/null || true
  hashcat -m 0 synthetic_target.hash --show 2>/dev/null || echo "If hashcat is not installed, run: sudo apt install -y hashcat"
  ```

* **Hands-On Step 2: Benchmark Legacy `MD5` vs. Modern Salted `bcrypt` Speed (`hashcat -b`):**
  Compare how many billions of guesses per second an attacker can test against unsalted MD5 vs. modern salted `bcrypt`:
  ```bash
  # Compare cracking speed (Hashes/sec) of MD5 (-m 0) vs. bcrypt (-m 3200)
  hashcat -b -m 0 -m 3200 --force --quiet 2>/dev/null || \
    python3 -c '
  import time, hashlib, os
  t0 = time.time(); hashlib.md5(b"test").hexdigest(); t_md5 = time.time() - t0
  t1 = time.time(); hashlib.pbkdf2_hmac("sha256", b"test", os.urandom(16), 300_000); t_kdf = time.time() - t1
  print(f"Single MD5 time   : {t_md5*1000:.4f} ms (Trillions/sec on GPU)")
  print(f"Single PBKDF2 time: {t_kdf*1000:.2f} ms (Intentionally slowed via Key Stretching)")
  '
  ```

* **Hands-On Step 3: Clean Up Synthetic Hash Artifacts:**
  ```bash
  rm -f ~/crypto_lab/synthetic_target.hash ~/crypto_lab/lab_wordlist.txt
  ```

---

## Quick-Reference Cryptography & PKI CLI Cheat Sheet (Exam & Lab Synthesis)

| Cryptographic Task | Primary CLI Command (`OpenSSL` / `GnuPG` / `Coreutils`) | Security+ Concept Reinforced |
| :--- | :--- | :--- |
| **Generate RSA-2048 Private Key** | `openssl genpkey -algorithm RSA -out priv.pem -pkeyopt rsa_keygen_bits:2048` | Asymmetric key generation (`2048`-bit minimum). |
| **Extract Matching Public Key** | `openssl rsa -pubout -in priv.pem -out pub.pem` | Public key derivation for encryption/signature verification. |
| **Create Certificate Signing Request** | `openssl req -new -key server.key -subj "/CN=app.local" -out server.csr` | PKCS#10 CSR sent to CA (private key stays on server). |
| **Verify X.509 Trust Chain** | `openssl verify -CAfile rootCA.crt server.crt` | Root of Trust & CA signature chain validation. |
| **Inspect Live TLS & Cert Details** | `openssl s_client -connect example.com:443 -tls1_3 </dev/null` | Transport encryption, cipher suites, SANs, CRL/OCSP. |
| **Sign & Verify Digital Signature** | `openssl dgst -sha256 -sign priv.pem -out file.sig file.txt`<br>`openssl dgst -sha256 -verify pub.pem -signature file.sig file.txt` | Integrity, Authenticity, and **Non-Repudiation**. |
| **Symmetric File Encryption (GPG)** | `gpg --cipher-algo AES256 -c secret.txt` | Data-at-rest confidentiality using AES-256. |
| **Generate CSPRNG 256-Bit Key** | `openssl rand -hex 32` | Cryptographically secure random key/salt generation. |
| **Verify File Checksum Integrity** | `sha256sum -c SHA256SUMS` | Collision-resistant integrity verification (`SHA-256`). |

---

### Module 5 Lab Completion Checklist
- [ ] Generated **RSA** and **ECC (`prime256v1`)** key pairs and locked down private key permissions (`chmod 600`).
- [ ] Computed **SHA-256 / SHA-512** hashes and verified file integrity (`sha256sum -c`).
- [ ] Built a two-tier **PKI** (**Root CA $\rightarrow$ CSR $\rightarrow$ SAN-enabled X.509 Certificate**) and verified the trust chain (`openssl verify`).
- [ ] Tested live **TLS 1.3** cipher suites vs. deprecated **TLS 1.1** rejection (`openssl s_client`).
- [ ] Signed/verified scripts with **OpenSSL Digital Signatures**, encrypted files with **GnuPG**, practiced **Envelope Encryption**, and demonstrated **Hashcat** password auditing + KDF benchmarking on synthetic hashes.
