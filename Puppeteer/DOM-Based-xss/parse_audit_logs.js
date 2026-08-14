const fs = require('fs');
const path = require('path');

const directoryPath = './'; // Directory where your audit_*.txt logs are saved

function parseLogs() {
    console.log(`[+] Scanning directory for audit log traces...`);
    const files = fs.readdirSync(directoryPath).filter(file => file.startsWith('audit_') && file.endsWith('.txt'));

    if (files.length === 0) {
        console.log(`[-] No audit files found matching 'audit_*.txt'.`);
        return;
    }

    files.forEach(file => {
        console.log(`\n----------------------------------------------------------------------`);
        console.log(`🔍 PARSING LOG ARCHIVE: ${file}`);
        console.log(`----------------------------------------------------------------------`);
        
        const content = fs.readFileSync(path.join(directoryPath, file), 'utf8');

        // 1. Check for explicit Cookie Risks flagged by the scanner
        if (content.includes('[⚠️ COOKIE RISK]')) {
            console.log(`[🚨 SECURITY RISK DETECTED]: Insecure Session Cookie Configuration found!`);
            const lines = content.split('\n');
            lines.forEach(line => {
                if (line.includes('[⚠️ COOKIE RISK]')) console.log(`   👉 ${line}`);
            });
        }

        // 2. Extract and Parse Cookies to analyze rotation rules
        try {
            const preMatch = content.match(/INITIAL COOKIES:\s*([\s\S]*?)\s*POST-SUBMISSION COOKIES:/);
            const postMatch = content.match(/POST-SUBMISSION COOKIES:\s*([\s\S]*?)\s*INITIAL SESSION STORAGE:/);

            if (preMatch && postMatch) {
                const initialCookies = JSON.parse(preMatch[1]);
                const finalCookies = JSON.parse(postMatch[1]);

                // Map initial values
                const initMap = {};
                initialCookies.forEach(c => initMap[c.name] = c.value);

                finalCookies.forEach(finalCookie => {
                    const initialValue = initMap[finalCookie.name];
                    if (initialValue && initialValue === finalCookie.value) {
                        // Check if the sensitive auth/session identifier failed to rotate across states
                        if (finalCookie.name.toLowerCase().includes('session') || finalCookie.name.toLowerCase().includes('auth')) {
                            console.log(`[⚠️ POTENTIAL SESSION FIXATION]: Token '${finalCookie.name}' did not rotate upon authentication state shift.`);
                        }
                    }
                });
            }
        } catch (e) {
            console.log(`[-] Failed to parse cookie JSON profiles within this log frame.`);
        }

        // 3. Search raw server outputs for database leakage identifiers
        if (content.includes('SQL syntax') || content.includes('mysql_fetch') || content.includes('Fatal error')) {
            console.log(`[🚨 CRITICAL INJECTION DETECTED]: Raw server backend syntax trace leak found inside network stream responses.`);
        }

        // 4. Check for leakage of sensitive keys or indicators
        if (content.includes('pawaPassEnv') || content.includes('sk_live_')) {
            console.log(`[🚨 DATA LEAK DETECTED]: Sensitive third-party infrastructure configurations revealed in text buffers.`);
        }
    });
}

parseLogs();
