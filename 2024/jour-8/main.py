import itertools


def import_map(filename):

    with open(filename, mode="r", encoding="utf8") as file:
        antenna_map = [list(line.strip()) for line in file]

    return antenna_map


def main(filename):
    antenna_map = import_map(filename)
    n = len(antenna_map)
    antenna_dico = {}

    for i, line in enumerate(antenna_map):
        for j, point in enumerate(line):

            if point != ".":
                antenna_dico.setdefault(point, [])
                antenna_dico[point].append((i, j))

    print(antenna_dico)
    antinodes_locations = set()

    for frequency, locations in antenna_dico.items():
        for a, b in itertools.combinations(locations, 2):
            x_a, y_a = a
            x_b, y_b = b

            vec_x, vec_y = x_a - x_b, y_a - y_b  # vector from b to a
            antinode_1_x, antinode_1_y = x_a + vec_x, y_a + vec_y
            antinode_2_x, antinode_2_y = x_b - vec_x, y_b - vec_y

            if 0 <= antinode_1_x <= n - 1 and 0 <= antinode_1_y <= n - 1:
                antinodes_locations.add((antinode_1_x, antinode_1_y))
            if 0 <= antinode_2_x <= n - 1 and 0 <= antinode_2_y <= n - 1:
                antinodes_locations.add((antinode_2_x, antinode_2_y))

    print(len(antinodes_locations))

    antinodes_locations = set()

    for frequency, locations in antenna_dico.items():
        for a, b in itertools.combinations(locations, 2):
            x_a, y_a = a
            x_b, y_b = b

            vec_x, vec_y = x_a - x_b, y_a - y_b  # vector from b to a
            for k in range(n):

                # k = 0 -> we add the antenna own location
                antinode_1_x, antinode_1_y = x_a + k * vec_x, y_a + k * vec_y
                antinode_2_x, antinode_2_y = x_b - k * vec_x, y_b - k * vec_y

                if 0 <= antinode_1_x <= n - 1 and 0 <= antinode_1_y <= n - 1:
                    antinodes_locations.add((antinode_1_x, antinode_1_y))
                if 0 <= antinode_2_x <= n - 1 and 0 <= antinode_2_y <= n - 1:
                    antinodes_locations.add((antinode_2_x, antinode_2_y))

    print(len(antinodes_locations))


if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    main(filename)
