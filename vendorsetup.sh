echo "Extra vendor detected"

# Fetch latest bormite webview apks
/usr/bin/python3 vendor/extra/scripts/latestbromite.py

# Update custom hosts including my changes
if [ -d "external/hosts/" ]; then
    /usr/bin/python3 external/hosts/updateHostsFile.py -n -m
fi
