#! /bin/bash

# Make sure you update the hostname and wifi settings to your needs.

echo "Installing software prerequisites"
sudo apt-get update
sudo apt install python3-pip
pip3 install azure-storage-blob

echo "Updating hostname"
sudo raspi-config nonint do_hostname "timelapse"
echo "Enable SSH"
sudo raspi-config nonint do_ssh 0
echo "Enable camera"
sudo raspi-config nonint do_camera 0

echo "Installing Crontab."
echo "* * * * * /usr/bin/python3 /home/pi/AzureCloudCam/Timelapse/pushStream.py > out.txt" >> /var/spool/cron/crontabs/pi