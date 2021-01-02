echo "Extra vendor detected"

# Fetch latest bormite webview apks
/usr/bin/python3 vendor/extra/scripts/latestbromite.py

# Update custom hosts including my changes
if [ -d "external/hosts/extensions/unconv/" ]; then
    echo "Merging personal changes to hosts file"
    /usr/bin/python3 external/hosts/updateHostsFile.py -n -m
    echo "Replacing duplicates domains with wildcards in hosts file"
    /usr/bin/python3 vendor/extra/scripts/wildcardhosts.py external/hosts/hosts_unconv vendor/extra/adaway/
fi

# Don't bother,get the zip ready without haste
export USER_BUILD_NO_CHANGELOG=1
echo "Changelog will be skipped"

# Build my custom Ad-block file
export INPUT_ADBLOCK_FILE=vendor/extra/adaway/hosts_unconv_w
