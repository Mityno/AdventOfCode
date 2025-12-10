from ast import literal_eval


def read_datas() -> list[str]:

    n = int(input())
    raw_machines = [input() for _ in range(n)]

    return raw_machines


def parse_machine(machine: str) -> tuple[str, list[tuple[int, ...]], list[int]]:

    parts = machine.split(" ")

    indicator_lights = parts[0].strip("[]")
    buttons: list[tuple[int, ...]] = list(
        map(lambda s: literal_eval(s.replace(")", ",)")), parts[1:-1])
    )
    joltages = list(map(int, parts[-1].strip("{}").split(",")))

    return indicator_lights, buttons, joltages


def get_score(lights: list[bool], button: tuple[int, ...]) -> int:
    return sum(lights[light_index] for light_index in button)


def press_button(lights: list[bool], button: tuple[int, ...]):
    for light_index in button:
        lights[light_index] = not lights[light_index]


def fewest_buttons(lights: str, buttons: list[tuple[int, ...]]) -> int:

    bin_lights = tuple(char == "#" for char in lights)
    # print(lights, list(map(int, bin_lights)))

    button_presses = a_star(bin_lights, buttons)

    return button_presses


node_type = tuple[bool, ...]


def not_goal(state: node_type):
    return bool(sum(state))


def heuristic(state: node_type):
    return 0
    return sum(state)


def get_next_node(state: node_type, action: tuple[int, ...]) -> node_type:
    return tuple(
        not value if index in action else value for index, value in enumerate(state)
    )


def update_node(
    next_node: node_type,
    curr_node: node_type,
    distances: dict[node_type, int],
    prev: dict[node_type, node_type],
) -> bool:

    if distances[curr_node] + 1 < distances.get(next_node, float("inf")):
        distances[next_node] = distances[curr_node] + 1
        prev[next_node] = curr_node
        return True
    return False


def a_star(state: node_type, actions: list[tuple[int, ...]]) -> int:

    end = (False,) * len(state)
    distances: dict[node_type, int] = {state: 0}
    prev: dict[node_type, node_type] = {}
    frontier = {state}
    while frontier:
        curr_node = min(frontier, key=lambda state: distances[state] + heuristic(state))

        if curr_node == end:
            break

        frontier.discard(curr_node)

        for action in actions:
            next_node = get_next_node(curr_node, action)
            is_updated = update_node(next_node, curr_node, distances, prev)
            if is_updated:
                frontier.add(next_node)

    return distances[end]


def main():

    raw_machines = read_datas()

    total_presses = 0
    for lights, buttons, joltages in map(parse_machine, raw_machines):
        # print(lights, buttons, joltages)
        button_presses = fewest_buttons(lights, buttons)
        total_presses += button_presses

    print(total_presses)


main()
