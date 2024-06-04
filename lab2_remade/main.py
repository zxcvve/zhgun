import codecs
from sys import getdefaultencoding
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sympy
from pylfsr import LFSR
import struct


def lcg(x, a, c, m):
    while True:
        x = (a * x + c) % m
        yield x


def random_uniform_sample(n, interval, seed=413):
    a, c, m = 1103515245, 12345, 2**31
    bsdrand = lcg(seed, a, c, m)

    lower, upper = interval[0], interval[1]
    sample = []

    for i in range(n):
        observation = (upper - lower) * (next(bsdrand) / (2**31 - 1)) + lower
        sample.append(round(observation))

    return sample


class BlumBlumShub(object):
    def __init__(self, length):
        self.length = length * 8

    def random_generator(self):
        x = 4
        while self.length:
            x += 1
            p, q = 11, 23
            m = p * q
            z = (x**2) % m
            self.length -= 1
            yield str(bin(z).count("1") % 2)

    def get_random_bits(self):
        return "".join(self.random_generator())


def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xFF)
        v >>= 8
    return bytes(b[::-1])


def visualize(array):
    np_carts = np.zeros(256)
    indx = np.arange(256)

    for i in array:
        code_i = i
        add_ = np_carts[code_i]
        add_ = add_ + 1
        np_carts[code_i] = add_

    plt.figure(figsize=(20, 9))

    plt.tight_layout()

    plt.xticks(np.arange(min(indx), max(indx) + 1, 5.0))
    plt.bar(indx, np_carts, color="#0B60B0", log=False)

    plt.ylabel("Frequency")
    plt.title("Frequency Analysis")
    plt.show()


# rus = random_uniform_sample(50, [0, 255])
# print(rus)
# print("LCGx50")
# visualize(rus)

# rus = random_uniform_sample(100, [0, 255])
# print(rus)
# print('LCGx100')
# visualize(rus)

# rus = random_uniform_sample(1000, [0, 255])
# print(rus)
# print('LCGx1000')
# visualize(rus)

# bb = BlumBlumShub(50)
# s = bb.get_random_bits()
# print(s)
# bl = list(int(s[i : i + 8], 2) for i in range(0, len(s), 8))
# #bl = bitstring_to_bytes(s)
# print(bl)
# print('BlumBlumShub x 50')
# visualize(bl)

# bb = BlumBlumShub(100)
# s = bb.get_random_bits()
# print(s)
# bl = list(int(s[i : i + 8], 2) for i in range(0, len(s), 8))
# print(bl)
# print('BlumBlumShub x 100')
# visualize(bl)

# bb = BlumBlumShub(1000)
# s = bb.get_random_bits()
# print(s)
# bl = list(int(s[i : i + 8], 2) for i in range(0, len(s), 8))
# print(bl)
# print('BlumBlumShub x 1000')
# visualize(bl)


# fpoly = [5,2]
# L = LFSR(fpoly=fpoly, initstate='random')

# # Generate K-bits
# k=50*8
# seq_k  = L.runKCycle(k)

# print('bits')
# print(L.arr2str(seq_k))

# bl = list(int(str(seq_k[i : i + 8]).replace(']','').replace('[','').replace(' ',''), 2) for i in range(0, len(seq_k), 8))
# print(bl)
# print('LFSR x 50')
# visualize(bl)

# fpoly = [5,2]
# L = LFSR(fpoly=fpoly, initstate='random')

# # Generate K-bits
# k=100*8
# seq_k  = L.runKCycle(k)

# print('bits')
# print(L.arr2str(seq_k))

# bl = list(int(str(seq_k[i : i + 8]).replace(']','').replace('[','').replace(' ',''), 2) for i in range(0, len(seq_k), 8))
# print(bl)
# print('LFSR x 100')
# visualize(bl)

fpoly = [5,2]
L = LFSR(fpoly=fpoly, initstate='random')

# Generate K-bits
k=1000*8
seq_k  = L.runKCycle(k)

print('bits')
print(L.arr2str(seq_k))

bl = list(int(str(seq_k[i : i + 8]).replace(']','').replace('[','').replace(' ',''), 2) for i in range(0, len(seq_k), 8))
print(bl)
print('LFSR x 1000')
visualize(bl)
