from collections.abc import Sequence
import numpy
import time
import functools


def import_map(filename: str):
    with open(filename, mode="r", encoding="utf8") as file:
        guard_map = file.readlines()

    guard_map = list(map(list, map(str.strip, guard_map)))
    guard_map = numpy.array(guard_map)
    return guard_map


@functools.cache
def next_direction(direction: tuple[int, int] | None) -> tuple[int, int]:
    "Returns the direction turned to its right"
    if direction is None:
        return (-1, 0)

    directions = ((-1, 0), (0, 1), (1, 0), (0, -1))
    curr_index = directions.index(direction)
    next_index = (curr_index + 1) % len(directions)
    return directions[next_index]


def walk(
    guard_map: Sequence[Sequence[str]],
    pos: tuple[int, int],
    direction: tuple[int, int] | None = None,
):
    if direction is None:
        direction = next_direction(direction)

    n = len(guard_map)
    pos_x, pos_y = pos

    while 0 <= pos_x <= n - 1 and 0 <= pos_y <= n - 1:
        guard_map[pos_x, pos_y] = "X"

        next_x = pos_x + direction[0]
        next_y = pos_y + direction[1]

        if not (0 <= next_x <= n - 1 and 0 <= next_y <= n - 1):
            # the guard went out
            break

        if guard_map[next_x, next_y] == "#":
            direction = next_direction(direction)

        pos_x = pos_x + direction[0]
        pos_y = pos_y + direction[1]


def walk_with_search(
    guard_map, pos: tuple[int, int], direction: tuple[int, int] | None = None
):
    if direction is None:
        direction = next_direction(direction)

    n = len(guard_map)
    pos_x, pos_y = pos
    history = {(pos_x, pos_y, direction)}
    path = {(pos_x, pos_y)}
    loop_counter = 0

    while 0 <= pos_x <= n - 1 and 0 <= pos_y <= n - 1:
        old_pos_x, old_pos_y = pos_x, pos_y
        old_direction = direction

        # check if "placing" an obstacle in front would cause a loop
        obstacle_x, obstacle_y = old_pos_x + direction[0], old_pos_y + direction[1]
        direction = next_direction(direction)  # hit an obstacle, change direction
        loop_history: set[tuple[int, int, tuple[int, int]]] = set()
        looped = False
        skipped = False

        if (obstacle_x, obstacle_y) in path:
            # the obstacle would have blocked us earlier
            skipped = True

        if guard_map[obstacle_x, obstacle_y] == "#":
            # we cannot place an obstacle where there is already a wall
            # (and we already know it won't cause a loop)
            skipped = True

        while not skipped and 0 <= pos_x <= n - 1 and 0 <= pos_y <= n - 1:
            next_x = pos_x + direction[0]
            next_y = pos_y + direction[1]

            if not (0 <= next_x <= n - 1 and 0 <= next_y <= n - 1):
                # the guard went out
                break

            if guard_map[next_x, next_y] == "#":
                direction = next_direction(direction)

            pos_x = pos_x + direction[0]
            pos_y = pos_y + direction[1]

            if (pos_x, pos_y, direction) in history or (
                pos_x,
                pos_y,
                direction,
            ) in loop_history:
                looped = True
                break

            loop_history.add((pos_x, pos_y, direction))

        if looped:
            loop_counter += 1

        pos_x, pos_y = old_pos_x, old_pos_y
        direction = old_direction

        next_x = pos_x + direction[0]
        next_y = pos_y + direction[1]

        if not (0 <= next_x <= n - 1 and 0 <= next_y <= n - 1):
            # the guard went out
            break

        if guard_map[next_x, next_y] == "#":
            direction = next_direction(direction)

        pos_x = pos_x + direction[0]
        pos_y = pos_y + direction[1]
        history.add((pos_x, pos_y, direction))
        path.add((pos_x, pos_y))

    return loop_counter


def main(filename: str):
    # Part 1
    guard_map = import_map(filename)
    print(guard_map)

    (pos_x,) , (pos_y,)= numpy.where(guard_map == "^")  # pyright: ignore[reportAny]

    walk(guard_map, (pos_x, pos_y))

    print((guard_map == "X").sum())

    # Part 2

    # possible_obstacles = guard_map == "X"
    # guard_map = import_map(filename)
    #
    # n = len(guard_map)
    # loop_counter = 0
    #
    # bef = time.perf_counter()
    # for obstacle_x in range(n):
    #     for obstacle_y in range(n):
    #         if not possible_obstacles[obstacle_x, obstacle_y]:
    #             continue
    #
    #         curr_guard_map = guard_map.copy()
    #
    #         if curr_guard_map[obstacle_x, obstacle_y] == "^":
    #             continue
    #
    #         curr_guard_map[obstacle_x, obstacle_y] = "O"
    #
    #         direction = next_direction(None)
    #         (pos_x,), (pos_y,) = numpy.where(curr_guard_map == "^")
    #
    #         history = {(pos_x, pos_y, direction)}
    #         looped = False
    #
    #         while 0 <= pos_x <= n - 1 and 0 <= pos_y <= n - 1:
    #             next_x = pos_x + direction[0]
    #             next_y = pos_y + direction[1]
    #
    #             if not (0 <= next_x <= n - 1 and 0 <= next_y <= n - 1):
    #                 # the guard went out
    #                 break
    #
    #             finished = False
    #
    #             while curr_guard_map[next_x, next_y] in ("#", "O"):
    #                 direction = next_direction(direction)
    #                 next_x = pos_x + direction[0]
    #                 next_y = pos_y + direction[1]
    #                 if not (0 <= next_x <= n - 1 and 0 <= next_y <= n - 1):
    #                     # the guard went out
    #                     finished = True
    #                     break
    #
    #             if finished:
    #                 break
    #
    #             pos_x = pos_x + direction[0]
    #             pos_y = pos_y + direction[1]
    #
    #             if (pos_x, pos_y, direction) in history:
    #                 looped = True
    #                 break
    #             history.add((pos_x, pos_y, direction))
    #
    #         if looped:
    #             loop_counter += 1
    # aft = time.perf_counter()
    # print(loop_counter)
    # print(f"Took {aft - bef:.2f}s")

    guard_map = import_map(filename)

    (pos_x,), (pos_y,) = numpy.where(guard_map == "^")  # pyright: ignore[reportAny]
    bef = time.perf_counter()
    loop_counter = walk_with_search(guard_map, (pos_x, pos_y))
    aft = time.perf_counter()

    print(loop_counter)
    print(f"Took {aft - bef:.2f}s")


if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    main(filename)
