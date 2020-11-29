#!/bin/sh
TAG=$1

rm -f "NFCScreenOff-$TAG.zip" 
cd NFCScreenOff
zip -r "../NFCScreenOff-$TAG.zip" customize.sh META-INF module.prop service.sh system bin
