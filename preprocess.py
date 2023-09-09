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
    with open(f"./data/{file}", "r", encoding="utf-8") as jp:
        content = jp.read().strip()
        obj = xtd.parse(content)["document"]

        if "#text" in obj.keys():
            obj.pop("#text")

    main = merge_dicts(main, obj)  # merge the dictionaries

# # final file with all the data
# with open(f"./json/main.json", "w", encoding="utf-8") as jp:
#     json.dump(
#         main,
#         jp,
#         indent=4,
#     )

json_files = os.listdir("./json")  # list of all the files in the json folder
main = []


def handle_data(data, k):
    if data == None:
        return
    if type(data) == str:
        main.append((data, k))
    elif type(data) == dict:
        if "#text" in data.keys():
            main.append((data["#text"], k))
    elif type(data) == list:
        for j in data:
            if type(j) == str:
                main.append((j, k))
            elif type(j) == dict:
                if "#text" in j.keys():
                    main.append((j["#text"], k))
            else:
                print("inlist", data, k)
                print("err")
    else:
        print("nontype", data, k)
        exit()


for file in json_files:
    if file == "main.json":
        continue
    with open(f"./json/{file}", encoding="utf-8") as jp:
        obj = json.load(jp)

    try:
        for k, v in obj.items():
            for i in v:
                handle_data(i, k)
    except:
        print(obj)

with open(f"./json/main.json", "w", encoding="utf-8") as jp:
    json.dump(
        main,
        jp,
        indent=4,
    )
