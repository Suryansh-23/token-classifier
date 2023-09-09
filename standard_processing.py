import re
from typing import Dict, List
import xmltodict as xtd, json, os

# files = [
#     "retailer system.xml"
#     # "2008 - keepass.xml"
# ]
# list of all the files in the data folder
files = os.listdir("./data")
main = []  # dictionary to store all the data
regex = r"</?[^>]+>"  # regex to remove the tags
sub = "|#|"  # separator
labels = [
    "no",
    "class",
    "method",
    "attribute",
    "association",
    "generalization",
]


def get_label(
    last_label: str,
    token: str,
    tokens: Dict[str, List[str]],
) -> str:
    """function to get the label of a token"""
    if last_label != "O":
        last_label = last_label.split("-")[1]
    for i in labels:
        if len(tokens.get(i, [])) == 0:
            continue
        if token == tokens[i][0]:
            tokens[i].pop(0)
            if last_label == i:
                return "I-" + i
            else:
                return "B-" + i
    else:
        return "O"


for file in files:
    file = os.path.splitext(file)[0]
    last_label = "O"  # default/last label
    per_file_main = []

    with open(f".\\json\\{file}.json", encoding="utf-8") as jp:
        tokens = json.load(jp)

    with open(f".\\data\\{file}.xml", encoding="utf-8") as fp:
        for i in fp.readlines():
            i = i.strip()
            if i == "":
                continue

            sentence = {"id": str(len(per_file_main)), "ner_tags": [], "tokens": []}
            subbed = re.sub(regex, sub, i, 0, re.MULTILINE)
            words = [i.strip() for i in subbed.split(sub) if i.strip() != ""]

            for word in words:
                label = get_label(last_label, word, tokens)
                last_label = label

                sentence["tokens"].append(word)
                sentence["ner_tags"].append(label)

            if len(sentence["tokens"]) == 0:
                continue

            per_file_main.append(sentence)

            sentence["id"] = str(len(main))
            main.append(sentence)

    with open(f".\\processed\\{file}.json", "w", encoding="utf-8") as jp:
        json.dump(
            per_file_main,
            jp,
            indent=4,
        )

with open(f".\\processed\\main.json", "w", encoding="utf-8") as jp:
    json.dump(
        main,
        jp,
        indent=4,
    )
