import functools
import operator


def read_datas():
    n_lines = int(input())

    nums_lines = [list(map(int, input().split())) for _ in range(n_lines - 1)]
    operators = input().split()

    return nums_lines, operators


def read_datas_part_2() -> tuple[list[list[int]], list[str]]:
    n_lines = int(input()) - 1

    lines = [input() for _ in range(n_lines)]
    raw_operators = input()

    n = len(lines[0])
    nums_lines: list[list[int]] = [[] for _ in range(n_lines)]
    curr_line = 0
    for i in range(n - 1, -1, -1):

        curr_num = 0
        for j in range(n_lines):
            curr_char = lines[j][i]
            if curr_char != " ":
                curr_num = curr_num * 10 + int(curr_char)

        if curr_num == 0:
            if curr_line > 0:
                # we finished a block of numbers, we must fill remaining holes with placeholder values
                op = raw_operators[i + 1]
                placeholder = 0 if op == "+" else 1
                for line in range(curr_line, n_lines):
                    nums_lines[line].append(placeholder)
                curr_line = 0
            continue

        nums_lines[curr_line].append(curr_num)
        curr_line += 1
        curr_line %= n_lines

    operators = raw_operators.split()[::-1]
    return nums_lines, operators


def calculate_total(nums_lines: list[list[int]], operators: list[str]):

    n_nums = len(nums_lines[0])
    n_lines = len(nums_lines)
    results: list[int] = []

    for i in range(n_nums):
        op_func = operator.add if operators[i] == "+" else operator.mul
        curr_result: int = functools.reduce(
            op_func, (nums_lines[j][i] for j in range(n_lines))
        )
        results.append(curr_result)

    total = sum(results)
    return total


def main():

    # Part 1
    # nums_lines, operators = read_datas()
    #
    # total = calculate_total(nums_lines, operators)
    # print(total)

    # Part 2
    nums_lines, operators = read_datas_part_2()

    total = calculate_total(nums_lines, operators)
    print(total)


main()
