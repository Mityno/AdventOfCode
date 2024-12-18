DIRECTIONS = ((-1, 0), (0, 1), (1, 0), (0, -1))


def import_maze_graph(
    filename: str,
) -> tuple[list[list[str]], dict[tuple[int, int], tuple[tuple[int, int], ...]]]:

    with open(filename, mode="r", encoding="utf8") as file:
        maze = file.read()

    maze = maze.strip().split()
    maze = list(map(list, maze))
    graph_dico: dict[tuple[int, int], tuple[tuple[int, int], ...]] = {}
    n = len(maze)
    for x in range(n):
        for y in range(n):
            if maze[y][x] == "#":
                continue

            curr_list: list[tuple[int, int]] = []
            for dx, dy in DIRECTIONS:
                if maze[y + dy][x + dx] != "#":
                    curr_list.append((x + dx, y + dy))
            graph_dico[(x, y)] = tuple(curr_list)

    return maze, graph_dico


def find(maze: list[list[str]], char: str) -> tuple[int, int]:
    n = len(maze)
    for y in range(n):
        for x in range(n):
            if maze[y][x] == char:
                return x, y
    raise ValueError(f"{char!r} not in given maze")


def custom_dijkstra(
    graph_dico: dict[tuple[int, int], tuple[tuple[int, int], ...]],
    start: tuple[int, int],
    end: tuple[int, int],
):

    n = len(graph_dico)
    graph_indices = {
        summit: index for summit, index in zip(graph_dico.keys(), range(n))
    }
    summits = list(graph_dico.keys())
    start_index = graph_indices[start]
    end_index = graph_indices[end]

    unseen: set[tuple[int, int]] = set(graph_dico.keys())
    distances: list[int] = [float("inf")] * n  # pyright: ignore[reportAssignmentType]
    prev: list[int] = [0] * n
    directions: list[tuple[int, int]] = [(0, 0)] * n

    directions[start_index] = (1, 0)
    distances[start_index] = 0

    while unseen:
        curr = min(unseen, key=lambda summit: distances[graph_indices[summit]])
        curr_index = graph_indices[curr]
        unseen.discard(curr)

        for neighbor in graph_dico[curr]:
            neighbor_index = graph_indices[neighbor]

            curr_direction = vector_difference(neighbor, curr)
            rotation = directions[curr_index] != curr_direction  # fmt: skip

            update_dist(
                distances,
                prev,
                directions,
                curr_index,
                neighbor_index,
                rotation,
                curr_direction,
            )

    return distances, prev, directions, start_index, end_index


def vector_difference(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return a[0] - b[0], a[1] - b[1]


def update_dist(
    distances: list[int],
    prev: list[int],
    directions: list[tuple[int, int]],
    a: int,
    b: int,
    rotation: bool,
    curr_direction: tuple[int, int],
):
    if distances[b] > distances[a] + 1 + 1000 * rotation:
        distances[b] = distances[a] + 1 + 1000 * rotation
        prev[b] = a
        directions[b] = curr_direction


def possible_summits(
    graph_idx_idx: dict[int, tuple[int, ...]],
    distances: list[int],
    prev: list[int],
    directions: list[tuple[int, int]],
    start_index: int,
    end_index: int,
):
    possibles = {start_index, end_index}
    real_cost = distances[end_index]

    def inner(curr: int):
        for neighbor in graph_idx_idx[curr]:
            if prev[neighbor] == curr:
                continue

            if neighbor == prev[curr]:
                possibles.add(neighbor)
                inner(neighbor)
                continue

            real_prev = prev[curr]
            real_direction = directions[curr]
            prev[curr] = neighbor
            directions[curr] = directions[neighbor]

            if compute_path_cost(end_index, start_index, prev, directions) == real_cost:
                possibles.add(neighbor)
                inner(neighbor)

            prev[curr] = real_prev
            directions[curr] = real_direction

    inner(end_index)
    return possibles


def compute_path_cost(
    start: int, end: int, next_table: list[int], directions: list[tuple[int, int]]
):

    total_cost = 0
    curr = start
    while curr != end:
        next = next_table[curr]
        if directions[curr] == directions[next]:
            total_cost += 1
        else:
            total_cost += 1001
        curr = next
    return total_cost


def main(filename: str):

    maze, graph_dico = import_maze_graph(filename)
    print(*map("".join, maze), sep="\n")
    start = find(maze, "S")
    end = find(maze, "E")
    distances, prev, directions, start_index, end_index = custom_dijkstra(
        graph_dico, start, end
    )
    print(start, end)

    # Part 1
    print(distances[end_index])

    curr_index = end_index
    summits = list(graph_dico.keys())
    while curr_index != start_index:
        prev_index = prev[curr_index]
        prev_coords = summits[prev_index]
        maze[prev_coords[1]][prev_coords[0]] = "X"
        curr_index = prev_index
    print(*map("".join, maze), sep="\n")

    # Part 2
    n = len(graph_dico)
    graph_indices = {
        summit: index for summit, index in zip(graph_dico.keys(), range(n))
    }
    graph_idx_idx = {
        graph_indices[summit]: tuple(graph_indices[neighbor] for neighbor in neighbors)
        for summit, neighbors in graph_dico.items()
    }
    possibles = possible_summits(
        graph_idx_idx, distances, prev, directions, start_index, end_index
    )
    for summit_index in possibles:
        x, y = summits[summit_index]
        maze[y][x] = "O"
    print(*map("".join, maze), sep="\n")
    print(len(possibles))


if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    main(filename)
