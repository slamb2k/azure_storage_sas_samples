# azure_storage_sas_samples
Just playing around with Azure Storage Service SAS

### Use Cases ###
    
1. **GENERATE** a valid token using the Python SDK for a Service SAS at a directory level. (sr=d)
2. The directory contents of a location specified in the generated SAS token **CAN** be retrieved.
3. A file **CAN** be uploaded to or downloaded from the location specified in the SAS token.
4. An attempt to upload or download a file using a location **NOT** in the SAS token should fail. 

### Examples ###

Using the Azure Storage Python SDK, the following examples are implemented:

1. Generates a SAS token for a specific directory and lists the contents

```
    # generate a token for a directory with all permissions
    token = generate_directory_sas(
        self.ACCOUNT_NAME,
        self.STORAGE_FILESYSTEM,
        storage_directory,
        self.ACCOUNT_KEY,
        permission=FileSystemSasPermissions(read=True,write=True,delete=True,list=True),
        expiry=datetime.utcnow() + timedelta(hours=1),
    )
```

2. Generates a SAS token for a specific directory and using this token:
    1. Uploads a file containing random data to the same directory.
    2. Downloads the same file again.

```
    # Try with a path that matches the SAS token
    try:
        self.inner_upload(registered_path, token)
    except:
        print("Upload failed.")
```

3. Using the SAS token from the previous step:
    1. Uploads a file containing random data to the a different directory.  
    2. Downloads the same file again.
    
```    
    # Try with a path that doesnt match the SAS token. Should fail!
    try:
        self.inner_upload(invalid_path, token)
    except:
        print("Upload failed.")   
```
