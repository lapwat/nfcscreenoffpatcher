#!/bin/sh
SERVER_URL=$1

rm -f NFCScreenOff.zip
cd NFCScreenOff
sed -i "s+https://patcher.lapw.at+http://$SERVER_URL:9001+" customize.sh
zip -r ../NFCScreenOff.zip customize.sh META-INF module.prop service.sh system bin
sed -i "s+http://$SERVER_URL:9001+https://patcher.lapw.at+" customize.sh
cd -
adb push NFCScreenOff.zip /sdcard/Download
