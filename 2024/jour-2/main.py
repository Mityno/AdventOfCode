import sys

def import_reports(filename):
    with open(filename, mode="r", encoding="utf8") as file:
        reports = file.readlines()

    reports = map(str.strip, reports)
    reports = map(lambda line: line.split(" "), reports)
    reports = [list(map(int, report)) for report in reports]
    return reports


def check_subreports(report):
    print(report)
    for i in range(len(report)):
        new_report = report[: max(i - 1, -1) + 1] + report[i + 1 :]
        print(i, new_report)
        if check_report(new_report):
            return True

    return False


def check_report(report):
    if report not in (sorted(report), sorted(report, reverse=True)):
        return False

    increments = [abs(a - b) for a, b in zip(report, report[1:])]

    if min(increments) < 1 or max(increments) > 3:
        return False

    return True


def main(filename):
    reports = import_reports(filename)

    counter = 0

    for report in reports:
        counter += check_report(report) or check_subreports(report)

    print(counter)


if __name__ == "__main__":
    main(sys.argv[1])
