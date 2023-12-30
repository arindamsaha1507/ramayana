"""Module to extract data."""

import multiprocessing
import re
from dataclasses import dataclass, field

import requests
import html2text

from bs4 import BeautifulSoup


SARGA_COUNT = [77, 119, 75, 67, 68, 131]


@dataclass
class RawData:
    """Class to store raw data."""

    kanda: int
    sarga: int
    shlokas: list[str]
    translation: list[str]
    explanation: list[str]
    sans_list: list[list[str]] = field(default_factory=list, init=False)
    eng_list: list[list[str]] = field(default_factory=list, init=False)
    anvaya: list[str] = field(default_factory=list, init=False)

    def __post_init__(self):
        """Post init function."""

        size = len(self.shlokas)

        if len(self.translation) != size:
            raise ValueError("Translation and shlokas must be of same size.")

        if len(self.explanation) != size:
            raise ValueError("Explanation and shlokas must be of same size.")

        self.clean_shloka()

        self.translation = [
            trans.replace("\n", " ").replace("  ", " ").replace(":", "ः")
            for trans in self.translation
        ]

        self.explanation = [
            exp.replace("\n", " ").replace("  ", " ").replace(":", "ः")
            for exp in self.explanation
        ]

        self.set_word_meanings()
        self.set_anvaya()
        self.write_all_to_files()

    def __repr__(self) -> str:
        """Representation function."""

        return f"RawData(kanda={self.kanda}, sarga={self.sarga})"

    def print(self) -> None:
        """Print function."""

        print(f"Kanda: {self.kanda}")
        print(f"Sarga: {self.sarga}")
        print()
        print()
        for index, _ in enumerate(self.shlokas):
            print(self.shlokas[index])
            print()
            print(self.translation[index])
            print()
            print(self.explanation[index])
            print("=================================")
            print()

    def clean_shloka(self):
        """Clean shloka."""

        for index, shloka in enumerate(self.shlokas):
            while "।।" in shloka:
                shloka = shloka.replace("।।", "॥")

            while "\n  \n" in shloka:
                shloka = shloka.replace("\n  \n", "\n")

            while ":" in shloka:
                shloka = shloka.replace(":", "ः")

            lines = shloka.split("\n")
            lines = [line.strip() for line in lines if not re.search(r"[a-zA-Z]", line)]
            shloka = "\n".join(lines)

            self.shlokas[index] = shloka

    def get_shloka_section(self, number: int) -> int:
        """Get shloka section."""

        search_string = f"॥{self.kanda}.{self.sarga}.{number}॥"

        section = [
            (index, shloka)
            for index, shloka in enumerate(self.shlokas)
            if search_string in shloka
        ]

        if len(section) == 0:
            raise ValueError("Shloka not found.")

        if len(section) > 1:
            raise ValueError("Multiple shlokas found.")

        return section[0][0]

    def set_word_meanings(self):
        """Set word meanings."""

        devanagari_regex = r"[\u0900-\u097F]"
        non_devanagari_regex = r"[^\u0900-\u097F]"

        word_wise = [trans.split(", ") for trans in self.translation]

        pattern = f"(?<={devanagari_regex}) (?={non_devanagari_regex})|(?<={non_devanagari_regex}) (?={devanagari_regex})"

        for section in word_wise:
            sans_list = []
            eng_list = []
            for word in section:
                meaning = re.split(pattern, word)
                if len(meaning) != 2:
                    continue
                sans_list.append(meaning[0])
                eng_list.append(meaning[1])

            self.sans_list.append(sans_list)
            self.eng_list.append(eng_list)

    def set_anvaya(self):
        """Set anvaya."""

        for section in self.sans_list:
            sentence = ""
            for word in section:
                sentence += word + " "
            self.anvaya.append(sentence.strip())

    def print_anvaya(self):
        """Print anvaya."""

        print(" ।\n".join(self.anvaya), end=" ॥\n")

    def write_all_to_files(self):
        """Write all data to files."""

        with open(
            f"text/shloka/{self.kanda}_{self.sarga}_shloka.txt", "w", encoding="utf-8"
        ) as file:
            file.write("\n\n".join(self.shlokas))

        with open(
            f"text/translation/{self.kanda}_{self.sarga}_translation.txt",
            "w",
            encoding="utf-8",
        ) as file:
            file.write("\n\n".join(self.translation))

        with open(
            f"text/explanation/{self.kanda}_{self.sarga}_explanation.txt",
            "w",
            encoding="utf-8",
        ) as file:
            file.write("\n\n".join(self.explanation))

        with open(
            f"text/anvaya/{self.kanda}_{self.sarga}_anvaya.txt", "w", encoding="utf-8"
        ) as file:
            file.write("\n\n".join(self.anvaya))

        with open(
            f"text/padas/{self.kanda}_{self.sarga}_padas.yml", "w", encoding="utf-8"
        ) as file:
            for index, section in enumerate(self.sans_list):
                file.write(f"{index+1}:\n")
                for word in section:
                    if " " not in word:
                        if word != "":
                            file.write(f"    - '{word}'\n")
                    else:
                        parts = word.split(" ")
                        for part in parts:
                            if part != "":
                                file.write(f"    - '{part}'\n")


class DataExtractor:
    """Class to extract data from the web."""

    @staticmethod
    def extract_div_text(div: BeautifulSoup) -> str:
        """Extract text from a div tag."""

        div = div.find("div", class_="field-content")
        div = html2text.html2text(str(div))
        div = div.strip()
        return div

    @staticmethod
    def extract_info(kanda: int, sarga: int) -> RawData:
        """Extract information from the website."""

        prefix = "https://www.valmiki.iitk.ac.in/sloka"
        query = f"?field_kanda_tid={kanda}&language=dv&field_sarga_value={sarga}"
        url = prefix + query

        max_retries = 5
        retries = 0

        while retries < max_retries:
            try:
                response = requests.get(url, timeout=10)
                break
            except requests.exceptions.Timeout as error:
                retries += 1
                if retries == max_retries:
                    raise ValueError("Timeout error.") from error
                print(f"Retrying {retries} for kanda {kanda} and sarga {sarga}...")

        soup = BeautifulSoup(response.text, "html.parser")
        shlokas = soup.find_all("div", class_="views-field-body")
        translation = soup.find_all("div", class_="views-field-field-htetrans")
        explanation = soup.find_all("div", class_="views-field-field-explanation")

        shlokas = [DataExtractor.extract_div_text(shloka) for shloka in shlokas]
        translation = [
            DataExtractor.extract_div_text(translation) for translation in translation
        ]
        explanation = [
            DataExtractor.extract_div_text(explanation) for explanation in explanation
        ]

        return RawData(kanda, sarga, shlokas, translation, explanation)

    @staticmethod
    def get_sarga_index(kanda: int, sarga: int) -> int:
        """Get sarga index."""

        index = 0
        for i in range(kanda - 1):
            index += SARGA_COUNT[i]

        index += sarga - 1

        return index

    @staticmethod
    def get_section(
        data: list[RawData], kanda: int, sarga: int, shloka: int
    ) -> tuple[str, str, str]:
        """Get section."""

        data_index = DataExtractor.get_sarga_index(kanda, sarga)
        data_sarga = data[data_index]
        section = data_sarga.get_shloka_section(shloka)

        return (
            data_sarga.shlokas[section],
            data_sarga.translation[section],
            data_sarga.explanation[section],
        )

    @staticmethod
    def download_data() -> list[RawData]:
        """Download data."""

        sargas = [
            (index + 1, sarga)
            for index, count in enumerate(SARGA_COUNT)
            for sarga in range(1, count + 1)
        ]

        with multiprocessing.Pool() as pool:
            data = pool.starmap(DataExtractor.extract_info, sargas)

        return data
