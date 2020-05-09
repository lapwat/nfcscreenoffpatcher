#!/bin/sh
EXTRACT_DIR=$1
APK_NAME=$2

cd "$EXTRACT_DIR/"
apktool b -f "$APK_NAME/" -o "${APK_NAME}_mod.apk"
zipalign -v 4 "${APK_NAME}_mod.apk" "${APK_NAME}_align.apk"
