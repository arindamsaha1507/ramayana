"""Module to collect dhaaturoopas."""

import json

import os
from dataclasses import dataclass

from dictionary.utils import WordType, Gana, Pada, Vachana, Lakar, Purusha, Prayoga
from dictionary.word import Word


LAKAR_MAP = {
    "lat": Lakar.LAT,
    "lit": Lakar.LIT,
    "lut": Lakar.LUT,
    "lrut": Lakar.LRT,
    "lot": Lakar.LOT,
    "lang": Lakar.LAN,
    "vidhiling": Lakar.VIDHILIN,
    "ashirling": Lakar.ASHIRLIN,
    "lung": Lakar.LUN,
    "lrung": Lakar.LRN,
}

GANA_MAP = {
    "1": Gana.BHVADI,
    "2": Gana.ADADI,
    "3": Gana.JUHOTYADI,
    "4": Gana.DIVADI,
    "5": Gana.SVADI,
    "6": Gana.TUDADI,
    "7": Gana.RUDHAADI,
    "8": Gana.TANADI,
    "9": Gana.KRYADI,
    "10": Gana.CHURADI,
}

PURUSHA_MAP = {
    0: Purusha.PRATHAMA,
    1: Purusha.MADHYAMA,
    2: Purusha.UTTAMA,
}

VACHANA_MAP = {
    0: Vachana.EKAVACHANA,
    1: Vachana.DVIVACHANA,
    2: Vachana.BAHUVACHANA,
}


@dataclass
class Tinganta(Word):
    """Class for a tinganta pada."""

    prayoga: Prayoga
    pada: Pada
    lakar: Lakar
    purusha: Purusha
    vachana: Vachana

    def __post_init__(self):
        """Post init method."""

        if self.word_type != WordType.TINGANTA:
            raise ValueError(f"Word {self.word} is not a tinganta pada.")

        super().__post_init__()


class TingantaMaker:
    """Class for creating tingantas."""

    @staticmethod
    def collect_info_from_key(key: str) -> tuple[Pada, Lakar]:
        """Collect info from a key."""

        pada = key[0]
        if pada == "p":
            pada = Pada.PARASMAIPADA
        else:
            pada = Pada.ATMANEPADA

        lakar = key[1:]
        lakar = LAKAR_MAP[lakar]

        return pada, lakar

    @staticmethod
    def store_tinganta(tingantas: list[Tinganta], filename: str):
        """Store a tinganta."""

        if not filename.endswith(".csv"):
            raise ValueError("Filename must end with .csv")

        with open(filename, "w", encoding="utf-8") as f:
            for tinganta in tingantas:
                f.write(
                    f"{tinganta.word},{tinganta.base},{tinganta.category},{tinganta.prayoga},{tinganta.pada},{tinganta.lakar},{tinganta.purusha},{tinganta.vachana}\n"
                )

    @staticmethod
    def extract_tinganta_from_line(
        line: str, prayoga: Prayoga, pada: Pada, lakar: Lakar, info: dict[str, str]
    ) -> list[Tinganta]:
        """Extract a tinganta from a word."""

        tingantas = []

        words = line.split(";")

        for idd, word in enumerate(words):
            purusha = PURUSHA_MAP[idd // 3]
            vachana = VACHANA_MAP[idd % 3]
            alt = word.split(",")
            for aa in alt:
                tinganta = Tinganta(
                    word=aa,
                    word_type=WordType.TINGANTA,
                    category=GANA_MAP[info["gana"]],
                    meaning=info["artha_english"],
                    base=f"{info['dhatu']} ({info['aupadeshik']})",
                    prayoga=prayoga,
                    pada=pada,
                    lakar=lakar,
                    purusha=purusha,
                    vachana=vachana,
                )
                tingantas.append(tinganta)

        return tingantas

    @staticmethod
    def collect_dhaatus(filename: str, prayoga: Prayoga):
        """Collect dhaatus from the dhaatu list."""

        with open("dhatu.json", "r", encoding="utf-8") as f:
            data = json.load(f)["data"]

        with open(filename, "r", encoding="utf-8") as f:
            roopas = json.load(f)

        tingantas = []

        for info in data:
            index = info["baseindex"]

            if index not in roopas:
                continue
            forms = roopas[index]

            for key, value in forms.items():
                if value == "":
                    continue

                pada, lakar = TingantaMaker.collect_info_from_key(key)

                tingantas.extend(
                    TingantaMaker.extract_tinganta_from_line(
                        value, prayoga, pada, lakar, info
                    )
                )

        TingantaMaker.store_tinganta(tingantas, f"tinganta_{prayoga.name.lower()}.csv")

    @staticmethod
    def combine_csvs(files: list[str], output: str):
        """Combine the csvs."""

        cmd = "cat "
        for file in files:
            cmd += f"{file} "
        cmd += f"> {output}"

        os.system(cmd)

        cmd = "rm "
        for file in files:
            cmd += f"{file} "
        os.system(cmd)


def main():
    """Main function."""

    TingantaMaker.collect_dhaatus("dhatuforms.json", Prayoga.KARTARI)
    TingantaMaker.collect_dhaatus("dhatuforms_yak.json", Prayoga.BHAVAKARMANI)
    TingantaMaker.combine_csvs(
        ["tinganta_kartari.csv", "tinganta_bhavakarmani.csv"], "verb_word_list.csv"
    )

    # print(dhaatus)


if __name__ == "__main__":
    main()
