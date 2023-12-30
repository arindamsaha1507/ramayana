"""Parser for the Monier-Williams Sanskrit-English Dictionary."""

from dataclasses import dataclass, field
import json
import os

import yaml

from dictionary.utils import Linga, UtilFuncs, WordType
from dictionary.word import SubantaMaker, Word


@dataclass
class MonierWilliamsParser:
    """Parser for the Monier-Williams Sanskrit-English Dictionary."""

    source: os.PathLike = field(default="dictionary/raw/monier_williams_sa_en.json")
    index: dict[str, str] = field(default_factory=dict, init=False)
    text: dict[str, str] = field(default_factory=dict, init=False)

    def __post_init__(self):
        if not os.path.isfile(self.source):
            raise FileNotFoundError(f"File {self.source} not found.")

        if not self.source.endswith(".json"):
            raise ValueError(f"File {self.source} is not a JSON file.")

        with open(self.source, "r", encoding="utf-8") as f:
            data = json.load(f)

        if "data" not in data:
            raise ValueError(f"File {self.source} is not a valid JSON file.")

        raw_data = data["data"]

        if "words" not in raw_data:
            raise ValueError(f"File {self.source} is not a valid JSON file.")

        self.index = raw_data["words"]

        if "text" not in raw_data:
            raise ValueError(f"File {self.source} is not a valid JSON file.")

        self.text = raw_data["text"]

    def word_exists(self, word: str) -> bool:
        """Check if the word exists in the dictionary."""

        return word in self.index

    def get_index(self, word: str) -> list[str]:
        """Get the index of the word in the dictionary."""

        if not self.word_exists(word):
            raise ValueError(f"Word {word} does not exist in the dictionary.")

        idx = self.index[word]

        if "," in idx:
            idx = idx.split(",")
        else:
            idx = [idx]

        return idx

    def get_meaning(self, word: str) -> list[str]:
        """Get the meaning of the word."""

        idx = self.get_index(word)

        meanings = []

        for i in idx:
            meanings.append(self.text[i][0])

        return meanings

    def get_category(self, word: str) -> set[Linga]:
        """Get the category of the word."""

        meanings = self.get_meaning(word)

        category = set()

        for meaning in meanings:
            words = meaning.split(" ")
            for word in words:
                word = UtilFuncs.remove_non_alphanumeric(word)
                if UtilFuncs.check_if_gender_word(word):
                    if "m" in word:
                        category.add(Linga.PULLINGA)
                    if "f" in word:
                        category.add(Linga.STRILINGA)
                    if "n" in word:
                        category.add(Linga.NAPUMSAKALINGA)
                if word == "ind":
                    category.add(Linga.AVAYAVA)
                if word == "cl":
                    category.add("v")

        return category


def create_primary_word_list(filename: str):
    """Create a primary word list."""

    if not filename.endswith(".csv"):
        raise ValueError(f"File {filename} is not a CSV file.")

    mwsa = MonierWilliamsParser()

    collection: list[Word] = []

    for entry in mwsa.index:
        typ = mwsa.get_category(entry)

        if "v" in typ:
            if typ == {"v"}:
                typ = WordType.DHATU
            else:
                typ = WordType.PRATIPADIKA
        else:
            typ = WordType.PRATIPADIKA

        for category in mwsa.get_category(entry):
            collection.append(
                Word(
                    entry,
                    typ,
                    category,
                    mwsa.get_meaning(entry),
                    entry,
                )
            )

    with open(filename, "w", encoding="utf-8") as file:
        for word in collection:
            if word.word_type == WordType.PRATIPADIKA:
                file.write(f"{word.word},{word.base},{word.category}\n")

    return collection


def create_secondary_word_list(filename: str):
    """Create a secondary word list."""

    if not filename.endswith(".csv"):
        raise ValueError(f"File {filename} is not a CSV file.")

    mwsa = MonierWilliamsParser()

    collection: list[Word] = []

    for entry in mwsa.index:
        typ = mwsa.get_category(entry)

        if "v" in typ:
            if typ == {"v"}:
                typ = WordType.DHATU
            else:
                typ = WordType.PRATIPADIKA
        else:
            typ = WordType.PRATIPADIKA

        for category in mwsa.get_category(entry):
            collection.append(
                Word(
                    entry,
                    typ,
                    category,
                    mwsa.get_meaning(entry),
                    entry,
                )
            )

    with open("subanta_rules.yml", "r", encoding="utf-8") as file:
        rules = yaml.safe_load(file)

    with open(filename, "w", encoding="utf-8") as file:
        for word in collection:
            if "ॐ" in word.word or "ॡ" in word.word:
                continue
            if word.word_type == WordType.PRATIPADIKA and word.category != "v":
                key = f"{UtilFuncs.find_last_letter(word.word)} {word.category.value}"
                if key in rules:
                    rule = rules[key]
                    for ii, rr in enumerate(rule):
                        subanta = SubantaMaker.replace_end(word.word, rr)
                        file.write(
                            f"{subanta},{word.word},{word.category},{(ii+1)//3}, {(ii+1)%3}\n"
                        )

    return collection


def main():
    """Main function."""

    create_primary_word_list("primary_word_list.csv")
    create_secondary_word_list("secondary_word_list.csv")

    # print(mwsa.get_meaning("राम"))
    # print(mwsa.get_meaning("पठ्"))

    # print(mwsa.get_category("राम"))
    # print(mwsa.get_category("पठ्"))
    # print(mwsa.get_category("लक्ष्मी"))
    # print(mwsa.get_category("श्यामा"))
    # print(mwsa.get_category("स्वामिन्"))
    # print(mwsa.get_category("स्वामि"))


# with open("raw/monier_williams_sa_en.json", "r") as f:
#     data = json.load(f)

if __name__ == "__main__":
    main()
