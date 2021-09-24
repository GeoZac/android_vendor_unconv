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
    - Set corners in searchbar and suggestion cards in Settings app
    - Disable All Caps in materials buttons
    - Enable Lockscreen shortcuts by default
    - Allow editing smart replies before sending
    - Shows empty wifi icon if not connected 
    - Show memory usage on app info screens
    - Default to full gesture navigation
    - Bump up default data limit to 30GB, the default 2GB is too low
    - Overlay the AOSP brightness thumb vector 
    - Allow more suggestions on AOSP keyboard
    - Hide the voice input key on AOSP keyboard 
    - Show more emoji on the emoji selector
    - ~Enable lockscreen rotation for all devices by default~
- Add some more fonts (The font-families data is injected into the vendor's fonts_customization.xml, if supported)
    - JetBrains Mono
    - Lato
    - Rubik
- Provides an improved hosts file for the build system to improve ad-blocking (if supported)
- Skips Changelog generation (if supported)
