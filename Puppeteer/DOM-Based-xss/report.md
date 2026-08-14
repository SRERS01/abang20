# [VULNERABILITY TITLE]
Example: DOM-Based Cross-Site Scripting via URL Parameters on https://1w.run

## Summary
Provide a brief, 2-3 sentence overview of the issue, what asset it affects, and the underlying cause.
Example: A DOM-Based Cross-Site Scripting (DOM XSS) flaw was discovered on the 1win affiliate landing page layout. The client-side Nuxt framework parses parameters from the URL window query interface unsafely and writes them directly into execution context elements in the DOM tree, enabling execution of unauthorized client script contexts.

## Vulnerability Type
* Choose from the accepted list: Remote Code Execution / SQL Injection / Local File Access / XSS

## Affected Asset
* URL/Domain: https://1w.run
* Parameter / Field involved: `search` query parameter / Username Input Field

## Severity
* [Critical / High / Medium / Low] based on worst-case realistic operational impact.

## Steps to Reproduce
Provide concise, copy-pasteable execution instructions so the triage analyst can reproduce it instantly.

1. Open a clean web browser instance and navigate to the target scope area: `https://1w.run`
2. Append the following payload string to the search parameter field or type it into the interface box:
   `?search=%22%3E%3Cscript%3Ealert(document.domain)%3C%2Fscript%3E`
3. Observe that the input boundary escapes the intended string element block.
4. An absolute execution trigger occurs, popping up an alert dialog block demonstrating execution control within the host session browser container.

## Proof of Concept (PoC)
```javascript
// Paste a snippet of your Puppeteer script execution verification path here if applicable
page.on('dialog', async dialog => {
    if (dialog.type() === 'alert') {
        console.log("XSS Triggered: " + dialog.message());
    }
});
```

## Impact
Explain the business risk clearly to maximize triage validity and payout tier status.
Example: An attacker can leverage this flaw to craft malicious target URL vectors. If an authorized user or system administrator clicks the link, the payload executes context logic inside their current browser workspace. This can be used to harvest session configurations, hijack anti-bot biometric checkpoints, or manipulate page visibility triggers.

## Mitigation Suggestions
Provide actionable instructions on how their engineering team can fix the code.
Example: Implement strict input parameter sanitization and avoid rendering context variables straight to runtime DOM elements without content encoding or utilizing safe text methods.
