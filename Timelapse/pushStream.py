#!/usr/bin/python3

# Crontab to take a picture every minute
# * * * * * /usr/bin/python3 /home/pi/AzureCloudCam/Timelapse/pushStream.py > out.log
#

# Backups video footage to the cloud
from os import listdir
from os.path import isfile, join
import os, uuid
import datetime
import calendar
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

try:
	scriptStartTime = datetime.datetime.utcnow()
	print("Initate backup script")

	# Connection string for azure storage
	connect_str = "<updateazkey>"

	# Camera name
	cameraname = "<updatehostname>"

	# root of storage container
	container = "timelapse-"

	# Local Path for blobs to upload
	uploadsrcpath = "./capture/"

	# Create the BlobServiceClient object
	blob_service_client = BlobServiceClient.from_connection_string(connect_str)

	# Create capture directory if not exists
	if not os.path.isdir(uploadsrcpath):
		print(f'Creating capture path')
		os.mkdir(uploadsrcpath)
	else:
		print('Capture path exisits')

except Exception as ex:
	print("Failed to initate script")
	print(ex)

try:
	print("Trying to take a picture, smile!")
	now = datetime.datetime.utcnow()
	#midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
	#seconds = (now-midnight).seconds
	cmd = f'raspistill -o ./capture/{now:%Y-%B-%d}-{now.timestamp()}.jpg'
	print(cmd)
	os.system(cmd)
	print("picture captured")
except Exception as ex:
	print("Failed to take capture")
	print(ex)


#try:
#	print("Clean up old containers")
#	time = datetime.datetime.now()
	# Chose to hard code this but this could also be an environment variable
#	monthsback = -2
#	timeback = datetime.date(time.year, time.month + monthsback, time.day)
#	oldmonth = timeback.strftime("%B")
#	oldcontainer_name = (container + oldmonth).lower()
#	print("Attempt to delete " + oldcontainer_name + " if exists")

	# Create the container
#	blob_service_client.delete_container(oldcontainer_name)

#except Exception as ex:
#	print("Ran into an issue cleaning up old blob containers")
#	print(ex)


try:
	print("Getting latest container...")

	# Get month from time
	time = datetime.datetime.now()
	month = time.strftime("%B")

	# Create a unique name for the container
	container_name = (container + month).lower()
	print("Container: " + container_name)

	# Create the container
	container_client = blob_service_client.get_container_client(container_name)

	# Check if container exists
	# this will thow an exception if the container doesnt exist
	# We will create the container in the exception block
	container_client.get_container_properties()

except Exception as ex:
	print('Exception:')
	print(ex)
	print('...')
	print('Creating new container...')
	container_client = blob_service_client.create_container(container_name)
	print('Container created: ' + container_name + '\n')


try:
	print("Pushing data to secure cloud storage: " + container_name + "/" + cameraname + '\n')

	# Get all files in local path
	onlyfiles = [f for f in listdir(uploadsrcpath) if isfile(join(uploadsrcpath, f))]

	#  File upload
	for fname in onlyfiles:
		print("\nUploading to Azure Storage as blob:\n\t" + uploadsrcpath + fname)

		# Create a blob client using the local file name as the name for the blob
		blob_client = blob_service_client.get_blob_client(container=container_name, blob=cameraname + "/" +fname)

		# Upload the created file if it doesn't already exist
		print("a0")
		# Delete on successful upload
		with open(join(uploadsrcpath,fname), "rb") as data:
			print("a1")
			try:
				print("a2")
				blob_client.upload_blob(data)
				print("a3")
				os.remove(join(uploadsrcpath,fname))
				print("a4")
			except Exception as nex:
				print("Exception:")
				print(nex)

except Exception as ex:
	print('Exception:')
	print(ex)

scriptEndTime = datetime.datetime.utcnow()
runtime = scriptEndTime - scriptStartTime

print(f'Complete. Runtime: {runtime.total_seconds()}')
