# files

## add

    ellipsis.path.file.add()

Adds a file.

**Mandatory arguments**

- filePath (string) path to the file to upload
- token (string), your token

**Optional arguments**

- parentId (uuid) id of folder to place the new folder in
- publicAccess (dict) dictionary describing the public access of the folder
- metadata (dict) dictionary describing the metadata of the folder


## download

    ellipsis.path.folder.listFolder()

Downloads a file

**Mandatory arguments**

- pathId (uuid) id of the folder
- filePath (string) location to download your file to


**Optional arguments**
- token (string), your token



