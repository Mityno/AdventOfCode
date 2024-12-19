import functools


def import_patterns_designs(filename: str) -> tuple[list[str], list[str]]:

    with open(filename, mode="r", encoding="utf8") as file:
        patterns = file.readline().strip().replace(",", "").split()
        _ = file.readline()
        designs = file.read().strip().split()
    return patterns, designs


@functools.cache
def design_is_possible(design: str, patterns: tuple[str]) -> int:
    if not design:
        return 1

    possible_ways = 0
    for pattern in patterns:
        n = len(pattern)
        if design[:n] == pattern:
            possible_ways += design_is_possible(design[n:], patterns)
            # if possible:
            #     return True

    return possible_ways


def main(filename: str):

    patterns, designs = import_patterns_designs(filename)
    print(patterns)
    print(designs)

    patterns = tuple(patterns)
    possible_counter = 0
    total_counter = 0
    for i, design in enumerate(designs):
        print(i)
        ways = design_is_possible(design, patterns)
        total_counter += ways
        if ways:
            possible_counter += 1
    print(possible_counter)
    print(total_counter)


if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    main(filename)
