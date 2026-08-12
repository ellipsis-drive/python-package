# File

## add

    ellipsis.path.mesh.timestamp.file.add()

Upload a mesh file.

**Mandatory arguments**

- token (string)
- pathId (uuid)
- timestampId (uuid)


**Optional arguments**

- filePath (string) path to file on local disk, required if no memFile is given
- memFile (bytes) a bytesIO memory file, required if no filePath is given
- name (string), the name for the file, only required in the case of a memFile

## get

    ellipsis.path.mesh.timestamp.file.get()

Get all uploads for a given timestamp.

**Mandatory arguments**

- token (string)
- pathId (uuid)
- timestampId (uuid)

**Optional arguments**

- pageStart (uuid)
- listAll (boolean), default true


## trash

    ellipsis.path.mesh.timestamp.file.trash()

Trashes an uploaded file.

**Mandatory arguments**

- token (string)
- pathId (uuid)
- fileId (uuid)
- timestampId)

## recover

    ellipsis.path.mesh.timestamp.file.recover()

Recovers a trashed upload.

**Mandatory arguments**

- token (string)
- pathId (uuid)
- fileId (uuid)
- timestampId)

## delete

    ellipsis.path.mesh.timestamp.file.delete()

Delete a given upload.

**Mandatory arguments**

- token (string)
- pathId (uuid)
- fileId (uuid)
- timestampId)

## download

    ellipsis.path.mesh.timestamp.file.download()

Downloads a previously uploaded file.

**Mandatory arguments**

- token (string)
- pathId (uuid)
- fileId (uuid)
- timestampId)



