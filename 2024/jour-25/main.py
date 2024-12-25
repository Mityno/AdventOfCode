def import_locks_keys(filename: str) -> tuple[list[tuple[int, ...]], ...]:

    locks_str: list[tuple[str, ...]] = []
    keys_str: list[tuple[str, ...]] = []
    curr_str: list[str] = []
    curr_type = None
    with open(filename, mode="r", encoding="utf8") as file:
        for line in file:
            line = line.strip()
            if not line:
                if curr_type == "key":
                    keys_str.append(tuple(curr_str))
                elif curr_type == "lock":
                    locks_str.append(tuple(curr_str))

                curr_str = []
                curr_type = None
                continue

            curr_str.append(line)
            if curr_type is None:
                curr_type = "lock" if line.count("#") == len(line) else "key"

        if curr_str:
            if curr_type == "key":
                keys_str.append(tuple(curr_str))
            elif curr_type == "lock":
                locks_str.append(tuple(curr_str))

    locks: list[tuple[int, ...]] = []
    for lock_str in locks_str:
        curr: list[int] = [0] * len(lock_str[0])
        for column in range(len(lock_str[0])):
            for height in range(len(lock_str)):
                if lock_str[height][column] == "." and curr[column] == 0:
                    curr[column] = height - 1
                    break
        locks.append(tuple(curr))

    keys: list[tuple[int, ...]] = []
    for key_str in keys_str:
        curr = [0] * len(key_str[0])
        for column in range(len(key_str[0])):
            for height in range(len(key_str)):
                if key_str[height][column] == "#" and curr[column] == 0:
                    curr[column] = len(key_str) - height - 1
                    break
        keys.append(tuple(curr))

    return locks, keys


def count_keys_locks(locks: list[tuple[int, ...]], keys: list[tuple[int, ...]]) -> int:
    counter = 0
    for lock in locks:
        for key in keys:
            if all(lock[i] + key[i] <= 5 for i in range(len(lock))):
                counter += 1
    return counter


def main(filename: str):

    locks, keys = import_locks_keys(filename)
    # print(locks)
    # print(keys)

    print(count_keys_locks(locks, keys))


if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    main(filename)
