from os.path import join
import sys


def replace_with_wildcards(args):
    new = []
    spam_domains = [
        ".302br.net",
        ".207.net",
        ".doubleclick.net",
    ]

    if len(args) == 2:
        input_file_path = args[0]
        output_file_path = args[1]

    else:
        raise ValueError("Wrong number of arguments %s" % len(args))

    with open(input_file_path, "r") as fip:
        new = fip.readlines()
        print("Initial size: ", len(new))

    with open(join(output_file_path, "hosts_unconv_w"), "w") as fop:
        i = 0
        for redirect in new:
            if any(item in redirect for item in spam_domains):
                continue
            fop.write(redirect)
            i += 1
        for domains in spam_domains:
            fop.write(f"0.0.0.0 *{domains}\n")
            i += 1
    print("Final   size: ", i)


if __name__ == "__main__":
    replace_with_wildcards(sys.argv[1:])
