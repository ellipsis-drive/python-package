# files

## add

    ellipsis.path.file.add()

Adds a file.

**Mandatory arguments**

- token (string), your token

**Optional arguments**

- filePath (string) path to file on local disk, required if no memFile is given
- memFile (bytes) a bytesIO memory file, required if no filePath is given
- name (string), the name for the file, only required in the case of a memFile
- parentId (uuid) id of folder to place the new folder in
- publicAccess (dict) dictionary describing the public access of the folder
- metadata (dict) dictionary describing the metadata of the folder


## download

    ellipsis.path.file.download()

Downloads a file

**Mandatory arguments**

- pathId (uuid) id of the folder
- filePath (string) location to download your file to


**Optional arguments**
- token (string), your token


## addPickle

    ellipsis.path.file.addPickle()

Pickles a Python object and adds it as a file.

**Mandatory arguments**

- x (any Python object) python object to be stored
- token (string), your token

**Optional arguments**

- parentId (uuid) id of folder to place the new folder in
- publicAccess (dict) dictionary describing the public access of the folder
- metadata (dict) dictionary describing the metadata of the folder


## getPickle

    ellipsis.path.file.getPickle()

Retrieves a file and returns it as a Python object

**Mandatory arguments**

- pathId (uuid) id of the folder


**Optional arguments**
- token (string), your token


## addCsv

    ellipsis.path.file.addCsv()

Stores a Pandas data frame as a csv.

**Mandatory arguments**

- df (Pandas DataFrame) data frame to be stored
- token (string), your token

**Optional arguments**

- parentId (uuid) id of folder to place the new folder in
- publicAccess (dict) dictionary describing the public access of the folder
- metadata (dict) dictionary describing the metadata of the folder


## getCsv

    ellipsis.path.file.getCsv()

Retrieves a file and returns it as a Pandas DataFrame

**Mandatory arguments**

- pathId (uuid) id of the folder


**Optional arguments**
- token (string), your token

## addJson

    ellipsis.path.file.addJson()

Stores a json serializable Python object as a JSON.

**Mandatory arguments**

- d (JSON serializable object) dictionary to be stored
- token (string), your token

**Optional arguments**

- parentId (uuid) id of folder to place the new folder in
- publicAccess (dict) dictionary describing the public access of the folder
- metadata (dict) dictionary describing the metadata of the folder


## getJson

    ellipsis.path.file.getJson()

Retrieves a file and returns it as a dictionary

**Mandatory arguments**

- pathId (uuid) id of the folder


**Optional arguments**
- token (string), your token

