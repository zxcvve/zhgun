# lcg_bbs_lfsr_histogram.py

import math
import random
import matplotlib.pyplot as plt

class LinearCongruentialGenerator:
    def __init__(self, seed, a, c, m):
        self.seed = seed
        self.a = a
        self.c = c
        self.m = m
        self.current = seed

    def next(self):
        self.current = (self.a * self.current + self.c) % self.m
        return self.current

    def generate_sequence(self, n):
        sequence = []
        for _ in range(n):
            sequence.append(self.next())
        return sequence

class BlumBlumShubGenerator:
    def __init__(self, seed, p, q):
        if not (self.is_prime(p) and self.is_prime(q)):
            raise ValueError("p and q must be prime numbers")
        
        self.p = p
        self.q = q
        self.m = p * q
        if math.gcd(seed, self.m) != 1:
            raise ValueError("Seed must be relatively prime to p*q")
        self.current = seed

    @staticmethod
    def is_prime(num):
        if num <= 1:
            return False
        if num <= 3:
            return True
        if num % 2 == 0 or num % 3 == 0:
            return False
        i = 5
        while i * i <= num:
            if num % i == 0 or num % (i + 2) == 0:
                return False
            i += 6
        return True

    def next(self):
        self.current = (self.current ** 2) % self.m
        return self.current

    def generate_sequence(self, n):
        sequence = []
        for _ in range(n):
            sequence.append(self.next())
        return sequence

class LinearFeedbackShiftRegister:
    def __init__(self, seed, taps):
        self.seed = seed
        self.taps = taps
        self.current = seed
        self.length = len(bin(seed)) - 2  # Length of the LFSR

    def next(self):
        xor = 0
        for tap in self.taps:
            xor ^= (self.current >> (tap - 1)) & 1
        self.current = ((self.current << 1) | xor) & ((1 << self.length) - 1)
        return self.current

    def generate_sequence(self, n):
        sequence = []
        for _ in range(n):
            sequence.append(self.next())
        return sequence

def convert_to_bytes(sequence):
    byte_sequence = []
    for num in sequence:
        byte_sequence.extend(num.to_bytes((num.bit_length() + 7) // 8, byteorder='big'))
    return byte_sequence

def plot_histogram(byte_sequence, length, title):
    plt.hist(byte_sequence[:length], bins=range(256), edgecolor='black', alpha=0.75)
    plt.title(f'Histogram of {title} for length {length}')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.xlim([0, 255])
    plt.show()

def main():
    # Parameters
    seed_lcg = 42
    a = 1664525
    c = 1013904223
    m = 2**32

    seed_bbs = random.randint(2, 100)
    p = 499
    q = 547

    # Update LFSR to use an 8-bit initial state and appropriate taps
    seed_lfsr = 0b10101010  # An 8-bit initial state
    taps = [8, 6, 5, 4]  # Feedback polynomial x^8 + x^6 + x^5 + x^4 + 1

    lengths = [50, 100, 1000]

    # LCG
    lcg = LinearCongruentialGenerator(seed_lcg, a, c, m)
    lcg_sequence = lcg.generate_sequence(1000)
    lcg_byte_sequence = convert_to_bytes(lcg_sequence)

    for length in lengths:
        plot_histogram(lcg_byte_sequence, length, 'LCG')

    # BBS
    bbs = BlumBlumShubGenerator(seed_bbs, p, q)
    bbs_sequence = bbs.generate_sequence(1000)
    bbs_byte_sequence = convert_to_bytes(bbs_sequence)

    for length in lengths:
        plot_histogram(bbs_byte_sequence, length, 'BBS')

    # LFSR
    lfsr = LinearFeedbackShiftRegister(seed_lfsr, taps)
    lfsr_sequence = lfsr.generate_sequence(1000)
    lfsr_byte_sequence = convert_to_bytes(lfsr_sequence)

    for length in lengths:
        plot_histogram(lfsr_byte_sequence, length, 'LFSR')

if __name__ == "__main__":
    main()
