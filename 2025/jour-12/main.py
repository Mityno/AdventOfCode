from functools import cache


region_t = tuple[tuple[int, int], list[int]]


def read_datas():

    shapes: list[tuple[str, ...]] = []

    n_shapes = int(input())
    for _ in range(n_shapes):
        id = input()
        shape = tuple(input() for _ in range(3))
        shapes.append(shape)

    n_regions = int(input())
    regions: list[region_t] = []

    for _ in range(n_regions):
        dims, shape_amounts_str = input().split(":")
        width, length = map(int, dims.split("x"))
        shape_amounts = list(map(int, shape_amounts_str.split()))
        regions.append(((width, length), shape_amounts))

    return shapes, regions


@cache
def rotate_left(shape: tuple[str, ...]) -> tuple[str, ...]:
    rotated_shape: list[str] = ["", "", ""]
    for j in range(3):
        for i in range(2, -1, -1):
            rotated_shape[j] += shape[i][j]
    return tuple(rotated_shape)


def fit_presents(region: region_t, shapes: list[tuple[str, ...]]) -> bool:
    (width, length), shape_distribution = region
    min_area = sum(shape_distribution)

    if (width / 3) * (length / 3) < min_area:
        return False

    return True


def main():

    shapes, regions = read_datas()

    possible_regions_counter = 0
    for region in regions:
        can_fit = fit_presents(region, shapes)
        possible_regions_counter += can_fit

    print(possible_regions_counter)


main()
