import functools


def import_links(filename: str) -> list[tuple[str, ...]]:
    links: list[tuple[str, ...]] = []
    with open(filename, mode="r", encoding="utf8") as file:
        for line in file:
            links.append(tuple(line.strip().split("-")))
    return links


def create_links_dict(links: list[tuple[str, ...]]) -> dict[str, list[str]]:

    dico_links: dict[str, list[str]] = {}
    for link in links:
        a, b = link
        dico_links.setdefault(a, []).append(b)
        dico_links.setdefault(b, []).append(a)
    return dico_links


def check_connected_to_group(
    name: str, group: list[str], dico_links: dict[str, list[str]]
) -> bool:
    return all(name in dico_links[member_name] for member_name in group)


def create_groups_of_three(dico_links: dict[str, list[str]]) -> list[tuple[str, ...]]:

    groups: list[tuple[str, ...]] = []

    def inner(curr_name: str, curr_group: list[str]):
        if len(curr_group) == 3:
            sorted_curr_group = tuple(sorted(curr_group))
            if sorted_curr_group not in groups:
                groups.append(sorted_curr_group)
            return

        for connected in dico_links[curr_name]:
            if connected in curr_group:
                continue

            if not check_connected_to_group(connected, curr_group, dico_links):
                continue

            curr_group.append(connected)
            inner(connected, curr_group)
            _ = curr_group.pop()

    for name in dico_links.keys():
        if name.startswith("t"):
            inner(name, [name])
    return groups


def find_largest_group(dico_links: dict[str, list[str]]) -> tuple[str, ...]:

    max_size = 0
    max_group: tuple[str, ...] = None  # pyright: ignore[reportAssignmentType]

    set_dico_links: dict[str, frozenset[str]] = {}
    for key in dico_links:
        set_dico_links[key] = frozenset(dico_links[key])

    @functools.cache
    def inner(curr_group: frozenset[str], possible_names: frozenset[str]):
        nonlocal max_size, max_group

        if not possible_names:
            if len(curr_group) > max_size:
                max_size = len(curr_group)
                max_group = tuple(curr_group)
            return

        for connected in possible_names:
            inner(curr_group | {connected}, possible_names & set_dico_links[connected])

    for name in dico_links.keys():
        inner(frozenset((name,)), set_dico_links[name])

    return max_group


def main(filename: str):
    links = import_links(filename)
    dico_links = create_links_dict(links)
    # print(*dico_links.items(), sep="\n")

    # Part 1
    groups = create_groups_of_three(dico_links)
    # print(groups)
    print(len(groups))

    # Part 2
    max_group = find_largest_group(dico_links)
    print(max_group)
    print(",".join(sorted(max_group)))


if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    main(filename)
