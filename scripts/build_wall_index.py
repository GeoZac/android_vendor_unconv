#!/usr/bin/env python3

import re
import sys
from json import dumps
from os import getenv
from os.path import realpath, dirname, join
from random import randint
from sys import argv

from requests import get, patch


def push_gist(gist_cn):
    gist_tn = getenv("GH_GIST_TOKEN")
    gist_fn = "wall_index.json"
    gist_id = "e4c7f3c3c451b859c7c70e43837e08c2"

    headers = {"Authorization": f"token {gist_tn}"}
    g_response = patch(
        f"https://api.github.com/gists/{gist_id}",
        data=dumps({"files": {gist_fn: {"content": gist_cn}}}),
        headers=headers,
    )
    if g_response.status_code != 200:
        print(f"GitHub API call failed with {g_response.status_code}")
        return None
    return g_response.json()["files"][gist_fn]["raw_url"]


def make_unsplash_api_call(page_no):
    u_api_url = f"https://api.unsplash.com/search/photos?page={page_no}"
    params = {
        "query": "wallpapers",
        "orientation": "portrait",
        "client_id": getenv("UNSPLASH_KEY"),
    }
    unsplash_response = get(u_api_url, params=params)
    if unsplash_response.status_code == 200:
        return unsplash_response.json()

    print(f"Unsplash API call failed with {unsplash_response.status_code}")
    return None


def parse_json(u_response, wall_list):
    count = len(wall_list)
    for wall in u_response["results"]:
        urls = wall["urls"]
        r_url = urls["raw"]
        new = dict()
        r_patrn = re.compile(r"(?<=.com/).*(?=\?ixid)")
        r_match = r_patrn.search(r_url).group()
        new["filename"] = f"{r_match}.jpg"
        new["url"] = f"{r_url}&cs=tinysrgb&fit=max&fm=jpg&h=2400"
        new["thumb"] = urls["thumb"]
        new["creator"] = wall["user"]["name"]
        new["name"] = f"Wallpaper {count + 1:03}"
        count += 1
        wall_list.append(new)
    return wall_list


def build_index():
    rand_page = randint(0, 10)
    max_count = 150
    count = 0
    wall_list = []
    while count < max_count:
        u_response = make_unsplash_api_call(rand_page)
        if u_response is None:
            sys.exit(0)
        wall_list = parse_json(u_response, wall_list)
        count = len(wall_list)
        rand_page = randint(0, u_response["total_pages"])
        print(f"Compiled list at {count} items")

    return dumps(
        wall_list,
        indent=4,
    )


def generate(arg):
    app_json = build_index()
    raw_url = push_gist(app_json).rjust(8)
    if raw_url is None:
        sys.exit(0)
    placeholder_line_found = False
    with open(join(dirname(realpath(__file__)), "stub.xml"), "r") as input_file:
        with open(join(arg, "config.xml"), "w") as output_file:
            for line in input_file:
                # If we've found the spot to add url, add it.
                if line.strip() == "<!-- index_raw_url_here -->":
                    placeholder_line_found = True
                    output_file.write(f"{raw_url}\n")
                    continue
                output_file.write(line)
    if not placeholder_line_found:
        raise ValueError(
            "Failed: Improper stub file"
        )


def main():
    if len(argv) > 1:
        generate(argv[1])
    else:
        raise ValueError("Pass output file location argument")


if __name__ == "__main__":
    main()
