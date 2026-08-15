const http = require('http');
const url = require('url');
const { exec } = require('child_process');

const PORT = 8085;

const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url, true);
    
    // Serve a simple HTML dashboard interface
    if (parsedUrl.pathname === '/') {
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end(`
            <!DOCTYPE html>
            <html>
            <head><title>Local RCE Practice Lab</title></head>
            <body style="font-family:sans-serif; padding:40px; background:#f4f7f6;">
                <div style="background:white; padding:30px; max-width:500px; margin:0 auto; border-radius:8px; box-shadow:0 2px 10px rgba(0,0,0,0.05);">
                    <h2>Network Diagnostic Portal</h2>
                    <p>Enter an IP address to execute a local system ping test:</p>
                    <form action="/ping" method="GET">
                        <input type="text" name="target" placeholder="e.g. 127.0.0.1" style="width:100%; padding:10px; margin-bottom:15px; border-radius:4px; border:1px solid #ccc;">
                        <button type="submit" style="width:100%; padding:10px; background:#007bff; color:white; border:none; border-radius:4px; font-weight:bold; cursor:pointer;">Run Diagnostic</button>
                    </form>
                </div>
            </body>
            </html>
        `);
        return;
    }

    // Vulnerable endpoint processing system terminal commands
    if (parsedUrl.pathname === '/ping') {
        const targetIp = parsedUrl.query.target;

        if (!targetIp) {
            res.writeHead(400, { 'Content-Type': 'text/plain' });
            res.end('Missing target parameter.');
            return;
        }

        // DANGEROUS: Input string is directly concatenated into an operating system command template
        const systemCommand = `ping -c 1 ${targetIp}`;
        console.log(`[🚀 SYSTEM WORKING]: Executing command -> ${systemCommand}`);

        exec(systemCommand, (error, stdout, stderr) => {
            res.writeHead(200, { 'Content-Type': 'text/plain; charset=utf-8' });
            
            // Return whatever output the terminal generated straight back to the user browser
            if (error) {
                res.end(`System Command Failed/Errored out.\n\nTerminal Output:\n${stdout}\n${stderr}`);
                return;
            }
            res.end(`System Diagnostic Successful!\n\nTerminal Output:\n${stdout}`);
        });
        return;
    }

    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('Not Found');
});

server.listen(PORT, () => {
    console.log(`\n📡 [VULNERABLE RCE LAB ACTIVE] -> Listening on http://localhost:${PORT}`);
    console.log(`💡 Test standard behavior: http://localhost:${PORT}/ping?target=127.0.0.1`);
});
