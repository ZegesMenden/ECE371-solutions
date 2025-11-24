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
from lfsr_prng import lfsr as _lfsr
from trng import trng as _trng
import lgpio
import time
import math
import matplotlib.pyplot as plt
import numpy as np

# ---------------- GPIO CONFIG ----------------
PIN_LED = 27
PIN_BUZZER = 18
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

def trng():
    """Redfine your trng function from trng.py here"""
    return _trng()

def lfsr():
    """Redefine your lfsr function from lfsr_prng.py"""
    # You can add parameters such as length or seed if your _lfsr supports them.
    # Example: return _lfsr(length=1000, seed=12345)
    return _lfsr(seed=12345)

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
    plt.title(f"Write a title here={H_prng:.3f}")
    plt.xticks([0, 1])
    plt.xlabel("Write the x label here")
    plt.ylabel("Write the y label here")

    plt.subplot(1, 2, 2)
    plt.hist(trng_bits, bins=2, color='orange', edgecolor='black')
    plt.title(f"Write a title here={H_trng:.3f}")
    plt.xticks([0, 1])
    plt.xlabel("Write the x label here")
    plt.ylabel("Write the x label here")

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