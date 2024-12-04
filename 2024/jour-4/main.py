def import_grid(filename):
    with open(filename, mode="r", encoding="utf8") as file:
        data = file.readlines()

    data = list(map(str.strip, data))
    print(*data, sep="\n")
    return data


def count_xmas(string, word="XMAS"):

    n = len(word)
    # started = []
    counter = 0

    for i in range(len(string)):

        if string[i : i + n] == word:
            counter += 1

    return counter


def count_x_mas(box) -> int:
    n = len(box)
    diag_1 = [box[i][i] for i in range(len(box))]
    diag_2 = [box[n - 1 - i][i] for i in range(len(box))]
    diag_1 = "".join(diag_1)
    diag_2 = "".join(diag_2)

    count_diag_1 = count_xmas(diag_1, word="MAS") + count_xmas(diag_1[::-1], word="MAS")
    count_diag_2 = count_xmas(diag_2, word="MAS") + count_xmas(diag_2[::-1], word="MAS")
    return 1 == count_diag_1 == count_diag_2


def main(filename):

    grid = import_grid(filename)
    n = len(grid)

    # Part 1
    total = 0

    # count horizontal
    for i, line in enumerate(grid):
        total += count_xmas(line)
        total += count_xmas(line[::-1])  # backward

    # count vertical
    for i in range(len(grid)):
        column = [line[i] for line in grid]
        column = "".join(column)
        total += count_xmas(column)
        total += count_xmas(column[::-1])  # backward

    # count diagonal
    # from top left
    for i in range(len(grid)):
        # lower diagonals
        diag_1 = [grid[i + j][j] for j in range(len(grid) - i)]
        diag_1 = "".join(diag_1)
        total += count_xmas(diag_1)
        total += count_xmas(diag_1[::-1])

        # upper diagonals
        # the first time, both diagonals are the same
        if i == 0:
            continue
        diag_2 = [grid[j][i + j] for j in range(len(grid) - i)]
        diag_2 = "".join(diag_2)
        total += count_xmas(diag_2)
        total += count_xmas(diag_2[::-1])

    # from top right
    for i in range(len(grid)):
        # upper diagonals
        diag_1 = [grid[n - 1 - (i + j)][j] for j in range(len(grid) - i)]
        diag_1 = "".join(diag_1)
        total += count_xmas(diag_1)
        total += count_xmas(diag_1[::-1])

        # lower diagonals
        # the first time, both diagonals are the same
        if i == 0:
            continue
        diag_2 = [grid[n - 1 - j][i + j] for j in range(len(grid) - i)]
        diag_2 = "".join(diag_2)
        total += count_xmas(diag_2)
        total += count_xmas(diag_2[::-1])

    print("END")
    print(total)

    # Part 2
    print()

    word = "MAS"
    n_word = len(word)
    total = 0

    for i in range(n - n_word + 1):
        for j in range(n - n_word + 1):
            # print(i, j, i + n_word, j + n_word)
            box = [line[j : j + n_word] for line in grid[i : i + n_word]]
            total += count_x_mas(box)

    print(total)


if __name__ == "__main__":
    main("input2")  # < 20387
