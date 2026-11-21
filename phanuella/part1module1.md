# Part 1 – Foundations Before Security+
## Module 1: Introduction to Computer Science (Practical Lab Guide)

> **Objective:** Gain hands-on familiarity with the foundational computing concepts required before tackling CompTIA Security+ domains.  
> **Prerequisites:** A Windows, Linux, or macOS computer with terminal/command prompt access and Python 3 installed.

---

### 1. Computer Science vs. Information Technology
* **Concept:** Computer Science (CS) focuses on creating software, algorithms, and computing theory. Information Technology (IT) focuses on deploying, managing, and securing systems and networks.
* **Practical Task:**
  1. Open your terminal or command prompt.
  2. Run a system diagnostic command (IT task):
     * **Windows:** `systeminfo`
     * **Linux/macOS:** `uname -a && uptime`
  3. Write a simple script to sort a list of numbers (CS task) using Python:
     ```bash
     python3 -c "nums =; print(sorted(nums))"
     ```

### 2. Computer Architecture (Von Neumann Model)
* **Concept:** Modern computers follow the Von Neumann architecture: Input $\rightarrow$ CPU (Control Unit + ALU) $\leftrightarrow$ Memory $\rightarrow$ Output.
* **Practical Task:**
  1. Trace a simple program execution in Python to see how instructions fetch data from memory, process it in the ALU, and output it:
     ```python
     # Save as architecture_demo.py and run: python3 architecture_demo.py
     a = 10          # Stored in Memory (RAM)
     b = 20          # Stored in Memory (RAM)
     c = a + b       # Fetched to CPU ALU, added, result sent back to RAM
     print(c)        # Sent to Output device (Monitor)
     ```

### 3. Hardware and Software
* **Concept:** Hardware is the physical machinery; software is the set of instructions telling hardware what to do (System Software vs. Application Software).
* **Practical Task:**
  1. List physical hardware components via CLI:
     * **Windows:** `wmic baseboard get product,Manufacturer`
     * **Linux:** `lshw -short` (or `lsblk` and `lscpu`)
     * **macOS:** `system_profiler SPHardwareDataType`
  2. List installed application software:
     * **Windows:** `winget list`
     * **Linux (Debian/Ubuntu):** `dpkg -l | head -n 20`
     * **macOS:** `ls /Applications`

### 4. Input and Output (I/O) Devices
* **Concept:** Peripherals that send data to the CPU (Input) or receive data from it (Output).
* **Practical Task:**
  1. Inspect connected USB/I/O devices:
     * **Windows:** `pnputil /enum-devices /connected`
     * **Linux:** `lsusb`
     * **macOS:** `system_profiler SPUSBDataType`
  2. Redirect standard input (`stdin`) to standard output (`stdout`) and a file:
     ```bash
     echo "Testing I/O Redirection" > io_test.txt
     cat < io_test.txt
     ```

### 5. CPU, RAM, and ROM
* **Concept:** CPU executes instructions; RAM is volatile working memory; ROM/UEFI stores non-volatile boot firmware.
* **Practical Task:**
  1. Check CPU cores, clock speed, and current RAM usage:
     * **Windows:** `taskmgr` (Performance Tab) or `wmic cpu get name,NumberOfCores`
     * **Linux:** `lscpu && free -h`
     * **macOS:** `sysctl -n machdep.cpu.brand_string && vm_stat`
  2. Check BIOS/UEFI (ROM) firmware version:
     * **Windows:** `wmic bios get smbiosbiosversion`
     * **Linux:** `sudo dmidecode -s bios-version`

### 6. Storage Devices
* **Concept:** Non-volatile media (HDD, SSD, NVMe) used for long-term data retention.
* **Practical Task:**
  1. View physical disks, partitions, and free space:
     * **Windows:** `wmic diskdrive get model,size,interfaceType`
     * **Linux:** `lsblk -o NAME,SIZE,TYPE,MOUNTPOINT`
     * **macOS:** `diskutil list`

### 7. Motherboards and Processors
* **Concept:** The motherboard connects the CPU, RAM, storage, and expansion buses (PCIe).
* **Practical Task:**
  1. Inspect PCI buses and chipset connections:
     * **Windows:** `msinfo32` (System Summary & Components)
     * **Linux:** `lspci`
     * **macOS:** `ioreg -l | grep -i "board-id"`

### 8. Operating Systems (OS)
* **Concept:** Manages hardware resources, provides a user interface, and enforces security boundaries between user space and kernel space.
* **Practical Task:**
  1. Identify your OS version, kernel build, and current user privileges:
     * **Windows:** `ver && whoami /priv`
     * **Linux/macOS:** `uname -r && id`

### 9. Files and File Systems
* **Concept:** File systems (NTFS, ext4, APFS, FAT32) organize how data is stored, indexed, and permissioned on a disk.
* **Practical Task:**
  1. Identify the file system format of your primary drive:
     * **Windows:** `fsutil fsinfo volumeinfo C:`
     * **Linux:** `df -Th`
     * **macOS:** `diskutil info / | grep "File System"`
  2. Create a file, inspect its metadata (inode/timestamps), and modify permissions:
     ```bash
     touch secplus_lab.txt
     stat secplus_lab.txt       # Linux/macOS (Use 'dir /q secplus_lab.txt' on Windows)
     chmod 600 secplus_lab.txt  # Restricts read/write to owner only (Linux/macOS)
     ```

### 10. Binary, Decimal, Hexadecimal, and Octal
* **Concept:** Computers operate in Base-2 (Binary); humans use Base-10 (Decimal); memory addresses and MAC addresses use Base-16 (Hex); Linux permissions use Base-8 (Octal).
* **Practical Task:**
  1. Use Python as an interactive base converter:
     ```python
     num = 255
     print("Decimal:", num)
     print("Binary:", bin(num))       # 0b11111111
     print("Hexadecimal:", hex(num))  # 0xff
     print("Octal:", oct(num))        # 0o377
     ```

### 11. Bits, Bytes, and Data Representation
* **Concept:** 1 Bit = 0 or 1. 1 Byte = 8 Bits. Text is represented via standards like ASCII and UTF-8.
* **Practical Task:**
  1. Convert text characters into their raw ASCII decimal and binary representations:
     ```python
     text = "SEC+"
     for char in text:
         print(f"{char} -> Decimal: {ord(char)} -> Binary: {format(ord(char), '08b')}")
     ```

### 12. Boolean Algebra
* **Concept:** Mathematical logic using `TRUE` (1) and `FALSE` (0) with operators `AND`, `OR`, `NOT`, and `XOR`. (Crucial for firewall rules and cryptography).
* **Practical Task:**
  1. Evaluate Boolean expressions in Python (pay special attention to `XOR` `^`, used heavily in encryption):
     ```python
     A = 1  # True
     B = 0  # False
     print("AND:", A & B)  # 0
     print("OR :", A | B)  # 1
     print("XOR:", A ^ B)  # 1 (True only when inputs differ)
     ```

### 13. Logic Gates
* **Concept:** Physical electronic circuits implementing Boolean operations (AND, OR, NOT, NAND, NOR, XOR).
* **Practical Task:**
  1. Build a truth-table generator script in Python to simulate a `NAND` gate (universal gate used in flash memory):
     ```python
     print("A | B | NAND")
     for a in:
         for b in:
             nand_out = int(not (a and b))
             print(f"{a} | {b} |  {nand_out}")
     ```

### 14. Number Systems and Conversions
* **Concept:** Converting IP addresses (dotted-decimal) and subnet masks into binary is essential for networking and security.
* **Practical Task:**
  1. Convert the IPv4 address `192.168.1.10` into 32-bit binary:
     ```python
     ip = "192.168.1.10"
     binary_ip = ".".join([format(int(octet), '08b') for octet in ip.split(".")])
     print(f"IP: {ip} -> Binary: {binary_ip}")
     ```

### 15. Data Structures
* **Concept:** Ways of organizing data in memory (Arrays/Lists, Hash Maps/Dictionaries, Stacks, Queues). Buffer overflows happen when data exceeds an array's allocated boundary.
* **Practical Task:**
  1. Implement a **Stack** (LIFO - Last In, First Out) and a **Hash Map** (Key-Value lookup) in Python:
     ```python
     # Stack (used for function call memory)
     call_stack = []
     call_stack.append("main()")
     call_stack.append("login()")
     print("Popped from stack:", call_stack.pop())

     # Hash Map / Dictionary (used for fast lookups, e.g., user database)
     users = {"admin": "UID_0", "guest": "UID_1001"}
     print("Admin ID:", users["admin"])
     ```

### 16. Algorithms
* **Concept:** Step-by-step instructions to solve a problem, evaluated by time and space complexity (Big-O notation).
* **Practical Task:**
  1. Compare Linear Search ($O(n)$) vs. Binary Search ($O(\log n)$) on a sorted list of 1,000,000 IDs:
     ```python
     import bisect, time

     data = list(range(1_000_000))
     target = 999_999

     # Linear Search
     start = time.time()
     found = target in data
     print(f"Linear Search time: {time.time() - start:.6f}s")

     # Binary Search
     start = time.time()
     index = bisect.bisect_left(data, target)
     print(f"Binary Search time: {time.time() - start:.6f}s")
     ```

### 17. Programming Fundamentals
* **Concept:** Variables, control flow (`if/else`), loops (`for/while`), and functions. Security analysts read scripts to spot malicious behavior.
* **Practical Task:**
  1. Write a basic log-parsing script that detects failed login attempts:
     ```python
     logs = [
         "INFO: User alice logged in",
         "ERROR: Failed password for root",
         "INFO: User bob logged in",
         "ERROR: Failed password for admin"
     ]

     def check_alerts(log_entries):
         for entry in log_entries:
             if "ERROR" in entry:
                 print(f"[SECURITY ALERT] {entry}")

     check_alerts(logs)
     ```

### 18. Processes and Threads
* **Concept:** A **Process** is an independent running program with its own memory space. A **Thread** is a lightweight execution unit inside a process that shares memory with other threads.
* **Practical Task:**
  1. View active Processes and their Process IDs (PIDs):
     * **Windows:** `tasklist`
     * **Linux/macOS:** `ps aux | head -n 15`
  2. View active Threads within a process:
     * **Linux:** `ps -eLf | head -n 15`
     * **Windows (PowerShell):** `Get-Process | Select-Object Name, Id, @{Name="Threads";Expression={$_.Threads.Count}} | Select-Object -First 10`

### 20. Memory Management (Deep-Dive Lab)
* **Concept:** The Operating System manages physical RAM and Virtual Memory (paging/swap), isolates process memory spaces, and enforces hardware/software security controls like **ASLR** (Address Space Layout Randomization) and **DEP/NX** (Data Execution Prevention) to block memory-corruption exploits.
* **Practical Task 1: Inspect Virtual Memory & Paging/Swap**
  * **Windows (PowerShell):**
    ```powershell
    Get-CimInstance Win32_OperatingSystem | Select-Object TotalVisibleMemorySize, FreePhysicalMemory, TotalVirtualMemorySize, FreeVirtualMemory
    ```
  * **Linux:**
    ```bash
    free -m && swapon --show
    ```
  * **macOS:**
    ```bash
    vm_stat && sysctl vm.swapusage
    ```

* **Practical Task 2: Observe Stack vs. Heap Allocation & Memory Addresses**
  Run this Python script to see how variables are assigned dynamic memory addresses in hexadecimal:
  ```python
  import sys

  a = 42
  b = [1, 2, 3, 4, 5]

  print(f"Integer 'a' | Address: {hex(id(a))} | Size: {sys.getsizeof(a)} bytes")
  print(f"List 'b'    | Address: {hex(id(b))} | Size: {sys.getsizeof(b)} bytes")
  ```

* **Practical Task 3: Verify ASLR (Security Control Check)**
  Run the script above **twice** in a row. Notice how the hexadecimal memory addresses (`0x7f...`) change every time the program executes—this is **ASLR** randomizing memory locations so attackers cannot predict where to inject malicious payloads.
  * **Check ASLR status on Linux:**
    ```bash
    cat /proc/sys/kernel/randomize_va_space
    # Output '2' = Full randomization enabled (Secure)
    # Output '0' = Disabled (Vulnerable)
    ```

* **Practical Task 4: Inspect a Process's Memory Map**
  See how an OS divides a running program into distinct regions (Code/Text, Heap, Stack, Shared Libraries):
  * **Linux:**
    ```bash
    pmap \$\$ | head -n 20   # Maps the memory regions of your current shell process
    ```
  * **Windows:** Download Microsoft Sysinternals **VMMap** or check working set memory via PowerShell:
    ```powershell
    Get-Process -Id \$PID | Select-Object ProcessName, WorkingSet, VirtualMemorySize, PagedMemorySize
    ```
