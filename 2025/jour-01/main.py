from math import dist


def read_datas():
    n = int(input())
    moves = [input() for _ in range(n)]
    return moves


def count_zeros(moves: list[str]) -> int:

    position = 50
    num_zeros = 0

    for move in moves:
        letter = move[0]
        distance = int(move[1:])
        direction = 1 if letter == "R" else -1

        old_position = position
        new_position = position + direction * distance
        position = new_position % 100
        # Part 1
        # num_zeros += position == 0
        # Part 2
        num_zeros += (
            abs(new_position // 100)
            - (new_position < 0 and old_position == 0 and position != 0)
            + (new_position == 0 and old_position != 0)
        )

    return num_zeros


def count_zeros_slow(moves: list[str]) -> int:
    position = 50
    num_zeros = 0

    for move in moves:
        letter = move[0]
        distance = int(move[1:])
        direction = 1 if letter == "R" else -1

        for _ in range(distance):
            position = (position + direction) % 100
            num_zeros += position == 0

    return num_zeros


def main():

    moves = read_datas()
    num_zeros = count_zeros(moves)
    print(num_zeros)


main()
