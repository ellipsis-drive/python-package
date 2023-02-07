# File

## add

    ellipsis.path.raster.timestamp.file.add()

Upload a raster file.

**Mandatory arguments**

- token (string)
- pathId (uuid)
- timestampId (uuid)
- filePath (string)

**Optional arguments**

- noDataValue (float)
- epsg (integer)
- fileFormat (string)

## get

    ellipsis.path.raster.timestamp.file.get()

Get all uploads for a given timestamp.

**Mandatory arguments**

- token (string)
- pathId (uuid)
- timestampId (uuid)

**Optional arguments**

- pageStart (uuid)
- listAll (boolean), default true


## trash

    ellipsis.path.raster.timestamp.file.trash()

Trashes an uploaded raster file.

**Mandatory arguments**

- token (string)
- pathId (uuid)
- fileId (uuid)
- timestampId)

## recover

    ellipsis.path.raster.timestamp.file.recover()

Recovers a trashed uploaded raster file.

**Mandatory arguments**

- token (string)
- pathId (uuid)
- fileId (uuid)
- timestampId)

## delete

    ellipsis.path.raster.timestamp.file.delete()

Delete a given upload.

**Mandatory arguments**

- token (string)
- pathId (uuid)
- fileId (uuid)
- timestampId)

## download

    ellipsis.path.raster.timestamp.file.download()

Downloads a previously uploaded raster file.

**Mandatory arguments**

- token (string)
- pathId (uuid)
- fileId (uuid)
- timestampId)



