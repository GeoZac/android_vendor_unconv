# unConv's vendor

## Forked from [SpiritCroc's vendor](https://github.com/SpiritCroc/android_vendor_spiritcroc)

This repository contains some ROM additions that I like to have in my personal builds,
but ~might~ *will* not be suitable for including by default in ~official~ any other build.

In order to use this, clone it into vendor/extra.
Custom ROMs like AICP or LineageOS will automatically call it if they find it in that location.

# Features

- Bromite systemWebView by default
    - (Where are the prebuilt apks you ask? They are fetched by a script when the ```source build/envsetup.sh``` is run, and will check for updates on subsequent script executions)
- Prefers *Lawnchair* over any other launcher by default, will add to the build if makefile is found
- A [manifest](manifests/unconv_remove.xml) file to remove some unused packages and add some alternatives
- Overlays
    - Enable rotation for all directions by default
    - Show Internal storage by default in DocumentsUI (Files) app and,
    - Show the Internal storage root on opening
    - Sets corners in searchbar and suggestion cards in Settings app
    - Disable All Caps in materials buttons
    - Enable Lockscreen shortcuts by default
    - Allow editing smart replies before sending
    - ~Enable lockscreen rotation for all devices by default~
