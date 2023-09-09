#!/bin/bash

# genymotion start instance
gmsaas config set android-sdk-path $ANDROID_HOME
gmsaas auth login $GM_USERNAME $GM_PASSWORD
echo "Login successful!"

python3.9 gm_app.py --start-instance

echo "Sleep 20 seconds!"
sleep 20

python3.9 gm_app.py --get-instance-id

echo "$(python3.9 gm_app.py --get-instance-id)"
echo "Initiate ADB connect!"
gmsaas instances adbconnect "$(python3.9 gm_app.py --get-instance-id | sed -e 's/^[ \t]*//' -e 's/[ \t]*$//')"

echo "Sleep 5 seconds!"
# give some time to adb
sleep 5

echo "List devices!"
# check adb devices
adb devices

echo "Start appium server!"
# start appium
appium