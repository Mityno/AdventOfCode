def read_datas():
    ranges: list[range] = []

    while True:
        curr_input = input()

        if curr_input == "":
            break

        start, end = map(int, curr_input.split("-"))
        ranges.append(range(start, end + 1))

    ids: list[int] = []

    while True:
        curr_input = input()

        if curr_input == "":
            break

        id = int(curr_input)
        ids.append(id)

    return ranges, ids


def count_fresh(ranges: list[range], ids: list[int]) -> int:

    fresh_counter = 0
    for id in ids:
        fresh_counter += any(id in range for range in ranges)
        # print(id, fresh_counter)

    return fresh_counter


def count_all_fresh_ids(ranges: list[range]) -> int:

    ids_bounds = [(range.start, range.stop) for range in ranges]

    changed = True
    indices_to_remove: set[int] = set()
    while changed:
        n = len(ids_bounds)
        indices_to_remove.clear()

        for i in range(n):
            curr_start, curr_end = ids_bounds[i]
            for j in range(i):
                other_start, other_end = ids_bounds[j]

                if curr_end < other_start or curr_start > other_end:
                    # the ranges are distinct
                    continue

                # there is an overlap, we will update the other range with the
                # merge result of the two ranges
                new_start = min(curr_start, other_start)
                new_end = max(curr_end, other_end)
                ids_bounds[j] = (new_start, new_end)
                # we will remove the curr range since it has been merged into other
                indices_to_remove.add(i)

                # we are finished with the curr range
                break

        changed = len(indices_to_remove) > 0
        ids_bounds = [ids_bounds[i] for i in range(n) if i not in indices_to_remove]

    total_number_of_ids = 0
    for start, end in ids_bounds:
        total_number_of_ids += end - start
    return total_number_of_ids


def main():

    ranges, ids = read_datas()

    # Part 1
    fresh_quantity = count_fresh(ranges, ids)
    print(fresh_quantity)

    # Part 2
    number_of_fresh_ids = count_all_fresh_ids(ranges)
    print(number_of_fresh_ids)


main()
