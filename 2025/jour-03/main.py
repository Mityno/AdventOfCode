import collections


def read_datas():
    n = int(input())
    banks = [input() for _ in range(n)]
    return banks


def find_largest_2digit(bank: str) -> int:

    if len(bank) <= 2:
        return int(bank)

    bank_length = len(bank)

    for curr_num in range(9, 0, -1):
        curr_num_str = str(curr_num)

        curr_num_index = bank.find(curr_num_str)

        if curr_num_index in (-1, bank_length - 1):
            continue

        second_largest = max(bank[curr_num_index + 1 :])

        return curr_num * 10 + int(second_largest)

    return -1


def find_largest_n_digit(bank: str, n: int) -> int:

    if len(bank) <= n:
        return int(bank)

    curr_digits: collections.deque[int] = collections.deque([])

    for new_digit in map(int, reversed(bank)):
        if len(curr_digits) < n:
            curr_digits.appendleft(new_digit)
            continue

        head_digit = curr_digits[0]

        if new_digit < head_digit:
            continue

        # we want to place the new digit near the head, but we need to make space for it
        # we will remove the smallest digit in the decreasing sequence starting from the head

        head, *tail_digits = curr_digits
        prev = head
        digit_to_remove = -1
        for digit in tail_digits:
            if digit < prev:
                # there is a smaller digit to remove
                digit_to_remove = digit
            elif digit > prev:
                # end of the decreasing sequence
                break
            prev = digit

        if digit_to_remove == -1:
            # we found no smaller digit than the head to remove, so we remove the head
            digit_to_remove = head_digit

        # remove the small digit
        curr_digits.remove(digit_to_remove)
        # add the new digit in the head
        curr_digits.appendleft(new_digit)

    return int("".join(map(str, curr_digits)))


def main():

    banks = read_datas()

    total_part_1 = 0
    total_part_2 = 0
    for bank in banks:
        # Part 1
        max_num = find_largest_n_digit(bank, 2)
        total_part_1 += max_num
        # Part 2
        max_num = find_largest_n_digit(bank, 12)
        total_part_2 += max_num
    print(total_part_1)
    print(total_part_2)


main()
