print("---- Diffie-Hellman Key Exchange (256-bit) ----\n")

# 1. Generate a 256-bit safe prime q (smaller for testing)
bits = 256
q = random_prime(2^bits - 1, lbound=2^(bits-1))  # 256-bit prime
print(f"Prime modulus (q) is {bits}-bit:", q.is_prime(), "\n")

# 2. Find a primitive root (generator) of q
g = primitive_root(q)
print("Generator (g):", g, "\n")

# 3. Alice and Bob generate private keys (1 < key < q-1)
PRA = randint(1, q-1)
PRB = randint(1, q-1)
print("Alice's private key (PRA):", hex(PRA))  # Print in hex for readability
print("Bob's private key (PRB):", hex(PRB), "\n")

# 4. Compute public keys
PUA = pow(g, PRA, q)
PUB = pow(g, PRB, q)
print("Alice's public key (PUA):", hex(PUA))
print("Bob's public key (PUB):", hex(PUB), "\n")

# 5. Compute shared secret
sca = pow(PUB, PRA, q)
scb = pow(PUA, PRB, q)
print("Alice's shared secret (sca):", hex(sca))
print("Bob's shared secret (scb):", hex(scb), "\n")

# 6. Verify
if sca == scb:
    print("--> SUCCESS: Shared secrets match!")
else:
    print("--> ERROR: Secrets differ!")