def import_data(filename):

    with open(filename, mode="r", encoding="utf8") as file:

        rules = {}
        while line := file.readline().strip():
            page, before = map(int, line.split("|"))
            rules.setdefault(page, [])
            rules[page].append(before)

        updates = []
        for line in file:
            updates.append(list(map(int, line.strip().split(","))))

        return rules, updates


def main(filename):

    rules, updates = import_data(filename)
    print(updates)
    print(rules)

    # Part 1
    total_middles = 0
    for update in updates:

        # check ordering
        ordered = True
        for index, curr_page in enumerate(update):
            pages_after = rules.get(curr_page, None)
            if pages_after is None:
                continue

            if any(page_before in pages_after for page_before in update[:index]):
                # at least one page shouldn't be before curr_page
                ordered = False
                break

        if not ordered:
            continue

        middle = update[len(update) // 2]
        total_middles += middle
    print(total_middles)


    # Part 2
    total_middles = 0
    for update in updates:

        # check and fixe ordering
        was_ordered = True
        index = 0
        while index < len(update):
            curr_page = update[index]
            pages_after = rules.get(curr_page, None)
            if pages_after is None:
                index += 1
                continue

            ordered = False
            while not ordered:
                ordered = True
                for j, page_before in enumerate(update[:index]):
                    if page_before in pages_after:
                        ordered = False
                        was_ordered = False
                        # swap the two values to order them
                        update[j], update[index] = update[index], update[j]
                        index = j
                        break
            index += 1

        if was_ordered:
            continue

        # add middle
        middle = update[len(update) // 2]
        total_middles += middle
    print(total_middles)

if __name__ == "__main__":
    main("input2")
