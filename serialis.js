// A simple simulation of a user session object
class UserSession {
    constructor(username, role) {
        this.username = username;
        this.role = role; // Roles: 'guest', 'user', 'admin'
    }

    // SIMULATION: How the server checks authorization
    checkAdminAccess() {
        if (this.role === 'admin') {
            console.log(`[SUCCESS] Access GRANTED for: ${this.username}. Welcome Admin!`);
        } else {
            console.log(`[DENIED] Access DENIED for: ${this.username}. Role '${this.role}' is unauthorized.`);
        }
    }
}

// ==========================================
// 1. THE LEGITIMATE FLOW (Serialization)
// ==========================================
console.log("--- Standard Legitimate Flow ---");
const normalUser = new UserSession("alice_cameroon", "user");

// Server serializes object to send to the client (or store in a cookie)
const serializedCookie = Buffer.from(JSON.stringify(normalUser)).toString('base64');
console.log(`Serialized Session Data (Base64 Cookie): ${serializedCookie}\n`);


// ==========================================
// 2. THE FLUID ATTACKER MATRIX (Tampering)
// ==========================================
console.log("--- Exploit Phase (Logic Manipulation) ---");
// The attacker decodes the string, notices the "role" property, and alters it
const tamperedPayload = {
    username: "alice_cameroon",
    role: "admin" // Logic Bug: Attacker escalates privilege manually
};
const maliciousCookie = Buffer.from(JSON.stringify(tamperedPayload)).toString('base64');
console.log(`Tampered Malicious Cookie Sent by Client: ${maliciousCookie}\n`);


// ==========================================
// 3. THE VULNERABLE SERVER (Insecure Deserialization)
// ==========================================
console.log("--- Server-Side Processing ---");

function processIncomingRequest(cookieStream) {
    // Server decodes the raw incoming data stream
    const decodedRaw = Buffer.from(cookieStream, 'base64').toString('utf-8');
    const parsedData = JSON.parse(decodedRaw);

    // Bug: The server reconstructs the state directly from untrusted input
    const session = new UserSession(parsedData.username, parsedData.role);
    
    // Evaluate the logical state
    session.checkAdminAccess();
}

// Server processes the tampered cookie
processIncomingRequest(maliciousCookie);
