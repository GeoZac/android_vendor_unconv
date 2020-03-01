from os.path import exists, isfile, getsize

from clint.textui.progress import bar
from packaging import version
from requests import get

DEBUG = False
BASE_PATH = "vendor/extra/prebuilt/apps/bromite-webview/"


def getlatesttag():
    repo_name = "bromite/bromite"
    repo_url = f"https://api.github.com/repos/{repo_name}/releases"
    data = get(repo_url).json()
    if DEBUG:
        print(data[0]["tag_name"])
    return data[0]["tag_name"]


def writetag(tag):
    fname = BASE_PATH + "bromite_version.txt"
    with open(fname, "w") as file_write:
        file_write.write(tag)


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


def getlatestbromite(forced=False):
    repo_name = "bromite/bromite"
    repo_url = f"https://api.github.com/repos/{repo_name}/releases"
    data = get(repo_url).json()
    tag_name = data[0]["tag_name"]
    print(f"Latest version: {tag_name}")
    fname = BASE_PATH + "bromite_version.txt"
    if exists(fname):
        with open(fname, "r") as file_read:
            current_version = file_read.readline()
    else:
        # Since we have no priors version,apply a sane value to check
        current_version = "0.0.0.0"

    if version.parse(tag_name) > version.parse(current_version) or forced:
        asset_names = ["arm64_SystemWebView.apk", "arm_SystemWebView.apk"]
        for asset in data[0]["assets"]:
            filename = BASE_PATH + str(asset["name"]).split("_")[0] + "/SystemWebView.apk"
            filesize = asset["size"]
            if not any(item in asset['name'] for item in asset_names) and DEBUG:
                print(f"Skipped {asset['name']}")
                continue
            # Assets will have same name, just check for size too, sha matching for a later time
            if isfile(filename) and (filesize == getsize(filename)):
                print(f"{filename} already up-to date")
            else:
                if DEBUG:
                    print(asset["browser_download_url"], filename, filesize)

                else:
                    fetchfile(asset["browser_download_url"], filename, filesize)
                    print(f"Updated {asset} to v{tag_name}")


def checkfileexits():
    # On a fresh clone the files are not supposed to exist, so get the latest tag, get the assets,mark the version
    if not exists(BASE_PATH + "bromite_version.txt"):
        print("Seems not initilized, will do it now")
        tag = getlatesttag()
        getlatestbromite(True)
        writetag(tag)
        return False
    print("File Exists, will see about updating")
    return True


if __name__ == "__main__":
    initilized = checkfileexits()

    if initilized:
        getlatestbromite()
    else:
        print("Everthing in order")
