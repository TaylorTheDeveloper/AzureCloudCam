# Simple Azure Cloud Camera (Security Camera)

Instructions to build a simple, light weight cloud camera. Each camera connects to your network wirelessley. You can use virtually any usb camera or rasberry pi camera. This specific application is for a security camera but you can tweak and modify as needed for other cloud camera applications. Data is backed up to azure blob storage in every 15 minutes- but you can tune this to your needs. These cameras are lightweight and cheap! Please git (ha) in touch with me on youtube! [Taylor Teaches Youtube](https://www.youtube.com/channel/UCp8czcysNQHKMI3rHCcCGBQ)

Although I use raspberry pi- you should be able to do this with any linux based system.

You can change the file format to various other formats or enable images and resolution. See my [video]() or check out the [motion docs](https://motion-project.github.io/motion_guide.html). 

# Hardware Requirements
  
  - Wifi Enabled Router for wireless networking
  - Raspberry Pi 3 B+ Wireless / Raspberry Pi Zero Wireless
  - Raspberry Pi Serial Camera / Any Usb Camera
  
# Azure Requirements
   - A free Azure Subscription
   - An Azure Storage Account
  
# Software Requirements
  - Raspbian Buster Lite OS [>> download](https://downloads.raspberrypi.org/raspbian_lite_latest)
  - Motion 4.1.1
  - crontab
  - python3 (should be installed)
  - pip3 
  - azure blob storage python client

All in all this project is a lot of fun, hope you enjoy building/learning about it. I decided to build this project because I've been learning more about IoT and thought this would be a fun/useful project.

This isn't a new idea- in fact there is the [MotionEyeOS](https://github.com/ccrisan/motioneyeos/wiki) project which acomplishes this very task. However it uses google drive which I didn't want to use, I persoanlly prefer Azure Strorage because I can easily manage the data or integrate it with other cloud applications. My needs for a front end are minimal and I am ok with accessing the streams via other computers on the network over HTTP in a browser. As such, each camera device is an indepenent self-sufficent node on my local network. When I plug it in- it start's recording and backing up the data to the cloud. If I decide later I want a viewer in Azure I can write one, but for now I only want 

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
 
# Security of system
- Devices are not currently placed outside- or if thery are it's only the camera portion and the unit can not be accessed
- Devices are never to be pointed inside, only to monitor vehicles and front door and exteriors
- Each device has a unique hostname on the network
- Each device shares the same username/password
- Password complexity to access device itself is high, 18 char minimum. 
- HTTP view in browser user name is the same as the host name
- HTTP view in browser password is simple enough for my family to remember, because all camera views are external and my network is secured I'm not super worried about the cameras getting hacked.
- Cameras connection to  Azure is via SAS (Shared Access Signature) so if they do get comprimised attacker can't delete data. Device needs the ability to create, read, and write data.
