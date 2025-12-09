from matplotlib import pyplot as plt


def read_datas() -> list[tuple[int, int]]:

    n = int(input())
    coords: list[tuple[int, int]] = [
        tuple(map(int, input().split(","))) for _ in range(n)
    ]  # pyright: ignore[reportAssignmentType]
    return coords


coords = read_datas()
xs, ys = zip(*coords)

# _ = plt.scatter(xs, ys)
_ = plt.fill(xs, ys)
plt.gca().set_aspect("equal")
# plt.savefig("out.png")
plt.show()
