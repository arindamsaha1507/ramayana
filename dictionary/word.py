"""Module for Word class."""

from dataclasses import dataclass
import json

from akshara import varnakaarya as vk

from dictionary.utils import UtilFuncs, WordType, Linga, Gana, Pada, Vibhakti, Vachana

VIBHAKTI_MAP = {
    1: Vibhakti.PRATHAMA,
    2: Vibhakti.DWITIYA,
    3: Vibhakti.TRITIYA,
    4: Vibhakti.CHATURTHI,
    5: Vibhakti.PANCHAMI,
    6: Vibhakti.SHASTHI,
    7: Vibhakti.SAPTAMI,
    8: Vibhakti.SAMBODHANA,
}

VACHANA_MAP = {
    1: Vachana.EKAVACHANA,
    2: Vachana.DVIVACHANA,
    3: Vachana.BAHUVACHANA,
}


@dataclass
class Word:
    """Class for a word."""

    word: str
    word_type: WordType
    category: Linga | Gana | Pada

    meaning: list[str]
    base: str

    def __post_init__(self):
        """Post init method."""

        if self.word_type == WordType.PRATIPADIKA:
            self.base = self.word


@dataclass
class Subanta(Word):
    """Class for a subanta."""

    linga: Linga
    vibhakti: Vibhakti
    vachana: Vachana

    def __post_init__(self):
        """Post init method."""

        if self.word_type != WordType.SUBANTA:
            raise ValueError(f"Word {self.word} is not a subanta.")

        super().__post_init__()


class SubantaMaker:
    """Class for making subantas."""

    @staticmethod
    def replace_end(word: str, replacement: str, number: int = 1) -> str:
        """Replace the end of a word with a given string."""

        vinyaasa = vk.get_vinyaasa(word)
        rep = vk.get_vinyaasa(replacement)

        part_1 = vinyaasa[:-number]
        part_2 = rep

        if UtilFuncs.is_eligible_for_natva(part_1, part_2):
            idd = part_2.index("न्")
            part_2[idd] = "ण्"

        return vk.get_shabda(part_1 + part_2)

    @staticmethod
    def collect_from_json(filename: str) -> list[Subanta]:
        """Collect subantas from a JSON file."""

        if not filename.endswith(".json"):
            raise ValueError("Filename must end with .json")

        subantas = []

        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)["data"]

        for entry in data:
            base = entry["word"]
            meaning = entry["artha_eng"]

            if entry["linga"] == "N":
                linga = Linga.NAPUMSAKALINGA
            elif entry["linga"] == "P":
                linga = Linga.PULLINGA
            else:
                linga = Linga.STRILINGA

            forms = entry["forms"].split(";")

            for idd, form in enumerate(forms):
                vibhakti = VIBHAKTI_MAP[idd // 3 + 1]
                vachana = VACHANA_MAP[idd % 3 + 1]

                alt = form.split("-")
                for aa in alt:
                    if aa == "-":
                        continue
                    if " " in aa:
                        aa = aa.split(" ")[1]
                    subantas.append(
                        Subanta(
                            aa,
                            WordType.SUBANTA,
                            linga,
                            [meaning],
                            base,
                            linga,
                            vibhakti,
                            vachana,
                        )
                    )

        return subantas


if __name__ == "__main__":
    wor = Word(
        "देव", WordType.PRATIPADIKA, {Linga.PULLINGA}, ["अमुक", "अमुक", "अमुक"], "देव"
    )
    sub = Subanta(
        "देव",
        WordType.SUBANTA,
        {Linga.PULLINGA},
        ["अमुक", "अमुक", "अमुक"],
        "देव",
        Linga.PULLINGA,
        Vibhakti.PRATHAMA,
        Vachana.EKAVACHANA,
    )

    print(wor)
    print(sub)

    print(SubantaMaker.replace_end("देव", "एन"))
    print(SubantaMaker.replace_end("ऋषि", "ईनाम्"))

    ww = "चारित्र"
    ending = "एन"

    print(SubantaMaker.replace_end(ww, ending))
