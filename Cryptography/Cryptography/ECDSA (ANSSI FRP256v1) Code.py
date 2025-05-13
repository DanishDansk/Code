print("---- ECDSA (ANSSI FRP256v1) ----\n")

# 1. Global Domain Parameters (ANSSI FRP256v1)
q = 109454571331697278617670725030735128145969349647868738157201323556196022393859
a = -3
b = 107744541122042688792155207242782455150382764043089114141096634497567301547839
ec = EllipticCurve(GF(q), [a, b])
G = ec(82638672503301278923015998535776227331280144783487139112686874194432446389503, 
       43992510890276411535679659957604584722077886330284298232193264058442323471611)
n = G.order()  # Order of G
print("Base point G =", G)
print("Order n =", n, "\n")

# 2. Key Generation
d = randint(1, n-1)  # Private key
Q = d * G  # Public key
print("Private key (d) =", d)
print("Public key (Q = d*G) =", Q, "\n")

# 3. Signature Generation
e = 13  # Hash of message (replace with actual SHA-256 hash)
print("Message hash (e) =", e)

# Generate signature (r, s)
while True:
    k = randint(1, n-1)
    P = k * G
    r = mod(P[0], n)
    if r == 0:
        continue
    s = mod(inverse_mod(k, n) * (e + d * r), n)
    if s != 0:
        break

print("Signature (r, s) =", (r, s), "\n")

# 4. Signature Verification (FIXED)
try:
    s_int = Integer(s)  # Explicit conversion
    w = inverse_mod(s_int, n)
    u1 = mod(e * w, n)
    u2 = mod(r * w, n)
    X = u1 * G + u2 * Q
    v = mod(X[0], n)
    
    print("Verification:")
    print("v =", v)
    print("r =", r, "\n")
    
    if v == r:
        print("--> SUCCESS: Signature is valid!")
    else:
        print("--> ERROR: Signature is invalid!")
except Exception as ex:
    print(f"Verification failed: {ex}")