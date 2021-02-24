import os
import random

from datetime import datetime, timedelta
from azure.storage.filedatalake import DataLakeServiceClient, FileSystemSasPermissions, generate_directory_sas

class SASSamples(object):

    ACCOUNT_NAME = "<ACCOUNT NAME FROM AZURE PORTAL>"
    ACCOUNT_KEY = "<ACCESS KEY FROM AZURE PORTAL>"

    STORAGE_FILESYSTEM = "demo-filesystem"
    STORAGE_URL = "https://{}.dfs.core.windows.net".format(ACCOUNT_NAME)

    def get_random_bytes(self, size):
        rand = random.Random()
        result = bytearray(size)
        for i in range(size):
            result[i] = int(rand.random()*255)  # random() is consistent between python 2 and 3
        return bytes(result)

    def test_using_directory_sas_to_read(self):
        storage_directory = "demo-folder-allowed"

        print("\nGenerating SAS for directory: {}".format(storage_directory))
        
        print("\nReading contents...")

        # generate a token for a directory with all permissions
        token = generate_directory_sas(
            self.ACCOUNT_NAME,
            self.STORAGE_FILESYSTEM,
            storage_directory,
            self.ACCOUNT_KEY,
            permission=FileSystemSasPermissions(read=True,write=True,delete=True,list=True),
            expiry=datetime.utcnow() + timedelta(hours=1),
        )

        service_client = DataLakeServiceClient(self.STORAGE_URL, credential=token)
        file_system_client = service_client.get_file_system_client(self.STORAGE_FILESYSTEM)
        paths = list(file_system_client.get_paths(storage_directory))
        
        for p in paths:
            print(p.name)



    def test_upload_download_data(self):
        registered_path = "demo-folder-allowed"
        invalid_path = "demo-folder-restricted"

        print("\nGenerating SAS for directory: {}".format(registered_path))

        # generate a token for a directory with all permissions
        token = generate_directory_sas(
            self.ACCOUNT_NAME,
            self.STORAGE_FILESYSTEM,
            registered_path,
            self.ACCOUNT_KEY,
            permission=FileSystemSasPermissions(read=True,write=True,delete=True,list=True),
            expiry=datetime.utcnow() + timedelta(hours=1),
        )

        # Try with a path that matches the SAS token
        try:
            self.inner_transfer(registered_path, token)
        except:
            print("Upload failed.")

        # Try with a path that doesnt match the SAS token. Should fail!
        try:
            self.inner_transfer(invalid_path, token)
        except:
            print("Upload failed.")   



    def inner_transfer(self, directory, token):
        basename = "upload"
        suffix = datetime.now().strftime("%y%m%d_%H%M%S")
        filename = "_".join([basename, suffix]) 
        data = self.get_random_bytes(200*1024)
        upload_path = "{}/{}".format(directory, filename)

        print("\nUploading {} to directory: {}".format(filename, directory))

        service_client = DataLakeServiceClient(self.STORAGE_URL, credential=token)
        file_client = service_client.get_file_client(self.STORAGE_FILESYSTEM, upload_path)
        file_client.upload_data(data, overwrite=True, max_concurrency=3)

        print("Upload complete. Re-downloading file...")

        downloaded_data = file_client.download_file().readall()
        print("Downloaded file. Bytes read: {}".format(len(downloaded_data)))


if __name__ == '__main__':
    sample = SASSamples()
    sample.test_using_directory_sas_to_read()
    sample.test_upload_download_data()
