import sys

# sys.setrecursionlimit(100000)

DIRECTIONS = ((-1, 0), (0, 1), (1, 0), (0, -1))


def import_maze_graph(
    filename: str,
) -> tuple[list[list[str]], dict[tuple[int, int], list[tuple[int, int]]]]:

    with open(filename, mode="r", encoding="utf8") as file:
        maze = file.read()

    maze = maze.strip().split()
    maze = list(map(list, maze))
    graph_dico: dict[tuple[int, int], list[tuple[int, int]]] = {}
    n = len(maze)
    for x in range(n):
        for y in range(n):
            if maze[y][x] == "#":
                continue

            curr_list: list[tuple[int, int]] = []
            graph_dico[(x, y)] = curr_list
            for dx, dy in DIRECTIONS:
                if maze[y + dy][x + dx] != "#":
                    curr_list.append((x + dx, y + dy))

    return maze, graph_dico


def find(maze: list[list[str]], char: str) -> tuple[int, int]:
    n = len(maze)
    for y in range(n):
        for x in range(n):
            if maze[y][x] == char:
                return x, y
    raise ValueError(f"{char!r} not in given maze")


def custom_dijkstra(
    graph_dico: dict[tuple[int, int], list[tuple[int, int]]],
    start: tuple[int, int],
    end: tuple[int, int],
):

    n = len(graph_dico)
    graph_indices = {
        summit: index for summit, index in zip(graph_dico.keys(), range(n))
    }
    summits = list(graph_dico.keys())
    unseen: set[tuple[int, int]] = set(graph_dico.keys())
    distances: list[int] = [float("inf")] * n  # pyright: ignore[reportAssignmentType]
    prev: list[int] = [0] * n

    start_index = graph_indices[start]
    end_index = graph_indices[end]
    distances[start_index] = 0

    while unseen:
        curr = min(unseen, key=lambda summit: distances[graph_indices[summit]])
        curr_index = graph_indices[curr]
        unseen.discard(curr)

        for neighbor in graph_dico[curr]:
            neighbor_index = graph_indices[neighbor]

            prev_index = prev[curr_index]
            prev_summit = summits[prev_index]
            if curr == start:
                rotation = (1, 0) != vector_difference(curr, neighbor)  # fmt: skip
            else:
                rotation = vector_difference(prev_summit, curr) != vector_difference(curr, neighbor)  # fmt: skip

            update_dist(distances, prev, curr_index, neighbor_index, rotation)

    return distances, start_index, end_index


def vector_difference(a: tuple[int, int], b: tuple[int, int]):
    return a[0] - b[0], a[1] - b[1]


def update_dist(distances: list[int], prev: list[int], a: int, b: int, rotation: bool):
    if distances[b] > distances[a] + 1 + 1000 * rotation:
        distances[b] = distances[a] + 1 + 1000 * rotation
        prev[b] = a


def main(filename: str):

    maze, graph_dico = import_maze_graph(filename)
    print(*map("".join, maze), sep="\n")
    start = find(maze, "S")
    end = find(maze, "E")
    distances, start_index, end_index = custom_dijkstra(graph_dico, start, end)
    print(distances[end_index])


if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    main(filename)
