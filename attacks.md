# Comprehensive List of Cyber Attacks

## 1. Malware (Malicious Software)
* **Ransomware:** Encrypts or locks a victim's files and demands a ransom payment for the decryption key.
* **Viruses:** Malicious code that attaches to clean files and spreads when the infected file is executed.
* **Worms:** Standalone malware that self-replicates and spreads across networks without human interaction.
* **Trojans (Trojan Horses):** Malware disguised as legitimate software to trick users into installing it.
* **Spyware:** Secretly monitors and collects user activity, browsing habits, and sensitive data.
* **Keyloggers:** Records every keystroke made on a device to capture passwords and private messages.
* **Adware:** Displays unwanted advertisements and often tracks user behavior in the background.
* **Rootkits:** Grants attackers hidden, privileged (root/admin) access while concealing its presence from the OS.
* **Fileless Malware:** Operates entirely in system memory (RAM) without writing files to the hard drive.

## 2. Social Engineering Attacks
* **Phishing:** Fraudulent emails impersonating trusted entities to steal credentials or financial data.
* **Spear Phishing:** Highly targeted phishing tailored to a specific individual or organization.
* **Whaling:** Spear phishing aimed specifically at high-profile targets like executives, politicians, or celebrities.
* **Smishing (SMS Phishing):** Phishing attacks delivered via text messages.
* **Vishing (Voice Phishing):** Phishing conducted over phone calls using urgency or voice impersonation.
* **Baiting:** Luring victims into a trap using enticing offers (e.g., free downloads or infected USB drives).
* **Pretexting:** Inventing a fabricated scenario to trick a victim into divulging sensitive information.
* **Business Email Compromise (BEC):** Compromising or spoofing corporate email accounts to authorize fraudulent wire transfers or data leaks.
* **Watering Hole Attack:** Compromising a legitimate website frequently visited by a targeted group to infect their devices.

## 3. Password & Authentication Attacks
* **Simple Brute Force:** Systematically trying every possible character combination until the password is found.
* **Dictionary Attack:** Testing a pre-compiled list of common words, phrases, and known passwords.
* **Hybrid Brute Force:** Combining dictionary words with systematic numbers, symbols, or capitalization tweaks.
* **Reverse Brute Force:** Testing one known/common password against thousands of different usernames.
* **Password Spraying:** Slowly testing a single common password across many accounts to avoid triggering lockout limits.
* **Credential Stuffing:** Automatically injecting leaked username/password pairs from one breach into other websites.
* **Rainbow Table Attack:** Using pre-computed hash tables to reverse unsalted cryptographic password hashes.
* **Pass-the-Hash:** Authenticating directly using a stolen password hash without needing to crack the plaintext password.

## 4. Network & Traffic Attacks
* **Denial-of-Service (DoS):** Flooding a system or network with traffic to exhaust resources and crash it.
* **Distributed Denial-of-Service (DDoS):** Launching a DoS attack simultaneously from thousands of compromised devices (a botnet).
* **Man-in-the-Middle (MitM):** Secretly intercepting and altering communications between two parties.
* **DNS Spoofing (Cache Poisoning):** Corrupting DNS records to redirect users from legitimate websites to fake ones.
* **ARP Spoofing:** Sending fake Address Resolution Protocol messages on a local network to intercept traffic.
* **Session Hijacking:** Stealing an active session ID or cookie to take over an authenticated user's session.
* **Evil Twin Attack:** Setting up a rogue Wi-Fi hotspot that mimics a legitimate network to intercept user data.

## 5. Web Application & Database Attacks
* **SQL Injection (SQLi):** Inserting malicious SQL queries into input fields to read, modify, or delete database data.
* **Cross-Site Scripting (XSS):** Injecting malicious scripts into trusted websites that execute in victims' browsers.
* **Cross-Site Request Forgery (CSRF):** Tricking an authenticated user into unknowingly executing unwanted actions on a web app.
* **Directory Traversal:** Exploiting improper file path validation to access restricted directories and files on a server.
* **Typosquatting (URL Hijacking):** Registering misspelled domains of popular websites to catch and exploit user typos.

## 6. Software & System Exploits
* **Zero-Day Exploit:** Attacking a software vulnerability before the vendor releases a patch.
* **Supply Chain Attack:** Compromising a third-party vendor or software update to infect all downstream customers.
* **Buffer Overflow:** Overwriting a program's memory buffer to crash the system or execute arbitrary malicious code.
* **Living off the Land (LotL):** Using legitimate, built-in system tools (like PowerShell) to carry out attacks stealthily.

## 7. Side-Channel Attacks
* **Timing Attacks:** Measuring tiny variations in execution time (cryptographic, string comparison, cache, web, or SQL) to deduce secrets.
* **Power Analysis Attacks:** Monitoring electrical power consumption of a chip to extract cryptographic keys.
* **Electromagnetic (EM) Attacks:** Capturing electromagnetic radiation emitted by devices to reconstruct screen data or memory.
* **Acoustic Cryptanalysis:** Analyzing sounds emitted by hardware components or keystrokes to infer secret data.
* **Differential Fault Analysis (DFA):** Inducing hardware errors (via voltage, heat, or lasers) and analyzing faulty outputs to extract keys.

## 8. Hardware & Firmware Attacks
* **BIOS/UEFI Rootkits:** Infecting motherboard firmware so malware survives hard drive wipes and OS reinstalls.
* **DMA (Direct Memory Access) Attacks:** Using external ports (like Thunderbolt) to read/write system RAM directly, bypassing OS security.
* **Rowhammer:** Rapidly accessing memory rows to cause electrical interference that flips bits in adjacent RAM rows.
* **Hardware Trojans:** Malicious circuit modifications secretly embedded into microchips during manufacturing.
* **Skimming / Juice Jacking:** Attaching physical hardware to card readers or public USB ports to steal data or install malware.

## 9. Wireless & Radio Frequency (RF) Attacks
* **BlueBorne / Bluetooth Spoofing:** Exploiting Bluetooth vulnerabilities to take over devices without pairing.
* **GPS Spoofing & Jamming:** Broadcasting fake or disruptive satellite signals to manipulate navigation systems.
* **IMSI Catchers (Stingrays):** Deploying fake cell towers to intercept mobile phone traffic and location data.
* **Replay Attacks:** Capturing wireless signals (e.g., key fobs, RFID badges) and retransmitting them to gain unauthorized access.

## 10. Cloud & IoT Attacks
* **Cryptojacking:** Hijacking computing resources on endpoints or cloud servers to mine cryptocurrency secretly.
* **Cloud Misconfiguration Exploits:** Accessing sensitive data left exposed due to improper permissions or storage settings.
* **IoT Botnet Attacks:** Compromising insecure smart devices to build massive botnets for DDoS or proxy networks.

## 11. AI-Driven & Emerging Attacks
* **Deepfake Fraud:** Using AI-generated audio or video to impersonate executives or trusted contacts for fraud.
* **Prompt Injection:** Crafting malicious text inputs to manipulate AI models into bypassing safeguards or leaking data.
* **Data Poisoning:** Corrupting machine learning training datasets to compromise model accuracy or insert backdoors.

## 12. Insider & Physical Threats
* **Malicious Insiders:** Authorized employees, contractors, or partners intentionally stealing data or sabotaging systems.
* **Negligent Insiders:** Accidental security breaches caused by employees mishandling data or falling for scams.
