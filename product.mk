VENDOR_EXTRA_PATH := vendor/extra

$(call inherit-product-if-exists, external/google-fonts/lato/fonts.mk)
$(call inherit-product-if-exists, external/google-fonts/rubik/fonts.mk)
$(call inherit-product-if-exists, external/jetbrainsmono/fonts.mk)

# Custom packages
PRODUCT_PACKAGES += \
    bromite-webview \
    Recorder \
    Terminal

# Extra overlays
PRODUCT_PACKAGE_OVERLAYS += $(VENDOR_EXTRA_PATH)/overlay/common

# Allow overlays to be excluded from enforcing RRO
PRODUCT_ENFORCE_RRO_EXCLUDED_OVERLAYS += $(VENDOR_EXTRA_PATH)/overlay/common

# Extra Font Overlays
PRODUCT_PACKAGES += \
    FontJetBrainsMono \
    FontLatoOverlay \
    FontRubikOverlay

# Add font families to fonts-customization.xml
ADDITIONAL_FONTS_FILE += \
   vendor/extra/fonts/fonts-unconv.xml

# Exclude some undesired packages
PRODUCT_PACKAGES += \
    NukePackages

# Some theming overlays
PRODUCT_PACKAGES += \
   CornerRadius-Moar_Round

# Add some nostalgic tunes
PRODUCT_COPY_FILES += \
    frameworks/base/data/sounds/ringtones/ogg/Dione_48k.ogg:$(TARGET_COPY_OUT_PRODUCT)/media/audio/ringtones/Unconv.ogg

# Ad-block
PRODUCT_PRODUCT_PROPERTIES += \
    persist.aicp.hosts_block=true
