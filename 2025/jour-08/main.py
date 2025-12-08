import functools
import operator
import time


def read_datas() -> tuple[int, list[tuple[int, int, int]]]:

    max_it = int(input())
    n = int(input())
    coords: list[tuple[int, int, int]] = [
        tuple(map(int, input().split(","))) for _ in range(n)
    ]  # pyright: ignore[reportAssignmentType]

    return max_it, coords


def distance(x1: int, y1: int, z1: int, x2: int, y2: int, z2: int) -> float:
    return float(((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2) ** 0.5)


def slow_union_find(coords: list[tuple[int, int, int]], max_it: int) -> list[list[int]]:

    n = len(coords)
    groups: list[list[int]] = [[i] for i in range(n)]
    index_to_group_index: dict[int, int] = {i: i for i in range(n)}
    connexions = {
        (i, j): distance(*coords[i], *coords[j])
        for i in range(n)
        for j in range(n)
        if i < j
    }
    sorted_connections = sorted(connexions.keys(), key=lambda k: connexions[k])

    for curr, closest in sorted_connections[:max_it]:

        # merge the groups from the current one and closest into the current one
        curr_group_index = index_to_group_index[curr]
        closest_group_index = index_to_group_index[closest]

        if curr_group_index == closest_group_index:
            # they are already in the same group
            continue

        # update index to group dict to point to the current group
        for index in groups[closest_group_index]:
            index_to_group_index[index] = curr_group_index

        # merge the points
        groups[curr_group_index].extend(groups[closest_group_index])
        # and clear the other group
        groups[closest_group_index].clear()

    return groups


def slow_union_until_fully_merged(
    coords: list[tuple[int, int, int]],
) -> tuple[int, int]:

    n = len(coords)
    groups: list[list[int]] = [[i] for i in range(n)]
    index_to_group_index: dict[int, int] = {i: i for i in range(n)}
    connexions = {
        (i, j): distance(*coords[i], *coords[j])
        for i in range(n)
        for j in range(n)
        if i < j
    }
    sorted_connections = sorted(connexions.keys(), key=lambda k: connexions[k])

    for curr, closest in sorted_connections:

        # merge the groups from the current one and closest into the current one
        curr_group_index = index_to_group_index[curr]
        closest_group_index = index_to_group_index[closest]

        if curr_group_index == closest_group_index:
            # they are already in the same group
            continue

        # update index to group dict to point to the current group
        for index in groups[closest_group_index]:
            index_to_group_index[index] = curr_group_index

        # merge the points
        groups[curr_group_index].extend(groups[closest_group_index])
        # and clear the other group
        groups[closest_group_index].clear()

        if len(groups[curr_group_index]) == n:
            return coords[curr][0], coords[closest][0]

    raise ValueError("couldn't finish merging into a single group")


def main():

    bef = time.perf_counter()
    max_it, coords = read_datas()
    aft = time.perf_counter()
    print(f"Reading : {aft-bef:.2f}s")

    # Part 1
    # bef = time.perf_counter()
    # groups = slow_union_find(coords, max_it)
    # aft = time.perf_counter()
    # print(f"Union : {aft-bef:.2f}s")
    #
    # bef = time.perf_counter()
    # three_largest = sorted(map(len, groups))[-3:]
    # aft = time.perf_counter()
    # print(f"Picking largests : {aft-bef:.2f}s")
    #
    # print(three_largest)
    # result: int = functools.reduce(operator.mul, three_largest)
    # print(result)

    # Part 2
    bef = time.perf_counter()
    a, b = slow_union_until_fully_merged(coords)
    aft = time.perf_counter()
    print(f"Union : {aft-bef:.2f}s")

    print(a * b)


main()
