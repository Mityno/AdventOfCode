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


def path_with_cheating(
    flat_maze: list[str],
    optimal_path: list[int],
    distances: list[int],
    previouses: list[int],
) -> int:
    start, end = optimal_path[0], optimal_path[-1]
    optimal_distance = distances[end]

    depth = int(sys.argv[2])
    print(f"{depth = }")

    cheats: set[tuple[int, int]] = set()
    cheating_counter = 0
    for curr in optimal_path:
        cheating_counter += recursive_cheat(
            flat_maze,
            distances,
            previouses,
            curr,
            depth,
            start,
            end,
            optimal_distance,
            cheats,
        )

    return cheating_counter


def recursive_cheat(
    flat_maze: list[str],
    distances: list[int],
    previouses: list[int],
    curr: int,
    depth: int,
    start: int,
    end: int,
    optimal_distance: int,
    cheats: set[tuple[int, int]] | None = None,
    cheat_start: int | None = None,
) -> int:
    if depth <= 0:
        return 0

    if cheats is None:
        cheats = set()
    if cheat_start is None:
        cheat_start = curr

    n = int(len(flat_maze) ** 0.5)

    cheating_counter = 0
    prev = previouses[curr]
    for neighbor in index_neighbors(curr, n):
        if neighbor == prev:  # or flat_maze[neighbor] != "#":
            # this is not cheating
            continue
        if flat_maze[neighbor] == "*":
            # this would create a loop
            continue

        old_neighbor_prev = previouses[neighbor]
        old_neighbor_dist = distances[neighbor]

        # in order not to create a loop by using this again later
        flat_maze[neighbor] = "*"
        previouses[neighbor] = curr

        distances[neighbor] = distances[curr] + 1

        # if can_cheat_more:
        # might cheat one more time
        cheating_counter += recursive_cheat(
            flat_maze,
            distances,
            previouses,
            neighbor,
            depth - 1,
            start,
            end,
            optimal_distance,
            cheats,
            cheat_start,
        )

        for neighbor_2 in index_neighbors(neighbor, n):

            if flat_maze[neighbor_2] == "#":
                # invalid last cell for a cheat
                continue

            old_neighbor_2_dist = distances[neighbor_2]
            updated = update_dist(distances, neighbor, neighbor_2)
            if updated:
                # it might be a shortcut
                new_distance = (
                    # distances[end] - old_neighbor_2_dist + distances[neighbor_2]
                    optimal_distance
                    - old_neighbor_2_dist
                    + distances[neighbor_2]
                )
                if new_distance <= optimal_distance - 70:  # - 70:
                    if (cheat_start, neighbor_2) not in cheats:
                        print(new_distance)
                        cheating_counter += 1
                        cheats.add((cheat_start, neighbor_2))

                distances[neighbor_2] = old_neighbor_2_dist

        previouses[neighbor] = old_neighbor_prev
        distances[neighbor] = old_neighbor_dist
        flat_maze[neighbor] = "#"

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

    distances, previouses = dijkstra(maze, start)

    optimal_path = [end_index]
    curr = end_index
    while curr != start_index:
        curr = previouses[curr]
        optimal_path.append(curr)
    optimal_path.reverse()
    # print(optimal_path)

    print(end_index)
    print("optimal distance", distances[end_index])

    cheating_counter = path_with_cheating(
        flat_maze, optimal_path, distances, previouses
    )
    print("total paths", cheating_counter)


if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    main(filename)
