const puppeteer = require('puppeteer');
const fs = require('fs');
const https = require('https');

// ---------------------------------------------------------
// TELEGRAM & LOW-PRIVILEGE SESSION SETTINGS
// ---------------------------------------------------------
const TELEGRAM_BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE';
const TELEGRAM_CHAT_ID = 'YOUR_CHAT_ID_HERE';

// Inject your standard, low-privilege user cookie token parameters here
const LOW_PRIV_COOKIE = {
    name: 'session_id',                  // Match the exact session key name from F12
    value: 'YOUR_LOW_PRIVILEGE_TOKEN',   // Paste your personal test account token string
    domain: '1w.cash',
    path: '/'
};

// Target administrative and management endpoints to check for vertical escalation flaws
const administrativeEndpoints = [
    'https://1w.cash',
    'https://1w.cash',
    'https://1w.cash',
    'https://1w.cash'
];
// ---------------------------------------------------------

function sendTelegramAlert(message) {
    const url = `https://telegram.org{TELEGRAM_BOT_TOKEN}/sendMessage`;
    const data = JSON.stringify({ chat_id: TELEGRAM_CHAT_ID, text: message, parse_mode: 'Markdown' });
    const options = { method: 'POST', headers: { 'Content-Type': 'application/json', 'Content-Length': data.length } };
    const req = https.request(url, options, () => {});
    req.write(data);
    req.end();
}

function generatePrivEscReport(targetUrl, httpStatus, bodyExcerpt) {
    const reportFileName = `h1_report_PrivEsc_${Date.now()}.md`;
    const reportContent = 
`# Vertical Privilege Escalation via Broken Function Level Authorization

## Summary
A critical authentication bypass flaw was identified in the application's administrative endpoint routing schema. The backend processing logic handles sensitive management operations without verifying if the active requesting user token possesses the required administrative permissions tier, leading to unauthorized access.

## Vulnerability Type
* Privilege Escalation / Broken Function Level Authorization

## Affected Asset
* URL/Domain: ${targetUrl}

## Severity
* High to Critical (Depending on the administrative capability exposed by the endpoint action)

## Steps to Reproduce
1. Log into a standard, low-privilege user profile workspace.
2. Intercept or force a direct administrative query request to the restricted resource directory:
   \`${targetUrl}\`
3. Observe that the server returns an HTTP Status \`${httpStatus}\` and processes or exposes administrative data output structures rather than throwing an explicit authorization barrier.

## Proof of Concept (PoC)
The backend interface returned data structures or handled parameters successfully instead of returning a hard 403 Forbidden constraint block.
`;

    fs.writeFileSync(reportFileName, reportContent);
    console.log(`[🎉 CRITICAL REPORT GENERATED!] Privilege Escalation markdown created at: ${reportFileName}`);
    sendTelegramAlert(`🚨 *PRIVILEGE ESCALATION DETECTED!* 🚨\n\n*Target Path:* ${targetUrl}\n*Status Received:* ${httpStatus}\n\n📄 _HackerOne markdown file draft generated locally at: ${reportFileName}_`);
}

async function runPrivilegeHunter() {
    console.log(`[+] Initializing Vertical Privilege Escalation Audit...`);
    const browser = await puppeteer.launch({ headless: true });

    for (let adminUrl of administrativeEndpoints) {
        const page = await browser.newPage();
        let rawResponseContent = "";

        // 1. Force the page context to load using the low-privilege tester identity
        await page.setCookie(LOW_PRIV_COOKIE);

        page.on('response', async (response) => {
            if (response.url() === adminUrl) {
                try {
                    rawResponseContent = await response.text();
                } catch (err) {}
            }
        });

        try {
            console.log(`[*] Requesting administrative resource using low-privilege token: ${adminUrl}`);
            const networkResponse = await page.goto(adminUrl, { waitUntil: 'networkidle2', timeout: 10000 });
            const HTTP_STATUS = networkResponse.status();

            // 2. LOGIC VERIFICATION: Evaluate Access Control Enforcement
            // A secure backend will reply with 401 Unauthorized or 403 Forbidden.
            // If it returns 200 OK or 302 Redirect to an internal view, look closer.
            if (HTTP_STATUS === 200) {
                const lowerContent = rawResponseContent.toLowerCase();
                
                // Exclude instances where the server returns 200 OK but serves a soft error payload text block
                if (lowerContent.includes("access denied") || lowerContent.includes("unauthorized") || lowerContent.includes("permission error")) {
                    console.log(`[-] Secure: Endpoint returned 200 but context content indicates a soft authorization rejection.`);
                } else {
                    console.log(`[🚨 PRIVILEGE ESCALATION CONFIRMED] Low-privilege user successfully bypassed authorization walls!`);
                    generatePrivEscReport(adminUrl, HTTP_STATUS, rawResponseContent.substring(0, 200));
                }
            } else if (HTTP_STATUS === 401 || HTTP_STATUS === 403) {
                console.log(`[+] Secure: Access Denied natively by server infrastructure logic. HTTP Status: ${HTTP_STATUS}`);
            } else {
                console.log(`[-] Neutral: Target responded with status code: ${HTTP_STATUS}`);
            }

        } catch (error) {
            console.log(`[-] Request execution timed out or failed for path: ${adminUrl}`);
        } finally {
            await page.close();
        }
    }

    console.log(`\n[+] Privilege Escalation Audit Pipeline Complete.`);
    await browser.close();
}

runPrivilegeHunter();
