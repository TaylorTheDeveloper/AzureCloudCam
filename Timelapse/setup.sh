#! /usr/bin/bash

# Make sure you update the hostname and wifi settings to your needs.

echo "Installing software prerequisites"

sudo apt install python3-pip
pip3 install azure-storage-blob

echo "Please elevate!!"
sudo -i
echo "Updating hostname"
sudo raspi-config nonint do_hostname "timelapse"
echo "Enable SSH"
sudo raspi-config nonint do_ssh 0
echo "Enable camera"
sudo raspi-config nonint do_camera 0
echo "Set Wifi Country"
sudo raspi-config nonint do_wifi_country "US"
echo "Set up Wifi"
sudo ifconfig wlan0
sudo iwconfig wlan0 essid SBG67AC- key
echo "Installing Crontab."
echo "* * * * * /usr/bin/python3 /home/pi/AzureCloudCam/Timelapse/pushStream.py > out.txt" >> /var/spool/cron/crontabs/pi
