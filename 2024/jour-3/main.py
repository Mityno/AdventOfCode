import re
import collections


def import_section(filename):
    with open(filename, mode="r", encoding="utf8") as file:
        section = file.read().strip().replace('\n', '')

    return section


def parse_mul(string, index) -> tuple[int, int] | None:
    mul_regex = r"mul\((\d{1,3}),(\d{1,3})\)"
    numbers = re.findall(mul_regex, string[index : index + len("mul(XXX,XXX)")])
    if not numbers:
        return
    ab = numbers[0]
    return tuple(map(int, ab))


def main(filename):
    section = import_section(filename)

    mul_regex = r"mul\((\d{1,3}),(\d{1,3})\)"

    # Part 1
    finds = re.findall(mul_regex, section)
    nums = [int(a) * int(b) for a, b in finds]
    res = sum(nums)

    print(res)

    # Part 2

    do_dont_regex = r"(?<=do\(\))(.*?)(?=don't\(\))"

    section = "do()" + section + "don't()"
    matches = re.findall(do_dont_regex, string=section)
    # print(any("don't" in match for match in matches))
    # print(len(matches))
    # print(matches[0])

    finds = [re.findall(mul_regex, match) for match in matches]
    finds = [nums for line in finds for nums in line]
    # print(len(finds))
    nums = [int(a) * int(b) for a, b in finds]
    res = sum(nums)

    print(res)

    dont_do_regex = r"don't\(\).*?(?>do\(\)|$)"
    file = open("result2", mode="w", encoding="utf8")

    do_section = re.sub(dont_do_regex, "", section)
    file.write(do_section)
    file.write("\n")
    # print(do_section)
    finds = re.findall(mul_regex, do_section)
    nums = [int(a) * int(b) for a, b in finds]
    res = sum(nums)

    file.close()
    print(res)

    total = 0
    enable = True
    for i in range(len(section)):
        if section[i : i + len("do()")] == "do()":
            enable = True
        elif section[i : i + len("don't()")] == "don't()":
            enable = False
        elif enable and section[i : i + len("mul")] == "mul":
            numbers = parse_mul(section, i)
            if numbers is not None:
                a, b = numbers
                total += a * b

    print(total)


if __name__ == "__main__":
    main("input2")
