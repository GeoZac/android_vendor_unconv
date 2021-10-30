from sys import argv
from glob import glob
from os import getcwd, path
from os.path import basename

# TODO Switch to logging module
DEBUG = False
VENDOR_LESS = True


# In that case, the final value is determined at runtime. The precedence is
#
#     product
#     odm
#     vendor
#     system_ext
#     system
#
# So, foo becomes true because vendor has higher priority than system.


def combine_prop_keys(combined_props, props_to_combine, partition):
    combined_prop_keys = [props[0] for props in combined_props]
    for dump_systemext_prop in props_to_combine:
        if dump_systemext_prop[0] not in combined_prop_keys:
            combined_props.append(dump_systemext_prop)
        else:
            print(f"Overridden prop in {partition}:", dump_systemext_prop[0])
    if DEBUG:
        print(len(combined_props), f"props after {partition}")

    return combined_props


def read_prop_file(prop_file, dump=False, footer=None):
    props = []
    with open(prop_file, mode="r") as in_prop:
        raw_props = in_prop.read().splitlines()

    skip = dump
    for raw_prop in raw_props:
        if raw_prop == footer and dump:
            skip = False

        if raw_prop.startswith("#") or skip:
            continue
        try:
            key, value = raw_prop.split("=")
            props.append([key, value])
        except ValueError:
            if DEBUG:
                print("ValueError", raw_prop)
            continue
    return props


def read_props_from_dump(dump_prop_files):
    dump_system_props = []
    dump_systemext_props = []
    dump_vendor_props = []
    dump_odm_props = []
    dump_product_props = []
    for dump_prop_file in dump_prop_files:
        head = path.split(dump_prop_file)[0]
        if basename(head) == "system":
            print("Found build.prop in system")
            dump_system_props = read_prop_file(
                dump_prop_file, True, "# end build properties"
            )
        elif basename(head) == "system_ext":
            print("Found build.prop in system_ext")
            dump_systemext_props = read_prop_file(
                dump_prop_file, True, "# end common build properties"
            )
        elif basename(head) == "vendor":
            print("Found build.prop in vendor")
            dump_vendor_props = read_prop_file(
                dump_prop_file, True, "# end common build properties"
            )
        elif "odm\\etc" in head:
            print("Found build.prop in odm")
            dump_odm_props = read_prop_file(
                dump_prop_file, True, "# end common build properties"
            )
        elif basename(head) == "product":
            print("Found build.prop in product")
            dump_product_props = read_prop_file(
                dump_prop_file, True, "# end common build properties"
            )
    return (
        dump_system_props,
        dump_systemext_props,
        dump_vendor_props,
        dump_odm_props,
        dump_product_props,
    )


def read_props_from_tree(tree_prop_files):
    tree_system_props = []
    tree_systemext_props = []
    tree_vendor_props = []
    tree_odm_props = []
    tree_product_props = []
    for tree_prop_file in tree_prop_files:
        if basename(tree_prop_file) == "system.prop":
            print("Found system.prop")
            tree_system_props = read_prop_file(tree_prop_file)
        elif basename(tree_prop_file) == "system_ext.prop":
            print("Found system_ext.prop")
            tree_systemext_props = read_prop_file(tree_prop_file)
        elif basename(tree_prop_file) == "vendor.prop":
            tree_vendor_props = read_prop_file(tree_prop_file)
        elif basename(tree_prop_file) == "odm.prop":
            tree_odm_props = read_prop_file(tree_prop_file)
        elif basename(tree_prop_file) == "product.prop":
            print("Found product.prop")
            tree_product_props = read_prop_file(tree_prop_file)
        else:
            print("Non-stand prop found", tree_prop_file)
    return (
        tree_system_props,
        tree_systemext_props,
        tree_vendor_props,
        tree_odm_props,
        tree_product_props,
    )


def collect_props_from_dump(props_dir):
    print("Collecting props from dump")
    dump_prop_files = glob(props_dir + "/**/build.prop", recursive=True)

    (
        dump_system_props,
        dump_systemext_props,
        dump_vendor_props,
        dump_odm_props,
        dump_product_props,
    ) = read_props_from_dump(dump_prop_files)

    dump_combined_props = [item for item in dump_system_props]
    if DEBUG:
        print(len(dump_combined_props), "props in system")

    dump_combined_props = combine_prop_keys(dump_combined_props, dump_systemext_props, "system_ext")

    dump_combined_props = combine_prop_keys(dump_combined_props, dump_vendor_props, "vendor")

    dump_combined_props = combine_prop_keys(dump_combined_props, dump_odm_props, "odm")

    combine_prop_keys(dump_combined_props, dump_product_props, "product")

    return [
        dump_system_props,
        dump_systemext_props,
        dump_vendor_props,
        dump_odm_props,
        dump_product_props,
    ]


def collect_props_from_tree(props_dir):
    print("Collecting props from tree")
    tree_prop_files = glob(props_dir + "*.prop", recursive=False)

    (
        tree_system_props,
        tree_systemext_props,
        tree_vendor_props,
        tree_odm_props,
        tree_product_props,
    ) = read_props_from_tree(tree_prop_files)

    tree_combined_props = [item for item in tree_system_props]
    if DEBUG:
        print(len(tree_combined_props), "props in system")

    tree_combined_props = combine_prop_keys(tree_combined_props, tree_systemext_props, "system_ext")

    tree_combined_props = combine_prop_keys(tree_combined_props, tree_vendor_props, "vendor")

    tree_combined_props = combine_prop_keys(tree_combined_props, tree_odm_props, "odm")

    combine_prop_keys(tree_combined_props, tree_product_props, "product")

    return [
        tree_system_props,
        tree_systemext_props,
        tree_vendor_props,
        tree_odm_props,
        tree_product_props,
    ]


def divvy_props():
    partitions = {
        0: "system",
        1: "system_ext",
        2: "vendor",
        3: "odm",
        4: "product",
    }
    
    tree_dir = getcwd() + "\\" + argv[1]
    dump_dir = getcwd() + "\\" + argv[2]

    dump_props = collect_props_from_dump(dump_dir)
    tree_props = collect_props_from_tree(tree_dir)

    for i in range(0, len(partitions)):
        if not dump_props[i]:
            continue

        if not tree_props[i]:
            if VENDOR_LESS:
                print("Pulled stock props from ", partitions[i])
                tree_props[i] = dump_props[i]
            if not VENDOR_LESS:
                print("No", partitions[i], "prop file in tree")
                for prop, value in dump_props[i]:
                    print("Manually resolve", prop, value)
                continue
        dump_prop_keys = [prop[0] for prop in dump_props[i]]
        tree_prop_keys = [prop[0] for prop in tree_props[i]]

        for dump_prop_key in dump_prop_keys:
            if not any(item in dump_prop_key for item in tree_prop_keys):
                print("Need to add to", partitions[i], ":", dump_prop_key)


if __name__ == "__main__":
    divvy_props()
