import matplotlib.pyplot as plt
from pylfsr import LFSR
from collections import Counter
import numpy as np
import os

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)

class VigenereCipher:
    def __init__(self, text, password):
        self.text = text
        self.password = password
        self.extended_password = self._extend_password()

    def _extend_password(self):
        extended_password = self.password
        while len(extended_password) < len(self.text):
            extended_password += self.password
        return extended_password[:len(self.text)]

    def encrypt(self):
        encrypted_text = []
        for i in range(len(self.text)):
            text_char = self.text[i]
            password_char = self.extended_password[i]
            if text_char.isalpha():  
                shift = ord(password_char.lower()) - ord('а')
                if text_char.islower():
                    encrypted_char = chr((ord(text_char) - ord('а') + shift) % 32 + ord('а'))
                else:
                    encrypted_char = chr((ord(text_char) - ord('А') + shift) % 32 + ord('А'))
                encrypted_text.append(encrypted_char)
            else:
                encrypted_text.append(text_char)
        return ''.join(encrypted_text)


def read_file(file_path):
    with open(file_path, "rb") as file:
        return file.read()

def plot_histogram(text_bin):
    frequency = Counter(text_bin)
    labels, values = zip(*frequency.most_common())
    plt.bar(labels, values)
    plt.xlabel("ASCII value")
    plt.ylabel("Frequency")
    plt.title("Text Histogram")
    plt.show()

file_path = f"{script_dir}/input.txt" 

# first task
password = "Поле глазасто, а лес ушаст."
text_binary = read_file(file_path)
text_str = text_binary.decode("windows-1251")

cipher = VigenereCipher(text_str, password)
encrypted_text = cipher.encrypt()
text_back_to_str = encrypted_text.encode("windows-1251")
plot_histogram(text_back_to_str)


# second task
password = "10"

cipher = VigenereCipher(text_str, password)
encrypted_text = cipher.encrypt()
text_back_to_str = encrypted_text.encode("windows-1251")
plot_histogram(text_back_to_str)

# third task
password = "Поле глазасто, а лес ушаст."
text_str = text_binary.decode("windows-1251").upper()

cipher = VigenereCipher(text_str, password)
encrypted_text = cipher.encrypt()
text_back_to_str = encrypted_text.encode("windows-1251")
plot_histogram(text_back_to_str)


# fourth task
fpoly = [5,2]
L = LFSR(fpoly=fpoly, initstate='random')

k=1000*8
seq_k  = L.runKCycle(k)

password = L.arr2str(seq_k)
cipher = VigenereCipher(text_str, password)
encrypted_text = cipher.encrypt()
text_back_to_str = encrypted_text.encode("windows-1251")
plot_histogram(text_back_to_str)