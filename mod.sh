#!/bin/sh
EXTRACT_DIR=$1
APK_NAME=$2

cd "$EXTRACT_DIR/"

# decompile
apktool if framework-res.apk
apktool d -f "$APK_NAME.apk" -o "$APK_NAME/"

# mod
sed -e '/.*if-lt.*/s/^/#/g' -i "$APK_NAME/smali/com/android/nfc/NfcService.smali"
sed 's/SCREEN_OFF/SCREEN_OFFA/' -i "$APK_NAME/smali/com/android/nfc/NfcService.smali"
sed 's/SCREEN_ON/SCREEN_ONA/' -i "$APK_NAME/smali/com/android/nfc/NfcService.smali"
sed 's/USER_PRESENT/USER_PRESENTA/' -i "$APK_NAME/smali/com/android/nfc/NfcService.smali"
sed 's/USER_SWITCHED/USER_SWITCHEDA/' -i "$APK_NAME/smali/com/android/nfc/NfcService.smali"

# build
apktool b -f "$APK_NAME/" -o "${APK_NAME}_mod.apk"
# keytool -genkey -v -keystore ~/.android/debug.keystore -storepass android -alias androiddebugkey -keypass android -keyalg RSA -keysize 2048 -validity 10000
# jarsigner -verbose -sigalg MD5withRSA -digestalg SHA1 -keystore ~/.android/debug.keystore -storepass android "${APK_NAME}_mod.apk" androiddebugkey
zipalign -v 4 "${APK_NAME}_mod.apk" "${APK_NAME}_align.apk"
