# Simple DIY Azure Cloud Wireless Security IoT Camera

Instructions to build a simple, light weight IoT cloud camera. *new* Instructions for doorbell camera as well. Each camera connects to your network wirelessley and effortlessly. You can use virtually any usb camera or rasberry pi camera. This specific application is for a security camera but you can tweak and modify as needed for other cloud camera applications. Data is backed up to azure blob storage in every 15 minutes- but you can tune this to your needs. These cameras are lightweight and cheap! Please git (ha) in touch with me on youtube! [Taylor Teaches Youtube](https://www.youtube.com/channel/UCp8czcysNQHKMI3rHCcCGBQ)

Although I use raspberry pi- you should be able to do this with any linux based system. These instructions will work for both the raspberry pi and the raspberry pi zero, but your milage may vary on the pi zero depending on configuration. 

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
3. Update the hostname of the device so we can find it later without the IP:
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
3. Update software on device by entering the following commands in order:
    - sudo apt-get update
    - sudo apt-get upgrade
3. Download and install motion, git, and pip3 (you'll)
    - Run: sudo apt-get install -y motion git python3-pip
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

### Optionally backup captures to Azure Blob Storage

1. Clone this repo to your machines home directory
1. Ensure you have a free [Azure Subscription and Azure Storage Account](https://portal.azure.com)
1. Install git and pip3 if you haven't already
    - sudo apt install -y python3-pip
2. From this point, you need to install the azure-storage-blob library and crontab configuration as root. Otherwise the script will not be able to delete files from /var/lib/motion after upload.
    - run sudo -i to enter root
    - pip3 install azure-storage-blob
3. Set up pushStream.py and crontab. 
    - Update the connection string with either connection string or a Shared Access Signature to your blob account.
    - Update the camera name to be whatever you want it to be. Leave this alone if you like my default name. ;)
    - Open cron tab with 'sudo crontab -e'
        - manually enter cron tab enteries I have provided in crontab.txt in this repo.
    - Your python script should now upload any files from motion to your cloud storage account

### Optional Additonal Steps to enable doorbell camera!

Recommend you grab yourself a 3.5" TFT screen and case like this one:


For the doorbell camera, we will use the same setup as above but with some light tweeks. We will also install a gui so we can see the otherside of the door.

1. Set up GUI environment [> more details](https://raspberrytips.com/upgrade-raspbian-lite-to-desktop/)

    sudo apt update
    
    sudo apt upgrade
    
    sudo apt dist-upgrade
    
    sudo reboot
    
    sudo apt install xserver-xorg
    
    sudo apt install raspberrypi-ui-mods // this instals PIXELS, you can isntall another GUI if you want.
    
    sudo apt install lightdm // this might already be installed. Run anyways to check
    
    sudo reboot
    

3. Install your TFT screen on GPIO[skip if using HDMI]
    Refer to your instructions on how to do this! For the unit I purchased, my drivers were located https://github.com/goodtft/LCD-show
    
    I installed the MHS35B-show driver because I am using a raspberry pi B +
    
    Note -> I had to disable/enable my camera after I did this. If your camera stops working after this install disable and renable in raspi-config. Reboot the machine. 
    
  
2. Set up chrome to run in fullscreen on startup [> more details](https://raspberrypi.stackexchange.com/questions/69204/open-chromium-full-screen-on-start-up)
    sudo apt install chromium-browser
    
    Then, check if this file exists. If not, create the file. Then edit the file.
    
    sudo nano /home/pi/.config/lxsession/LXDE-pi/autostart
    
    
    Add the follow items to run chrome on startup and navigate to our localhost view. This will also start it fullscreen mode. You can optionally skip the localhost configuration and have this point to the stream server url you configured before instead of localhost.
    
    @xset s off
    
    @xset -dpms
    
    @xset s noblank
        
    @chromium-browser --kiosk -app=http://localhost:8081 --check-for-update-interval=31536000
    
    The last line starts our 'app' aka our stream in kiosk mode- so the rest of the gui is disabled. There is currently a bug in chromium where the update pop up comes up to frequently, so I also pass a flag to check for an update a year after boot time. 
    
    More info:
    https://raspberrypi.stackexchange.com/questions/68734/how-do-i-disable-restore-pages-chromium-didnt-shut-down-correctly-prompt
    https://www.raspberrypi.org/forums/viewtopic.php?t=265626
    
    Some users may want to refresh chromium for various reasons. This can be done by installing xdotool and adding a simple script to trigger a refresh. Because we are in kiosk mode, the browser is in keyboard focus context.
    
    sudo apt-get install xdotool
    
    Then add the script "refreshChromium.sh" from this repo to your root user directory. Make it executable.
    
    sudo chmod a+x refreshChromium.sh 
    
    Then add the following line to your autostart script.
    
    @/home/pi/refreshChromium.sh
    
    sudo reboot    
    
3. Hide the mouse curor in kiosk mode

    sudo apt-get install unclutter
    
    sudo nano ~/.config/lxsession/LXDE-pi/autostart
    
    Add this line to autostart: 
    
    @unclutter -idle 0
    
    sudo reboot

    More info:
    https://jackbarber.co.uk/blog/2017-02-16-hide-raspberry-pi-mouse-cursor-in-raspbian-kiosk
    
3. Set up autologin so we login to GUI on startup [> more details](https://www.raspberrypi.org/forums/viewtopic.php?t=164906)

    sudo nano /etc/lightdm/lightdm.conf
    
    update the below line:
    
    #autologin-user=
    
    to be (you can use your username if different)
    
    autologin-user=pi
    

4.  Modify /etc/motion/motion.conf to enable local viewing of doorbell camera from tft screen.

    set stream_localhost=on
    
    set stream_auth_method 0
    
    comment ;stream_authentication pi:raspberry
    


There you go! You've now extended your cloud security camera to also be a doorbell camera. The data will still push to the cloud. I recommend giving each camera a unique name in pushStream.py.

### Review footage in Azure Storage Explorer

![model](https://homesecurityfootage.blob.core.windows.net/images-public/cam1.PNG) 
![model](https://homesecurityfootage.blob.core.windows.net/images-public/cam2.PNG) 




