from collections.abc import Sequence
import functools
import numpy


DIRECTIONS = ((-1, 0), (0, 1), (1, 0), (0, -1))


def import_topo_map(filename: str):

    with open(filename) as file:
        topo_map = file.readlines()

    topo_map = map(str.strip, topo_map)
    topo_map = map(list, topo_map)
    topo_map = numpy.array([list(map(int, line)) for line in topo_map])
    return topo_map


@functools.cache
def neighbors(point: tuple[int, int], n: int) -> list[tuple[int, int]]:
    x, y = point
    return [
        (x + dx, y + dy)
        for dx, dy in DIRECTIONS
        if 0 <= x + dx <= n - 1 and 0 <= y + dy <= n - 1
    ]


def solve_trail(topo_map: Sequence[Sequence[int]], trailhead: tuple[int, int]):

    trail_ends: set[tuple[int, int]] = set()
    trail_paths: set[tuple[tuple[int, int], ...]] = set()
    curr_path = [trailhead]
    n = len(topo_map)

    def inner(curr_point: tuple[int, int]):
        # fmt: off
        if topo_map[curr_point] == 9:  # pyright: ignore[reportArgumentType, reportCallIssue]
            # fmt: on
            trail_ends.add(curr_point)
            trail_paths.add(tuple(curr_path))
            return

        for neighbor in neighbors(curr_point, n):
            # fmt: off
            if topo_map[neighbor] == topo_map[curr_point] + 1:  # pyright: ignore[reportArgumentType, reportCallIssue]
                # fmt: on
                curr_path.append(neighbor)
                inner(neighbor)
                curr_path.pop()

    inner(trailhead)
    return len(trail_ends), len(trail_paths)


def main(filename: str):
    topo_map = import_topo_map(filename)
    print(topo_map)

    trailheads = list(zip(*numpy.where(topo_map == 0)))
    print(*trailheads)
    print(len(trailheads))

    hikes_counter = 0
    distinct_trails_counter = 0
    for trailhead in trailheads:
        new_trails, distincs_trails = solve_trail(topo_map, trailhead)
        hikes_counter += new_trails  # Part 1
        distinct_trails_counter += distincs_trails  # Part 2

    print(hikes_counter)
    print(distinct_trails_counter)


if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    main(filename)
