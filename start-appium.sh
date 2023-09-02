#!/bin/bash

# genymotion start instance
gmsaas config set android-sdk-path $ANDROID_HOME
gmsaas auth login $GM_USERNAME $GM_PASSWORD
gmsaas instances start 95016679-8f8d-4890-b026-e4ad889aadf1 hr-dashboard-emulator --max-run-duration 10
gmsaas instances list > instances.txt
cat instances.txt
sleep 20
echo "$(cat instances.txt | awk '/hr-dashboard-emulator/ {print $(NF-3)}')"
gmsaas instances adbconnect "$(cat instances.txt | awk '/hr-dashboard-emulator/ {print $(NF-3)}')"

# give some time to adb
sleep 5

# check adb devices
adb devices

# start appium
appium