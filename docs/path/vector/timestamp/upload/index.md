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
- method (string) one of simplify or full. In case of simplify lower level geometries are created to increase rendering performance.
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
