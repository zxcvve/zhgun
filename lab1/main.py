import matplotlib.pyplot as plt
from collections import Counter

def analyze_file(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
    frequency = Counter(content)
    return frequency

def plot_histogram(frequency):
    labels, values = zip(*frequency.items())
    plt.bar(labels, values)
    plt.xlim(0, 255)
    plt.ylim(0, max(values))
    plt.xlabel('ASCII value')
    plt.ylabel('Frequency')
    plt.title('Frequency Analysis')
    plt.show()

# Пример использования
frequency = analyze_file('a.txt')
plot_histogram(frequency)