import re


def import_robots(filename: str):

    with open(filename, mode="r", encoding="utf8") as file:
        text = file.read()

    positions: list[tuple[str, str]] = re.findall(r"p=(\d+),(\d+)", text)
    velocities: list[tuple[str, str]] = re.findall(r"v=(-?\d+),(-?\d+)", text)

    robots = [
        ((int(p_x), int(p_y)), (int(v_x), int(v_y)))
        for (p_x, p_y), (v_x, v_y) in zip(positions, velocities)
    ]

    return robots


def main(filename: str):

    robots = import_robots(filename)

    wide = 11 if filename == "input1" else 101
    tall = 7 if filename == "input1" else 103
    length = 100

    old_robots_coords = [robot[0] for robot in robots]
    robot_map = [
        [str(old_robots_coords.count((x, y)) or ".") for x in range(wide)]
        for y in range(tall)
    ]
    print(*map("".join, robot_map), sep="\n")
    print()

    # Part 1
    left_top_count = 0
    left_bot_count = 0
    right_top_count = 0
    right_bot_count = 0
    new_robots_coords: list[tuple[int, int]] = []
    for robot in robots:
        (p_x, p_y), (v_x, v_y) = robot

        new_x = (p_x + length * v_x) % wide
        new_y = (p_y + length * v_y) % tall
        new_robots_coords.append((new_x, new_y))

        if new_x > wide // 2 and new_y > tall // 2:
            right_bot_count += 1
        elif new_x > wide // 2 and new_y < tall // 2:
            right_top_count += 1
        elif new_x < wide // 2 and new_y > tall // 2:
            left_bot_count += 1
        elif new_x < wide // 2 and new_y < tall // 2:
            left_top_count += 1

    robot_map = [
        [str(new_robots_coords.count((x, y)) or ".") for x in range(wide)]
        for y in range(tall)
    ]
    print(*map("".join, robot_map), sep="\n")

    print(left_top_count, left_bot_count, right_top_count, right_bot_count)
    print(left_top_count * left_bot_count * right_top_count * right_bot_count)

    # Part 1
    with open("custom_output", mode="w", encoding="utf8") as output_file:
        for length in range(10_000):

            new_robots_coords = []
            for robot in robots:
                (p_x, p_y), (v_x, v_y) = robot

                new_x = (p_x + length * v_x) % wide
                new_y = (p_y + length * v_y) % tall
                new_robots_coords.append((new_x, new_y))

            robot_map = [
                [str(new_robots_coords.count((x, y)) or ".") for x in range(wide)]
                for y in range(tall)
            ]
            print(length, file=output_file)
            print(*map("".join, robot_map), sep="\n", file=output_file)
            print("\n", file=output_file)


if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    main(filename)
