from hashlib import sha256
from os.path import exists, isfile, getsize

from clint.textui.progress import bar
from packaging import version
from requests import get

DEBUG = False
VERIFY = False
BASE_PATH = "vendor/extra/prebuilt/apps/bromite-webview/"


def writetag(tag):
    fname = BASE_PATH + "bromite_version.txt"
    with open(fname, "w") as file_write:
        file_write.write(tag)


def getfilehash(file_name):
    with open(file_name, "rb") as file:
        sha256_hash = sha256()
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: file.read(4096), b""):
            sha256_hash.update(byte_block)
        print("Filename:", file_name, "\nSHA256 checksum :", sha256_hash.hexdigest(), "\n")


def fetchfile(url, filename, filesize):
    asset_file_data = get(url, stream=True)
    with open(filename, "wb") as out_file:
        print(filename)
        total_length = int(filesize)
        for chunk in bar(
                asset_file_data.iter_content(chunk_size=4096),
                expected_size=(total_length / 4096) + 1,
        ):
            if chunk:
                out_file.write(chunk)
                out_file.flush()
    out_file.close()


def updateassets(tag, assets):
    asset_names = ["arm64_SystemWebView.apk", "arm_SystemWebView.apk"]
    for asset in assets:
        asset_name = asset["name"]
        filename = BASE_PATH + asset_name.split("_")[0] + "/SystemWebView.apk"
        filesize = asset["size"]
        if not any(item in asset_name for item in asset_names):
            if DEBUG:  # Silently continue in case not DEBUG
                print(f"Skipped {asset_name}")
            continue
        # Assets will have same name, just check for size too, sha matching for a later time
        if isfile(filename) and (filesize == getsize(filename)):
            print(f"{filename} already up-to date")
        else:
            if DEBUG:
                print(asset["browser_download_url"], filename, filesize)

            else:
                fetchfile(asset["browser_download_url"], filename, filesize)
                print(f"Updated {asset_name} to v{tag}")

        if VERIFY:
            getfilehash(filename)

    if not DEBUG:
        writetag(tag)


def getlatestbromite():
    repo_name = "bromite/bromite"
    repo_url = f"https://api.github.com/repos/{repo_name}/releases"
    data = get(repo_url).json()
    index = 0
    tag_name = data[index]["tag_name"]
    prerelease = data[index]["prerelease"]
    fname = BASE_PATH + "bromite_version.txt"
    if exists(fname):
        if prerelease:
            # Skip prerelease versions
            return
        with open(fname, "r") as file_read:
            current_version = file_read.readline()
            print(f"Current Version: {current_version}")
    else:
        # Since we have no priors version,apply a sane value to check
        current_version = "0.0.0.0"
        # Also check if the latest version is a pre-release, in which case, get the previos version
        if prerelease:
            index += 1
            tag_name = data[index]["tag_name"]

    print(f"Latest version : {tag_name}")
    updateallowed = False
    if version.parse(tag_name) > version.parse(current_version):
        updateallowed = input(f"Update apk assets to {tag_name}?") == "y"
    if updateallowed:
        updateassets(tag_name, data[index]["assets"])


def checkfileexits():
    # On a fresh clone the files are not supposed to exist, so get the latest tag, get the assets,mark the version
    if not exists(BASE_PATH + "bromite_version.txt"):
        print("Seems not initilized, will do it now")
        getlatestbromite()
        return False
    print("File Exists, will see about updating")
    return True


def latest_bromite():
    initilized = checkfileexits()

    if initilized:
        getlatestbromite()
    else:
        print("Everthing in order")


if __name__ == "__main__":
    latest_bromite()
