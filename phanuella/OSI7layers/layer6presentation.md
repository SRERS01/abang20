## Layer 6: Presentation Layer (Translation, Encryption, Serialization & Encoding)

The Presentation Layer acts as the data translator for the network. It converts application-level data into standardized formats for transmission—handling **character encoding**, **data serialization**, **compression**, and **cryptographic encryption/decryption** before passing payloads to Layer 5 or Layer 7.

### Environment Differences: Ubuntu vs. Termux
* **Ubuntu:** Full access to cryptographic auditing suites (`testssl.sh`, `sslyze`), binary/serialization parsers (`ysoserial`, `protoc`, `jq`, `xxd`), and GUI traffic interceptors (`Burp Suite`, `Wireshark`).
* **Termux:** Almost all Layer 6 operations work natively without root because they manipulate user-space data streams rather than raw network interfaces (`openssl`, `python3`, `jq`, `base64`, `gzip`, `testssl.sh`).

---

### Core Layer 6 Standards & Testing Tools

| Standard / Mechanism | Full Name & Role | Security Auditing Focus | Testing Tools (Ubuntu & Termux) |
| :--- | :--- | :--- | :--- |
| **TLS / SSL (X.509 PKI)** | Transport Layer Security & Public Key Infrastructure (encryption, integrity, certificate validation). | Weak cipher suites (RC4, 3DES, NULL), deprecated protocols (TLS 1.0/1.1), expired/self-signed certs, HSTS absence, and downgrade attacks. | `testssl.sh`, `sslyze`, `sslscan`, `openssl`, `nmap --script ssl-*` |
| **Character Encoding (UTF-8 / ASCII / URL / HTML)** | Translates human-readable text into byte sequences across different platforms. | **WAF/Filter Evasion** via double URL encoding (`%252e`), Unicode normalization bugs, overlong UTF-8 sequences, and charset mismatch XSS (`UTF-7`). | `cyberchef`, `python3`, `iconv`, `xxd`, `burpsuite` (Decoder) |
| **Data Serialization (JSON / XML / YAML / Protobuf)** | Converts structured in-memory objects into transmittable byte/text formats. | **Insecure Deserialization** (RCE via Java/PHP/Python gadgets), **XXE** (XML External Entity injection), YAML arbitrary code execution, and Prototype Pollution. | `ysoserial`, `phpggc`, `xmllint`, `jq`, `yq`, `protoc` |
| **Binary & Transport Encoding (Base64 / Hex / ASN.1)** | Encodes arbitrary binary data into ASCII-safe strings or structured binary trees. | Hardcoded secrets in Base64 blobs, malleable JWT/cookie payloads, and X.509 certificate ASN.1 parsing vulnerabilities. | `base64`, `xxd`, `hexdump`, `openssl asn1parse`, `jwt_tool` |
| **Compression (Gzip / Brotli / Deflate)** | Reduces payload size prior to encryption or transmission. | **BREACH / CRIME** side-channel attacks (recovering secrets like CSRF tokens from compressed HTTPS response lengths) and Zip Bombs / Archive Slip (`../`). | `gzip`, `brotli`, `zcat`, `python3` (`zlib`), `evilarc` |
| **Media & Document Formats (MIME / PDF / SVG / JPEG)** | Standardizes rich media and file structures (`Content-Type` headers & magic bytes). | **MIME Sniffing** XSS, malicious SVG uploads containing `<script>`, PDF JavaScript injection, and ImageMagick/FFmpeg parser exploits. | `exiftool`, `file`, `binwalk`, `pdfinfo`, `qpdf` |

---

### Practical Layer 6 Auditing Commands (Ubuntu & Termux)

```bash
# 1. Run a comprehensive TLS/SSL cipher, protocol, and vulnerability audit (Ubuntu & Termux)
testssl.sh --fast https://example.com

# 2. Inspect a remote server's X.509 certificate chain and SAN domains (Ubuntu & Termux)
echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | openssl x509 -noout -text | grep -E "Subject:|Issuer:|DNS:|Not After"

# 3. Decode Base64 or URL-encoded tokens/payloads quickly on the CLI (Ubuntu & Termux)
echo "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" | base64 -d 2>/dev/null; echo

# 4. Inspect file magic bytes and metadata to test file-upload validation bypasses (Ubuntu & Termux)
file suspicious_upload.png && exiftool suspicious_upload.png

# 5. Pretty-print and query nested JSON API responses for sensitive data exposure (Ubuntu & Termux)
curl -s https://example.com | jq '.'

# 6. Test an XML endpoint for External Entity (XXE) processing using curl (Ubuntu & Termux)
curl -X POST https://example.com \
  -H "Content-Type: application/xml" \
  -d '<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file:///etc/passwd">]><root>&test;</root>'
```

---

### Layer 6 -> Web Security Connection
* **WAF Evasion via Encoding & Normalization:** Web Application Firewalls often inspect raw strings at Layer 7, while back-end frameworks decode Layer 6 representations (Unicode normalization, double URL-encoding, JSON `\u003c` escapes) *after* the WAF check—allowing XSS and SQLi payloads to slip through.
* **Insecure Deserialization:** When web apps accept serialized objects in cookies, `ViewState`, or API bodies (PHP `unserialize()`, Python `pickle`, Java `ObjectInputStream`, Node.js `node-serialize`), attackers can manipulate Layer 6 object structures to achieve Remote Code Execution (RCE).
* **Content-Type & Magic Byte Mismatches:** Uploading a polyglot file (valid JPEG magic bytes + embedded PHP/HTML payload) exploits discrepancies between Layer 6 file-header validation and Layer 7 web server execution rules.
