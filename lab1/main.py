import matplotlib.pyplot as plt
from collections import Counter
from PIL import Image
from math import log2


def compute_entropy(frequency):
    total = sum(frequency.values())
    if total == 0:
        return 0
    entropy = -sum(
        (count / total) * log2(count / total) if count != 0 else 0
        for count in frequency.values()
    )
    return entropy


def analyze_file(file_path):
    if file_path.endswith(".bmp"):
        image = Image.open(file_path)
        r, g, b = image.split()
        r_freq = Counter(r.getdata())
        g_freq = Counter(g.getdata())
        b_freq = Counter(b.getdata())
        entropy = {
            "red": compute_entropy(r_freq),
            "green": compute_entropy(g_freq),
            "blue": compute_entropy(b_freq),
        }
        return {"red": r_freq, "green": g_freq, "blue": b_freq, "entropy": entropy}
    else:
        with open(file_path, "rb") as file:
            content = file.read()
            frequency = Counter(content)
        return {"text": frequency, "text_entropy": compute_entropy(frequency)}


def plot_histogram(frequency, title):
    if "red" in frequency:
        fig, (ax1, ax2, ax3) = plt.subplots(
            1, 3, figsize=(15, 5), sharex=True, sharey=True
        )
        ax1.bar(list(frequency["red"].keys()), list(frequency["red"].values()))
        ax1.set_title("Red Channel")
        ax1.set_yscale("log")

        ax2.bar(list(frequency["green"].keys()), list(frequency["green"].values()))
        ax2.set_title("Green Channel")
        ax2.set_yscale("log")

        ax3.bar(list(frequency["blue"].keys()), list(frequency["blue"].values()))
        ax3.set_title("Blue Channel")
        ax3.set_yscale("log")

        fig.suptitle(title)
        plt.show()
        # print(
        #     f"Entropy - Red: {frequency['entropy']['red']:.4f}, Green: {frequency['entropy']['green']:.4f}, Blue: {frequency['entropy']['blue']:.4f}"
        # )
    elif "text" in frequency:
        labels, values = zip(*frequency["text"].most_common())
        plt.bar(labels, values)
        plt.xlabel("ASCII value")
        plt.ylabel("Frequency")
        plt.title(title)
        print(f"Entropy - Text: {frequency['text_entropy']:.4f}")
        plt.show()
    else:
        raise ValueError("Unsupported frequency format")


frequency = analyze_file("./materials/bmp/rofl.bmp")
# plot_histogram(frequency, "Frequency Analysis of BMP Image")
# frequency = analyze_file("./materials/txt/4.txt")
plot_histogram(frequency, "Frequency Analysis of Text File")
