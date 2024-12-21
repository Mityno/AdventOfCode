import functools


DIRECTIONS = ((-1, 0), (0, 1), (1, 0), (0, -1))


def import_maze(filename: str) -> list[list[str]]:

    with open(filename, mode="r", encoding="utf8") as file:
        data = file.read().strip()
    lines = data.split()
    lines = list(map(list, lines))
    return lines


def find(maze: list[list[str]], char: str) -> tuple[int, int]:
    n = len(maze)
    for y in range(n):
        for x in range(n):
            if maze[y][x] == char:
                return x, y
    raise ValueError(f"{char!r} not in given maze")


@functools.cache
def coord_to_index(coord: tuple[int, int], n: int) -> int:
    return coord[0] + n * coord[1]


@functools.cache
def index_to_coord(index: int, n: int) -> tuple[int, int]:
    return index % n, index // n


@functools.cache
def index_distance(a: int, b: int, n: int) -> int:
    x_a, y_a = a % n, a // n
    x_b, y_b = b % n, b // n
    return abs(x_a - x_b) + abs(y_a - y_b)


@functools.cache
def index_neighbors(index: int, n: int) -> tuple[int, ...]:
    up = index - n
    down = index + n
    left = index - 1
    right = index + 1

    neighbors: list[int] = []
    if up >= n:  # not before the second line
        neighbors.append(up)
    if down < n**2 - n:  # not after the last but one line
        neighbors.append(down)
    if left // n == index // n and left % n != 0:  # fmt: skip # check they are on the same line (== same y) and not on the edge
        neighbors.append(left)
    if right // n == index // n and right % n != n - 1:
        neighbors.append(right)
    return tuple(neighbors)


@functools.cache
def generate_point_in_circle(center: int, radius: int, n: int) -> set[int]:
    x, y = index_to_coord(center, n)
    points: set[int] = set()
    for y_dist in range(radius + 1):
        for x_dist in range(radius + 1 - y_dist):
            if 0 < x - x_dist and 0 < y - y_dist:
                points.add(center - y_dist * n - x_dist)
            if x + x_dist < n and 0 < y - y_dist:
                points.add(center - y_dist * n + x_dist)
            if 0 < x - x_dist and y + y_dist < n:
                points.add(center + y_dist * n - x_dist)
            if x + x_dist < n and y + y_dist < n:
                points.add(center + y_dist * n + x_dist)
    for point in tuple(points):
        if point < 0 or point >= n**2:
            points.discard(point)
    return points


def compute_path_cost(
    start: int, end: int, next_table: list[int], max_length: int | None = None
):
    if max_length is None:
        max_length = len(next_table)

    total_cost = 0
    curr = start
    while curr != end:
        next = next_table[curr]
        total_cost += 1
        if total_cost > max_length:
            return max_length  # return a greater distance than possible without loop
        curr = next
    return total_cost


def create_adjacency_matrix(space: list[list[str]]) -> list[None | tuple[int, ...]]:
    n = len(space)
    adjacency: list[tuple[int, ...] | None] = [None] * n**2

    for x in range(n):
        for y in range(n):
            if space[y][x] == "#":
                continue

            neighbors: list[int] = []
            for dx, dy in DIRECTIONS:
                if (
                    0 <= x + dx <= n - 1
                    and 0 <= y + dy <= n - 1
                    and space[y + dy][x + dx] != "#"
                ):
                    neighbor_index: int = coord_to_index((x + dx, y + dy), n)
                    neighbors.append(neighbor_index)
            index = coord_to_index((x, y), n)
            adjacency[index] = tuple(neighbors)

    return adjacency


def update_dist(distances: list[int], new: int, current: int) -> int:
    if distances[current] > distances[new] + 1:
        distances[current] = distances[new] + 1
        return True
    return False


def dijkstra(space: list[list[str]], start_coord: tuple[int, int]):

    n = len(space)
    adjacency = create_adjacency_matrix(space)
    start = coord_to_index(start_coord, n)

    distances: list[int] = [
        float("inf")
    ] * n**2  # pyright: ignore[reportAssignmentType]
    previouses: list[int] = [start] * n**2
    unseen = set(
        index for index, neighbors in enumerate(adjacency) if neighbors is not None
    )

    distances[start] = 0

    while unseen:
        curr = min(unseen, key=distances.__getitem__)
        unseen.discard(curr)
        neighbors = adjacency[curr]
        assert neighbors is not None

        for neighbor in neighbors:
            updated = update_dist(distances, curr, neighbor)
            if updated:
                previouses[neighbor] = curr

    return distances, previouses


def count_cheating_paths(
    distances_to_start: list[int], distances_to_end: list[int], optimal_distance: int
) -> int:
    cheating_counter = 0
    n_points = len(distances_to_start)
    n = int(n_points**0.5)

    # minimum_distance = optimal_distance - 2
    # minimum_distance = optimal_distance - 50
    minimum_distance = optimal_distance - 100

    possible_starts = [
        index
        for index in range(n_points)
        if distances_to_start[index] <= minimum_distance
    ]
    possible_ends = [
        index
        for index in range(n_points)
        if distances_to_end[index] <= minimum_distance
    ]
    print(n_points)
    print(len(possible_starts))
    print(len(possible_ends))
    print(len(set(possible_starts) & set(possible_ends)))

    for cheating_start in possible_starts:
        start_dist = distances_to_start[cheating_start]
        if start_dist > minimum_distance:
            # should be useless
            continue

        # for cheating_end in possible_ends:
        for cheating_end in generate_point_in_circle(cheating_start, 20, n):
            cheating_distance = index_distance(cheating_start, cheating_end, n)
            total_distance = (
                start_dist + cheating_distance + distances_to_end[cheating_end]
            )
            if total_distance > minimum_distance:
                continue
            cheating_counter += 1

    return cheating_counter


def main(filename: str):

    maze = import_maze(filename)
    flat_maze = [cell for line in maze for cell in line]

    n = len(maze)
    start: tuple[int, int] = find(maze, "S")
    end: tuple[int, int] = find(maze, "E")
    start_index = coord_to_index(start, n)
    end_index = coord_to_index(end, n)

    # Part 1

    # print(*map("".join, maze), sep="\n")

    distances_to_start, previouses_to_start = dijkstra(maze, start)

    optimal_path = [end_index]
    curr = end_index
    while curr != start_index:
        curr = previouses_to_start[curr]
        optimal_path.append(curr)
    optimal_path.reverse()
    # print(optimal_path)

    optimal_distance = distances_to_start[end_index]
    print(end_index)
    print("optimal distance", optimal_distance)

    distances_to_end, previouses_to_end = dijkstra(maze, end)
    cheating_counter = count_cheating_paths(
        distances_to_start, distances_to_end, optimal_distance
    )
    print("total paths", cheating_counter)


if __name__ == "__main__":
    import sys

    # n = 50
    # center = coord_to_index((2, 2), n)
    # print(center)
    # points = generate_point_in_circle(center, 10, n)
    # print(points)
    # for point in points:
    #     print(index_distance(center, point, n))
    # exit()
    filename = sys.argv[1]
    main(filename)
