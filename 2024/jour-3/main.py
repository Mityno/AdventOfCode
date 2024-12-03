import re


def import_sections(filename):

    with open(filename, mode="r", encoding="utf8") as file:
        sections = file.readlines()

    sections = list(map(str.strip, sections))
    return sections


def main(filename):

    sections = import_sections(filename)

    mul_regex = r"mul\((\d+),(\d+)\)"
    do_dont_regex = r"(?<=do\(\))(.*?)(?=don't\(\))"

    # Part 1
    res = 0
    for section in sections:
        finds = re.findall(mul_regex, section)
        nums = [int(a) * int(b) for a, b in finds]
        res += sum(nums)

    print(res)

    re.purge()

    # part 2
    res = 0
    for section in sections:
        section = "do()" + section + "don't()"
        matches = re.findall(do_dont_regex, string=section)
        print(len(matches))
        print(matches[0])

        finds = [re.findall(mul_regex, match) for match in matches]
        finds = [nums for line in finds for nums in line]
        print(len(finds))
        nums = [int(a) * int(b) for a, b in finds]
        res += sum(nums)

    print(res)


if __name__ == "__main__":
    main("input2")
