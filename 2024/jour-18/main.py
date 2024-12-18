def import_bytes(filename: str) -> list[tuple[int, int]]:

    limit = 1024 if filename == "input2" else 12

    incoming_bytes: list[tuple[int, int]] = list()
    with open(filename, mode="r", encoding="utf8") as file:
        for _, line in zip(range(limit), file):
            incoming_bytes.append(tuple(map(int, line.strip().split(","))))  # fmt: skip # pyright: ignore[reportArgumentType]
    return incoming_bytes


def main(filename: str):

    incoming_bytes = import_bytes(filename)
    print(incoming_bytes)


if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    main(filename)
