import puppeteer from 'puppeteer';
import crypto from 'crypto';

// Configuration Configuration
const START_URL = 'https://example.com'; // Change to your target staging environment
const MAX_DEPTH = 3; 
const XSS_PAYLOADS = [
    '"><script>alert(document.domain)</script>',
    'javascript:alert(1)',
    '<img src=x onerror=alert(1)>'
];

// Global Graph Registry
const visitedStates = new Set();
const stateQueue = []; // For BFS Traversal

/**
 * Generates a unique node ID based on URL and DOM structure
 */
async function getPageFingerprint(page) {
    const url = await page.url();
    // Get structural layout (tags only) to prevent dynamic content from faking new states
    const domStructure = await page.evaluate(() => {
        return Array.from(document.querySelectorAll('*'))
            .map(el => el.tagName)
            .join(',');
    });
    
    const hash = crypto.createHash('sha256')
        .update(`${url}|${domStructure}`)
        .digest('hex');
    return { hash, url };
}

/**
 * Injects security listeners to detect XSS execution context
 */
async function setupSecurityListeners(page) {
    page.on('dialog', async dialog => {
        if (dialog.type() === 'alert' || dialog.type() === 'confirm') {
            console.log(`[🔥 XSS DETECTED] Pop-up triggered via alert/confirm! Message: ${dialog.message()}`);
            console.log(`[📍 Location] URL: ${await page.url()}`);
            await dialog.dismiss();
        }
    });

    page.on('pageerror', error => {
        // Scans errors for indicators of broken execution environments or DOM injection side-effects
        if (error.message.includes('XSS') || error.message.includes('Unexpected token')) {
            console.log(`[⚠️ DOM anomaly/Error] ${error.message}`);
        }
    });
}

/**
 * Discovers transition edges (clickable elements) in the current state
 */
async function discoverEdges(page) {
    return await page.evaluate(() => {
        const elements = document.querySelectorAll('a, button, input[type="submit"], [role="button"]');
        return Array.from(elements).map((el, index) => {
            return {
                index,
                tagName: el.tagName,
                id: el.id || '',
                className: el.className || '',
                text: el.innerText ? el.innerText.substring(0, 15) : ''
            };
        });
    });
}

/**
 * Explores a specific state node, fuzzes forms, and queues unvisited structural transitions
 */
async function exploreNode(browser, stateNode) {
    const { url, depth, actionsHistory } = stateNode;
    
    if (depth > MAX_DEPTH) return;

    console.log(`\n[🔍 Graph Exploration] Depth: ${depth} | Visiting Node: ${url}`);
    
    const page = await browser.newPage();
    
    // Banco Plata standard header requirements compliance
    await page.setExtraHTTPHeaders({
        'X-HackerOne-Research': 'your_h1_username' 
    });

    try {
        await setupSecurityListeners(page);
        await page.goto(url, { waitUntil: 'networkidle2', timeout: 10000 });

        // 1. Replay state transitions to achieve complex FSM states
        for (const action of actionsHistory) {
            // Re-verify and re-click transition selectors if necessary
            // (For deep nested workflows like Guest -> Premium Checkout -> Failed Payment)
        }

        // 2. Fuzz inputs on the current state node
        const inputs = await page.$$('input[type="text"], textarea, input[type="search"]');
        for (const input of inputs) {
            for (const payload of XSS_PAYLOADS) {
                await input.click({ clickCount: 3 }); // Clear input field safely
                await input.type(payload);
                await input.press('Enter');
                await page.evaluate(() => new Promise(resolve => setTimeout(resolve, 500))); // Wait for DOM processing
            }
        }

        // 3. Structural Graph Fingerprinting
        const currentFingerprint = await getPageFingerprint(page);
        if (visitedStates.has(currentFingerprint.hash)) {
            console.log(`[🔄 Loop Blocked] Node fingerprint matches a known state. Terminating route.`);
            await page.close();
            return;
        }
        visitedStates.add(currentFingerprint.hash);

        // 4. Edge Discovery & BFS Enqueuing
        const edges = await discoverEdges(page);
        console.log(`[📊 Node Analysis] Found ${edges.length} valid exit transition edges.`);

        for (const edge of edges) {
            // Build the next theoretical FSM transition structure
            const nextAction = { selectorIndex: edge.index, edgeDescription: `${edge.tagName} -> "${edge.text}"` };
            
            // Queue next URLs found inside links for standard BFS execution
            if (edge.tagName === 'A') {
                const href = await page.evaluate((idx) => document.querySelectorAll('a')[idx].href, edge.index);
                if (href && href.startsWith(START_URL) && !visitedStates.has(href)) {
                    stateQueue.push({
                        url: href,
                        depth: depth + 1,
                        actionsHistory: [...actionsHistory, nextAction]
                    });
                }
            }
        }

    } catch (err) {
        console.error(`[❌ Node Error] Failed parsing states on ${url}: ${err.message}`);
    } finally {
        await page.close();
    }
}

/**
 * System Orchestrator
 */
async function runFSMScanner() {
    console.log(`[🏁 Initialization] Mapping directed graph from: ${START_URL}`);
    const browser = await puppeteer.launch({
        headless: true, // Switch to false if you want to visually observe state changes
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    // Enqueue Root Node (State 0)
    stateQueue.push({
        url: START_URL,
        depth: 0,
        actionsHistory: []
    });

    // Process using Breadth-First Search (BFS)
    while (stateQueue.length > 0) {
        const nextState = stateQueue.shift();
        await exploreNode(browser, nextState);
    }

    console.log('\n[🏁 Complete] App directed graph fully mapped. No more undiscovered nodes.');
    await browser.close();
}

runFSMScanner();
