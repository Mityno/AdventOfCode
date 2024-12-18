# 0 5 43 346 2770 22163 177309 1418475 11347807 90782456 726259649 5810077193 46480617544

# goals = [2, 4, 1, 2, 7, 5, 4, 3, 0, 3, 1, 7, 5, 5, 3, 0]
goals = [0, 3, 5, 4, 3, 0]


solutions: list[int] = []


def solve(curr: int, goals: list[int]):
    if not goals:
        solutions.append(curr)
        print("Finished, solution :", curr)
        return

    curr_goal = goals[-1]

    for i in range(curr * 8, (curr + 1) * 8):
        b = (i % 8) ^ 2
        c = int(i / (2**b))
        result = (b ^ c ^ 7) % 8
        if result == curr_goal:
            solve(i, goals[:-1])


solve(0, goals)
print(solutions)
print(min(solutions))
print(8**15, 8**16 - 1)
