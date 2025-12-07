import collections


def read_datas():

    n = int(input())

    grid = [input() for _ in range(n)]
    return grid


def count_beam_splits(grid: list[str]) -> int:

    split_count = 0

    start_index = grid[0].find("S")
    current_indices: set[int] = {start_index}
    height = len(grid)
    width = len(grid[0])

    next_indices: set[int] = set()
    for h in range(1, height):
        next_line = grid[h]
        next_indices.clear()

        for index in current_indices:
            match next_line[index]:
                case ".":
                    next_indices.add(index)
                case "^":
                    if index > 0:
                        next_indices.add(index - 1)
                    if index < width:
                        next_indices.add(index + 1)
                    split_count += 1
                case _:
                    raise ValueError("invalid grid")

        current_indices.clear()
        current_indices.update(next_indices)

    return split_count


def count_timelines(grid: list[str]) -> int:

    timelines_count = 0

    start_index = grid[0].find("S")
    current_indices: collections.Counter[int] = collections.Counter([start_index])
    height = len(grid)
    width = len(grid[0])

    for h in range(1, height):
        next_line = grid[h]

        for index, amount in tuple(current_indices.items()):
            match next_line[index]:
                case ".":
                    pass
                case "^":
                    current_indices[index] = 0
                    if index > 0:
                        current_indices[index - 1] += amount
                    if index < width:
                        current_indices[index + 1] += amount
                    timelines_count += 1
                case _:
                    raise ValueError("invalid grid")

    return sum(current_indices.values())


def main():

    grid = read_datas()

    # Part 1
    split_count = count_beam_splits(grid)
    print(split_count)

    # Part 2
    timelines_count = count_timelines(grid)
    print(timelines_count)


main()
