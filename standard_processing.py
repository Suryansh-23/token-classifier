import json  # to load the json files
import os  # to get the list of files in a folder
import re  # to remove the tags from the xml files
from typing import Dict, List  # for type hinting

# files = [
#     "retailer system.xml"
#     # "2008 - keepass.xml"
# ] # Test files

files = os.listdir("./data")  # list of all the files in the data folder
main = []  # dictionary to store all the data
regex = r"</?[^>]+>"  # regex to remove the tags
sub = "|#|"  # separator to be substituted in the regex
labels = [
    "no",
    "class",
    "method",
    "attribute",
    "association",
    "generalization",
]  # labels to be used

# short list of stop words to be removed
stop_words = [
    "i",
    "is",
    "a",
    "an",
    "the",
    "and",
    "them",
    "they",
    "their",
    "these",
    "that",
    "this",
    "those",
    "isn't",
    "it",
]


def is_stop_word(word: str) -> bool:
    """function to check if a word is a stop word"""
    return word in stop_words


def get_label(
    last_label: str,
    token: str,
    tokens: Dict[str, List[str]],
) -> str:
    """function to get the label of a token"""
    if is_stop_word(token):  # if the token is a stop word, return "O"
        return "O"
    if last_label != "O":  # if the last label is not "O", return the raw last label
        last_label = last_label.split("-")[1]

    for i in labels:
        if len(tokens.get(i, [])) == 0:  # if there are no tokens for the label,
            continue

        if token == tokens[i][0]:  # if the token is the first token for the label,
            tokens[i].pop(0)
            if last_label == i:  # if the last label is the same as the current label,
                return "I-" + i
            else:
                return "B-" + i
    else:  # if the token is not the first token for any label,
        return "O"


for file in files:
    file = os.path.splitext(file)[0]
    per_file_main = []

    with open(f".\\json\\{file}.json", encoding="utf-8") as jp:
        tokens = json.load(jp)

    with open(f".\\data\\{file}.xml", encoding="utf-8") as fp:
        for i in fp.readlines():
            last_label = "O"  # default/previous label
            i = i.strip()

            if i == "":
                continue

            sentence = {
                "id": str(len(per_file_main)),
                "ner_tags": [],
                "tokens": [],
            }  # sentence dictionary
            subbed = re.sub(regex, sub, i, 0, re.MULTILINE)  # removing the tags
            words = [
                i.strip() for i in subbed.split(sub) if i.strip() != ""
            ]  # getting the words

            # getting the label for each word
            for word in words:
                label = get_label(last_label, word, tokens)
                last_label = label

                sentence["tokens"].append(word)
                sentence["ner_tags"].append(label)

            # if there are no words in the sentence, skip it
            if len(sentence["tokens"]) == 0:
                continue

            per_file_main.append(sentence)

            sentence["id"] = str(len(main))
            main.append(sentence)

    # writing to the corresponding file with the data for each file
    with open(f".\\processed\\{file}.json", "w", encoding="utf-8") as jp:
        json.dump(
            per_file_main,
            jp,
            indent=4,
        )

# writing to the final file with all the data
with open(f".\\processed\\main.json", "w", encoding="utf-8") as jp:
    json.dump(
        main,
        jp,
        indent=4,
    )
