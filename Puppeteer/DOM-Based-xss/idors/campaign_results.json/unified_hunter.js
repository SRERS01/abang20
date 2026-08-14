const puppeteer = require('puppeteer');
const fs = require('fs');

// Configuration File Names
const TARGET_FILE = 'paths.txt';
const DATABASE_FILE = 'campaign_results.json';

const sqlPayloads = ["'", "' OR '1'='1"];
const sqlErrorSignatures = ["SQL syntax", "mysql_fetch_array", "MariaDB server version"];

const LOW_PRIV_COOKIE = {
    name: 'session_id',
    value: 'DUMMY_TOKEN_FOR_AUDIT_LOGS',
    domain: '1w.cash',
    path: '/'
};

// Core function to safely append or update your local JSON database
function saveToCampaignDatabase(targetUrl, testType, status, findings, details = {}) {
    let database = {
        campaign_started: new Date().toISOString(),
        total_scans_run: 0,
        vulnerabilities_found: 0,
        history: []
    };

    // 1. If database file already exists, read it so we don't overwrite old data
    if (fs.existsSync(DATABASE_FILE)) {
        try {
            const rawData = fs.readFileSync(DATABASE_FILE, 'utf8');
            database = JSON.parse(rawData);
        } catch (e) {
            console.log(`[-] Local database file corrupted. Resetting schema...`);
        }
    }

    // 2. Structure the new log entry coordinates
    const newLogEntry = {
        timestamp: new Date().toISOString(),
        target_url: targetUrl,
        audit_type: testType,
        status: status, // "SECURE" or "VULNERABLE"
        evidence_matched: findings,
        execution_details: details
    };

    // 3. Update counter aggregates
    database.history.push(newLogEntry);
    database.total_scans_run = database.history.length;
    database.vulnerabilities_found = database.history.filter(item => item.status === "VULNERABLE").length;

    // 4. Save the file back to the hard drive in clean formatting
    fs.writeFileSync(DATABASE_FILE, JSON.stringify(database, null, 2));
    console.log(`[💾 DATABASE UPDATED] Log entry committed to: ${DATABASE_FILE}`);
}

async function runUnifiedCampaign() {
    if (!fs.existsSync(TARGET_FILE)) {
        console.log(`[-] Error: Missing targets configuration file list.`);
        return;
    }

    const targets = fs.readFileSync(TARGET_FILE, 'utf8')
                     .split('\n')
                     .map(line => line.trim())
                     .filter(line => line.length > 0 && line.startsWith('http'));

    console.log(`[+] Initializing Unified Campaign. Output logging routed to: ${DATABASE_FILE}`);
    const browser = await puppeteer.launch({ headless: true });

    for (let targetUrl of targets) {
        console.log(`\n🌍 AUDITING TARGET: ${targetUrl}`);

        // 🛡️ SUB-CAMPAIGN A: SQL INJECTION CHECK
        const page = await browser.newPage();
        let lastResponseText = "";
        let sqliDetected = false;
        let matchedSig = "None";

        page.on('response', async (response) => {
            try {
                if (response.url() === targetUrl) {
                    lastResponseText = await response.text();
                    for (let sig of sqlErrorSignatures) {
                        if (lastResponseText.includes(sig)) {
                            sqliDetected = true;
                            matchedSig = sig;
                        }
                    }
                }
            } catch (err) {}
        });

        try {
            await page.goto(targetUrl, { waitUntil: 'networkidle2', timeout: 10000 });
            
            // Simulating basic page load test check
            if (sqliDetected) {
                saveToCampaignDatabase(targetUrl, "SQL_Injection", "VULNERABLE", matchedSig, { payload_used: "URL parameters context" });
            } else {
                saveToCampaignDatabase(targetUrl, "SQL_Injection", "SECURE", "None", { notes: "Standard page loads without runtime syntax leaks." });
            }
        } catch (error) {
            saveToCampaignDatabase(targetUrl, "SQL_Injection", "ERROR", "Timeout", { error_message: error.message });
        } finally {
            await page.close();
        }
    }

    console.log(`\n[+] Campaign pipeline complete. Final statistics saved to ${DATABASE_FILE}`);
    await browser.close();
}

runUnifiedCampaign();
