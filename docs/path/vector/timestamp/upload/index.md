# Upload

## add

    ellipsis.path.vector.timestamp.upload.add()

**Mandatory arguments**

- pathId (uuid)
- timestampId (uuid)
- filePath (string)
- token (string)

**Optional arguments**

- epsg (integer)
- fileFormat (string)
- dateColumns (array of strings)
- datePatterns (array of strings)

## get

    ellipsis.path.vector.timestamp.upload.get()

**Mandatory arguments**

- pathId (uuid)
- timestampId (uuid)
- token (string)

**Optional arguments**

- pageStart (uuid)
- listAll (boolean), default True
