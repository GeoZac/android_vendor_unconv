LOCAL_PATH:= $(call my-dir)
include $(CLEAR_VARS)

LOCAL_RRO_THEME := NotifDark-System-NotifDark-SystemUI-AOSPGray
LOCAL_PRODUCT_MODULE := true
LOCAL_CERTIFICATE := platform
LOCAL_SDK_VERSION := current
LOCAL_RESOURCE_DIR := $(LOCAL_PATH)/res
LOCAL_PACKAGE_NAME := NotifDark-System-NotifDark-SystemUI-AOSPGray

include $(BUILD_RRO_PACKAGE)
