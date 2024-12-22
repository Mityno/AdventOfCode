import time


def concat_numbers(a, b):
    return int(str(a) + str(b))


def import_equations(filename):

    equations = []
    with open(filename, mode="r", encoding="utf8") as file:
        for line in file:
            split = line.split(":")
            total = int(split[0])
            numbers = tuple(map(int, split[1].strip().split()))
            equations.append((total, numbers))

    return equations


def solve_equation(total, numbers):
    if total < 0 or int(total) != total:
        return False

    if len(numbers) == 1:
        return total == numbers[0]

    last = numbers[-1]
    new_numbers = numbers[:-1]
    return solve_equation(total - last, new_numbers) or solve_equation(
        total / last, new_numbers
    )


def solve_equation_2(total, numbers):
    if total < 0 or int(total) != total:
        return False

    if len(numbers) == 1:
        return total == numbers[0]

    if 1 not in numbers and sum(numbers) > total:
        return False

    a, b = numbers[:2]
    tail_numbers = numbers[2:]
    return (
        solve_equation_2(total, (a + b,) + tail_numbers)
        or solve_equation_2(total, (a * b,) + tail_numbers)
        or solve_equation_2(total, (concat_numbers(a, b),) + tail_numbers)
    )


def main(filename):
    equations = import_equations(filename)

    acc = 0
    bef = time.perf_counter()
    for total, numbers in equations:
        if solve_equation_2(total, numbers):
            acc += total
    aft = time.perf_counter()
    print(acc)
    print(aft - bef)


if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    main(filename)
