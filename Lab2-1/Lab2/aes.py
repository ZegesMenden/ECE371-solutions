import os
from Cryptodome.Cipher import AES

BLOCK = 16

def pad(b):
    """Pad data so length is a multiple of 16 bytes."""
    # TODO: append extra bytes; each added byte has value = number of bytes added
    if len(b) % 16 == 0:
        return b
    bytes_to_add = 16-(len(b)%16)
    return b + [bytes_to_add]*bytes_to_add

def unpad(b):
    """Remove padding added by pad()."""
    # TODO: check last byte value and strip that many bytes
    if len(b) % 16 == 0:
        return b
    return b[0:len(b)-b[-1]]

def encrypt_ecb_blocks(pt, key):
    """Remove padding added by pad()."""
    # TODO: check last byte value and strip that many bytes
    encrypter = AES.new(key, AES.MODE_ECB)
    return encrypter.encrypt(pad(pt))

def decrypt_ecb_blocks(ct, key):
    """Decrypt data with AES in ECB mode."""
    # TODO: decrypt then unpad
    decrypter = AES.new(key, AES.MODE_ECB)
    ret_msg = decrypter.decrypt(pad(ct))
    return unpad(ret_msg)


def encrypt_cbc_blocks(pt, key):
    """Encrypt data with AES in CBC mode, return (iv, ciphertext)."""
    # TODO: generate random iv, pad, encrypt using AES.MODE_CBC
    iv = os.urandom(BLOCK)
    encrypter = AES.new(key, AES.MODE_CBC, iv)
    ret_msg = encrypter.encrypt(pad(pt))
    return iv, ret_msg

def decrypt_cbc_blocks(iv, ct, key):
    """Decrypt data with AES in CBC mode."""
    # TODO: decrypt, then unpad
    decrypter = AES.new(key, AES.MODE_CBC, iv)
    return unpad(decrypter.decrypt(ct))
