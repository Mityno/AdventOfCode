from ast import literal_eval
import sympy
import numpy


def read_datas():

    n = int(input())
    raw_machines = [input() for _ in range(n)]

    return raw_machines


def parse_machine(machine):

    parts = machine.split(" ")

    indicator_lights = parts[0].strip("[]")
    buttons = list(map(lambda s: literal_eval(s.replace(")", ",)")), parts[1:-1]))
    joltages = list(map(int, parts[-1].strip("{}").split(",")))

    return indicator_lights, buttons, joltages


def heuristic(state, end):
    # return 0
    return max(
        end[index] - state[index] if end[index] >= state[index] else float("inf")
        for index in range(len(state))
    )


def get_next_node(state, action):
    if isinstance(state[0], bool):
        return tuple(
            not value if index in action else value for index, value in enumerate(state)
        )
    else:
        return tuple(value + (index in action) for index, value in enumerate(state))


def update_node(
    next_node,
    curr_node,
    distances,
    prev,
):

    if distances[curr_node] + 1 < distances.get(next_node, float("inf")):
        distances[next_node] = distances[curr_node] + 1
        prev[next_node] = curr_node
        return True
    return False


def a_star(state, actions, end):

    distances = {state: 0}
    prev = {}
    frontier = {state}
    while frontier:
        curr_node = min(
            frontier, key=lambda state: distances[state] + heuristic(state, end)
        )

        if curr_node == end:
            break

        frontier.discard(curr_node)

        for action in actions:
            next_node = get_next_node(curr_node, action)
            is_updated = update_node(next_node, curr_node, distances, prev)
            if is_updated:
                frontier.add(next_node)

    return distances[end]


def fewest_light_buttons(lights, buttons):

    bin_lights = tuple(char == "#" for char in lights)
    # print(lights, list(map(int, bin_lights)))

    goal_lights = (False,) * len(bin_lights)
    button_presses = a_star(bin_lights, buttons, goal_lights)

    return button_presses


def get_buttons_matrix(buttons, n_joltages):

    matrix = numpy.zeros((n_joltages, len(buttons)), dtype=int)
    for column, button in enumerate(buttons):
        for line in button:
            matrix[line, column] = 1

    return matrix


def fewest_joltage_buttons(joltages, buttons):

    n_buttons = len(buttons)
    goal_joltages = tuple(joltages)
    start_joltages = (0,) * len(joltages)
    # button_presses = a_star(start_joltages, buttons, goal_joltages)

    matrix = get_buttons_matrix(buttons, len(joltages))
    # print(matrix)

    # variables = sympy.symbols(
    #     " ".join(chr(index + ord("a")) for index in range(n_buttons))
    # )
    # space = {var: sympy.Naturals0 for var in variables}
    # print(space)
    # for line_index, line in enumerate(matrix):
    #     left_side = sum(line * variables)
    #     reference_variable = left_side.args[0]
    #     print(left_side.args)
    #     equation = sympy.Eq(left_side, joltages[line_index])
    #     solution_set = sympy.solveset(
    #         equation, reference_variable, domain=sympy.Naturals0
    #     )
    #     restricted_set = space[reference_variable].intersect(solution_set)
    #     space[reference_variable] = restricted_set
    #     print(space)

    A = sympy.Matrix(matrix)
    b = sympy.Matrix(joltages)
    # print(A)
    # print(b, sympy.shape(b))
    X = sympy.linsolve((A, b))
    # X: FiniteSet = sympy.solveset((A, b), domain=sympy.Naturals0)
    # print(X)
    sum_X = sum(X.args[0])
    args = sum_X.args
    # print(X.args, sum(X.args[0]), args)
    if args:
        constant = args[0]
    else:
        constant = sum_X

    gcd = sum_X.primitive()[0]
    if any(int(value.primitive()[0]) != value.primitive()[0] for value in X.args[0]):
        print(joltages)
        print(buttons)
        # print(X)
        # print(next(iter(X.intersect(sympy.Naturals0**n_buttons))))
        # print(X.args)
        # print(sum_X, sum_X.primitive())
        # print(args)
        # print()
        return a_star(start_joltages, buttons, goal_joltages)

    return constant


def main():

    raw_machines = read_datas()

    total_presses = 0
    for lights, buttons, joltages in map(parse_machine, raw_machines):
        # # Part 1
        # button_presses = fewest_light_buttons(lights, buttons)

        # Part 2
        button_presses = fewest_joltage_buttons(joltages, buttons)

        total_presses += button_presses

    print(total_presses)


main()
