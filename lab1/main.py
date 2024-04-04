import matplotlib.pyplot as plt
from collections import Counter
from PIL import Image


def analyze_file(file_path):
    if file_path.endswith(".bmp"):
        # Analyze BMP image
        image = Image.open(file_path)
        r, g, b = image.split()
        r_freq = Counter(r.getdata())
        g_freq = Counter(g.getdata())
        b_freq = Counter(b.getdata())
        return {"red": r_freq, "green": g_freq, "blue": b_freq}
    else:
        # Analyze text file
        with open(file_path, "rb") as file:
            content = file.read()
        frequency = Counter(content)
        return {"text": frequency}


def plot_histogram(frequency, title):
    if "red" in frequency and "green" in frequency and "blue" in frequency:
        # Plot histograms for each RGB channel
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
        ax1.bar(list(frequency["red"].keys()), list(frequency["red"].values()))
        ax1.set_title("Red Channel")
        ax2.bar(list(frequency["green"].keys()), list(frequency["green"].values()))
        ax2.set_title("Green Channel")
        ax3.bar(list(frequency["blue"].keys()), list(frequency["blue"].values()))
        ax3.set_title("Blue Channel")
        fig.suptitle(title)
        plt.show()
    elif "text" in frequency:
        # Plot histogram for text file
        labels, values = zip(*frequency["text"].most_common())
        plt.bar(labels, values)
        plt.xlim(0, 255)
        plt.ylim(0, max(values))
        plt.xlabel("ASCII value")
        plt.ylabel("Frequency")
        plt.title(title)
        plt.show()
    else:
        raise ValueError("Unsupported frequency format")


available_bmp = [
    "./materials/bmp/blackbuck.bmp",
    "./materials/bmp/bmp_08.bmp",
    "./materials/bmp/bmp_24.bmp",
    "./materials/bmp/snail.bmp",
]

available_txt = [
    "./materials/txt/1.txt",
    "./materials/txt/2.txt",
    "./materials/txt/3.txt",
    "./materials/txt/4.txt",
]

# Analyze BMP image
frequency = analyze_file(available_bmp[0])
plot_histogram(frequency, "Frequency Analysis of BMP Image")

# Analyze text file
# frequency = analyze_file(available_txt[1])
# plot_histogram(frequency, "Frequency Analysis of Text File")
