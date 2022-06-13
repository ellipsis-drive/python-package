# Upload

## upload

    ellipsis.path.vector.layer.upload.upload()

**Mandatory arguments**
- pathId (uuid)
- layerId (uuid)
- filePath (string)
- token (string)

**Optional arguments**
- epsg (int)
- fileFormat (string)
- dateColumns (array of strings)
- datePatterns (array of strings)

## get

    ellipsis.path.vector.layer.upload.get()

**Mandatory arguments**
- pathId (uuid)
- layerId (uuid)
- token (string)

**Optional arguments**
- pageStart (uuid)
- listAll (bool), default True