import sys

sys.setrecursionlimit(100000)

DIRECTIONS = ((-1, 0), (0, 1), (1, 0), (0, -1))


def import_maze(filename: str):

    with open(filename, mode="r", encoding="utf8") as file:
        maze = file.read()

    maze = maze.strip().split()
    maze = list(map(list, maze))
    return maze


def find(maze: list[list[str]], char: str) -> tuple[int, int]:
    n = len(maze)
    for y in range(n):
        for x in range(n):
            if maze[y][x] == char:
                return x, y
    raise ValueError(f"{char!r} not in given maze")


def solve_min(maze: list[list[str]]) -> int:
    start_x, start_y = find(maze, "S")
    end_x, end_y = find(maze, "E")
    visited = {(start_x, start_y)}
    path = list(visited)
    best_score = 100000

    def inner(pos_x: int, pos_y: int, curr_dir: tuple[int, int], curr_score: int):
        nonlocal best_score

        if curr_score > best_score:
            return

        if (pos_x, pos_y) == (end_x, end_y):

            if curr_score < best_score:
                print('here', curr_score)
                best_score = curr_score
                return

        for dir in DIRECTIONS:
            dx, dy = dir
            if (pos_x + dx, pos_y + dy) in visited:
                continue

            if maze[pos_y + dy][pos_x + dx] == "#":
                continue

            next_score = curr_score + 1 + (curr_dir != dir) * 1000
            path.append((pos_x + dx, pos_y + dy))
            visited.add((pos_x + dx, pos_y + dy))
            inner(pos_x + dx, pos_y + dy, dir, next_score)
            visited.discard((pos_x + dx, pos_y + dy))
            _ = path.pop()

    inner(start_x, start_y, (0, 1), 0)
    return best_score


def main(filename: str):

    maze = import_maze(filename)
    print(*map("".join, maze), sep="\n")
    best_score = solve_min(maze)
    print(best_score)


if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    main(filename)
