# Upload

## add

    ellipsis.path.vector.timestamp.file.add()

**Mandatory arguments**

- pathId (uuid)
- timestampId (uuid)
- filePath (string)
- token (string)

**Optional arguments**

- epsg (integer)
- method (string) either 'simplify' or 'full'. In case of simplify lower level geometries are created to increase rendering performance.
- fileFormat (string)
- dateColumns (array of strings)
- datePatterns (array of strings)

## get

    ellipsis.path.vector.timestamp.file.get()

**Mandatory arguments**

- pathId (uuid)
- timestampId (uuid)

**Optional arguments**
- token (string)
- pageStart (uuid)
- listAll (boolean), default True


## download

    ellipsis.path.vector.timestamp.file.download()

**Mandatory arguments**

- pathId (uuid)
- fileId (uuid)
- timestampId (uuid)

**Optional arguments**
- token (string)

