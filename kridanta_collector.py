"""Module to collect kridantas."""

import pandas as pd

import akshara.varnakaarya as vk

from dictionary.utils import Linga


class KridantaCollector:
    """Class to collect kridantas."""

    @staticmethod
    def create_gendered_line(words: list[str], replacement: str = "", suffix="") -> str:
        """Create gendered line."""

        words = [str(word).split(",") for word in words if str(word) != "nan"]
        temp = []
        for word in words:
            if len(word) == 4:
                temp.append(word[0])
                temp.append(word[2])
                temp.append(word[1])
                temp.append(word[3])
            elif len(word) == 2:
                temp.append(word[0])
                temp.append(word[1])
            elif len(word) == 6:
                temp.append(word[0])
                temp.append(word[3])
                temp.append(word[1])
                temp.append(word[4])
                temp.append(word[2])
                temp.append(word[5])
            elif len(word) == 8:
                temp.append(word[0])
                temp.append(word[4])
                temp.append(word[1])
                temp.append(word[5])
                temp.append(word[2])
                temp.append(word[6])
                temp.append(word[3])
                temp.append(word[7])
            elif len(word) == 3:
                temp.append(word[0])
                temp.append(word[1])
            else:
                print("Invalid word" + str(word))
        words = temp

        if replacement == "":
            words = [
                vk.get_shabda(vk.get_vinyaasa(word)[:-1]) if idd % 2 == 0 else word
                for idd, word in enumerate(words)
            ]
        else:
            vv = vk.get_vinyaasa(replacement)
            ll = len(vv)
            words = [
                vk.get_shabda(vk.get_vinyaasa(word)[:-ll] + vv + [suffix])
                if idd % 2 == 0
                else word
                for idd, word in enumerate(words)
            ]

        lines = [
            f"{ll},{ll},{Linga.PULLINGA}"
            if idd % 2 == 0
            else f"{ll},{ll},{Linga.STRILINGA}"
            for idd, ll in enumerate(words)
        ]

        return "\n".join(lines) + "\n"

    @staticmethod
    def collect_kridantas(source_filename: str, filename: str):
        """Collect kridantas from the kridanta list."""

        data = pd.read_csv(source_filename)
        data = data[
            [
                "ल्युट्",
                "अनीयर्",
                "ण्वुल्",
                "तुमुन्",
                "तव्य",
                "तृच्",
                "क्त्वा",
                "ल्यप्",
                "क्तवतुँ",
                "क्त",
                "शतृँ",
                "शानच्",
            ]
        ]

        lyut = data["ल्युट्"].tolist()
        aniiyar = data["अनीयर्"].tolist()
        nvl = data["ण्वुल्"].tolist()
        tumun = data["तुमुन्"].tolist()
        tavya = data["तव्य"].tolist()
        trc = data["तृच्"].tolist()
        ktva = data["क्त्वा"].tolist()
        lyap = data["ल्यप्"].tolist()
        ktvtn = data["क्तवतुँ"].tolist()
        kt = data["क्त"].tolist()
        satr = data["शतृँ"].tolist()
        shaanac = data["शानच्"].tolist()

        with open(filename, "w", encoding="utf-8") as f:
            lyut = [str(word).split(",") for word in lyut if str(word) != "nan"]
            lyut = [word for sublist in lyut for word in sublist]
            lyut = [vk.get_shabda(vk.get_vinyaasa(word)[:-1]) for word in lyut]
            lines = [f"{ll},{ll},{Linga.NAPUMSAKALINGA}" for ll in lyut]
            f.write("\n".join(lines) + "\n")

            f.write(KridantaCollector.create_gendered_line(aniiyar))
            f.write(KridantaCollector.create_gendered_line(nvl))

            tumun = [str(word).split(",") for word in tumun if str(word) != "nan"]
            tumun = [word for sublist in tumun for word in sublist]
            tumun = [f"{ll},{ll},{Linga.AVAYAVA}" for ll in tumun]
            f.write("\n".join(tumun) + "\n")

            f.write(KridantaCollector.create_gendered_line(tavya))
            f.write(KridantaCollector.create_gendered_line(trc, "ऋ"))

            ktva = [str(word).split(",") for word in ktva if str(word) != "nan"]
            ktva = [word for sublist in ktva for word in sublist]
            ktva = [f"{ll},{ll},{Linga.AVAYAVA}" for ll in ktva]
            f.write("\n".join(ktva) + "\n")

            lyap = [str(word).split(",") for word in lyap if str(word) != "nan"]
            lyap = [word for sublist in lyap for word in sublist]
            lyap = [vk.get_shabda(vk.get_vinyaasa(word)[3:]).strip() for word in lyap]
            lines = [f"{ll},{ll},{Linga.AVAYAVA}" for ll in lyap]
            f.write("\n".join(lines) + "\n")

            f.write(KridantaCollector.create_gendered_line(ktvtn, "अत्"))
            f.write(KridantaCollector.create_gendered_line(kt))
            f.write(KridantaCollector.create_gendered_line(satr, "त्", "छ्"))
            f.write(KridantaCollector.create_gendered_line(shaanac))


if __name__ == "__main__":
    KridantaCollector.collect_kridantas("dhatuforms_krut.csv", "kridanta_word_list.csv")
