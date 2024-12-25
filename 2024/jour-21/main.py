from collections.abc import Sequence
import functools
import itertools


# NUMERIC_KEYPAD = list(map(list, ("798", "456", "123", " 0A")))
# DIRECTIONAL_KEYPAD = list(map(list, (" ^A", "<v>")))


def import_codes(filename: str):
    with open(filename, mode="r", encoding="utf8") as file:
        codes = file.read()
    codes = codes.strip().split()
    print(codes)
    return codes


def distance(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs(x1 - x2) + abs(y1 - y2)


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
def numeric_coord_to_char(x: int, y: int) -> str:
    match (x, y):
        case 0, 0:
            return "7"
        case 1, 0:
            return "8"
        case 2, 0:
            return "9"
        case 0, 1:
            return "4"
        case 1, 1:
            return "5"
        case 2, 1:
            return "6"
        case 0, 2:
            return "1"
        case 1, 2:
            return "2"
        case 2, 2:
            return "3"
        case 1, 3:
            return "0"
        case 2, 3:
            return "A"
        case _:
            raise ValueError(f"unexpected coord : {x = !r} {y = !r}")


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


def check_route_avoid_point(
    x: int, y: int, moves: Sequence[str], avoid_point: tuple[int, int]
) -> bool:

    for move in moves:
        match move:
            case "^":
                y -= 1
            case "v":
                y += 1
            case "<":
                x -= 1
            case ">":
                x += 1
            case _:
                raise ValueError(f"unexpected move : {move!r}")

        if (x, y) == avoid_point:
            return False
    return True


def solve_numeric_rec(code: str) -> list[str]:

    solutions: list[str] = []

    def inner(x: int, y: int, code: list[str], moves: list[str] | None = None):
        if moves is None:
            moves = []

        if not code:
            solutions.append("".join(moves))
            return

        next_char, *code = code
        next_x, next_y = numeric_char_pos(next_char)

        if next_x == x:
            # move along y
            dir_char = "^" if y > next_y else "v"
            moves.extend([dir_char] * abs(y - next_y))
            moves.append("A")
            inner(next_x, next_y, code, moves)
            return
        elif next_y == y:
            # move along x
            dir_char = "<" if x > next_x else ">"
            moves.extend([dir_char] * abs(x - next_x))
            moves.append("A")
            inner(next_x, next_y, code, moves)
            return

        # must move along both x and y
        all_next_moves: list[str] = []
        x_dir_char = "<" if x > next_x else ">"
        all_next_moves.extend([x_dir_char] * abs(x - next_x))
        y_dir_char = "^" if y > next_y else "v"
        all_next_moves.extend([y_dir_char] * abs(y - next_y))

        for dir_comb in set(itertools.permutations(all_next_moves)):
            if check_route_avoid_point(x, y, dir_comb, (0, 3)):
                new_moves = moves[:]
                new_moves.extend(dir_comb)
                new_moves.append("A")
                inner(next_x, next_y, code, new_moves)

    x, y = numeric_char_pos("A")
    inner(x, y, list(code))
    return solutions


def solve_directional_rec(code: str) -> frozenset[str]:
    x, y = directional_char_pos("A")
    return frozenset(_solve_directional_rec_inner(x, y, code))


@functools.cache
def add_to_next_moves(moves: str, all_next_moves: frozenset[str]) -> frozenset[str]:
    all_moves: set[str] = set()
    for next_moves in all_next_moves:
        all_moves.add(moves + next_moves)
    return frozenset(all_moves)


@functools.cache
def _solve_directional_rec_inner(
    x: int,
    y: int,
    code: str,
) -> frozenset[str]:

    if not code:
        return frozenset(("",))

    next_char, *code_chars = code
    code = "".join(code_chars)
    next_x, next_y = directional_char_pos(next_char)

    if next_x == x:
        # move along y
        dir_char = "^" if y > next_y else "v"
        next_moves = _solve_directional_rec_inner(
            next_x,
            next_y,
            code,
        )
        moves = dir_char * abs(y - next_y) + "A"
        return add_to_next_moves(moves, next_moves)
    elif next_y == y:
        # move along x
        dir_char = "<" if x > next_x else ">"
        next_moves = _solve_directional_rec_inner(
            next_x,
            next_y,
            code,
        )
        moves = dir_char * abs(x - next_x) + "A"
        return add_to_next_moves(moves, next_moves)

    # must move along both x and y
    all_next_moves: str = ""
    x_dir_char = "<" if x > next_x else ">"
    all_next_moves += x_dir_char * abs(x - next_x)
    y_dir_char = "^" if y > next_y else "v"
    all_next_moves += y_dir_char * abs(y - next_y)

    solutions: set[str] = set()
    for dir_comb in set(itertools.permutations(all_next_moves)):
        if check_route_avoid_point(x, y, dir_comb, (0, 0)):
            next_moves = _solve_directional_rec_inner(
                next_x,
                next_y,
                code,
            )
            moves = "".join(dir_comb) + "A"
            solutions.update(add_to_next_moves(moves, next_moves))
    return frozenset(solutions)


@functools.cache
def find_best_sol(code: str, depth: int) -> tuple[list[str], int]:
    if depth == 0:
        return [code], len(code)

    best_sol: list[str] = []
    best_len: int = float("inf")  # pyright: ignore[reportAssignmentType]

    for sol in solve_directional_rec(code):
        next_sol: list[list[str]] = []
        next_len: int = 0
        for part in split_in_part(sol):
            best_part_sol, part_len = find_best_sol(part, depth - 1)
            next_sol.append(best_part_sol)
            next_len += part_len

        if next_len < best_len:
            best_sol = next_sol
            best_len = next_len

    return best_sol, best_len


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


def compute_numeric_code(code: str) -> str:
    moves: list[str] = []
    x, y = 2, 3
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
                moves.append(numeric_coord_to_char(x, y))
            case _:
                raise ValueError(
                    f"unexpect char : {char!r}, moves so far : {''.join(moves)!r}"
                )

    return "".join(moves)


def split_in_part(sequence: str) -> list[str]:
    return [part + "A" for part in sequence.strip("A").split("A")]


def flatten(container: Sequence[str | Sequence[str]]):
    for i in container:
        if isinstance(i, (list, tuple)):
            yield from flatten(i)
        else:
            yield i


def main(filename: str):

    codes = import_codes(filename)

    complexity = 0
    for code in codes:
        sols1 = solve_numeric_rec(code)

        depth = int(sys.argv[2])
        best_sol_len: int | float = float("inf")

        for sol in sols1:
            curr_sol, curr_sol_len = find_best_sol(sol, depth)
            if curr_sol_len < best_sol_len:
                best_sol_len = curr_sol_len

        complexity += best_sol_len * int("".join(filter(str.isdigit, code)))

        print(best_sol_len)
        print(find_best_sol.cache_info())
        print(_solve_directional_rec_inner.cache_info())
        print()
    print(complexity)


if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    main(filename)
