# File

## add

    ellipsis.path.vector.timestamp.file.add()

**Mandatory arguments**

- pathId (uuid)
- timestampId (uuid)
- token (string)

**Optional arguments**

- filePath (string) path to file on local disk, required if no memFile is given
- memFile (bytes) a bytesIO memory file, required if no filePath is given
- name (string), the name for the file, only required in the case of a memFile
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

