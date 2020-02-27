# unConv's vendor

## Forked from [SpiritCroc's vendor](https://github.com/SpiritCroc/android_vendor_spiritcroc)

This repository contains some ROM additions that I like to have in my personal builds,
but ~might~ *will* not be suitable for including by default in ~official~ any other build.

In order to use this, clone it into vendor/extra.
Custom ROMs like AICP or LineageOS will automatically call it if they find it in that location.

# Features

- Use /etc/hosts similar to one created by AdAway to block ads. This might break some apps!
    - If the hosts file is not applied when using this repo, apply [this patch](https://github.com/SpiritCroc/android_build/commit/567169f3c70c5ca9d45a0ea868140ac390790c85)
    - To update hosts, run `./adaway/generate.sh`
- Custom bootanimation
    - If you want to go back to the default bootanimation, you can delete `/product/media/bootanimation.zip` on your device
- Enable lockscreen rotation for all devices by default
