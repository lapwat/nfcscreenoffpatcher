#!/bin/sh

rm -f NFCScreenOff.zip
cd NFCScreenOff
sed -i 's+https://patcher.lapw.at+http://192.168.1.20:9001+' customize.sh
zip -r ../NFCScreenOff.zip customize.sh META-INF module.prop service.sh system bin
sed -i 's+http://192.168.1.15:9001+https://patcher.lapw.at+' customize.sh
cd -
adb push NFCScreenOff.zip /sdcard/Download
