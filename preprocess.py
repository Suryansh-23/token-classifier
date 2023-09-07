import xmltodict as xtd, json, os

files = os.listdir("./data")  # list of all the files in the data folder
main = {}  # dictionary to store all the data


def merge_dicts(d1, d2):
    """function to merge two dictionaries"""
    for k, v in d2.items():
        if k in d1.keys():
            if type(d1[k]) == list:
                d1[k].append(v)
            else:
                d1[k] = [d1[k], v]
        else:
            d1[k] = v
    return d1


# loop across all the files and merge them into one
for file in files:
    with open(f"./data/{file}", "r", encoding="utf-8") as fp:
        content = fp.read().strip()
        obj = xtd.parse(content)["document"]

        if "#text" in obj.keys():
            obj.pop("#text")

    main = merge_dicts(main, obj)  # merge the dictionaries

# final file with all the data
with open(f"./json/main.json", "w", encoding="utf-8") as jp:
    json.dump(
        main,
        jp,
        indent=4,
    )
