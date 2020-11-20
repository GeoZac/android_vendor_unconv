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

# Extra Font Overlays
PRODUCT_PACKAGES += \
    FontJetBrainsMono \
    FontLatoOverlay \
    FontRubikOverlay

# Add font families to fonts-customization.xml
ADDITIONAL_FONTS_FILE += \
   external/jetbrainsmono/fonts-jetbrains.xml \
   vendor/extra/fonts/fonts-unconv.xml

# Exclude some undesired packages
PRODUCT_PACKAGES += \
    NukePackages
