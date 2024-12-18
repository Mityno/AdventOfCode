def import_program(filename: str) -> tuple[int, int, int, list[int]]:

    with open(filename, mode="r", encoding="utf8") as file:
        a = int(file.readline().strip())
        b = int(file.readline().strip())
        c = int(file.readline().strip())

        program = list(map(int, file.readline().strip().split(",")))

    return a, b, c, program


def get_combo_value(a: int, b: int, c: int, opcombo: int) -> int:
    if 0 <= opcombo <= 3 or opcombo == 7:
        return opcombo
    elif 4 <= opcombo <= 6:
        return (a, b, c)[opcombo - 4]
    else:
        raise ValueError(f"received {opcombo = !r}, illegal value")


def eval_operation(
    a: int, b: int, c: int, opcode: int, opcombo: int
) -> tuple[int, int, int, None | int]:

    value = get_combo_value(a, b, c, opcombo)

    match opcode:
        case 0:  # adv
            numerator = a
            denominator = 2**value
            return int(numerator // denominator), b, c, None
        case 1:  # bxl
            return a, b ^ opcombo, c, None
        case 2:  # bst
            return a, value % 8, c, None
        case 3:  # jnz
            if a == 0:
                return a, b, c, None
            return a, b, c, opcombo
        case 4:  # bxc
            return a, b ^ c, c, None
        case 5:  # out
            return a, b, c, value % 8
        case 6:  # bdv
            numerator = a
            denominator: int = 2**value
            return a, int(numerator // denominator), c, None
        case 7:  # cdv
            numerator = a
            denominator = 2**value
            return a, b, int(numerator // denominator), None
        case _:
            pass

    raise ValueError(f"invalid opcode : {opcode!r}")


def main(filename: str):

    a, b, c, program = import_program(filename)
    n = len(program)
    assert n % 2 == 0

    pointer = 0
    output: list[int] = []

    while pointer < n:
        print("Before")
        print("A", a)
        print("B", b)
        print("C", c)
        print("pointer", pointer)
        print("output", output)

        opcode = program[pointer]
        opcombo = program[pointer + 1]

        print(f"{opcode = } {opcombo = }")
        # breakpoint()
        a, b, c, special = eval_operation(a, b, c, opcode, opcombo)

        if special is not None:
            if opcode == 3:  # jnz
                pointer = special
                continue
            elif opcode == 5:  # out
                output.append(special)
            else:
                raise ValueError(
                    f"unexpected special return for opcode {opcode!r} : {special = !r}"
                )

        pointer += 2
        print("Before")
        print("A", a)
        print("B", b)
        print("C", c)
        print("pointer", pointer)
        print("output", output)
        # breakpoint()

    print("A", a)
    print("B", b)
    print("C", c)
    print("output", ",".join(map(str, output)))

    # Part 2

    breakpoint()
    import math
    curr = 35184372088832
    while output != program:

        if math.log10(curr).is_integer():
            print(curr)

        _, b, c, program = import_program(filename)
        a = curr
        n = len(program)
        pointer = 0
        output: list[int] = []

        while pointer < n and output == program[:len(output)]:
            opcode = program[pointer]
            opcombo = program[pointer + 1]
            a, b, c, special = eval_operation(a, b, c, opcode, opcombo)

            if special is not None:
                if opcode == 3:  # jnz
                    pointer = special
                    continue
                elif opcode == 5:  # out
                    output.append(special)
                else:
                    raise ValueError(
                        f"unexpected special return for opcode {opcode!r} : {special = !r}"
                    )

            pointer += 2

        curr += 1
    print(curr - 1)


if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    main(filename)
