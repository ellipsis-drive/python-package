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


## traverse

    ellipsis.path.folder.traverse()

Traverse a folder to find a specific path

**Mandatory arguments**

- pathId (uuid) id of the folder you wish to traverse
- pathType (string) one of 'file', 'folder', 'raster', 'pointCloud' or 'vector'
- location (array of strings), the path via which you would like to traverse the folder

**Optional arguments**
- token (string), your token

