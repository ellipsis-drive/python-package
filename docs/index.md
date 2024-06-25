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

Retrieve metadata for a specific layer with id.

    import ellipsis as el

    layerId = '46e1e919-8b73-42a3-a575-25c6d45fd93b'

    token = el.account.logIn("username", "password")

    info = el.path.get(folderId, token)

Find layers matching certain search criteria.

    import ellipsis as el

    token = el.account.logIn("username", "password")

    result = el.path.search(pathTypes = ['raster', 'vector'], extent= {'xMin': -20, 'xmax':10, 'yMin':23, 'yMax':40}, text='test', token = token )


ALL RELEVANT METADATA OF A LAYER/FOLDER CAN BE FOUND IN THE METADATA DICTIONARY THAT IS RETURNED IN THESE FUNCTIONS.

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


**Fetching data**

The below example fetches a raster as a numpy array.

    import ellipsis as el
    
    token = el.account.logIn("username", "password")
    rasterLayerId = "173bf9f0-b28b-418f-bfa8-5d3436ec0dd7"
    timestampId = "a8ec20d6-9571-4f44-a411-caf0f916af69"
    
    extent = {"yMax":-2.29048,  "xMax": 55.04837, "yMin": -2.26255 "xMin": 55.04037}

    r = el.path.raster.timestamp.getRaster(pathId =rasterLayerId, timestampId=timestampId, extent = extent, epsg = 4326, token=token)

    el.util.plotRaster(r)


Similarly, you can fetch vector data from a layer as a geopandas dataframe.

    import ellipsis as el
    
    token = el.account.logIn("username", "password")
    vectorLayerId = "312907b1-9bab-4776-b271-413e7596cf1a"
    timestampId = "6e9b7020-ba52-4cbc-94ea-5c2c14927233"
    
    extent = {"yMax":-2.29048,  "xMax": 55.04837, "yMin": -2.26255 "xMin": 55.04037}

    r = el.path.vector.timestamp.getFeaturesByExtent(pathId =vectorLayerId, timestampId=timestampId, extent = extent, epsg = 4326, token=token)

    el.util.plotVector(r)

```{toctree}
---
maxdepth: 10
caption: Contents
---
account/index
user/index
path/index
util/index
```

&nbsp;
&nbsp;
