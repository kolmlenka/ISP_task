def depth(node):
    if not node:
        return 0
    if not node.get("children"):
        return 1
    return max(depth(d) for d in node.get("children", [])) + 1


def clickable(node, flag=None):
    if not flag:
        flag = False
    for k in node.keys():
        if (k == "clickable") and (node[k] is True):
            return True
        elif type(node[k]) is dict:
            flag = clickable(node[k], flag)
        elif k == "children":
            for j in range(len(node[k])):
                flag = clickable(node[k][j], flag)
    return flag


def test(node):
    if not node or not node.get("clickable"):
        return False
    for c in node.get("children", []):
        return test(c)


def main():

    import json
    import imagesize
    import matplotlib.pyplot as plt
    import argparse
    from pathlib import Path

    aspect_ratios = set()
    count = 0
    interactive = 0
    list_of_depths = []

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "pathname",
        type=Path,
        help="Path to a Dataset",
    )
    parser.add_argument(
        "--limit",
        dest="n",
        type=int,
        help="number of screenshots to process",
    )
    args = parser.parse_args()

    list_of_jsons = list(args.pathname.glob("*.json"))
    if args.n is None:
        limit = len(list_of_jsons)
    else:
        limit = args.n
    for name_json in list_of_jsons:
        count += 1
        if count > limit:
            break
        with open(name_json, "r") as my_file:
            cur_json = my_file.read()
        current = json.loads(cur_json)

        list_of_depths += [depth(current["activity"]["root"])]

        if clickable(current) is True:
            interactive += 1

        name_jpg = name_json.with_suffix(".jpg")
        width, height = imagesize.get(name_jpg)
        res = width / height
        aspect_ratios.add(round(res, 4))

    print("aspect ratios: ", end="")
    print(aspect_ratios)

    print("interactive screenshots: " + str(interactive))

    fig = plt.figure(figsize=(6, 4))
    x = fig.add_subplot()
    x.hist(list_of_depths, 25)
    x.grid()
    plt.show()


if __name__ == "__main__":
    main()
