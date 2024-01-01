"""Module for utility functions."""

import re
from enum import Enum

from akshara import varnakaarya as vk


class WordType(Enum):
    """Enum for WordType."""

    PRATIPADIKA = 1
    DHATU = 2
    SUBANTA = 3
    TINGANTA = 4


class Linga(Enum):
    """Enum for Gender."""

    PULLINGA = 1
    STRILINGA = 2
    NAPUMSAKALINGA = 3
    AVAYAVA = 4


class Vachana(Enum):
    """Enum for Number."""

    EKAVACHANA = 1
    DVIVACHANA = 2
    BAHUVACHANA = 3


class Vibhakti(Enum):
    """Enum for Case."""

    PRATHAMA = 1
    DWITIYA = 2
    TRITIYA = 3
    CHATURTHI = 4
    PANCHAMI = 5
    SHASTHI = 6
    SAPTAMI = 7
    SAMBODHANA = 8


class Purusha(Enum):
    """Enum for Person."""

    PRATHAMA = 1
    MADHYAMA = 2
    UTTAMA = 3


class Lakar(Enum):
    """Enum for Tense."""

    LAT = 1
    LIT = 2
    LUT = 3
    LRT = 4
    LOT = 5
    LAN = 6
    VIDHILIN = 7
    ASHIRLIN = 8
    LUN = 9
    LRN = 10
    NONE = 11


class Prayoga(Enum):
    """Enum for Voice."""

    KARTARI = 1
    BHAVAKARMANI = 2


class Pada(Enum):
    """Enum for Pada."""

    PARASMAIPADA = 1
    ATMANEPADA = 2
    UBHAYAPADA = 3


class Gana(Enum):
    """Enum for Gana."""

    BHVADI = 1
    ADADI = 2
    JUHOTYADI = 3
    DIVADI = 4
    SVADI = 5
    TUDADI = 6
    RUDHAADI = 7
    TANADI = 8
    KRYADI = 9
    CHURADI = 10


class UtilFuncs:
    """Class for utility functions."""

    @staticmethod
    def is_eligible_for_natva(vinyaasa_1: list[str], vinyaasa_2: list[str]) -> bool:
        """Check if the words are eligible for natva."""

        if (
            "र्" not in vinyaasa_1 and "ष्" not in vinyaasa_1
        ) or "न्" not in vinyaasa_2:
            return False

        end_index = vinyaasa_2.index("न्")

        if end_index == len(vinyaasa_2) - 1:
            return False

        permitted_letters = [
            "अ",
            "आ",
            "इ",
            "ई",
            "उ",
            "ऊ",
            "ऋ",
            "ॠ",
            "ऌ",
            "ॡ",
            "ए",
            "ऐ",
            "ओ",
            "औ",
            "ह्",
            "य्",
            "व्",
            "र्",
            "क्",
            "ख्",
            "ग्",
            "घ्",
            "ङ्",
            "प्",
            "फ्",
            "ब्",
            "भ्",
            "म्",
        ]

        for index in range(end_index):
            if vinyaasa_2[index] not in permitted_letters:
                return False

        for index in range(1, len(vinyaasa_1) + 1):
            if vinyaasa_1[-index] not in permitted_letters:
                return False
            if vinyaasa_1[-index] in ["र्", "ष्"]:
                return True

        return False

    @staticmethod
    def check_if_gender_word(string: str) -> bool:
        """Check if the word is gendered."""

        return re.fullmatch(r"[mfn]*[^a-zA-Z]*[mfn]*", string) is not None

    @staticmethod
    def remove_non_alphanumeric(string: str) -> str:
        """Remove non-alphanumeric characters from the string."""

        return re.sub(r"[^a-zA-Z0-9]", "", string)

    @staticmethod
    def find_last_letter(string: str, number: int = 1) -> str:
        """Find the last letter of the string."""

        if number == 1:
            return vk.get_vinyaasa(string)[-1]
        else:
            return vk.get_shabda(vk.get_vinyaasa(string)[-number:])

    @staticmethod
    def create_subanta_key(word: str, category: int) -> str:
        """Create a key for the subanta."""

        last_letter = UtilFuncs.find_last_letter(word)

        if last_letter == "न्":
            nn = 2
        elif last_letter == "त्":
            nn = 2
        elif last_letter == "स्":
            nn = 2
        else:
            nn = 1
        last_letter = UtilFuncs.find_last_letter(word, nn)

        return f"{last_letter} {category}", nn


if __name__ == "__main__":
    print(UtilFuncs.create_subanta_key("स्वामिन्", 1))
    print(UtilFuncs.create_subanta_key("राजन्", 1))
    print(UtilFuncs.create_subanta_key("देव", 1))

    print(
        UtilFuncs.is_eligible_for_natva(
            vk.get_vinyaasa("अग्निः"), vk.get_vinyaasa("अग्निन्")
        )
    )
    print(
        UtilFuncs.is_eligible_for_natva(vk.get_vinyaasa("राम"), vk.get_vinyaasa("नाम्"))
    )

    print(
        UtilFuncs.is_eligible_for_natva(vk.get_vinyaasa("राम"), vk.get_vinyaasa("आन्"))
    )

    print(
        UtilFuncs.is_eligible_for_natva(
            vk.get_vinyaasa("कृष्ण्"), vk.get_vinyaasa("एन")
        )
    )
