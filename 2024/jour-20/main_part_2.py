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


def update_dist_with_cheat(
    distances: list[tuple[int, int]],
    flat_maze: list[str],
    limit: int,
    new: int,
    current: int,
) -> int:
    curr_dist, _ = distances[current]
    new_dist, new_cheat = distances[new]
    must_cheat = flat_maze[new] == "#"
    add_cheat = must_cheat or new_cheat > 0

    if must_cheat and new_cheat + add_cheat > limit:
        return False

    if curr_dist > new_dist + 1:
        distances[current] = new_dist + 1, min(new_cheat + add_cheat, limit)
        return True
    return False


def dijkstra_with_cheat(flat_maze: list[str], start_coord: tuple[int, int]):
    n = int(len(flat_maze) ** 0.5)
    adjacency = [index_neighbors(index, n) for index in range(n**2)]
    start = coord_to_index(start_coord, n)

    distances: list[tuple[int, int]] = [
        (float("inf"), 0)
    ] * n**2  # pyright: ignore[reportAssignmentType]
    previouses: list[int] = [start] * n**2
    unseen = set(range(n**2))

    distances[start] = 0, 0
    limit = 20

    while unseen:
        curr = min(unseen, key=distances.__getitem__)
        unseen.discard(curr)
        neighbors = adjacency[curr]

        for neighbor in neighbors:
            updated = update_dist_with_cheat(
                distances, flat_maze, limit, curr, neighbor
            )
            if updated:
                previouses[neighbor] = curr

    return distances, previouses

def count_cheats(distances: list[tuple[int, int]], previouses: list[int], curr:int, optimal_distance: int) -> int:
    pass

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

    distances, previouses = dijkstra(maze, start)

    optimal_path = [end_index]
    curr = end_index
    while curr != start_index:
        curr = previouses[curr]
        optimal_path.append(curr)
    optimal_path.reverse()
    # print(optimal_path)

    print(end_index)
    print(distances[end_index])

    # Part 2
    print()
    print("Part 2")
    distances, previouses = dijkstra_with_cheat(flat_maze, start)
    print(distances[end_index])

    # print(*map("".join, maze), sep="\n")
    curr = previouses[end_index]
    while curr != start_index:
        flat_maze[curr] = "O"
        curr = previouses[curr]

    # for limit in range(n):
    #     print("".join(flat_maze[n * limit : n * (limit + 1)]))
    # print(distances)


if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    main(filename)
