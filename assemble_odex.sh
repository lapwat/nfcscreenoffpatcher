#!/bin/sh
EXTRACT_DIR=$1
APK_NAME=$2

cd "$EXTRACT_DIR/"
java -jar /app/smali.jar a -o classes.dex "$APK_NAME"
cp "$APK_NAME.apk" "${APK_NAME}_mod.apk"
zip -rv "${APK_NAME}_mod.apk" classes.dex
zipalign -v 4 "${APK_NAME}_mod.apk" "${APK_NAME}_align.apk"
