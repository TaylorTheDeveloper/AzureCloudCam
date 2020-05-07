# Simple DIY Azure Cloud Wireless Security IoT Camera

Instructions to build a simple, light weight IoT cloud camera. Each camera connects to your network wirelessley and effortlessly. You can use virtually any usb camera or rasberry pi camera. This specific application is for a security camera but you can tweak and modify as needed for other cloud camera applications. Data is backed up to azure blob storage in every 15 minutes- but you can tune this to your needs. These cameras are lightweight and cheap! Please git (ha) in touch with me on youtube! [Taylor Teaches Youtube](https://www.youtube.com/channel/UCp8czcysNQHKMI3rHCcCGBQ)

Although I use raspberry pi- you should be able to do this with any linux based system. 

You can change the file format to various other formats or enable images and resolution. See my [video]() or check out the [motion docs](https://motion-project.github.io/motion_guide.html). 

# Hardware Requirements
  
  - Wifi Enabled Router for wireless networking
  - Raspberry Pi 3 B+ Wireless / Raspberry Pi Zero Wireless
  - Raspberry Pi Serial Camera / Any Usb Camera
  - 16GB SD Card (you may be able to user smaller depending on how you conifure things. If using my configuration, I recommend 16GB)
  
# Azure Requirements
   - A free Azure Subscription
   - An Azure Storage Account
  
# Software Requirements
- Etcher (or another SD Card Flashing software) [>> download](https://www.balena.io/etcher/)
- Raspbian Buster Lite OS [>> download](https://downloads.raspberrypi.org/raspbian_lite_latest)
- Motion 4.1.1 [>> check out](https://motion-project.github.io/motion_guide.html)
- crontab (should be installed if using raspbian)
- python3 (should be installed if using raspbian)
- pip3 [>> check out](https://www.raspberrypi.org/documentation/linux/software/python.md)
- azure blob storage python client (via pip3) [>> microsoft docs](https://docs.microsoft.com/en-us/python/api/azure-storage-blob/azure.storage.blob?view=azure-python)

All in all this project is a lot of fun, hope you enjoy building/learning about it. I decided to build this project because I've been learning more about IoT and thought this would be a fun/useful project. I'm interested in home automation and cloud technology. I'm thinking of using cameras like these for other computer vision projects at home and this seemed like a great way to learn more about it.

This mini security camera concept isn't a new idea- in fact there is the [MotionEyeOS](https://github.com/ccrisan/motioneyeos/wiki) project which acomplishes this very task. However it uses google drive which I didn't want to use, I persoanlly prefer Azure Strorage because I can easily manage the data or integrate it with other cloud applications easily. My needs for a front end are minimal and I am ok with accessing the streams via other computers on the network over HTTP in a browser. As such, each camera device is an indepenent self-sufficent node on my local network. When I plug it in- it start's recording and backing up the data to the cloud. If I decide later I want a viewer in Azure I can write one, but for now I only want the ability to review video on as needed basis. I'm hoping never! 

## My Requirements for this security camera
 - Wirelessly communication so it can be placed virtually anywhere
 - High quality captures
 - Allow for live stream via http
 - Automatic backup of stream data to cloud storage
 - Automatic cleanup of files in storage after 2 months
 - Resonable Security measures (physical and soft discussed below)
 - [TODO] Send Camera health data to another system such as IoT Hub, IoT Central, or simple alert system to let me know if a camera goes offline. Looking at healthchecks.io as a simple serivce or you can write your own.
 - [TODO] Doorbell camera has live monitor
 - Learn something new and have fun doing it 

# Model with N Cameras
![model](https://homesecurityfootage.blob.core.windows.net/images-public/securitymodel.png) 

# Security of system
- Devices are not currently placed outside- or if thery are it's only the camera portion and the unit can not be accessed
- Devices are never to be pointed inside, only to monitor vehicles and front door and exteriors
- Each device has a unique hostname on the network
- Each device shares the same username/password
- Password complexity to access device itself is high, 18 char minimum. 
- HTTP view in browser user name is the same as the host name
- HTTP view in browser password is simple enough for my family to remember, because all camera views are external and my network is secured I'm not super worried about the cameras getting hacked.
- Cameras connection to  Azure is via SAS (Shared Access Signature) so if they do get comprimised attacker can't delete data. Device needs the ability to create, read, and write data.

# Instructions

### Set up Raspberry Pi 3 B+

1. Download Raspbian Buster Lite and flash it to a SD card 
2. Place SD card into raspberry pi and power on
     -for inital setup many users find it easer to plug the device into a monitor. Recommend doing that and then swapping to terminal after SSH is enabled. 
3. Sign in with the default username and password: 
    -username: pi 
    -password: raspberry
3. Update software on device by entering the following commands in order:
    - sudo apt-get update
    - sudo apt-get upgrade
4. Update the hostname of the device so we can find it later without the IP:
    - [How to update hostname](https://www.cyberciti.biz/faq/ubuntu-change-hostname-command/)
    - You should just need to update /etc/hostname and /etc/hosts with your custom name.
5. Enable Wifi on the Pi! Wifi allows us to connect to the device over the wireless network instead of a hard line.
    - [How to enable WiFi](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md)
    - Run: sudo raspi-config
    - Select Network Options 
    - then select the Wi-fi option
    - specify the country in which the device is being used
    - Then set the SSID of the network (this is generally found on the back of your router)
    - Then set the passphrase for the network. (also generally on the back of your router)
3. Enable SSH on the Pi! SSH allows us to connect to the device from another computer. 
    - [How to enable SSH](https://www.raspberrypi.org/documentation/remote-access/ssh/)
    - Run: sudo raspi-config
    - Select Interfacing Options
    - Navigate to and select SSH
    - Choose Yes
    - Select Ok
    - Choose Finish
3. (Optional only if using raspberry pi camera, usb cameras can skip this step) Enable Raspberry Pi camera
    - Run: sudo raspi-config
    - Select Interfacing options
    - Navigate to camera
    - Enable
    - Finish
    - Reboot
3. Important! Update your password to something secure! You can skip this step if you don't care about security. 
    - Run: passwd and update password
3. Download and install motion
    - Run: sudo apt-get install motion 
    - reboot after installation
5. Configure Motion
    - You also need to enable the motion daemon so that motion will always run.
        - open /etc/default/motion
        - update 'start_motion_daemon=no' to 'start_motion_daemon=yes'
    - Update the motion config with the motion config from my repo
        - Replace the config at /etc/motion/motion.conf with my config.
        - Make sure to update the camera name, stream_localhost, username, and password from my default values.
            - For the setting 'stream_localhost' if should be set to 'on' if you only want to view the stream on the device. If you want to view the stream over http port 8081 on another machine (you can change the port if needed in the config) set this setting to 'off'
            - If 'stream_localhost' is 'off' then you need to supply credentials or you can use my defaults.
                - 'stream_auth_method' should be '2'
                - 'stream_authentication' should be '<\ your username \>:<\ your password \>'
                - These credentials are independent of the machine credentials! 
        - Make sure the daemon is marked as 'on' in this config file or it will not work! 
        - You can modify the video code, frame rate, and video resultion amongst many other parameters. 
        - You can enable image capture if you prefer that over video stream. 
    - This is the bear minimum needed to set up the camera and view it from anoother device! Next we will push this data to the cloud. 

### Backup captures to Azure Blob Storage

1. Ensure you have a free Azure Subscription and Azure Storage Account
1. Install pip3 
    - sudo apt install python3-pip
2. Recommend at this point doing everything as root. Install Azure Blob Service Client
    - run sudo -i to enter root
    - pip3 install azure-storage-blob
3. Set up pushStream.py and crontab. 
    - run cd ~ to go to root home directory
    - copy pushStream.py from this repo to your root home directory (~)
    - Update the connection string with either connection string or a Shared Access Signature to your blob account.
    - chmod a+x ./pushstream.sh to [ensure it can execute](https://stackoverflow.com/questions/8727935/execute-python-script-via-crontab)
    - Open cron tab with 'sudo crontab -e'
        - manually enter cron tab enteries I have provided in crontab.txt in this repo.
        - The first line cleans up any data that may get skipped. This should never happen- but just in case if any files are older than 1 day in this directory then they will be removed.
        - The second line runs pushStream.py every 15 minutes and backs up data to the cloud. As data is backed up is it freed from memory on the camera. This script also automatically deletes blobs older than 2 months. You can disable this part of the code if you wish. 


