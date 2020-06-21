#!/bin/sh
curl --fail -X PUT --upload-file NfcNci.zip -o NfcNci_align.apk localhost:9001 
filesize=$(stat --printf="%s" NfcNci_align.apk)
rm -f NfcNci_align.apk
[ $filesize -eq 2010845 ] && echo OK || echo "KO: expected 2010845 but got $filesize"
