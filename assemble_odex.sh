#!/bin/sh
EXTRACT_DIR=$1
APK_NAME=$2

# cd "$EXTRACT_DIR/"
# java -jar /app/smali.jar a "$APK_NAME" -o classes.dex
# cp "$APK_NAME.apk" "${APK_NAME}_mod.apk"
# zip -rv "${APK_NAME}_mod.apk" classes.dex
# zipalign -v 4 "${APK_NAME}_mod.apk" "${APK_NAME}_align.apk"

cd "$EXTRACT_DIR/"
java -jar /app/smali.jar a smali_classes -o "$APK_NAME/classes.dex"
cd "$APK_NAME"
zip -r "../${APK_NAME}_mod.apk" *
cd ..
zipalign -v 4 "${APK_NAME}_mod.apk" "${APK_NAME}_align.apk"
