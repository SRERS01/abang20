#!/bin/bash

# Ensure a target domain argument is provided
if [ -z "$1" ]; then
    echo "❌ Error: Target domain missing."
    echo "💡 Usage: ./hunter_pipeline.sh targetdomain.com"
    exit 1
fi

DOMAIN=$1
TARGET_FILE="targets.txt"

echo "================================================================="
echo "🥷  LAUNCHING RECON & SCAN PIPELINE FOR: $DOMAIN"
echo "================================================================="

# Step 1: Subdomain Discovery
# Checks if subfinder is installed. If not, falls back to a clean single URL target.
if command -v subfinder &> /dev/null; then
    echo "[🔍] Phase A: Enumerating subdomains via Subfinder..."
    subfinder -d "$DOMAIN" -silent > raw_subs.txt
else
    echo "[⚠️] Warning: 'subfinder' tool not found on system. Creating single domain list..."
    echo "$DOMAIN" > raw_subs.txt
fi

# Step 2: Live Protocol Validation
# Checks if httpx is installed to clean up HTTP/HTTPS access points.
if command -v httpx &> /dev/null; then
    echo "[⚡] Phase B: Checking live web assets via HTTPX..."
    cat raw_subs.txt | httpx -silent -title -status-code | awk '{print $1}' > "$TARGET_FILE"
else
    echo "[⚠️] Warning: 'httpx' tool not found. Pre-pending default protocol structure..."
    sed 's/^/https:\/\//' raw_subs.txt > "$TARGET_FILE"
fi

# Clean up raw artifacts
rm -f raw_subs.txt

# Count discovered scope assets
NUM_TARGETS=$(wc -l < "$TARGET_FILE")
echo "[+] Pipeline Recon Complete: $NUM_TARGETS live endpoints gathered inside $TARGET_FILE."

# Step 3: Run the XSS Fuzzer Matrix
if [ "$NUM_TARGETS" -gt 0 ]; then
    echo "[🚀] Phase C: Launching multi-vector Puppeteer cluster scan..."
    node  xxs_detectorabang5b.js "$TARGET_FILE"
else
    echo "❌ Error: No viable target vectors found for scanning."
fi

echo "================================================================="
echo "🏁 Pipeline Finished. Check 'loot/findings.json' for bugs!"
echo "================================================================="
