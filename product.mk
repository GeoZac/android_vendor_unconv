VENDOR_EXTRA_PATH := vendor/extra

# Custom packages
PRODUCT_PACKAGES += \
    bromite-webview

# Custom bootanimation
PRODUCT_COPY_FILES += \
    $(VENDOR_EXTRA_PATH)/bootanimation/bootanimation.zip:system/product/media/bootanimation.zip

# Extra overlays
PRODUCT_PACKAGE_OVERLAYS += $(VENDOR_EXTRA_PATH)/overlay/common

# Hosts file
PRODUCT_COPY_FILES += \
    $(VENDOR_EXTRA_PATH)/prebuilt/system/etc/hosts:system/etc/hosts
