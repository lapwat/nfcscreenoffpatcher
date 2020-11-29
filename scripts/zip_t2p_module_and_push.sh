#!/bin/sh

rm -f NFCScreenOffT2P.zip
cd NFCScreenOffT2P
zip -r ../NFCScreenOffT2P.zip customize.sh META-INF module.prop service.sh system bin base_align.apk
cd -
adb push NFCScreenOffT2P.zip /sdcard/Download
