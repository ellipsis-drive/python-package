# SetUpTasks

## get

    ellipsis.path.setUpTask.get()

Get a list of your previous tasks

**Mandatory arguments**
- token (string) a valid token


## copernicusImport

    ellipsis.path.setUpTask.copernicusImport()

Create a task to import a Copernicus asset as an Ellipsis Drive layer

**Mandatory arguments**

- Parameters (dict) A dictionary containing as it's keys collection, assetId and optionally parentId. Collection should be one of 'sentinel1' or 'sentinel2'. AssetId should be the id of the asset. ParentId should be the id of the Ellipsis Drive folder to place the asset into. 
- token (string) a valid token

## fileImport

    ellipsis.path.setUpTask.fileImport()

Create a task to import layers from a certain file

**Mandatory arguments**

- token (string) a valid token



**Optional arguments**
- parentId (string) The id of the Ellipsis Drive folder to write the layers to. 
- fileFormat (string) the fileFormat, defaults to geopackage.
- filePath (string) the location of the file to import the layers from on your local disk.
- memFile (memory file) the memory file to import the layers from
- name (string) the name under which to import

