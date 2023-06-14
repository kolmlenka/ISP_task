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


def file_processing(name_json):
    import json
    import imagesize

    with open(name_json, "r") as my_file:
        cur_json = my_file.read()
    current = json.loads(cur_json)

    d = depth(current["activity"]["root"])

    interactivity = clickable(current)

    name_jpg = name_json.with_suffix(".jpg")
    width, height = imagesize.get(name_jpg)
    res = width / height

    aspect_ratios = round(res, 4)

    return [d, interactivity, aspect_ratios]


def main():
    import matplotlib.pyplot as plt
    import argparse
    from pathlib import Path
    import multiprocessing

    aspect_ratios = set()
    non_interactive = 0
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

    with multiprocessing.Pool(multiprocessing.cpu_count()) as p:
        answers = p.map(file_processing, list_of_jsons[:limit])
        p.close()
        p.join()

    for i in range(limit):
        list_of_depths += [answers[i][0]]

        if answers[i][1] is False:
            non_interactive += 1

        aspect_ratios.add(answers[i][2])

    print("aspect ratios: ", aspect_ratios)

    print("non-interactive screenshots: " + str(non_interactive))

    print(list_of_depths)

    fig = plt.figure(figsize=(6, 4))
    x = fig.add_subplot()
    x.hist(list_of_depths, 25)
    x.grid()
    plt.show()


if __name__ == "__main__":
    main()
