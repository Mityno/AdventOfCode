import functools
import numpy
from numpy._typing import NDArray


@functools.cache
def get_direction(move: str) -> tuple[int, int]:
    possible_moves = "^<>v"
    directions = ((0, -1), (-1, 0), (1, 0), (0, 1))
    return directions[possible_moves.find(move)]


def double_map(robot_map: list[list[str]]) -> list[list[str]]:
    return [
        list(
            "".join(
                [
                    "[]" if loc == "O" else "@." if loc == "@" else loc * 2
                    for loc in line
                ]
            )
        )
        for line in robot_map
    ]


def move_up_down(x: int, y: int, dy: int, robot_map: NDArray):
    if robot_map[y, x] == "[":
        if move_up_down(x, y + dy, dy, robot_map) and move_up_down(
            x + 1, y + dy, dy, robot_map
        ):
            robot_map[y + dy, x : x + 2] = list("[]")
            robot_map[y, x : x + 2] = ".."
            return True
    elif robot_map[y, x] == "]":
        if move_up_down(x - 1, y + dy, dy, robot_map) and move_up_down(
            x, y + dy, dy, robot_map
        ):
            robot_map[y + dy, x - 1 : x + 1] = list("[]")
            robot_map[y, x - 1 : x + 1] = ".."
            return True
    elif robot_map[y, x] == "#":
        return False
    else:  # robot_map[y, x] == "."
        return True


def import_robot_map(filename: str):

    robot_map: list[list[str]] = []
    with open(filename, mode="r", encoding="utf8") as file:
        for line in file:
            line = line.strip()
            if line:
                robot_map.append(list(line))
            else:
                break

        moves = file.read().replace("\n", "")
    return robot_map, moves


def main(filename: str):

    # Part 1
    robot_map, moves = import_robot_map(filename)
    robot_map = numpy.array(robot_map)
    robot_x: int
    robot_y: int
    (robot_y,), (robot_x,), = numpy.where(robot_map == "@")  # fmt: skip

    # print(*map("".join, robot_map), sep="\n")
    # print(moves)
    for move in moves:
        # print(*map("".join, robot_map), sep="\n")

        direction = get_direction(move)
        dx, dy = direction

        if robot_map[robot_y + dy, robot_x + dx] == ".":
            robot_map[robot_y, robot_x] = "."
            robot_x += dx
            robot_y += dy
            robot_map[robot_y, robot_x] = "@"
            continue
        elif robot_map[robot_y + dy, robot_x + dx] == "#":
            continue  # the robot is against a wall

        # the robot has box(es) in front of him
        # let's count how many and find if it is against a wall

        k = 1
        while robot_map[robot_y + (k + 1) * dy, robot_x + (k + 1) * dx] == "O":
            k += 1

        if robot_map[robot_y + (k + 1) * dy, robot_x + (k + 1) * dx] == "#":
            continue  # the boxes are against a wall

        robot_map[robot_y + (k + 1) * dy, robot_x + (k + 1) * dx] = "O"
        robot_map[robot_y, robot_x] = "."
        robot_x += dx
        robot_y += dy
        robot_map[robot_y, robot_x] = "@"

    # print(*map("".join, robot_map), sep="\n")

    score = 0
    for x in range(1, len(robot_map) - 1):
        for y in range(1, len(robot_map) - 1):
            if robot_map[y, x] == "O":
                score += x + 100 * y
    print(score)

    # Part 2
    robot_map, moves = import_robot_map(filename)
    robot_map = double_map(robot_map)
    robot_map = numpy.array(robot_map)
    robot_x: int
    robot_y: int
    (robot_y,), (robot_x,), = numpy.where(robot_map == "@")  # fmt: skip

    # print(*map("".join, robot_map), sep="\n")
    for i, move in enumerate(moves):
        direction = get_direction(move)
        dx, dy = direction

        if robot_map[robot_y + dy, robot_x + dx] == ".":
            robot_map[robot_y, robot_x] = "."
            robot_x += dx
            robot_y += dy
            robot_map[robot_y, robot_x] = "@"
            continue
        elif robot_map[robot_y + dy, robot_x + dx] == "#":
            continue  # the robot is against a wall

        # the robot has box(es) in front of him
        # let's count how many and find if it is against a wall

        if dy == 0:
            k = 1
            while robot_map[robot_y, robot_x + (k + 1) * dx] in (
                "[",
                "]",
            ):
                k += 1

            if robot_map[robot_y, robot_x + (k + 1) * dx] == "#":
                continue  # the boxes are against a wall

            robot_map[robot_y, robot_x + 2 * dx : robot_x + (k + 2) * dx : dx] = (
                robot_map[robot_y, robot_x + dx : robot_x + (k + 1) * dx : dx]
            )
            robot_map[robot_y, robot_x] = "."
            robot_x += dx
            robot_y += dy
            robot_map[robot_y, robot_x] = "@"
        else:
            old_map = robot_map.copy()
            has_moved = move_up_down(robot_x, robot_y + dy, dy, robot_map)
            if has_moved:
                robot_map[robot_y, robot_x] = "."
                robot_y += dy
                robot_map[robot_y, robot_x] = "@"
            else:
                robot_map = old_map

    # with open('custom_output', mode='w') as output_file:
    #     print(*map("".join, robot_map), sep="\n", file=output_file)

    score = 0
    for x in range(len(robot_map[0])):
        for y in range(len(robot_map)):
            if robot_map[y, x] == "[":
                score += x + 100 * y
    print(score)


if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    main(filename)
