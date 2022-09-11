import sys
from hashlib import sha256
from os.path import exists, isfile
from urllib.request import urlopen

from clint.textui.progress import bar
from inputimeout import inputimeout, TimeoutOccurred
from packaging import version
from requests import exceptions, get

ENABLED = True
DEBUG = False
VERIFY = False
BASE_PATH = "vendor/extra/prebuilt/apps/bromite-webview/"

ASSET_NAMES = [
    "arm64_SystemWebView.apk",
    "arm_SystemWebView.apk",
]


def write_tag(tag):
    f_name = BASE_PATH + "bromite_version.txt"
    with open(f_name, "w") as file_write:
        file_write.write(tag)


def get_file_hash(file_name):
    with open(file_name, "rb") as file:
        sha256_hash = sha256()
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: file.read(4096), b""):
            sha256_hash.update(byte_block)
        print("Filename:", file_name, "\nSHA256 checksum :", sha256_hash.hexdigest(), "\n")


def fetch_file(url, filename, file_size):
    asset_file_data = get(url, stream=True)
    with open(filename, "wb") as out_file:
        print(filename)
        total_length = int(file_size)
        for chunk in bar(
                asset_file_data.iter_content(chunk_size=4096),
                expected_size=(total_length / 4096) + 1,
        ):
            if chunk:
                out_file.write(chunk)
                out_file.flush()
    out_file.close()


def get_asset_hashes(assets, files_to_hash):
    for asset in assets:
        hashes = {}
        if "sha256.txt" in asset["name"]:
            for line in urlopen(asset["browser_download_url"]):
                line = line.decode('utf-8')
                if any(x in line for x in files_to_hash):
                    file_hash = line.split(" ")
                    hashes[file_hash[-1].rstrip()] = file_hash[0]
            return hashes
    return None


def update_assets(tag, assets):
    asset_hashes = get_asset_hashes(assets, ASSET_NAMES)
    for asset in assets:
        asset_name = asset["name"]
        filename = BASE_PATH + asset_name.split("_")[0] + "/SystemWebView.apk"
        file_size = asset["size"]
        if not any(item in asset_name for item in ASSET_NAMES):
            if DEBUG:  # Silently continue in case not DEBUG
                print(f"Skipped {asset_name}")
            continue
        # Assets will have same name, just check for SHA256 hash too
        if isfile(filename) and get_file_hash(filename) == asset_hashes[asset_name]:
            print(f"{filename} already up-to date")
        else:
            if DEBUG:
                print(asset["browser_download_url"], filename, file_size)

            else:
                fetch_file(asset["browser_download_url"], filename, file_size)
                print(f"Updated {asset_name} to v{tag}")

        if VERIFY:
            get_file_hash(filename)

    if not DEBUG:
        write_tag(tag)


def get_latest_bromite():
    repo_name = "bromite/bromite"
    repo_url = f"https://api.github.com/repos/{repo_name}/releases"
    data = get(repo_url).json()
    index = 0
    skip_version = False
    tag_name = data[index]["tag_name"]
    pre_release = data[index]["prerelease"]
    f_name = BASE_PATH + "bromite_version.txt"
    if exists(f_name):
        if pre_release:
            # Skip pre-release versions
            return
        with open(f_name, "r") as file_read:
            current_version = file_read.readline()
            print(f"Current Version: {current_version}")
    else:
        # Since we have no priors version,apply a sane value to check
        current_version = "0.0.0.0"
        # Also check if the latest version is a pre-release, in which case, get the previous version
        if pre_release:
            print(f"Skipping Pre-release version: {tag_name}")
            skip_version = True

    # Unpack available asset's names to a list
    available_assets = [asset["name"] for asset in data[index]["assets"]]

    # Skip upgrading in case a release doesn't have all the assets we require
    for asset_name in ASSET_NAMES:
        if asset_name not in available_assets:
            print(f"No {asset_name} found in v{tag_name}")
            skip_version = True
            break

    if skip_version:
        index += 1
        tag_name = data[index]["tag_name"]

    print(f"Latest version : {tag_name}")
    update_allowed = False
    if version.parse(tag_name) > version.parse(current_version):
        try:
            console_input = inputimeout(prompt=f"Update apk assets to {tag_name}? :", timeout=5)
        except TimeoutOccurred:
            console_input = "n"
        update_allowed = console_input == "y"
    if update_allowed:
        update_assets(tag_name, data[index]["assets"])


def check_file_exists():
    # On a fresh clone the files are not supposed to exist, so get the latest tag, get the assets,mark the version
    if not exists(BASE_PATH + "bromite_version.txt"):
        print("Seems not initialised, will do it now")
        get_latest_bromite()
        return False
    print("File Exists, will see about updating")
    return True


def latest_bromite():
    initialised = check_file_exists()

    if initialised:
        get_latest_bromite()
    else:
        print("Everything in order")


def check_internet():
    try:
        get("https://api.github.com")
    except exceptions.ConnectionError:
        print("No internet, bailing...")
        sys.exit(0)


if __name__ == "__main__":
    if ENABLED:
        check_internet()
        latest_bromite()
