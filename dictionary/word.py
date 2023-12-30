"""Module for Word class."""

from dataclasses import dataclass

from akshara import varnakaarya as vk

from dictionary.utils import WordType, Linga, Gana, Pada, Vibhakti, Vachana


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
    def replace_end(word: str, replacement: str) -> str:
        """Replace the end of a word with a given string."""

        vinyaasa = vk.get_vinyaasa(word)
        rep = vk.get_vinyaasa(replacement)

        return vk.get_shabda(vinyaasa[:-1] + rep)


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
