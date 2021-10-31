# Copyright (C) 2019 baalajimaestro
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# Save all denials line by line to denials.txt in the same folder as code
# Fixes are saved to fixes.txt

from re import search
from sys import argv

skip_contexts = [
    "gmscore_app",
    "untrusted_app",
    "vendor_install_recovery"
]


def write_policy():
    fixes = []

    with open(argv[1], "r", encoding="utf8") as den_file:
        denials = den_file.readlines()

    for denial in denials:
        if "avc: denied" not in denial:
            continue

        test = search("{", denial)
        test2 = search("}", denial)
        se_context = denial[test.span()[0]:test2.span()[0] + 1]
        test = search("scontext", denial)
        scontext = denial[(test.span()[0]):].split(":")[2]
        if scontext in skip_contexts:
            continue
        test = search("tcontext", denial)
        tcontext = denial[(test.span()[0]):].split(":")[2]
        test = search("tclass", denial)
        tclass = denial[(test.span()[0]):].split("=")[1].split(" ")[0]
        fix = f"allow {scontext} {tcontext}:{tclass} {se_context};\n"
        if fix not in fixes:
            fixes.append(fix)

    # Get it sorted so i can make macros out of it
    fixes.sort()

    with open("fixes.txt", "w") as fix_file:
        fix_file.writelines(fixes)


if __name__ == "__main__":
    write_policy()
