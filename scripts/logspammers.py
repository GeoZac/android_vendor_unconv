import collections
import re
import sys

PATTERN = r"\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3}\s{2,}\d{1,}\s{1,}\d{1,}\s\w"


def logcat_spammers(args):
    with open(args[1], "r", errors='replace') as file_iput:
        lines = file_iput.readlines()
    domains = []
    for line in lines:
        matches = re.findall(PATTERN, line)
        if matches:
            splits = line.split(matches[0][:-1])
            domains.append(splits[1])

    ctr = collections.Counter(domains)
    most_com = ctr.most_common(100)
    max_count = len(str(most_com[0][1]))
    for com, tim in most_com:
        print(
            str(tim).rjust(max_count, " "),
            com.strip()
        )


if __name__ == "__main__":
    logcat_spammers(sys.argv)
