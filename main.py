"""Main testing module."""

import pandas as pd
import yaml


def search_results(index, word, word_sets, primary=False) -> list[tuple]:
    """Print search results."""

    results = []

    primary_word_set, secondary_word_set, verb_word_set = word_sets

    if primary:
        word_set = primary_word_set
    else:
        word_set = secondary_word_set

    if word in word_set:
        results.append((index, word, True))
    elif "-" in word:
        components = word.split("-")
        for idd, component in enumerate(components):
            if idd < len(components) - 1:
                rr = search_results(
                    index,
                    component,
                    word_sets,
                    primary=True,
                )
            else:
                rr = search_results(
                    index,
                    component,
                    word_sets,
                )
            results.extend(rr)
    elif word in verb_word_set:
        results.append((index, word, True))
    else:
        results.append((index, word, False))

    return results


def make_word_sets() -> tuple[set, set, set]:
    """Make word sets."""

    primary_word_df = pd.read_csv("primary_word_list.csv", header=None)
    primary_word_list = primary_word_df[0].tolist()
    avayava_list = primary_word_df[primary_word_df[2] == "Linga.AVAYAVA"][0].tolist()

    erratum_df = pd.read_csv("erratum.csv", header=None)
    erratum = erratum_df[0].tolist()

    avayava_list.extend(erratum_df[erratum_df[2] == "Linga.AVAYAVA"][0].tolist())
    primary_word_list.extend(erratum)

    primary_word_set = set(primary_word_list)

    secondary_word_list = pd.read_csv("secondary_word_list.csv", header=None)[
        0
    ].tolist()
    secondary_word_list.extend(avayava_list)

    special_word_list = pd.read_csv("special_word_list.csv", header=None)[0].tolist()
    secondary_word_list.extend(special_word_list)

    secondary_word_set = set(secondary_word_list)

    verb_word_list = pd.read_csv("verb_word_list.csv", header=None)[0].tolist()
    verb_word_set = set(verb_word_list)

    return primary_word_set, secondary_word_set, verb_word_set


def search_all_words(kanda, sarga, section, word_sets):
    """Search all words in a section."""

    with open(f"text/padas/{kanda}_{sarga}_padas.yml", "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)[section]

    results = []
    for index, word in enumerate(data):
        results.append(search_results(index, word, word_sets))

    sentence = []
    for result in results:
        for rr in result:
            if rr[2] is not True:
                raise ValueError(
                    f"Word {rr[1]} in {kanda}_{sarga}_{section} not found."
                )
        ww = "-".join([rr[1] for rr in result])
        sentence.append(ww)

    print(" ".join(sentence))


def main():
    """Main function."""

    word_sets = make_word_sets()

    kanda = 1
    sarga = 1

    for section in range(1, 4):
        search_all_words(kanda, sarga, section, word_sets)


if __name__ == "__main__":
    main()
