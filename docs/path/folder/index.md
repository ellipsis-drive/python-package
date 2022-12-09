# folders

## add

    ellipsis.path.folder.add()

Adds a folder.

**Mandatory arguments**

- name (string) name for the folder
- token (string), your token

**Optional arguments**

- parentId (uuid) id of folder to place the new folder in
- publicAccess (dict) dictionary describing the public access of the folder
- metadata (dict) dictionary describing the metadata of the folder


## listFolder

    ellipsis.path.folder.listFolder()

List the content of a folder

**Mandatory arguments**

- pathId (uuid) id of the folder


**Optional arguments**
- pathTypes (list) list containing 'file', 'folder', 'raster' or 'vector'
- pageStart (uuid), from where to start the listing
- listAll (boolean), wether to get all results or only the first page
- token (string), your token



