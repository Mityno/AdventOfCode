def import_secrets(filename: str) -> list[int]:
    with open(filename, mode="r", encoding="utf8") as file:
        data = file.read()
    secrets = list(map(int, map(str.strip, data.split())))
    return secrets


def next_secret(secret: int):
    secret = secret * 64 ^ secret
    secret %= 16777216
    secret = secret // 32 ^ secret
    secret %= 16777216
    secret = secret * 2048 ^ secret
    secret %= 16777216
    return secret


def find_best_seq(secrets: list[int]) -> tuple[int, int, int, int]:
    variations: list[tuple[tuple[int, int], ...]] = []
    for secret in secrets:
        curr_variation: list[tuple[int, int]] = []
        prev = secret % 10
        for _ in range(2_000):
            secret = next_secret(secret)
            secret_one_digit = secret % 10
            variation = secret_one_digit - prev
            prev = secret_one_digit
            curr_variation.append((variation, secret_one_digit))
        variations.append(tuple(curr_variation))

    dico_variations_to_secrets: dict[tuple[int, ...], dict[int, int]] = {}

    for variation_index, variation in enumerate(variations):
        for i in range(len(variation) - 4):
            curr_seq_data = tuple(variation[i : i + 4])
            seq_value = curr_seq_data[-1][1]
            curr_seq = tuple(var for var, _ in curr_seq_data)
            _ = dico_variations_to_secrets.setdefault(curr_seq, {}).setdefault(
                variation_index, seq_value
            )

    best_seq = max(
        dico_variations_to_secrets.keys(),
        key=lambda key: sum(dico_variations_to_secrets[key].values()),
    )
    print(best_seq)
    print(sum(dico_variations_to_secrets[best_seq].values()))


def main(filename: str):
    secrets = import_secrets(filename)

    total = 0
    for secret in secrets:
        for _ in range(2_000):
            secret = next_secret(secret)
        total += secret
    print("total", total)

    seq = find_best_seq(secrets)


if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    main(filename)
