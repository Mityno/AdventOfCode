from collections.abc import Callable
import re
from typing import Any


def import_wires_gates(
    filename: str,
) -> tuple[dict[str, int], dict[str, tuple[str, str, str]]]:
    wires: dict[str, int] = {}
    gates: dict[str, tuple[str, str, str]] = {}
    with open(filename, mode="r", encoding="utf8") as file:
        for line in file:
            line = line.strip()
            if not line:
                break

            name, value = line.split(": ")
            wires[name] = int(value)

        for line in file:
            line = line.strip()
            wire_1: str
            wire_2: str
            result_wire: str
            operator: str
            wire_1, operator, wire_2, result_wire = re.findall(r"(\w+)", line)
            gates[result_wire] = (wire_1, operator, wire_2)

    return wires, gates


def binary_and(a: int, b: int):
    return a & b


def binary_or(a: int, b: int):
    return a | b


def binary_xor(a: int, b: int):
    return a ^ b


def add(a: int, b: int):
    return a + b


def get_parent(name: str, gates: dict[str, tuple[str, str, str]]) -> set[str]:
    # if name not in gates:
    if name.startswith("x") or name.startswith("y"):
        return set()

    parent_1, _, parent_2 = gates[name]
    parents = get_parent(parent_1, gates)
    parents.update(get_parent(parent_2, gates))
    parents.add(name)
    return parents


def create_gates_parents(gates: dict[str, tuple[str, str, str]]) -> dict[str, set[str]]:
    parents_dico: dict[str, set[str]] = {
        name: get_parent(name, gates) for name in gates.keys()
    }
    return parents_dico


def create_custom_wires(x: int, y: int) -> dict[str, int]:

    bin_x, bin_y = bin(x)[2:][::-1], bin(y)[2:][::-1]

    new_wires: dict[str, int] = {}
    for i in range(45):
        x_bit_value = int(bin_x[i]) if i < len(bin_x) else 0
        _ = new_wires.setdefault(f"x{i:02}", x_bit_value)

        y_bit_value = int(bin_y[i]) if i < len(bin_y) else 0
        _ = new_wires.setdefault(f"y{i:02}", y_bit_value)

    return new_wires


def compute_circuit(
    wires: dict[str, int], gates: dict[str, tuple[str, str, str]]
) -> dict[str, int]:

    while True:
        name_to_pop: list[str] = []
        for result_wire, operation in gates.items():
            wire_1, operator_name, wire_2 = operation
            if wires.get(wire_1, None) is None or wires.get(wire_2, None) is None:
                continue
            operator_function = OP_NAME_TO_FUNCTION[operator_name]
            wires[result_wire] = operator_function(wires[wire_1], wires[wire_2])
            name_to_pop.append(result_wire)

        for wire_name in name_to_pop:
            _ = gates.pop(wire_name)

        if not name_to_pop:
            break

    return wires


def check_up_to(
    max_n: int,
    gates: dict[str, tuple[str, str, str]],
    operation: Callable[[int, int], int],
) -> bool:
    # print("here", max_n)
    mask = max_n - 1
    max_n = min(max_n, 20)
    for curr_1 in range(max_n):
        for curr_2 in range(max_n):
            curr_wires = create_custom_wires(curr_1, curr_2)
            curr_wires = compute_circuit(curr_wires, gates.copy())
            z_value = get_wires_value(curr_wires, "z")
            if operation(curr_1, curr_2) & mask != z_value & mask:
                # print("here")
                return False
    return True


def check_nth_bit(
    wires: dict[str, int],
    gates: dict[str, tuple[str, str, str]],
    n: int,
    operation: Callable[[int, int], int],
) -> bool:
    low_check = check_up_to(int(2 ** (n + 1)), gates, operation)
    if not low_check:
        return False

    new_wires = create_custom_wires(int(2 ** (n + 1) - 1), int(2**n - 1))
    computed_wires = compute_circuit(new_wires, gates.copy())

    x_value = get_wires_value(computed_wires, "x")
    y_value = get_wires_value(computed_wires, "y")
    computed_z_value = get_wires_value(computed_wires, "z")
    computed_z_bin = bin(computed_z_value)[2:][::-1]

    real_z_value = operation(x_value, y_value)
    real_z_bin = bin(real_z_value)[2:][::-1]
    if n >= len(computed_z_bin) or len(real_z_bin) != len(computed_z_bin):
        return False
    return real_z_bin[n] == computed_z_bin[n]


def solve_swaps(
    wires: dict[str, int],
    gates: dict[str, tuple[str, str, str]],
    process_func: Callable[[int, int], int],
    depth: int,
):

    solution: list[str] = []
    counter = 0
    parents = create_gates_parents(gates)
    max_z = int(max(wires.keys())[1:])

    def inner(swapable: set[str], curr: int, depth: int) -> bool:
        nonlocal counter

        if curr > max_z and depth > 0:
            print("skipping")
            return False

        if depth == 0:
            counter += 1
            # x, y = 2**44 - 1, 2**43
            # new_wires = create_custom_wires(x, y)
            # computed_wires = compute_circuit(new_wires, gates.copy())
            # x_value = get_wires_value(computed_wires, "x")
            # y_value = get_wires_value(computed_wires, "y")
            # z_value = get_wires_value(computed_wires, "z")
            # print(x_value, y_value, "sum", x_value + y_value, "computed sum", z_value)
            # same = (x_value + y_value) == z_value
            # if same:
            #     print("here")

            print("checking")
            computed_wires = compute_circuit(wires.copy(), gates.copy())
            x_value = get_wires_value(computed_wires, "x")
            y_value = get_wires_value(computed_wires, "y")
            z_value = get_wires_value(computed_wires, "z")
            return process_func(x_value, y_value) == z_value

        if check_nth_bit(wires, gates, curr, process_func):
            print("skipping nth :", curr + 1)
            return inner(swapable, curr + 1, depth)

        lead_wires_seen: set[str] = set()
        untouchable_wires = set()
        for prec in range(curr):
            untouchable_wires |= parents[f"z{prec:02}"]

        if curr > 0:
            lead_wires = parents[f"z{curr:02}"] - untouchable_wires
        else:
            untouchable_wires: set[str] = set()
            lead_wires = parents[f"z{curr:02}"]
        lead_wires = lead_wires & swapable

        if lead_wires:
            print("here", curr, depth, lead_wires)

        for wire_a in lead_wires:
            lead_wires_seen.add(wire_a)
            for wire_b in swapable - untouchable_wires - lead_wires_seen:
                # counter += 1
                # print(counter, depth)
                dico_swap(gates, wire_a, wire_b)
                next_swapable = swapable - {wire_a, wire_b}

                if check_nth_bit(wires, gates, curr, process_func):
                    result = inner(next_swapable, curr + 1, depth - 1)

                    if result:
                        solution.append(wire_a)
                        solution.append(wire_b)
                        return True

                print(wire_a, wire_b, curr, depth, lead_wires_seen)

                # reset gates as they were
                dico_swap(gates, wire_a, wire_b)

        if lead_wires_seen:
            print("seen", lead_wires_seen)
        return False

    start_swapable = set(gates.keys())
    print(start_swapable)
    print("total wires", len(start_swapable))
    solution_exists = inner(start_swapable, 0, depth)

    print("counter", counter)

    if solution_exists:
        return solution
    else:
        raise ValueError("could not find a solution for given input")


def get_wires_value(wires: dict[str, int], startswith: str) -> int:
    names: list[str] = [name for name in wires.keys() if name.startswith(startswith)]
    names.sort(reverse=True)
    bin_str = "".join([str(wires[name]) for name in names])
    bin_num = int(bin_str, 2)
    return bin_num


def dico_swap(
    dico: dict[str, Any], key_1: str, key_2: str  # pyright: ignore[reportExplicitAny]
):
    dico[key_1], dico[key_2] = dico[key_2], dico[key_1]


def show_previouses(gates: dict[str, tuple[str, str, str]]):
    parents = create_gates_parents(gates)
    curr = 0
    seen: set[str] = set()
    while gates:
        seen.add(f"x{curr:02}")
        seen.add(f"y{curr:02}")
        curr_z_name = f"z{curr:02}"

        to_pop: list[str] = []
        for curr_name, (parent_1, op, parent_2) in gates.items():
            if (
                parent_1 in seen
                and parent_2 in seen
                and curr_name in parents[curr_z_name]
            ):
                print(parent_1, op, parent_2, "->", curr_name)
                seen.add(curr_name)
                to_pop.append(curr_name)

        for name in to_pop:
            _ = gates.pop(name)

        if not to_pop:
            curr += 1


def main(filename: str):

    wires, gates = import_wires_gates(filename)
    # print(wires)
    # print(gates)

    # Part 1
    computed_wires = compute_circuit(wires.copy(), gates.copy())
    # print(wires)

    z = get_wires_value(computed_wires, "z")
    # print(f"{z = }")

    # Part 2
    # x = get_wires_value(wires, "x")
    # y = get_wires_value(wires, "y")
    # print(f"{x = }, {y = }, {x + y = }")
    # diff = z - (x + y)
    # print("diff", diff, f"({diff/(x + y) * 100:.2f}%)")

    # custom_wires = create_custom_wires(0b101010, 0b010101)
    # print(custom_wires)
    # solution = solve_swaps(wires, gates, binary_and, 2)

    # custom_wires = create_custom_wires(2**44 - 1, 2**43)
    solution = solve_swaps(wires, gates, add, 4)
    print(solution)
    print(",".join(sorted(solution)))

    # show_previouses(gates.copy())


OP_NAME_TO_FUNCTION = {"AND": binary_and, "OR": binary_or, "XOR": binary_xor}

if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    main(filename)
