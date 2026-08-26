# The hidden server-side variables (The Hacker doesn't know these initially)
m = 2**31 - 1  # Modulus
a = 1103515245 # Multiplier
c = 12345      # Increment

# Simulated server function generating numbers
def server_next_random(current_state):
    return (a * current_state + c) % m

# --- HACKER ATTACK PHASE ---
# Hacker intercepts 3 sequential public numbers from the network
X1 = 123456789
X2 = server_next_random(X1)
X3 = server_next_random(X2)

print(f"[!] Intercepted Public Numbers: X2={X2}, X3={X3}")

# Hacker executes Modular Inverse algebra to solve for 'a'
# (Using Python's pow function for modular inverse math)
diff_x = (X2 - X1) % m
inv_diff_x = pow(diff_x, -1, m)
solved_a = ((X3 - X2) * inv_diff_x) % m

# Hacker easily solves for 'c'
solved_c = (X2 - solved_a * X1) % m

print(f"[+] Broken Constants -> Solved Multiplier (a): {solved_a}, Solved Increment (c): {solved_c}")

# Now the Server generates the Secret Cryptographic Key
secret_key = server_next_random(X3)

# The Hacker calculates the exact same key without authorization
predicted_key = (solved_a * X3 + solved_c) % m

print(f"[*] Server's Secret Key:   {secret_key}")
print(f"[+] Hacker's Predicted Key: {predicted_key}")
print(f" Winning Condition Match?  {secret_key == predicted_key}")
