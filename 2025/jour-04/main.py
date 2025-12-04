def read_datas() -> list[list[str]]:
    n = int(input())
    grid = [list(input()) for _ in range(n)]
    return grid


def count_available_rolls(grid: list[list[str]]) -> int:

    n = len(grid)
    neighbors_displacements = [
        (1, 0),
        (1, -1),
        (0, -1),
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, 1),
        (1, 1),
    ]

    available_rolls_counter = 0

    for i in range(n):
        for j in range(n):
            if grid[i][j] != "@":
                # this cell is not a roll
                continue

            neighbor_rolls_count = 0

            for di, dj in neighbors_displacements:
                if not (0 <= i + di < n and 0 <= j + dj < n):
                    continue

                if grid[i + di][j + dj] == "@":
                    neighbor_rolls_count += 1

            available_rolls_counter += neighbor_rolls_count < 4

    return available_rolls_counter


def count_available_rolls_with_reduce(grid: list[list[str]]) -> int:

    n = len(grid)
    neighbors_displacements = [
        (1, 0),
        (1, -1),
        (0, -1),
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, 1),
        (1, 1),
    ]

    total_removable_rolls_counter = 0
    rolls_to_remove: list[tuple[int, int]] = []

    changed = True
    while changed:
        for i in range(n):
            for j in range(n):
                if grid[i][j] != "@":
                    # this cell is not a roll
                    continue

                neighbor_rolls_count = 0

                for di, dj in neighbors_displacements:
                    if not (0 <= i + di < n and 0 <= j + dj < n):
                        continue

                    if grid[i + di][j + dj] == "@":
                        neighbor_rolls_count += 1

                if neighbor_rolls_count < 4:
                    rolls_to_remove.append((i, j))

        total_removable_rolls_counter += len(rolls_to_remove)

        for i, j in rolls_to_remove:
            grid[i][j] = "."

        if not rolls_to_remove:
            changed = False

        rolls_to_remove.clear()

    return total_removable_rolls_counter


def main():

    grid = read_datas()

    # Part 1
    rolls_amount = count_available_rolls(grid)
    print(rolls_amount)
    # Part 2
    repeated_rolls_amount = count_available_rolls_with_reduce(grid)
    print(repeated_rolls_amount)


main()
