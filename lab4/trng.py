"""
Lab 4 - Part 2: True Random Number Generator using GPIO Jitter
with LED and Buzzer Feedback
"""

# import lgpio
import time
import math
import matplotlib.pyplot as plt

# --- GPIO CONFIGURATION ---
PIN_INPUT = 17        # floating input / noisy pin
PIN_LED = 27          # LED output
PIN_BUZZER = 18       # buzzer output

NUM_BITS = 512
SAMPLE_DELAY = 0.00002

# --- Setup ---
chip = lgpio.gpiochip_open(0)
lgpio.gpio_claim_input(chip, PIN_INPUT, lgpio.SET_PULL_UP)
lgpio.gpio_claim_output(chip, PIN_LED)
lgpio.gpio_claim_output(chip, PIN_BUZZER)


def beep(duration=0.05):
    lgpio.gpio_write(chip, PIN_BUZZER, 1)
    time.sleep(duration)
    lgpio.gpio_write(chip, PIN_BUZZER, 0)


def blink_led(bit, duration=0.02):
    lgpio.gpio_write(chip, PIN_LED, bit)
    time.sleep(duration)
    lgpio.gpio_write(chip, PIN_LED, 0)


def trng(bits=NUM_BITS):
    """Collect entropy via GPIO jitter."""
    """TODO"""
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




def main():
    print("Running TRNG with LED/Buzzer feedback...\n")
    bits = trng(NUM_BITS)

    beep(0.2)
    print(f"Collected {len(bits)} bits.")

    plt.figure(figsize=(10, 4))
    plt.plot(bits[:200], marker='o', linestyle='-', color='blue')
    plt.title("Write a title here")
    plt.xlabel("Write an xlabel here")
    plt.ylabel("Write a ylabel here")
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(5, 4))
    plt.hist(bits, bins=2, color='orange', edgecolor='black', rwidth=0.8)
    plt.xticks([0, 1])
    plt.title("Write a title here")
    plt.xlabel("Write an xlabel here")
    plt.ylabel("Write a ylabel here")
    plt.show()

    lgpio.gpiochip_close(chip)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        lgpio.gpiochip_close(chip)
        print("\nInterrupted. Cleaned up GPIO.")
