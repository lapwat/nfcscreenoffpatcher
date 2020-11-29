#/bin/sh
HOST_DIR=test
DEVICE_DIR='/data/app/com.google.android.apps.wallet*/base.apk'
WALLET_DIR=$(adb shell su -c ls $DEVICE_DIR)
echo $WALLET_DIR
adb pull "$WALLET_DIR" "$HOST_DIR/"
cd $HOST_DIR
apktool d base.apk
