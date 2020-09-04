$container_name = '<replace-with-blob-container-name>'
$connection_string = '<replace-with-storage-account-connection-string>'
$destination_path = 'C:\blobs'

$storage_account = New-AzureStorageContext -ConnectionString $connection_string

$blobs = Get-AzureStorageBlob -Container $container_name -Context $storage_account

foreach ($blob in $blobs)
    {
		New-Item -ItemType Directory -Force -Path $destination_path
  
        Get-AzureStorageBlobContent `
        -Container $container_name -Blob $blob.Name -Destination $destination_path `
		-Context $storage_account
      
    }