# Welcome to Ellipsis' documentation!

**Please note that we are currently still working on the documentation.**

This is the documentation for the official python package of [Ellipsis Drive](https://ellipsis-drive.com/).
You can find the source code of the package at <https://github.com/ellipsis-drive/python-package>.
The package eases the use of the Ellipsis Drive API, by wrapping many of the API calls in python functions and adding some more intricate functions as well.

## Examples

**Uploading files**

The below example uploads a raster file.

    import ellipsis as el

    token = el.account.logIn("username", "password")
    rasterMapId = el.path.add("raster", "some name", token)['id']
    timestampId = el.path.raster.timestamp.add(rasterMapId, token)
    el.path.raster.timestamp.upload.upload(rasterMapId, timestampId, pathToYourLocalFile, token)
    #don't forget to activate the timestamp once upload is completed
    el.path.raster.timestamp.activate(rasterMapId, timestampId, token)

Similarly, the below example uploads a vector file.

    import ellipsis as el

    token = el.account.logIn("username", "password")
    vectorMapId = el.path.add("vector", "some name", token)['id']
    layerId = el.path.vector.layer.add(vectorMapId, token)
    el.path.vector.layer.upload.upload(vectorMapId, layerId, pathToYourLocalFile, token)

**General usage**

Retrieving all maps in "My Drive".

    import ellipsis as el

    # log in
    token = el.account.logIn("username", "password")

    # retrieve all maps in "My Drive"
    maps = el.account.listRootMaps("myDrive", token=token)

Retrieve all maps and folders inside a specific folder, and retreive information about the folder itself.

    import ellipsis as el

    folderId = '46e1e919-8b73-42a3-a575-25c6d45fd93b'

    token = el.account.logIn("username", "password")

    info = el.path.get(folderId, token)
    maps = el.path.listMaps(folderId, token = token, listAll = True)
    folders = el.path.listFolders(folderId, token = token, listAll = True)

```{toctree}
---
maxdepth: 10
caption: Contents
---
account/index
user/index
path/index
raster/index
vector/index
```

&nbsp;
&nbsp;
