echo "Extra vendor detected"

# Fetch latest bormite webview apks
/usr/bin/python3 vendor/extra/scripts/latestbromite.py

# Update custom hosts including my changes
if [ -d "external/hosts/" ]; then
    /usr/bin/python3 external/hosts/updateHostsFile.py -n -m
fi

# Don't bother,get the zip ready without haste
export USER_BUILD_NO_CHANGELOG=1
echo "Changelog will be skipped"

# Build my custom Ad-block file
export INPUT_ADBLOCK_FILE=external/hosts/hosts_unconv
