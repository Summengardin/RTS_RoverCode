#!/bin/bash

cd dev/dependencies  # change directory to the dependencies folder
if [ -d "sphero-sdk-raspberrypi-python" ] then
    echo "sphero-sdk-raspberrypi-python already exists"
else
    git clone https://github.com/sphero-inc/sphero-sdk-raspberrypi-python.git  # clone the the RVR SDK
fi



