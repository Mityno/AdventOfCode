import numpy
import time
import functools


def import_map(filename):
    with open(filename, mode="r", encoding="utf8") as file:
        guard_map = file.readlines()

    guard_map = list(map(list, map(str.strip, guard_map)))
    guard_map = numpy.array(guard_map)
    return guard_map


@functools.cache
def next_direction(direction):
    "Returns the direction turned to its right"
    if direction is None:
        return (-1, 0)

    directions = ((-1, 0), (0, 1), (1, 0), (0, -1))
    curr_index = directions.index(direction)
    next_index = (curr_index + 1) % len(directions)
    return directions[next_index]


def walk(guard_map, pos: tuple[int, int], direction: tuple[int, int] | None = None):
    if direction is None:
        direction = next_direction(direction)

    n = len(guard_map)
    pos_x, pos_y = pos

    while 0 <= pos_x <= n - 1 and 0 <= pos_y <= n - 1:
        guard_map[pos_x, pos_y] = "X"

        new_x = pos_x + direction[0]
        new_y = pos_y + direction[1]

        if not (0 <= new_x <= n - 1 and 0 <= new_y <= n - 1):
            # the guard went out
            break

        if guard_map[new_x, new_y] == "#":
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
    loop_set = set()

    while 0 <= pos_x <= n - 1 and 0 <= pos_y <= n - 1:
        old_pos_x, old_pos_y = pos_x, pos_y
        old_direction = direction

        # check is "placing" an obstacle in front would cause a loop
        direction = next_direction(direction)
        looped = False
        loop_history = history.copy()
        while 0 <= pos_x <= n - 1 and 0 <= pos_y <= n - 1:
            new_x = pos_x + direction[0]
            new_y = pos_y + direction[1]

            if not (0 <= new_x <= n - 1 and 0 <= new_y <= n - 1):
                # the guard went out
                break

            if guard_map[new_x, new_y] == "#":
                direction = next_direction(direction)

            pos_x = pos_x + direction[0]
            pos_y = pos_y + direction[1]

            if (pos_x, pos_y, direction) in loop_history:
                looped = True
                break

            loop_history.add((pos_x, pos_y, direction))

        if looped:
            loop_set.add((old_pos_x + direction[0], old_pos_y + direction[1]))

        pos_x, pos_y = old_pos_x, old_pos_y
        direction = old_direction

        new_x = pos_x + direction[0]
        new_y = pos_y + direction[1]

        if not (0 <= new_x <= n - 1 and 0 <= new_y <= n - 1):
            # the guard went out
            break

        if guard_map[new_x, new_y] == "#":
            direction = next_direction(direction)

        pos_x = pos_x + direction[0]
        pos_y = pos_y + direction[1]
        history.add((pos_x, pos_y, direction))

    return len(loop_set)


def main(filename):
    # Part 1
    guard_map = import_map(filename)
    print(guard_map)

    (pos_x,), (pos_y,) = numpy.where(guard_map == "^")

    walk(guard_map, (pos_x, pos_y))

    print((guard_map == "X").sum())
    possible_obstacles = guard_map == "X"

    # Part 2

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
    #         direction = next_direction(direction)
    #         (pos_x,), (pos_y,) = numpy.where(curr_guard_map == "^")
    #
    #         history = {(pos_x, pos_y, direction)}
    #         looped = False
    #
    #         while 0 <= pos_x <= n - 1 and 0 <= pos_y <= n - 1:
    #             new_x = pos_x + direction[0]
    #             new_y = pos_y + direction[1]
    #
    #             if not (0 <= new_x <= n - 1 and 0 <= new_y <= n - 1):
    #                 # the guard went out
    #                 break
    #
    #             finished = False
    #
    #             while curr_guard_map[new_x, new_y] in ("#", "O"):
    #                 direction = next_direction(direction)
    #                 new_x = pos_x + direction[0]
    #                 new_y = pos_y + direction[1]
    #                 if not (0 <= new_x <= n - 1 and 0 <= new_y <= n - 1):
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

    (pos_x,), (pos_y,) = numpy.where(guard_map == "^")
    bef = time.perf_counter()
    loop_counter = walk_with_search(guard_map, (pos_x, pos_y))
    aft = time.perf_counter()

    print(loop_counter)
    print(f"Took {aft - bef:.2f}s")


if __name__ == "__main__":
    main("input1")
