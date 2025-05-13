Cryptographic Protocols in SageMath

**Overview**
This repository implements three cryptographic protocols in SageMath (a Python-based math environment):
* RSA (Encryption, Decryption, Signatures)
* Diffie-Hellman (Secure Key Exchange)
* ECDSA (ANSI FRP256v1 & NIST P-256)

**Why SageMath?**
* Python-like syntax with advanced math features.
* Native support for large-number arithmetic and elliptic curves.

**Protocol Details**
1. RSA
* Key Generation: 1024-bit primes, e = 65537.
* Features:
  * AES key wrapping
  * SHA-256 hashing (hashlib compatible)
  * Digital signatures

2. Diffie-Hellman
* Parameters: 1000+ bit primes (adjustable for testing).
* Verification: Shared secret validation.

3. ECDSA
* Curves: ANSI FRP256v1 and NIST P-256 (standards-compliant).

**🐍 Python Compatibility**
All code is written in SageMath, which:
✔️ Uses Python syntax (e.g., def, print, lists/dicts).
✔️ Integrates with Python libraries like hashlib.
✔️ Can be mixed with pure Python code.
