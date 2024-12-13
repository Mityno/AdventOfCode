import re
from fractions import Fraction


def import_machines(filename: str):

    machines: list[tuple[tuple[int, int], ...]] = []
    with open(filename, mode="r", encoding="utf8") as file:
        while True:
            a_button = file.readline()
            b_button = file.readline()
            prize = file.readline()

            x_a, y_a = map(int, re.findall(r"\+(\d+)", a_button))
            x_b, y_b = map(int, re.findall(r"\+(\d+)", b_button))
            x_prize, y_prize = map(int, re.findall(r"(\d+)", prize))

            # Part 2
            x_prize += 10000000000000
            y_prize += 10000000000000

            machines.append(((x_a, y_a), (x_b, y_b), (x_prize, y_prize)))

            if not file.readline():
                break

    return machines


def find_min_token(machine: tuple[tuple[int, int], ...]) -> int:
    (x_a, y_a), (x_b, y_b), (x_p, y_p) = machine

    # solve
    # x_p = k * x_a + i * x_b
    # y_p = k * y_x + i * y_b

    k = (x_p - y_p * Fraction(x_b, y_b)) / (x_a - y_a * Fraction(x_b, y_b))
    if not k.is_integer():
        return 0
    i = (y_p - k * y_a) / y_b
    if not k.is_integer():
        return 0
    return int(k * 3 + i)


def main(filename: str):
    machines = import_machines(filename)

    total_tokens = 0
    for machine in machines:
        tokens = find_min_token(machine)
        total_tokens += tokens
    print(total_tokens)


if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    main(filename)
