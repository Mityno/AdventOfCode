def import_data(filename: str):

    with open(filename, mode="r", encoding="utf8") as file:
        data = file.read()

    data = data.strip()
    return data


def main(filename: str):
    data = import_data(filename)

    # Part 1
    string: list[str | int] = []
    index = 0
    blank = False
    for count in data:
        if blank:
            string.extend(["."] * int(count))
        else:
            string.extend([index] * int(count))
            index += 1
        blank = not blank
    # print(string)

    left_index = 0
    right_index = len(string) - 1
    while left_index < right_index:

        while left_index < right_index and string[left_index] != ".":
            left_index += 1

        while left_index < right_index and string[right_index] == ".":
            right_index -= 1

        if left_index >= right_index:
            break

        string[left_index], string[right_index] = (
            string[right_index],
            string[left_index],
        )
        left_index += 1
        right_index -= 1

    checksum = 0
    last_index = string.index(".")
    numbers = string[:last_index]
    for index, num in enumerate(map(int, numbers)):
        checksum += index * num
    print(checksum)

    # Part 2
    string = []
    index = 0
    blank = False
    for count in data:
        if blank:
            string.extend(["."] * int(count))
        else:
            string.extend([index] * int(count))
            index += 1
        blank = not blank
    # print(string)

    right_index = len(string) - 1
    while (first_free_space_index := string.index(".")) < right_index:

        while first_free_space_index < right_index and string[right_index] == ".":
            right_index -= 1

        if string[right_index] == ".":
            break

        right_size = 1
        while (
            first_free_space_index <= right_index - right_size
            and string[right_index - right_size] == string[right_index]
        ):
            right_size += 1

        left_index = first_free_space_index
        left_size = 0
        while left_index <= right_index - right_size and right_size > left_size:

            while left_index <= right_index - right_size and string[left_index] != ".":
                left_index += 1

            if left_index > right_index - right_size:
                break

            left_size = 1
            while (
                left_index + left_size <= right_index - right_size
                and string[left_index + left_size] == "."
            ):
                left_size += 1

            if right_size > left_size:
                left_index += left_size

        if left_index + left_size - 1 >= right_index - right_size + 1:
            right_index -= right_size
            continue

        assert left_size >= right_size, f"Size issue : {left_size = } | {right_size = }"

        (
            string[left_index : left_index + right_size],
            string[right_index - right_size + 1 : right_index + 1],
        ) = (
            string[right_index - right_size + 1 : right_index + 1],
            string[left_index : left_index + right_size],
        )
        right_index -= right_size

    checksum = 0
    for index, num in enumerate(string):
        if num == ".":
            continue
        assert isinstance(num, int)
        checksum += index * num
    print(checksum)


if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    main(filename)
