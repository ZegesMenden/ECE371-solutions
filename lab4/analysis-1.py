"""
Lab 4 - Part 3: PRNG vs TRNG Comparative Analysis
Platform: Raspberry Pi 5 (Python 3.11)

This script compares:
    - PRNG (LFSR-based pseudorandom generator)
    - TRNG (hardware jitter-based true random generator)

Outputs:
    - Entropy values for both
    - Histograms, autocorrelation plots
    - LED + buzzer feedback for higher entropy source
"""
# from lfsr_prng import lfsr as _lfsr
# from trng import trng as _trng
import lgpio
import time
import math
import matplotlib.pyplot as plt
import numpy as np

# ---------------- GPIO CONFIG ----------------
PIN_LED = 8
PIN_BUZZER = 7
PIN_INPUT = 17  # For TRNG input

chip = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(chip, PIN_LED)
lgpio.gpio_claim_output(chip, PIN_BUZZER)
lgpio.gpio_claim_input(chip, PIN_INPUT)

# ---------------- UTILITIES ----------------
def beep(duration=0.1):
    lgpio.gpio_write(chip, PIN_BUZZER, 1)
    time.sleep(duration)
    lgpio.gpio_write(chip, PIN_BUZZER, 0)
    pass

def blink_led(bit=1, duration=0.05):
    lgpio.gpio_write(chip, PIN_LED, bit)
    time.sleep(duration)
    lgpio.gpio_write(chip, PIN_LED, 0)
    pass

NUM_BITS = 512
def trng(bits=NUM_BITS):
    """Redfine your trng function from trng.py here"""
    random_bits = []
    previous_time = time.time_ns()

    while len(random_bits) < bits:
        while lgpio.gpio_read(chip, PIN_INPUT) == 0:
            pass

        current_time = time.time_ns()
        delta = current_time - previous_time
        raw_bit = delta & 1
        random_bits.append(raw_bit)
        blink_led(raw_bit)
        previous_time = current_time
    return random_bits

SEED_FIXED = 0b100111 # Fixed reproducible seed
TAPS = (5, 4)
N_BITS = 6
N_VALUES = (1 << N_BITS) - 1   # 63 outputs
def lfsr(seed=SEED_FIXED, taps=TAPS, n_bits=N_BITS, n_values=N_VALUES):
    """Generate pseudorandom sequence using LFSR."""
    """TODO"""
    # Avoid all-zero seed
    if seed == 0:
        seed = 1

    # Ensure state fits in n_bits
    mask = (1 << n_bits) - 1
    state = seed & mask

    sequence = []

    for _ in range(n_values):
        # 1. Take LSB as output bit
        output_bit = state & 1
        sequence.append(output_bit)

        # 2. Compute feedback bit (XOR of tap bits)
        feedback = 0
        for t in taps:          # assume taps are 0-based indices
            feedback ^= (state >> t) & 1

        # 3. Shift right and insert feedback at MSB
        state >>= 1
        state |= (feedback << (n_bits - 1))

        # (Optional safety) avoid getting stuck in all-zero state
        if state == 0:
            state = 1

    return sequence

def entropy(data):
    """Shannon entropy (bits per symbol)."""
    # Expect data as an iterable of bits (0/1). Returns entropy per bit.
    data_list = list(data)
    n = len(data_list)
    if n == 0:
        return 0.0

    count1 = sum(1 for b in data_list if b == 1)
    count0 = n - count1

    p0 = count0 / n
    p1 = count1 / n

    def term(p):
        return -p * math.log2(p) if p > 0 else 0.0

    return term(p0) + term(p1)
    

def autocorrelation(bits):
    """Compute lag-1 autocorrelation coefficient."""
    bits_array = np.array(bits)
    n = len(bits_array)
    if n < 2:
        return 0.0

    mean = np.mean(bits_array)
    var = np.var(bits_array)

    if var == 0:
        return 0.0

    cov = np.sum((bits_array[:-1] - mean) * (bits_array[1:] - mean)) / (n - 1)
    return cov / var

def plot_comparison(prng_bits, trng_bits, H_prng, H_trng):
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    plt.hist(prng_bits, bins=2, color='skyblue', edgecolor='black')
    plt.title(f"PRNG histogram (entropy={H_prng:.3f})")
    plt.xticks([0, 1])
    plt.xlabel("bit value")
    plt.ylabel("frequency")

    plt.subplot(1, 2, 2)
    plt.hist(trng_bits, bins=2, color='orange', edgecolor='black')
    plt.title(f"TRNG histogram (entropy={H_trng:.3f})")
    plt.xticks([0, 1])
    plt.xlabel("bit value")
    plt.ylabel("frequency")

    plt.tight_layout()
    plt.show()

# ---------------- MAIN ----------------
def main():
    print("Collecting data from both generators...\n")

    prng_bits = lfsr()
    trng_bits = trng()

    H_prng = entropy(prng_bits)
    H_trng = entropy(trng_bits)
    R_prng = autocorrelation(prng_bits)
    R_trng = autocorrelation(trng_bits)

    print(f"PRNG Entropy = {H_prng:.3f} bits/bit,  Autocorr = {R_prng:.3f}")
    print(f"TRNG Entropy = {H_trng:.3f} bits/bit,  Autocorr = {R_trng:.3f}\n")

    plot_comparison(prng_bits, trng_bits, H_prng, H_trng)

    if H_trng > H_prng:
        print("TRNG shows higher entropy — more random.")
        blink_led(1)
        beep(0.2)
    else:
        print("PRNG appears more uniform in this run.")
        for _ in range(2):
            blink_led(1)
            time.sleep(0.1)
            blink_led(0)

    lgpio.gpiochip_close(chip)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        lgpio.gpiochip_close(chip)
        print("\nInterrupted — GPIO cleaned up.")