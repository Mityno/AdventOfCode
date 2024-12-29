import re


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
            wire_1, operator, wire_2, result_wire = re.findall(r"(\w+)", line)
            gates[result_wire] = (wire_1, operator, wire_2)

    return wires, gates


def binary_and(a: int, b: int):
    return a & b


def binary_or(a: int, b: int):
    return a | b


def binary_xor(a: int, b: int):
    return a ^ b


def compute_circuit(
    wires: dict[str, int], gates: dict[str, tuple[str, str, str]]
) -> dict[str, int]:

    while gates:
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

    return wires


def main(filename: str):

    wires, gates = import_wires_gates(filename)
    print(wires)
    print(gates)

    _ = compute_circuit(wires, gates)
    print(wires)

    z_names: list[str] = [name for name in wires.keys() if name.startswith("z")]
    z_names.sort(reverse=True)
    bin_str = "".join([str(wires[z_name]) for z_name in z_names])
    bin_num = int(bin_str, 2)
    print(bin_num)


OP_NAME_TO_FUNCTION = {"AND": binary_and, "OR": binary_or, "XOR": binary_xor}

if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    main(filename)
