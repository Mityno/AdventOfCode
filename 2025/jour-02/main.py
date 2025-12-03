def read_datas() -> list[tuple[int, int]]:
    range_limits = input().split(",")
    ranges: list[tuple[int, int]] = [
        tuple(map(int, limits.split("-"))) for limits in range_limits
    ]  # pyright: ignore[reportAssignmentType]
    return ranges


def solve(ranges: list[tuple[int, int]]) -> int:

    sum_of_invalids = 0

    for limits in ranges:
        start, end = limits
        for num in range(start, end + 1):
            num_str = str(num)
            n = len(num_str)

            is_invalid = False
            for divisor in range(2, n + 1):
                if n % divisor != 0:
                    # there cannot be a pattern with this divisor
                    continue

                step = n // divisor
                reference_str = num_str[:step]
                is_invalid = True
                for i in range(1, divisor):
                    if num_str[i * step : (i + 1) * step] != reference_str:
                        # there cannot be a pattern with this divisor
                        is_invalid = False
                        break

                if is_invalid:
                    # we found a repeating pattern
                    break

            if is_invalid:
                sum_of_invalids += num

    return sum_of_invalids


def main():

    ranges = read_datas()

    sum_of_invalids = solve(ranges)
    print(sum_of_invalids)


main()
