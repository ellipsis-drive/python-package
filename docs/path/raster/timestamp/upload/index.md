# Upload

## upload

    ellipsis.path.raster.timestamp.upload.add()

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

    ellipsis.path.raster.timestamp.upload.get()

Get all uploads for a given timestamp.

**Mandatory arguments**

- token (string)
- pathId (uuid)
- timestampId (uuid)

**Optional arguments**

- pageStart (uuid)
- listAll (boolean), default true

## delete

    ellipsis.path.raster.timestamp.upload.delete()

Delete a given upload.

**Mandatory arguments**

- token (string)
- pathId (uuid)
- uploadId (uuid)
- timestampId)
