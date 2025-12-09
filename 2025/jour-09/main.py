def read_datas() -> list[tuple[int, int]]:

    n = int(input())
    coords: list[tuple[int, int]] = [
        tuple(map(int, input().split(","))) for _ in range(n)
    ]  # pyright: ignore[reportAssignmentType]
    return coords


def get_area(x1: int, y1: int, x2: int, y2: int) -> int:
    return (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)


def check_invalid_rectangle(
    i1: int, x1: int, y1: int, i2: int, x2: int, y2: int, coords: list[tuple[int, int]]
) -> bool:

    x1, x2 = sorted((x1, x2))
    y1, y2 = sorted((y1, y2))

    n = len(coords)
    border_indices: set[int] = set()
    for other_i, (other_x, other_y) in enumerate(coords):
        if other_i in (i1, i2):
            border_indices.add(other_i)
            continue

        # check if the point is inside the rectangle
        if x1 < other_x < x2 and y1 < other_y < y2:
            return True
        if x1 <= other_x <= x2 and y1 <= other_y <= y2:
            border_indices.add(other_i)
            continue

        # check that the point is not part of a line cutting the rectangle
        next_i = (other_i + 1) % n
        xn, yn = coords[next_i]

        if x1 <= other_x == xn <= x2:
            # vertical line
            ya, yb = sorted((other_y, yn))
            if ya < y1 and y2 < yb:
                return True

        if y1 <= other_y == yn <= y2:
            # horizontal line
            xa, xb = sorted((other_x, xn))
            if xa < x1 and x2 < xb:
                return True

    real_x1, real_y1 = coords[i1]
    real_x2, real_y2 = coords[i2]

    # check that there is no line pointing inside the rectangle
    for index in border_indices:
        if index in (i1, i2):
            continue

        next_index = (index + 1) % n
        prev_index = (index - 1) % n

        # the point is a corner inside the rectangle, check if that's a problem
        xc, yc = coords[index]

        if xc == real_x1 and yc == real_y2 or xc == real_x2 and yc == real_y1:
            # this is a true corner
            continue

        xn, yn = coords[next_index]
        xp, yp = coords[prev_index]

        # looking at the segment (prev, curr) and (curr, next), check if they're
        # going THROUGH the rectangle or not (touching the border is fine)

        if xc == x1:
            # left border
            if xp > x1:
                return True
            if xn > x1:
                return True
        elif xc == x2:
            # right border
            if xp < x2:
                return True
            if xn < x2:
                return True
        elif yc == y1:
            # top border
            if yp > y1:
                return True
            if yn > y1:
                return True
        elif yc == y2:
            # bottom border
            if yp < y2:
                return True
            if yn < y2:
                return True

    # check that the inside is valid by checking the directions of the lines on the border
    for index in border_indices:

        next_index = (index + 1) % n
        prev_index = (index - 1) % n

        xc, yc = coords[index]
        xn, yn = coords[next_index]
        xp, yp = coords[prev_index]
        check_next = next_index in border_indices
        check_prev = prev_index in border_indices

        # we know that the "inside" (valid squares) is to the "right" of each edge
        # we check that property after the previous one

        if xc == x1:
            # left border
            if check_prev and xp == x1 and yp < yc:
                return True
            if check_next and xn == x1 and yc < yn:
                return True
        if xc == x2:
            # right border
            if check_prev and xp == x2 and yp > yc:
                return True
            if check_next and xn == x2 and yc > yn:
                return True
        if yc == y1:
            # top border
            if check_prev and yp == y1 and xp > xc:
                return True
            if check_next and yn == y1 and xc > xn:
                return True
        if yc == y2:
            # bottom border
            if check_prev and yp == y2 and xp < xc:
                return True
            if check_next and yn == y2 and xc < xn:
                return True

    return False


def find_largest_area(coords: list[tuple[int, int]]) -> int:

    max_area: int = 0
    max_coords: tuple[tuple[int, int], tuple[int, int]] | None = None

    for i_a, (x_a, y_a) in enumerate(coords):

        for i_b, (x_b, y_b) in enumerate(coords):

            # Part 2
            is_invalid = check_invalid_rectangle(i_a, x_a, y_a, i_b, x_b, y_b, coords)
            if is_invalid:
                continue

            curr_area = get_area(x_a, y_a, x_b, y_b)

            if curr_area > max_area:
                max_area = curr_area
                max_coords = ((x_a, y_a), (x_b, y_b))

    # print(max_coords)
    return max_area


def main():

    coords = read_datas()

    max_area = find_largest_area(coords)
    print(max_area)


main()
