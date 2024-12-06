import numpy
import itertools


def import_map(filename):

    with open(filename, mode="r", encoding="utf8") as file:
        guard_map = file.readlines()

    guard_map = list(map(list, map(str.strip, guard_map)))
    guard_map = numpy.array(guard_map)
    return guard_map


def main(filename):

    # Part 1
    guard_map = import_map(filename)
    print(guard_map)

    directions = itertools.cycle(((-1, 0), (0, 1), (1, 0), (0, -1)))
    direction = next(directions)
    (pos_x,), (pos_y,) = numpy.where(guard_map == "^")

    n = len(guard_map)
    while 0 <= pos_x <= n - 1 and 0 <= pos_y <= n - 1:

        guard_map[pos_x, pos_y] = "X"

        new_x = pos_x + direction[0]
        new_y = pos_y + direction[1]

        if not (0 <= new_x <= n - 1 and 0 <= new_y <= n - 1):
            # the guard went out
            break

        if guard_map[new_x, new_y] == "#":
            direction = next(directions)

        pos_x = pos_x + direction[0]
        pos_y = pos_y + direction[1]

    print((guard_map == "X").sum())
    possible_obstacles = guard_map == "X"

    # Part 2
    guard_map = import_map(filename)

    n = len(guard_map)
    loop_counter = 0

    for obstacle_x in range(n):
        for obstacle_y in range(n):
            if not possible_obstacles[obstacle_x, obstacle_y]:
                continue

            curr_guard_map = guard_map.copy()

            if curr_guard_map[obstacle_x, obstacle_y] == "^":
                continue

            curr_guard_map[obstacle_x, obstacle_y] = "O"

            directions = itertools.cycle(((-1, 0), (0, 1), (1, 0), (0, -1)))
            direction = next(directions)
            (pos_x,), (pos_y,) = numpy.where(curr_guard_map == "^")

            history = {(pos_x, pos_y, direction)}
            looped = False

            while 0 <= pos_x <= n - 1 and 0 <= pos_y <= n - 1:

                curr_guard_map[pos_x, pos_y] = "X"

                new_x = pos_x + direction[0]
                new_y = pos_y + direction[1]

                if not (0 <= new_x <= n - 1 and 0 <= new_y <= n - 1):
                    # the guard went out
                    break

                finished = False

                while curr_guard_map[new_x, new_y] in ("#", "O"):

                    direction = next(directions)
                    new_x = pos_x + direction[0]
                    new_y = pos_y + direction[1]
                    if not (0 <= new_x <= n - 1 and 0 <= new_y <= n - 1):
                        # the guard went out
                        finished = True
                        break

                if finished:
                    break

                pos_x = pos_x + direction[0]
                pos_y = pos_y + direction[1]

                if (pos_x, pos_y, direction) in history:
                    looped = True
                    break
                history.add((pos_x, pos_y, direction))

            if looped:
                loop_counter += 1
    print(loop_counter)


if __name__ == "__main__":
    main("input2")
