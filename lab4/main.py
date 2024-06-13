import numpy as np
from collections import Counter
import matplotlib.pyplot as plt

import os

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)


def read_file(file_path):
    with open(file_path, "rb") as file:
        return file.read()


def plot_histogram(text_bin, title="Text Histogram"):
    frequency = Counter(text_bin)
    labels, values = zip(*frequency.most_common())
    plt.bar(labels, values)
    plt.xlabel("ASCII value")
    plt.ylabel("Frequency")
    plt.title(title)
    plt.show()


def string_to_bits(s):
    return "".join(format(ord(c), "08b") for c in s)


def bits_to_string(b):
    return "".join(chr(int(b[i : i + 8], 2)) for i in range(0, len(b), 8))


def bitwise_xor(a, b):
    return "".join("1" if x != y else "0" for x, y in zip(a, b))


def feistel_round(left, right, round_key):
    # Feistel function F
    combined = bitwise_xor(right, round_key)
    # Left circular shift by 1 bit
    combined_shifted = combined[1:] + combined[0]
    new_right = bitwise_xor(left, combined_shifted)
    return right, new_right


def generate_round_keys(main_key, num_rounds, block_size):
    key_bits = string_to_bits(main_key)
    round_keys = [
        key_bits[i : i + block_size] for i in range(0, len(key_bits), block_size)
    ]
    return round_keys[:num_rounds]


def feistel_network(data, round_keys, encrypt=True):
    block_size = len(round_keys[0])
    data_bits = string_to_bits(data)
    left = data_bits[:block_size]
    right = data_bits[block_size:]
    rounds = round_keys if encrypt else round_keys[::-1]

    print(f"Initial L0: {left}, R0: {right}")

    for i, key in enumerate(rounds):
        left, right = feistel_round(left, right, key)
        print(f"Round {i+1}: L{i+1}: {left}, R{i+1}: {right}")

    combined = left + right
    return bits_to_string(combined)


def main():
    file_path = f"{script_dir}/input.txt"
    main_key = "Поле глазасто, а лес ушаст."
    num_rounds = 8
    block_size = 16  # For simplicity, assuming each block is 16 bits

    text = read_file(file_path).decode("windows-1251")
    round_keys = generate_round_keys(main_key, num_rounds, block_size)

    print("Encryption Process:")
    encrypted_text = feistel_network(text, round_keys, encrypt=True)
    print("Encrypted text:", encrypted_text)

    print("\nDecryption Process:")
    decrypted_text = feistel_network(encrypted_text, round_keys, encrypt=False)
    print("Decrypted text:", decrypted_text)

    plot_histogram(string_to_bits(text), title="Original Text Histogram")
    plot_histogram(string_to_bits(encrypted_text), title="Encrypted Text Histogram")


if __name__ == "__main__":
    main()
