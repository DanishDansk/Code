print("----RSA----\n")

# Import hashlib for SHA-256 (required in SageMath)
import hashlib

# 1a. Generate 1024-bit primes p and q
min_bits = 1024
p = random_prime(2^(min_bits + 1) - 1, lbound=2^min_bits)
print("Is p prime?", p.is_prime())
print("p =", p, "\n")

q = random_prime(2^(min_bits + 1) - 1, lbound=2^min_bits)
print("Is q prime?", q.is_prime())
while p == q:  # Ensure p ≠ q
    q = random_prime(2^(min_bits + 1) - 1, lbound=2^min_bits)
print("q =", q, "\n")

# 1b. Compute n and φ(n)
n = p * q
phi_n = (p - 1) * (q - 1)
print("n =", n, "\n")
print("φ(n) =", phi_n, "\n")

# 1c. Public key e = 65537, private key d
e = 65537
gcd_phine = gcd(phi_n, e)
print("GCD(φ(n), e) =", gcd_phine, "\n")

if gcd_phine != 1:
    print("ERROR: e and φ(n) are not coprime. Choose a different e.\n")
else:
    d = inverse_mod(e, phi_n)
    print("Private key d =", d, "\n")

# 1d. Generate random 256-bit AES key (m)
k_aes = randint(0, 2^256 - 1)
m = k_aes
print("--RSA Encryption--")
print("AES Key (m) =", m, "\n")

# 1e. Encrypt m: c = m^e mod n
ciphertext = power_mod(m, e, n)
print("Ciphertext (c = m^e mod n) =", ciphertext, "\n")

# Decrypt (verification)
plaintext = power_mod(ciphertext, d, n)
print("--RSA Decryption--")
print("Decrypted Plaintext =", plaintext, "\n")
if plaintext == m:
    print("SUCCESS: Decrypted plaintext matches original message!\n")
else:
    print("ERROR: Decryption failed!\n")

# 1f. Compute SHA-256 hash of m (fingerprint f1)
print("--SHA-256 Hashing--")
hash_m = hashlib.sha256(str(m).encode('utf-8')).hexdigest()
f1 = int(hash_m, 16)  # Convert hex to integer
print("SHA-256 Hash (f1) =", hash_m)
print("f1 (as integer) =", f1, "\n")

# 1g. Digital Signature: DS = f1^d mod n
print("--Digital Signature--")
DS = power_mod(f1, d, n)
print("Digital Signature (DS = f1^d mod n) =", DS)