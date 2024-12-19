DIRECTIONS = ((-1, 0), (0, 1), (1, 0), (0, -1))


def import_bytes(filename: str) -> list[tuple[int, int]]:

    incoming_bytes: list[tuple[int, int]] = list()
    with open(filename, mode="r", encoding="utf8") as file:
        for line in file:
            incoming_bytes.append(tuple(map(int, line.strip().split(","))))  # fmt: skip # pyright: ignore[reportArgumentType]
    return incoming_bytes


def create_space(n: int) -> list[list[str]]:
    return [["." for _ in range(n)] for _ in range(n)]


def coord_to_index(coord: tuple[int, int], n: int) -> int:
    return coord[0] + n * coord[1]


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


def main(filename: str):

    incoming_bytes = import_bytes(filename)
    limit = 1024 if filename == "input2" else 12

    n: int = 71 if filename == "input2" else 7
    space = create_space(n)
    start: tuple[int, int] = (0, 0)
    end: tuple[int, int] = (n - 1, n - 1)

    # Part 1
    for x, y in incoming_bytes[:limit]:
        space[y][x] = "#"

    print(incoming_bytes)
    print(*map("".join, space), sep="\n")

    distances, previouses = dijkstra(space, start)

    end_index = coord_to_index(end, n)
    print(end_index)
    print(distances[end_index])

    # Part 2
    curr_byte: int = limit - 1
    while distances[end_index] != float("inf"):

        if curr_byte % 100 == 0:
            print(curr_byte)
        curr_byte += 1
        x, y = incoming_bytes[curr_byte]

        # index = coord_to_index((x, y), n)
        # distances[index] = float('inf')

        space[y][x] = "#"

        distances, previouses = dijkstra(space, start)

    print(curr_byte)
    print(incoming_bytes[curr_byte])

if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    main(filename)
