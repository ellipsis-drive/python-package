# Welcome to Ellipsis' documentation!


This is the documentation for the official python package of [Ellipsis Drive](https://ellipsis-drive.com/).
You can find the source code of the package at <https://github.com/ellipsis-drive/python-package>.
The package eases the use of the Ellipsis Drive API, by wrapping many of the API calls in python functions and adding some more intricate functions as well.

## Examples

**General usage**

Retrieving all items in "My Drive".

    import ellipsis as el

    # log in
    token = el.account.logIn("username", "password")

    # retrieve all items in "My Drive"
    items = el.account.listRoot("myDrive", pathTypes = ['folder', 'raster','vector','file'], token=token)

Retrieve all layers and folders inside a specific folder, and retreive information about the folder itself.

    import ellipsis as el

    folderId = '46e1e919-8b73-42a3-a575-25c6d45fd93b'

    token = el.account.logIn("username", "password")

    info = el.path.get(folderId, token)
    items = el.path.listPath(folderId, pathTypes = ['folder', 'raster','vector','file'], token = token, listAll = True)

**Uploading files**

The below example uploads a raster file.

    import ellipsis as el

    pathToYourLocalFile = ""
    
    token = el.account.logIn("username", "password")
    rasterLayerId = el.path.raster.add( "some name", token)['id']
    timestampId = el.path.raster.timestamp.add(rasterLayerId, token)['id']
    el.path.raster.timestamp.file.add(pathId =rasterLayerId, timestampId=timestampId, filePath= pathToYourLocalFile, fileFormat='tif', token=token)
    #don't forget to activate the timestamp once upload is completed
    el.path.raster.timestamp.activate(rasterLayerId, timestampId, token)


Similarly, the below example uploads a vector file.

    import ellipsis as el

    pathToYourLocalFile = ""

    token = el.account.logIn("username", "password")
    vectorLayerId = el.path.vector.add( "some name", token)['id']
    timestampId = el.path.vector.timestamp.add(vectorLayerId, token)['id']
    el.path.vector.timestamp.file.add(vectorLayerId, timestampId, pathToYourLocalFile, token)

```{toctree}
---
maxdepth: 10
caption: Contents
---
account/index
user/index
path/index
view/index
util/index
```

&nbsp;
&nbsp;
