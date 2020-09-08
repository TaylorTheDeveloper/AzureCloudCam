#!/usr/bin/python3

# Backups video footage to the cloud
from os import listdir
from os.path import isfile, join
import os, uuid
import datetime
import calendar
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

try:
	print("Initate backup script")

	# Connection string for azure storage
	connect_str = "<replace with your azure storage connection string>"

	# Camera name
	cameraname = "picam1"

	# root of storage container
	rootStorageContainerName = "securityfoot"
	container = rootStorageContainerName + "-"

	# Local Path for blobs to upload
	uploadsrcpath = "/var/lib/motion/"

	# Create the BlobServiceClient object
	blob_service_client = BlobServiceClient.from_connection_string(connect_str)

except Exception as ex:
	print("Failed to initate script")
	print(ex)

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
	print(container_client.get_container_properties())

except Exception as ex:
	print('Exception:')
	print(ex)
	print('...')
	print('Creating new container...')
	container_client = blob_service_client.create_container(container_name)
	print('Container created: ' + container_name)


try:
	print("Pushing data to secure cloud storage: " + container_name + "/" + cameraname)

	# Get all files in local path
	onlyfiles = [f for f in listdir(uploadsrcpath) if isfile(join(uploadsrcpath, f))]

	#  File upload
	for fname in onlyfiles:
		print("\nUploading to Azure Storage as blob:\n\t" + uploadsrcpath + fname)

		# Create a blob client using the local file name as the name for the blob
		blob_client = blob_service_client.get_blob_client(container=container_name, blob=cameraname + "/" +fname)

		# Upload the created file if it doesn't already exist
		# Delete on successful upload
		with open(join(uploadsrcpath,fname), "rb") as data:
			try:
				blob_client.upload_blob(data)
				os.remove(join(uploadsrcpath,fname))
			except Exception as nex:
				print("Exception:")
				print(nex)

except Exception as ex:
	print('Exception:')
	print(ex)
