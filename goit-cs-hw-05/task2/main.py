import matplotlib.pyplot as plt
import numpy as np
import string
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

import requests


def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return None


def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))


def map_func(word):
    return word, 1


def shuffle_func(map_val):
    shuffled = defaultdict(list)
    for key, value in map_val:
        shuffled[key].append(value)
    return shuffled.items()


def reduce_func(key_val):
    key, values = key_val
    return key, sum(values)


def map_reduce(text, srch_words=None):
    txt = remove_punctuation(text)
    words = txt.split()

    if srch_words:
        srch_words = remove_punctuation(srch_words).split()
        words = [word for word in words if word in srch_words]

    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_func, words))

    shuffled_values = shuffle_func(mapped_values)

    with ThreadPoolExecutor() as executor:
        reduc_val = list(executor.map(reduce_func, shuffled_values))

    return reduc_val


def visualize_top_words(data):
    data = data[::-1]
    words, frequencies = zip(*data)

    plt.barh(words, frequencies, color="lightblue", edgecolor="black")

    plt.title("Top 10 Most Frequent Words")
    plt.xlabel("Frequency")
    plt.ylabel("Words")

    plt.show()


if __name__ == "__main__":
    url = input("Enter url: ")
    txt = get_text(url.strip())
    search_words = input(
        "Find specific word to search, if none just press enter (e.g: and me I we fairy ship): "
    )

    if txt:
        result = map_reduce(txt, search_words)
        sorted = sorted(result, key=lambda x: x[1], reverse=True)
        visualize_top_words(sorted[:10])
    else:
        print("Text not found")
