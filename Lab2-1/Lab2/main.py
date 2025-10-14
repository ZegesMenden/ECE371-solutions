import sys, getpass, os
from buzzer import success, fail
from aes import (
    encrypt_ecb_blocks, decrypt_ecb_blocks,
    encrypt_cbc_blocks, decrypt_cbc_blocks
)

def r(p):  return open(p, "rb").read()
def w(p,b): open(p, "wb").write(b)

cmd = sys.argv[1]
path = sys.argv[2]

k = getpass.getpass("16-char key: ").encode()[:16]

if cmd == "encrypt_ecb":
    w(path, encrypt_ecb_blocks(r(path), k))
    success()

elif cmd == "decrypt_ecb":
    w(path, decrypt_ecb_blocks(r(path), k))
    success()

elif cmd == "encrypt_cbc":
    iv, ct = encrypt_cbc_blocks(r(path), k)
    w(path, iv + ct)                     
    success()

elif cmd == "decrypt_cbc":
    blob = r(path)
    w(path, decrypt_cbc_blocks(blob[:16], blob[16:], k))
    success()

elif cmd == "visualize":
    from PIL import Image
    img = Image.open(path).convert("RGB").resize((256,256))
    rgb = img.tobytes()
    need = len(rgb)

    ecb = encrypt_ecb_blocks(rgb, k)[:need]
    _, cbc_ct = encrypt_cbc_blocks(rgb, k)
    cbc = cbc_ct[:need]

    Image.frombytes("RGB", img.size, ecb).save("ecb.png")
    Image.frombytes("RGB", img.size, cbc).save("cbc.png")
    success()
