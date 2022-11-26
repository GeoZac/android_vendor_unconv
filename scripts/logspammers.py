#!/usr/bin/env python3

import collections
import re
import argparse

PATTERN = r"\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3}\s{1,}\d{1,}\s{1,}\d{1,}\s\w"
LOG_LEVELS = {
    "V": 5,
    "D": 4,
    "I": 3,
    "W": 2,
    "E": 1,
    "F": 0,
}


def logcat_spammers(args):
    with open(args.file, "r", errors="replace") as file_iput:
        lines = file_iput.readlines()
    domains = []
    evaded_regex = []
    for line in lines:
        matches = re.search(PATTERN, line)
        if matches:
            splits = line.split(matches[0][:-1])
            if args.T:
                domains.append(splits[1].split(":")[0])
            else:
                domains.append(splits[1])

        else:
            evaded_regex.append(line)
    ctr = collections.Counter(domains)
    most_com = ctr.most_common(100)
    if not most_com:
        return
    max_count = len(str(most_com[0][1]))
    for com, tim in most_com:
        if LOG_LEVELS[com[0]] > args.L:
            continue
        print(
            str(tim).rjust(max_count, " "),
            com.strip()
        )

    print("Evaded regex")
    for item in evaded_regex:
        print(item.strip())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("-L", type=int, default=6, help="Filter to log levels")
    parser.add_argument(
        "-T", action="store_true", default=False, help="Search just the tags"
    )
    argv = parser.parse_args()
    logcat_spammers(argv)
