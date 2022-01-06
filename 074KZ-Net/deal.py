import csv


def deal():
    """

    :return:
    """
    file_in = "./rib.CSV"
    file_read = open(file_in, 'r', encoding='utf-8')
    prefix_19_list = []
    prefix_20_list = []
    for line in file_read.readlines():
        line = line.strip().split(",")
        print(line)
        if line[0] is not None:
            prefix_19_list.append(line[0])
        if line[1] is not None:
            prefix_20_list.append(line[1])

    diff_list = []
    for item in prefix_19_list:
        if item not in prefix_20_list:
            diff_list.append(item)
    print(len(set(diff_list)))
    print(set(diff_list))
    print("占比：", len(set(diff_list))/len(set(prefix_19_list)))


if __name__ == "__main__":
    deal()