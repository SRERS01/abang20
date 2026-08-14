#!/bin/bash
if [ -z "$1" ]; then echo "❌ Error: Missing domain"; exit 1; fi
DOMAIN=$1
TARGET_FILE="targets.txt"
RAW_URLS="wayback_raw.txt"
echo "[🔍] Phase A: Fetching Subdomains..."
if command -v subfinder &> /dev/null; then subfinder -d "$DOMAIN" -silent > raw_subs.txt; else echo "$DOMAIN" > raw_subs.txt; fi
echo "[📜] Phase B: Extracting Historical Paths..."
curl -s "https://archive.org{DOMAIN}/*&output=json&fl=original&collapse=urlkey" | jq -r ".[]" 2>/dev/null | grep "?" > "$RAW_URLS"
if [ ! -s "$RAW_URLS" ]; then cat raw_subs.txt > "$RAW_URLS"; fi
echo "[⚡] Phase C: Verifying Active HTTP Status codes..."
if command -v httpx &> /dev/null; then cat "$RAW_URLS" raw_subs.txt | sort -u | httpx -silent -status-code | grep -v "404" | awk "{print \$1}" > "$TARGET_FILE"; else cat "$RAW_URLS" raw_subs.txt | sort -u | sed "s/^/https:\/\//" > "$TARGET_FILE"; fi
rm -f raw_subs.txt "$RAW_URLS"
NUM=$(wc -l < "$TARGET_FILE")
echo "[+] Live Targets Found: $NUM"
if [ "$NUM" -gt 0 ]; then echo "[🚀] Starting Puppeteer Matrix..."; node xss_detectorabang8.js "$TARGET_FILE"; fi
