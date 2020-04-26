#!/bin/sh

# retrieve temporary directory
#TMP_DIR=$(mktemp -d -t nso-$(date +%Y-%m-%d-%H-%M-%S)-XXXXXXXX)
#echo -n "$TMP_DIR"
TMP_DIR=$1

# unzip
unzip apks.zip -d "$TMP_DIR/"

cd "$TMP_DIR/"

set 'NfcNci' 'NQNfcNci' 'NxpNfcNci'
for name do
  if [ -f "$name.apk" ]; then
    APK_NAME="$name"
  fi
done

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
# need if serverless?: keytool -genkey -v -keystore ~/.android/debug.keystore -storepass android -alias androiddebugkey -keypass android -keyalg RSA -keysize 2048 -validity 10000
#jarsigner -verbose -sigalg MD5withRSA -digestalg SHA1 -keystore ~/.android/debug.keystore -storepass android "${APK_NAME}_mod.apk" androiddebugkey
zipalign -v 4 "${APK_NAME}_mod.apk" "${APK_NAME}_align.apk"

cd -
cp "$TMP_DIR/${APK_NAME}_align.apk" out.apk 

