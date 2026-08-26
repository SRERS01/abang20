import random

# --- HACKER'S TOOLKIT: THE REVERSAL MATHEMATICS ---
def untamper(y):
    """ Reverses the bitwise tempering operations of MT19937 step-by-step """
    # Reverse: y = y ^ (y >> 18)
    y ^= (y >> 18)
    
    # Reverse: y = y ^ ((y << 15) & 0xefc60000)
    y ^= ((y << 15) & 0xefc60000)
    
    # Reverse: y = y ^ ((y << 7) & 0x9d2c5680)
    # Must be undone in 7-bit chunks
    for i in range(4):
        mask = (0x9d2c5680 >> (7 * (i + 1))) << (7 * (i + 1))
        y ^= ((y << 7) & 0x9d2c5680)
        
    # Reverse: y = y ^ (y >> 11)
    y ^= (y >> 11)
    y ^= (y >> 11)
    
    return y

# --- STAGE 1: SIMULATING THE SECURE TARGET SERVER ---
# The server is securely seeded; the hacker does not know this seed.
secret_seed = 9876543210
random.seed(secret_seed)

print("[*] Server started. Generating authentication tokens...")
# Hacker intercepts 624 consecutive public values (e.g., password reset tokens)
intercepted_outputs = [random.getrandbits(32) for _ in range(624)]


# --- STAGE 2: THE STATE RECOVERY ATTACK ---
print("[!] Reversing the mathematical state of the server...")
cloned_state = []

for output in intercepted_outputs:
    # Reverse engineering the tempering function to reveal the raw state integer
    raw_state_val = untamper(output)
    cloned_state.append(raw_state_val)

# The Mersenne Twister state format requires a tuple: (version, array of 624 ints, pos)
# Version 3 is standard for Python's MT19937; position 624 forces an immediate twist.
injected_state = (3, tuple(cloned_state) + (0,), 624)


# --- STAGE 3: THE COMPROMISE ---
# The hacker instantiates a completely separate, clean local generator
hacker_generator = random.Random()
hacker_generator.setstate(injected_state) # Injecting the stolen state configuration

print("[+] Internal state successfully cloned.\n")

# Let's test predictability. The server generates the next critical secret key:
server_next_secret = random.getrandbits(32)

# The hacker calculates the exact same key locally without querying the server:
hacker_predicted_secret = hacker_generator.getrandbits(32)

print(f"[*] Target Server's Next Token:  {server_next_secret}")
print(f"[+] Hacker's Predicted Token:   {hacker_predicted_secret}")
print(f" Are they perfectly synchronized? {server_next_secret == hacker_predicted_secret}")
