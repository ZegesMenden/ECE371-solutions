"""TODO: Make the server more secure against side-channel attacks"""

import socket, time
from pathlib import Path
import random

SOCK_PATH = "/tmp/passwordchecker.sock"
Path(SOCK_PATH).unlink(missing_ok=True)

SECRET = b"S3cret!"
BASE_PER_BYTE_DELAY = 0.0005
MIN_TOTAL_DELAT = 0.02
MAX_JITTER = 0.001

def constant_time_compare(secret: bytes, candidate: bytes) -> bool:
    max_len = max(len(secret), len(candidate))
    diff = 0

    for i in range(max_len):
        s_byte = secret[i] if i < len(secret) else 0
        c_byte = candidate[i] if i < len(candidate) else 0
        diff |= (s_byte ^ c_byte)

        time.sleep(BASE_PER_BYTE_DELAY)
    return (diff == 0) and (len(secret) == len(candidate))

def vulnerableCompare(secret: bytes, candidate: bytes) -> bool:
    start = time.perf_counter()

    
    ok = constant_time_compare(secret, candidate)

    jitter = random.uniform(0, MAX_JITTER)
    time.sleep(jitter)

    elapsed = time.perf_counter() - start
    remaining = MIN_TOTAL_DELAT - elapsed
    if remaining > 0:
        time.sleep(remaining)
    return ok

with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
    s.bind(SOCK_PATH)
    s.listen(1)
    print("Listening on:", SOCK_PATH)
    while True:
        conn, _ = s.accept()
        with conn:
            data = conn.recv(1024)
            if not data:
                continue
            candidate = data.strip()
            ok = vulnerableCompare(SECRET, candidate)
            conn.sendall(b"1" if ok else b"0")



    
    
    """for i in range(min(len(secret), len(candidate))):
        if secret[i] != candidate[i]:
            return False
        time.sleep(DELAY_PER_MATCH)
    return len(secret) == len(candidate)

with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
    s.bind(SOCK_PATH)
    s.listen(1)
    print("Listening on:", SOCK_PATH)
    while True:
        conn, _ = s.accept()
        with conn:
            data = conn.recv(1024)
            if not data:
                continue
            candidate = data.strip()
            ok = vulnerableCompare(SECRET, candidate)
            conn.sendall(b"1" if ok else b"0")"""
