import functools

DIRECTIONS = ((-1, 0), (0, 1), (1, 0), (0, -1))


def import_map(filename: str):

    with open(filename, mode="r", encoding="utf8") as file:
        lines = file.readlines()

    lines = map(str.strip, lines)
    lines = map(list, lines)
    return list(lines)


def neighbors(point: tuple[int, int], n: int) -> set[tuple[int, int]]:
    x, y = point
    return {
        (x + dx, y + dy)
        for dx, dy in DIRECTIONS
        if 0 <= x + dx <= n - 1 and 0 <= y + dy <= n - 1
    }


@functools.cache
def next_direction(direction: tuple[int, int]) -> tuple[int, int]:
    "Returns the direction turned to its right"
    directions = ((-1, 0), (0, 1), (1, 0), (0, -1))
    curr_index = directions.index(direction)
    next_index = (curr_index + 1) % len(directions)
    return directions[next_index]


def calculate_region_perimeter(region: set[tuple[int, int]], n: int) -> int:

    perimeter = 0
    for point in region:
        point_neighbors = neighbors(point, n)

        match len(point_neighbors & region):
            case 0:
                # region with single point
                perimeter += 4
            case 1:
                perimeter += 3
            case 2:
                perimeter += 2
            case 3:
                perimeter += 1
            case _:
                pass

    return perimeter


def are_inline(a: tuple[int, int], b: tuple[int, int]):
    x_a, y_a = a
    x_b, y_b = b
    return x_a == x_b or y_a == y_b


def calculate_region_sides(region: set[tuple[int, int]]) -> int:

    if not region:
        return 0
    elif len(region) == 1:
        return 4

    sides = 0

    for direction in DIRECTIONS:
        dx, dy = direction
        ndx, ndy = next_direction(direction)
        on_the_side_edge = [(x, y) for x, y in region if (x + dx, y + dy) not in region]
        on_the_side_edge.sort()

        for x, y in on_the_side_edge:
            # check if curr is the start of a wall
            prev = (x - ndx, y - ndy)
            prev_plus_direction = (x - ndx + dx, y - ndy + dy)
            if prev not in region or prev_plus_direction in region:
                sides += 1

    return sides


def merge_regions(
    regions: list[set[tuple[int, int]]],
    region_1: int,
    region_2: int,
    coord_to_region: dict[tuple[int, int], int],
):
    regions[region_1].update(regions[region_2])

    for x, y in regions[region_2]:
        coord_to_region[(x, y)] = region_1

    regions[region_2].clear()


def main(filename: str):

    crops = import_map(filename)
    print(*crops, sep="\n")
    n = len(crops)

    # Part 1
    regions: list[set[tuple[int, int]]] = []
    coord_to_region: dict[tuple[int, int], int] = {}
    regions.append({(0, 0)})
    coord_to_region[(0, 0)] = 0

    # First column
    for i in range(1, n):
        curr_crop = crops[i][0]
        curr_coord = (i, 0)

        prev = crops[i - 1][0]
        prev_coord = (i - 1, 0)
        if curr_crop == prev:
            region = coord_to_region[prev_coord]
            coord_to_region[curr_coord] = region
            regions[region].add(curr_coord)
        else:
            regions.append({curr_coord})
            coord_to_region[curr_coord] = len(regions) - 1

    # First line
    for i in range(1, n):
        curr_crop = crops[0][i]
        curr_coord = (0, i)

        prev = crops[0][i - 1]
        prev_coord = (0, i - 1)
        if curr_crop == prev:
            region = coord_to_region[prev_coord]
            coord_to_region[curr_coord] = region
            regions[region].add(curr_coord)
        else:
            regions.append({curr_coord})
            coord_to_region[curr_coord] = len(regions) - 1

    for i in range(1, n):
        for j in range(1, n):
            curr = crops[i][j]
            curr_coord = (i, j)

            top = crops[i - 1][j]
            top_coord = (i - 1, j)

            left = crops[i][j - 1]
            left_coord = (i, j - 1)

            if top == left == curr:
                # we might need to merge the left and top regions
                left_region = coord_to_region[left_coord]
                top_region = coord_to_region[top_coord]

                if left_region != top_region:
                    merge_regions(regions, top_region, left_region, coord_to_region)

                coord_to_region[curr_coord] = top_region
                regions[top_region].add(curr_coord)

            elif curr == top:
                region = coord_to_region[top_coord]
                coord_to_region[curr_coord] = region
                regions[region].add(curr_coord)

            elif curr == left:
                region = coord_to_region[left_coord]
                coord_to_region[curr_coord] = region
                regions[region].add(curr_coord)

            else:
                regions.append({curr_coord})
                coord_to_region[curr_coord] = len(regions) - 1

    perimeters: list[int] = [
        calculate_region_perimeter(region, n) for region in regions
    ]

    price_perimeter = 0
    for region, perimeter in zip(regions, perimeters):
        if not region:
            # the region has been cleared when merged
            continue

        price_perimeter += len(region) * perimeter  # area * perimeter

    print(price_perimeter)

    price_side = 0
    for region in regions:
        if not region:
            continue

        sides = calculate_region_sides(region)
        area = len(region)

        price_side += area * sides

    print(price_side)


if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    main(filename)
