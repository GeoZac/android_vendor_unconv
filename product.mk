VENDOR_EXTRA_PATH := vendor/extra

# Include Lawnchair 
$(call inherit-product-if-exists, vendor/lawnchair/lawnchair.mk)

# Custom packages
PRODUCT_PACKAGES += \
    bromite-webview

# Extra overlays
PRODUCT_PACKAGE_OVERLAYS += $(VENDOR_EXTRA_PATH)/overlay/common

# Hosts file
PRODUCT_COPY_FILES += \
    $(VENDOR_EXTRA_PATH)/prebuilt/system/etc/hosts:system/etc/hosts
