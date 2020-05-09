#!/bin/bash

export DISPLAY=':0.0'

while true;
do
sleep 1200
xdotool key "ctrl+F5" &
done
