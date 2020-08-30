echo "Installing software prerequisites"

sudo apt install python3-pip
pip3 install azure-storage-blob

echo "Installing Crontab. Please authorize this step"
sudo -i
echo "* * * * * /usr/bin/python3 /home/pi/AzureCloudCam/Timelapse/pushStream.py > out.txt" >> /var/spool/cron/crontabs/pi
