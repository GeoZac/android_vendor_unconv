#!/usr/bin/env python3

from json import dumps
from os import getenv
from os.path import realpath, dirname, join
from random import randint
from re import compile
from sys import argv

from requests import get, patch

PARAMS = {
    'query': 'wallpapers',
    'orientation': 'portrait',
    'client_id': getenv('UNSPLASH_KEY')
}

token = getenv('GH_GIST_TOKEN')
filename = "wall_index.json"
gist_id = "e4c7f3c3c451b859c7c70e43837e08c2"

print(len(argv))
if len(argv) > 1:
    output_file_path = argv[1]
else:
    raise ValueError("Pass output file location argument")

rand_page = randint(0, 10)
URL = f"https://api.unsplash.com/search/photos?page={rand_page}"
max_count = 150
count = 0
wall_list = []
while count <= max_count:
    # global URL
    response = get(URL, params=PARAMS).json()
    for index, wall in enumerate(response["results"]):
        urls = wall["urls"]
        r_url = urls["raw"]
        new = dict()
        p = compile(r"(?<=.com/).*(?=\?ixid)")
        r_match = p.search(r_url).group()
        new["filename"] = r_match + ".jpg"
        new["url"] = f"{r_url}&cs=tinysrgb&fit=max&fm=jpg&h=2400"
        new["thumb"] = urls["thumb"]
        new["creator"] = wall["user"]["name"]
        new["name"] = f"Wallpaper {count + 1:03}"
        count += 1
        wall_list.append(new)
    rand_page = randint(0, response["total_pages"])
    URL = f"https://api.unsplash.com/search/photos?page={rand_page}"

app_json = dumps(
    wall_list,
    indent=4,
    # sort_keys=True
)
print(app_json)
content = app_json
headers = {'Authorization': f'token {token}'}
r = patch(
    'https://api.github.com/gists/' + gist_id,
    data=dumps({'files': {filename: {"content": content}}}),
    headers=headers
)
print(r.json())
raw_url = url = r.json()['files'][filename]['raw_url']
final_xml = 'config.xml'
placeholder_line_found = False
with open(join(dirname(realpath(__file__)), "stub.xml"), "r") as input_file:
    with open(join(output_file_path, "config.xml"), "w") as output_file:
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
