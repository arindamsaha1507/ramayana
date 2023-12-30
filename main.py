"""Main testing module."""

import pandas as pd
import yaml


def print_search_results(
    index, word, primary_word_set, secondary_word_set, primary=False
):
    """Print search results."""

    if primary:
        word_set = primary_word_set
    else:
        word_set = secondary_word_set

    if word in word_set:
        print(index, word, "True")
    elif "-" in word:
        components = word.split("-")
        for idd, component in enumerate(components):
            if idd < len(components) - 1:
                print_search_results(
                    index, component, primary_word_set, secondary_word_set, primary=True
                )
            else:
                print_search_results(
                    index, component, primary_word_set, secondary_word_set
                )
    else:
        print(index, word, "False")


def main():
    """Main function."""

    # data = DataExtractor.download_data()

    primary_word_list = pd.read_csv("primary_word_list.csv", header=None)[0].tolist()
    primary_word_set = set(primary_word_list)
    secondary_word_list = pd.read_csv("secondary_word_list.csv", header=None)[
        0
    ].tolist()
    secondary_word_set = set(secondary_word_list)

    kanda = 1
    sarga = 1
    section = 1

    with open(f"text/padas/{kanda}_{sarga}_padas.yml", "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)[section]

    # print(data[2])
    # print(word_set)

    for index, word in enumerate(data):
        print_search_results(index, word, primary_word_set, secondary_word_set)


if __name__ == "__main__":
    main()
