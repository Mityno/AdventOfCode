def import_lists(filename):

    lst1, lst2 = [], []

    with open(filename, mode="r", encoding="utf8") as input_file:
        for line in input_file:
            elem1, elem2 = map(int, line.strip().split("   "))
            lst1.append(elem1)
            lst2.append(elem2)

    return lst1, lst2


def main():

    lst1, lst2 = import_lists('input.txt')
    print(len(lst1))
    print(lst1[:5], lst2[:5])
    lst1.sort()
    lst2.sort()
    print(sum(abs(a - b) for a, b in zip(lst1, lst2)))

    print(sum(a * lst2.count(a) for a in lst1))

if __name__ == "__main__":
    main()
