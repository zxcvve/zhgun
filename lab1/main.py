import matplotlib.pyplot as plt
from collections import Counter


def analyze_file(file_path):
    with open(file_path, "rb") as file:
        content = file.read()
    frequency = Counter(content)
    return frequency


def plot_histogram(frequency):
    labels, values = zip(*frequency.items())
    plt.bar(labels, values)
    plt.xlim(0, 255)
    plt.ylim(0, max(values))
    plt.xlabel("ASCII value")
    plt.ylabel("Frequency")
    plt.title("Frequency Analysis")
    plt.show()


available_bmp = [
    "./materials/bmp/blackbuck.bmp",
    "./materials/bmp/bmp_08.bmp",
    "./materials/bmp/bmp_24.bmp",
    "./materials/bmp/snail.bmp",
]

# 2.txt - статья из СМИ
available_txt = [
    "./materials/txt/1.txt",
    "./materials/txt/2.txt",
    "./materials/txt/3.txt",
    "./materials/txt/4.txt",
]
frequency = analyze_file(available_txt[1])
plot_histogram(frequency)
