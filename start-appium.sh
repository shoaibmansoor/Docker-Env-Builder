#!/bin/bash

# genymotion start instance
gmsaas config set android-sdk-path $ANDROID_HOME
gmsaas auth login $GM_USERNAME $GM_PASSWORD
echo "Login successful!"
gmsaas instances start 95016679-8f8d-4890-b026-e4ad889aadf1 hrdashboard-emulator
echo "Instance Started!"
gmsaas instances list > instances.txt
echo "Instance List Fetched!"
cat instances.txt
echo "Sleep 20 seconds!"
sleep 20
echo "$(cat instances.txt | awk '/hr-dashboard-emulator/ {print $(NF-3)}')"
echo "Initiate ADB connect!"
gmsaas instances adbconnect "$(cat instances.txt | awk '/hr-dashboard-emulator/ {print $(NF-3)}')"

echo "Sleep 5 seconds!"
# give some time to adb
sleep 5

echo "List devices!"
# check adb devices
adb devices

echo "Start appium server!"
# start appium
appium