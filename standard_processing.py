import re
from typing import Dict, List
import json, os

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
count = 0
"""
stop_words = [
    "i",
    "me",
    "my",
    "myself",
    "we",
    "our",
    "ours",
    "ourselves",
    "you",
    "you're",
    "you've",
    "you'll",
    "you'd",
    "your",
    "yours",
    "yourself",
    "yourselves",
    "he",
    "him",
    "his",
    "himself",
    "she",
    "she's",
    "her",
    "hers",
    "herself",
    "it",
    "it's",
    "its",
    "itself",
    "they",
    "them",
    "their",
    "theirs",
    "themselves",
    "what",
    "which",
    "who",
    "whom",
    "this",
    "that",
    "that'll",
    "these",
    "those",
    "am",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "have",
    "has",
    "had",
    "having",
    "do",
    "does",
    "did",
    "doing",
    "a",
    "an",
    "the",
    "and",
    "but",
    "if",
    "or",
    "because",
    "as",
    "until",
    "while",
    "of",
    "at",
    "by",
    "for",
    "with",
    "about",
    "against",
    "between",
    "into",
    "through",
    "during",
    "before",
    "after",
    "above",
    "below",
    "to",
    "from",
    "up",
    "down",
    "in",
    "out",
    "on",
    "off",
    "over",
    "under",
    "again",
    "further",
    "then",
    "once",
    "here",
    "there",
    "when",
    "where",
    "why",
    "how",
    "all",
    "any",
    # "both",
    # "each",
    # "few",
    # "more",
    # "most",
    # "other",
    # "some",
    # "such",
    "no",
    "nor",
    "not",
    # "only",
    # "own",
    # "same",
    "so",
    "than",
    "too",
    "very",
    "s",
    "t",
    "can",
    "will",
    "just",
    "don",
    "don't",
    "should",
    "should've",
    "now",
    "d",
    "ll",
    "m",
    "o",
    "re",
    "ve",
    "y",
    "ain",
    "aren",
    "aren't",
    "couldn",
    "couldn't",
    "didn",
    "didn't",
    "doesn",
    "doesn't",
    "hadn",
    "hadn't",
    "hasn",
    "hasn't",
    "haven",
    "haven't",
    "isn",
    "isn't",
    "ma",
    # "mightn",
    # "mightn't",
    # "mustn",
    # "mustn't",
    # "needn",
    # "needn't",
    # "shan",
    # "shan't",
    # "shouldn",
    # "shouldn't",
    # "wasn",
    # "wasn't",
    # "weren",
    # "weren't",
    # "won",
    # "won't",
    # "wouldn",
    # "wouldn't",
]
"""
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
    if is_stop_word(token):
        return "O"
    if last_label != "O":
        last_label = last_label.split("-")[1]

    for i in labels:
        if len(tokens.get(i, [])) == 0:
            # if i in tokens and all([len(tokens.get(k, [])) == 0 for k in labels]):
            #     global count
            #     print("empty", count)
            #     count += 1

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
    per_file_main = []

    with open(f".\\json\\{file}.json", encoding="utf-8") as jp:
        tokens = json.load(jp)

    with open(f".\\data\\{file}.xml", encoding="utf-8") as fp:
        for i in fp.readlines():
            last_label = "O"  # default/previous label
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
