print("---- ECDSA with NIST P-256 ----\n")

# 1. Global Domain Parameters (NIST P-256)
p = 2^256 - 2^224 + 2^192 + 2^96 - 1  # Prime field
a = -3
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
E = EllipticCurve(GF(p), [a,b])
G = E(0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296, 
      0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)
n = G.order()  # Order of G
print("Base point G =", G)
print("Order n =", hex(n), "\n")

# 2. Key Generation
d = randint(1, n-1)  # Private key
Q = d * G  # Public key
print("Private key (d) =", hex(d))
print("Public key (Q = d*G) =", Q, "\n")

# 3. Signature Generation
e = 0x13  # Hash of message (replace with actual hash)
print("Message hash (e) =", hex(e))

# Generate signature (r, s)
while True:
    k = randint(1, n-1)
    P = k * G
    r = Integer(mod(P[0], n))  # Explicit conversion to Sage Integer
    if r == 0:
        continue
        
    s = Integer((inverse_mod(k, n) * (e + d * r)) % n)  # Fixed missing parenthesis
    if s != 0:
        break

print("Signature (r, s) =", (hex(r), hex(s)), "\n")

# 4. Signature Verification
try:
    s_int = Integer(s)  # Ensure proper type
    w = inverse_mod(s_int, n)
    u1 = mod(e * w, n)
    u2 = mod(r * w, n)
    X = Integer(u1) * G + Integer(u2) * Q
    v = mod(X[0], n)
    
    print("Verification:")
    print("v =", hex(v))
    print("r =", hex(r), "\n")
    
    if v == r:
        print("--> SUCCESS: Signature is valid!")
    else:
        print("--> ERROR: Signature is invalid!")
except Exception as ex:
    print(f"Verification failed: {ex}")