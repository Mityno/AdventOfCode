import collections


def read_datas() -> dict[str, list[str]]:
    n = int(input())

    adjency_dict: dict[str, list[str]] = {}
    for _ in range(n):
        line = input()
        source, dsts = line.split(":")
        adjency_dict[source] = dsts.split()

    return adjency_dict


def bfs_count_paths(adjency_dict: dict[str, list[str]], start: str, goal: str) -> int:

    frontier = collections.deque([start])

    path_counter = 0
    while frontier:

        curr_node = frontier.popleft()

        if curr_node == goal:
            path_counter += 1
            continue

        for next_node in adjency_dict[curr_node]:
            frontier.append(next_node)

    return path_counter


def get_all_reachable_nodes(
    adjency_dict: dict[str, list[str]], start: str, goal: str
) -> set[str]:

    reached: set[str] = set()
    frontier = collections.deque([start])

    while frontier:

        curr_node = frontier.popleft()

        if curr_node == goal:
            continue

        for next_node in adjency_dict[curr_node]:
            if next_node in reached:
                continue
            frontier.append(next_node)
            reached.add(next_node)

    return reached


node_valid_t = tuple[str, tuple[bool, ...]]


def bfs_count_paths_with_constraints(
    adjency_dict: dict[str, list[str]], start: str, goal: str, *constraints: str
) -> int:

    n_constraints = len(constraints)
    empty_constraints = (False,) * n_constraints
    frontier: collections.deque[node_valid_t] = collections.deque(
        [(start, empty_constraints)]
    )

    lost_nodes: set[str] = set(adjency_dict.keys()) | {goal}
    for constraint in constraints:
        lost_nodes &= get_all_reachable_nodes(adjency_dict, constraint, "out")

    path_counter = 0

    node_path_counter: dict[node_valid_t, int] = {(start, empty_constraints): 1}

    while frontier:

        curr_node_with_info = curr_node, curr_valid = frontier.popleft()

        if curr_node in lost_nodes and not all(curr_valid):
            continue

        if curr_node == goal:
            # the state is valid because we pruned the invalid path before
            path_counter += node_path_counter[curr_node_with_info]
            continue

        updated_valid = tuple(
            old_valid or curr_node == constraint_node
            for old_valid, constraint_node in zip(curr_valid, constraints)
        )

        for next_node in adjency_dict[curr_node]:
            next_node_with_info = (next_node, updated_valid)

            if next_node_with_info in frontier:
                # add the path counter for its next expansion
                _ = node_path_counter.setdefault(next_node_with_info, 0)
                node_path_counter[next_node_with_info] += node_path_counter[
                    curr_node_with_info
                ]
                continue
            else:
                # reset the counter and add the current path count
                node_path_counter[next_node_with_info] = node_path_counter[
                    curr_node_with_info
                ]

            frontier.append(next_node_with_info)

    return path_counter


def main():

    adjency_dict = read_datas()

    # Part 1
    number_of_paths = bfs_count_paths(adjency_dict, "you", "out")
    print(number_of_paths)

    # Part 2
    number_of_paths = bfs_count_paths_with_constraints(
        adjency_dict, "svr", "out", "dac", "fft"
    )
    print(number_of_paths)


main()
