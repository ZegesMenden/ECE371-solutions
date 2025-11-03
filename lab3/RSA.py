"""
RSA.py

Lab: Secure Communication with RSA, DES, and Raspberry Pi GPIO

Your task:
-----------
Implement the RSA functions below:
- gcd
- multiplicative_inverse
- is_prime
- generate_keypair
- encrypt
- decrypt

You will use these functions in both chat and image client/server code.

Notes:
- Work step by step. First get gcd() working, then move to modular inverse, etc.
- Test your implementation with the provided example at the bottom.
"""

import random

def gcd(a, b):
    """
    Compute the greatest common divisor of a and b.
    """
    # TODO: implement Euclidean algorithm
    while b != 0:
        a, b = b, a % b
    return a
    pass


def multiplicative_inverse(e, phi):
    """
    Compute the modular inverse of e modulo phi.
    Returns d such that (d*e) % phi == 1
    """
    # TODO: implement Extended Euclidean Algorithm
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    _, x, _ = extended_gcd(e, phi)
    return (x % phi + phi) % phi
    pass



def is_prime(num):
    """
    Check if a number is prime.
    Return True if prime, False otherwise.
    """
    # TODO: implement primality check
    if num <= 1:
        return False
    if num == 2:
        return True
    if num % 2 == 0:
        return False
    
    for i in range(3, int(num**0.5) + 1, 2):
        if num % i == 0:
            return False
    return True


def generate_keypair(p, q):
    """
    Generate RSA keypair given two primes p and q.
    Returns (public, private) where:
    - public = (e, n)
    - private = (d, n)
    """
    # TODO: implement RSA keypair generation
    # Steps:
    # 1. Compute n = p * q
    # 2. Compute phi = (p-1)*(q-1)
    # 3. Choose e such that gcd(e, phi) = 1
    # 4. Compute d = multiplicative_inverse(e, phi)
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Both numbers must be prime.") 
    if p ==q:
        raise ValueError("p and q cannot be equal.")
    
    n = p * q

    phi = (p - 1) * (q - 1)

    e = 65537
    if gcd(e, phi) != 1:
        for i in range(3, phi, 2):
            if gcd(i, phi) == 1:
                e = i
                break
    d = multiplicative_inverse(e, phi)
    return ((e, n), (d, n))  
pass


def encrypt(pk, plaintext):
    """
    Encrypt plaintext using key pk = (e or d, n).
    Plaintext is a string; return a list of integers (ciphertext).
    """
    # Block-oriented RSA encryption using bytes and PKCS#7-style padding.
    key, n = pk
    if not isinstance(plaintext, (bytes, bytearray)):
        data = plaintext.encode('utf-8')
    else:
        data = bytes(plaintext)

    k = (n.bit_length() - 1) // 8
    if k <= 0:
        raise ValueError("Modulus n is too small to encrypt any data")

    # PKCS#7 padding
    pad_len = k - (len(data) % k)
    if pad_len == 0:
        pad_len = k
    data += bytes([pad_len]) * pad_len

    cipher = []
    for i in range(0, len(data), k):
        block = data[i:i+k]
        m = int.from_bytes(block, byteorder='big')
        cipher.append(pow(m, key, n))
    return cipher


def decrypt(pk, ciphertext):
    """
    Decrypt ciphertext using key pk = (e or d, n).
    Ciphertext is a list of integers; return a string (plaintext).
    """
    # Block-oriented RSA decryption matching encrypt().
    key, n = pk
    k = (n.bit_length() - 1) // 8
    if k <= 0:
        raise ValueError("Modulus n is too small to decrypt any data")

    out_bytes = bytearray()
    for num in ciphertext:
        m = pow(num, key, n)
        block = m.to_bytes(k, byteorder='big')
        out_bytes.extend(block)

    if len(out_bytes) == 0:
        return ''

    pad_len = out_bytes[-1]
    if pad_len < 1 or pad_len > k:
        try:
            return out_bytes.decode('utf-8')
        except Exception:
            return ''.join(chr(b) for b in out_bytes)

    if out_bytes[-pad_len:] != bytes([pad_len]) * pad_len:
        try:
            return out_bytes.decode('utf-8')
        except Exception:
            return ''.join(chr(b) for b in out_bytes)

    plain_bytes = out_bytes[:-pad_len]
    try:
        return plain_bytes.decode('utf-8')
    except Exception:
        return plain_bytes.decode('latin-1')
    pass


# --- Example test case ---
if __name__ == "__main__":
    print("RSA Test Example")

    # Example primes (small for testing)
    p, q = 61, 53
    public, private = generate_keypair(p, q)

    print("Public key:", public)
    print("Private key:", private)

    message = "HELLO"
    print("Original message:", message)

    encrypted_msg = encrypt(public, message)
    print("Encrypted message:", encrypted_msg)

    decrypted_msg = decrypt(private, encrypted_msg)
    print("Decrypted message:", decrypted_msg)
