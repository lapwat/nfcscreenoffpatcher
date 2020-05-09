#!/bin/sh
EXTRACT_DIR=$1
APK_NAME=$2

cd "$EXTRACT_DIR/"
apktool if framework-res.apk
apktool d -f "$APK_NAME.apk" -o "$APK_NAME/"
