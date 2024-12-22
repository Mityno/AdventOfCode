import functools


# NUMERIC_KEYPAD = list(map(list, ("798", "456", "123", " 0A")))
# DIRECTIONAL_KEYPAD = list(map(list, (" ^A", "<v>")))


def import_codes(filename: str):
    with open(filename, mode="r", encoding="utf8") as file:
        codes = file.read()
    codes = codes.strip().split()
    print(codes)
    return codes


@functools.cache
def numeric_char_pos(char: str) -> tuple[int, int]:
    match char:
        case "A":
            return (2, 3)
        case "0":
            return (1, 3)
        case "1":
            return (0, 2)
        case "2":
            return (1, 2)
        case "3":
            return (2, 2)
        case "4":
            return (0, 1)
        case "5":
            return (1, 1)
        case "6":
            return (2, 1)
        case "7":
            return (0, 0)
        case "8":
            return (1, 0)
        case "9":
            return (2, 0)
        case _:
            raise ValueError(f"unexpect char : {char!r}")


@functools.cache
def directional_char_pos(char: str) -> tuple[int, int]:
    match char:
        case "^":
            return (1, 0)
        case "A":
            return (2, 0)
        case "<":
            return (0, 1)
        case "v":
            return (1, 1)
        case ">":
            return (2, 1)
        case _:
            raise ValueError(f"unexpect char : {char!r}")


@functools.cache
def directional_coord_to_char(x: int, y: int) -> str:
    match (x, y):
        case 1, 0:
            return "^"
        case 2, 0:
            return "A"
        case 0, 1:
            return "<"
        case 1, 1:
            return "v"
        case 2, 1:
            return ">"
        case _:
            raise ValueError(f"unexpected coord : {x = !r} {y = !r}")


def solve_numeric(code: str) -> str:

    curr_x, curr_y = (2, 3)

    moves: list[str] = []
    for char in code:
        char_x, char_y = numeric_char_pos(char)
        # print(char, char_x, char_y, curr_x, curr_y)
        assert (curr_x, curr_y) != (0, 3)

        if char_x >= curr_x:
            # move x first to avoid the "hole"
            moves.extend([">"] * (char_x - curr_x))
            curr_x = char_x

            y_dir = "^" if curr_y > char_y else "v"
            moves.extend([y_dir] * abs(curr_y - char_y))
            curr_y = char_y
        else:

            if curr_x == 2 and char_x == 0 and curr_y != 3:
                moves.extend(["<"] * 2)
                curr_x = char_x

            # move y first to avoid the "hole"
            y_dir = "^" if curr_y > char_y else "v"
            moves.extend([y_dir] * abs(curr_y - char_y))
            curr_y = char_y

            moves.extend(["<"] * (curr_x - char_x))
            curr_x = char_x

        moves.append("A")

    return "".join(moves)


def solve_directional(code: str, left_priority: bool = False) -> str:

    curr_x, curr_y = (2, 0)

    moves: list[str] = []
    for char in code:
        char_x, char_y = directional_char_pos(char)
        # print(char, char_x, char_y, curr_x, curr_y)
        assert (curr_x, curr_y) != (0, 0)

        if char_x >= curr_x:
            # move x first to avoid the "hole"
            moves.extend([">"] * (char_x - curr_x))
            curr_x = char_x

            y_dir = "^" if curr_y > char_y else "v"
            moves.extend([y_dir] * abs(curr_y - char_y))
            curr_y = char_y
        else:
            while left_priority and curr_x > 1 and curr_x > char_x:
                moves.append("<")
                curr_x -= 1

            # move y first to avoid the "hole"
            y_dir = "^" if curr_y > char_y else "v"
            moves.extend([y_dir] * abs(curr_y - char_y))
            curr_y = char_y

            moves.extend(["<"] * (curr_x - char_x))
            curr_x = char_x

        moves.append("A")

    return "".join(moves)


def compute_code(code: str) -> str:
    moves: list[str] = []
    x, y = 2, 0
    for char in code:
        match char:
            case "<":
                x -= 1
            case "v":
                y += 1
            case ">":
                x += 1
            case "^":
                y -= 1
            case "A":
                moves.append(directional_coord_to_char(x, y))
            case _:
                raise ValueError(
                    f"unexpect char : {char!r}, moves so far : {''.join(moves)!r}"
                )

    return "".join(moves)


def main(filename: str):

    codes = import_codes(filename)

    complexity = 0
    for code in codes:  # [4:]:
        sol1 = solve_numeric(code)
        sol2 = solve_directional(sol1)
        sol3 = solve_directional(sol2, left_priority=True)
        complexity += len(sol3) * int("".join(filter(str.isdigit, code)))
        print(sol1)
        print(sol2)
        print(sol3)
        print(len(sol3), int("".join(filter(str.isdigit, code))))
    print(complexity)


if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    main(filename)
