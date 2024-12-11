import functools


def import_line(filename: str):

    with open(filename, mode="r", encoding="utf8") as file:
        line = file.read()

    line = line.strip()
    line = map(int, line.split())
    return list(line)


def process_number(number: int) -> "int | tuple[int, int]":

    if number == 0:
        return 1

    if len(str(number)) % 2 == 0:
        half = len(str(number)) // 2
        return int(str(number)[:half]), int(str(number)[half:])

    return number * 2024


@functools.cache
def calculate_number_stones(number: int, depth: int) -> int:
    if depth == 0:
        return 1

    result = process_number(number)
    if isinstance(result, int):
        return calculate_number_stones(result, depth - 1)
    else:
        left, right = result
        return calculate_number_stones(left, depth - 1) + calculate_number_stones(
            right, depth - 1
        )


def main(filename: str):
    line = import_line(filename)

    # Part 1
    # for step in range(25):
    #     offset = 0
    #     for i in range(len(line)):
    #         j = i + offset  # current real index
    #         curr_num = line[j]
    #         result = process_number(curr_num)
    #         if isinstance(result, int):
    #             line[j] = result
    #         else:
    #             left, right = result
    #             line[j] = left
    #             line.insert(j + 1, right)
    #             offset += 1
    # print(len(line))

    counter = 0
    for num in line:
        counter += calculate_number_stones(num, 25)
    print(counter)

    # Part 2

    # line = import_line(filename)

    counter = 0
    for num in line:
        counter += calculate_number_stones(num, 75)
    print(counter)


if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    main(filename)
