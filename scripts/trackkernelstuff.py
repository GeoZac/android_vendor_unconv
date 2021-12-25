from re import search

from bs4 import BeautifulSoup as bS
from pygerrit2 import GerritRestAPI
from requests import get

from cherrypicker import STARS

# Variable to store CAF releases page data
PAGE_CACHE = None

AOSP_CLANG_REPO = "https://android.googlesource.com/platform/prebuilts/clang/host/linux-x86/+log/refs/heads/master"
CAF_REPO_URL = "https://wiki.codeaurora.org/xwiki/bin/QAEP/release"
LINUX_REPO_URL_ST = "https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable.git/log/?h=linux-{0}.y"
LINUX_REPO_URL_RC = LINUX_REPO_URL_ST.replace(".git", "-rc.git")
AOSP_GERRIT_URL = "https://android-review.googlesource.com/"

DEVICES = {
    "sdm660c": {
        "kernel": "4.4",
        "qcom_r": r"LA.UM.8.2.r1-\d{5}-sdm660.0",
        "qc_tag": "sdm660_64",
    },
    "miatoll": {
        "kernel": "4.14",
        "qcom_r": r"LA.UM.9.1.r1-\d{5}-SMxxx0.0",
        "qc_tag": "msmnile",
        "aosp_q": "project:kernel/common+branch:android-4.14-stable"
    },
}


def make_soup(url):
    user_agent = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko)"
        " Chrome/35.0.1916.47 Safari/537.36"
    )
    headers = {"User-Agent": user_agent}
    response = get(url, headers=headers)
    return bS(response.content, "html.parser")


def track_aosp_clang():
    soup = make_soup(AOSP_CLANG_REPO)
    log = soup.find_all("li", {"class": "CommitLog-item CommitLog-item--default"})
    if log:
        for items in log[:7]:
            commit = items.find_all("a")
            print(  # str(commit[1]['href']).split("/")[-1], # the commit ID
                commit[1].get_text(),  # the commit message
                sep="\t"
            )


def track_linux_stable(r_c=False, r_v=None):
    url = (LINUX_REPO_URL_ST if not r_c else LINUX_REPO_URL_RC).format(r_v)
    soup = make_soup(url)
    links = soup.find_all("table", {"class": "list nowrap"})
    for link in links[0].contents[2].find_all("td")[:-3]:
        if "linux" in link.get_text():
            print(str(link.get_text()).replace("v4", "\nv4").replace("li", "\nli"))
        else:
            print(link.get_text())


def track_caf_releases(caf_tag):
    found = False
    global PAGE_CACHE
    if not PAGE_CACHE:
        soup = make_soup(CAF_REPO_URL)
        data = soup.find("table")
        PAGE_CACHE = data
    else:
        data = PAGE_CACHE
    if not data:
        print("Unable to fetch page data")
        return
    for row in data.find_all("tr")[1:10]:
        row_text = ""
        for cell in row.find_all("td"):
            row_text += str(cell.text).strip() + "\t"
        if search(caf_tag, row_text):
            print(row_text)
            found = True
    if not found:
        print("No qcom updates found")


def check_aosp_gerrit(device):
    count = 0
    index = 0
    query = device.get("aosp_q")
    if query:
        rest = GerritRestAPI(url=AOSP_GERRIT_URL, auth=None)
        changes = rest.get(f"/changes/?q={query}")
        while count < 10:
            change = changes[index]
            if change["status"] != "ABANDONED":
                print(change["status"], change["subject"], sep="\t")
                count += 1
            index += 1


def track_kernel_components():
    print(STARS)
    track_aosp_clang()
    print(STARS)
    for device in DEVICES:
        device_name = DEVICES[device]
        print(device)
        kernel_ver = device_name["kernel"]
        print(STARS)
        track_linux_stable(r_c=True, r_v=kernel_ver)
        print(STARS)
        track_linux_stable(r_v=kernel_ver)
        print(STARS)
        track_caf_releases(device_name["qcom_r"])
        print(STARS)
        check_aosp_gerrit(device_name)
    print(STARS)


if __name__ == "__main__":
    track_kernel_components()
