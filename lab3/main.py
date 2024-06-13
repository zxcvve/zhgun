import matplotlib.pyplot as plt
from pylfsr import LFSR
from collections import Counter
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
        return extended_password[: len(self.text)]

    def encrypt(self):
        encrypted_text = []
        for i in range(len(self.text)):
            text_char = self.text[i]
            password_char = self.extended_password[i]
            if text_char.isalpha():
                shift = ord(password_char.lower()) - ord("а")
                if text_char.islower():
                    encrypted_char = chr(
                        (ord(text_char) - ord("а") + shift) % 32 + ord("а")
                    )
                else:
                    encrypted_char = chr(
                        (ord(text_char) - ord("А") + shift) % 32 + ord("А")
                    )
                encrypted_text.append(encrypted_char)
            else:
                encrypted_text.append(text_char)
        return "".join(encrypted_text)


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


def plot_multiple_histograms(text_bin1, text_bin2, title="Text Histogram"):
    frequency1 = Counter(text_bin1)
    frequency2 = Counter(text_bin2)
    labels, values = zip(*frequency1.most_common())
    plt.bar(labels, values)
    labels, values = zip(*frequency2.most_common())
    plt.bar(labels, values)
    plt.xlabel("ASCII value")
    plt.ylabel("Frequency")
    plt.title(title)
    plt.show()


class CaesarCipher:
    def __init__(self, text, shift):
        self.text = text
        self.shift = shift

    def encrypt(self):
        encrypted_text = []
        for char in self.text:
            if char.isalpha():
                shift = self.shift % 32
                if char.islower():
                    encrypted_char = chr((ord(char) - ord("а") + shift) % 32 + ord("а"))
                else:
                    encrypted_char = chr((ord(char) - ord("А") + shift) % 32 + ord("А"))
                encrypted_text.append(encrypted_char)
            else:
                encrypted_text.append(char)
        return "".join(encrypted_text)


file_path = f"{script_dir}/input.txt"

# вывод гистограммы для текста до шифрования
init_file = read_file(file_path)
plot_histogram(init_file, "Текст до шифрования")


# first task
password = "Поле глазасто, а лес ушаст."
init_file = read_file(file_path)
text_str = init_file.decode("windows-1251")

cipher = VigenereCipher(text_str, password)
encrypted_text = cipher.encrypt()
caesar_encrypted = encrypted_text.encode("windows-1251")
plot_histogram(
    caesar_encrypted,
    "Текст после шифрования (шифр Виженера)",
)


# second task
shift = 10

cipher = CaesarCipher(text_str, shift)
encrypted_text = cipher.encrypt()
caesar_encrypted = encrypted_text.encode("windows-1251")
plot_histogram(caesar_encrypted, "Текст после шифрования (шифр Цезаря)")

# third task
password = "Поле глазасто, а лес ушаст."
text_str = init_file.decode("windows-1251").upper()

cipher = VigenereCipher(text_str, password)
encrypted_text = cipher.encrypt()
z32 = encrypted_text.encode("windows-1251")
plot_histogram(z32, "Текст после шифрования (Z32)")


# fourth task
fpoly = [5, 2]
L = LFSR(fpoly=fpoly, initstate="random")

k = 1000 * 8
seq_k = L.runKCycle(k)

text_str = init_file.decode("windows-1251")
password = L.arr2str(seq_k)
cipher = VigenereCipher(text_str, password)
encrypted_text = cipher.encrypt()
lfsr_encrypted = encrypted_text.encode("windows-1251")
plot_histogram(lfsr_encrypted, "Текст после шифрования (LFSR)")
