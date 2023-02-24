# Path

```{toctree}
---
maxdepth: 5
---
raster/index
vector/index
folder/index
file/index
invite/index
hashtag/index
member/index
usage/index
```

## searchRaster

    ellipsis.path.searchRaster()

Search for rasters matching specified search criteria.

**Mandatory arguments**
- pathTypes (array containing 'raster', 'vector', 'folder', 'file')

**Optional arguments**
- token (string)
- root (array of strings containing 'myDrive', 'sharedWithMe', 'favorite', 'public')
- text (string)
- userId (uuid)
- pageStart (uuid, use None to start at begining)
- hashtag (string)
- listAll (boolean)
- active (boolean)
- extent (a dictionary with properties xMin, xMax, yMin, yMax of type float)
- date (dictionary with keys from and to, both should be python dates)
- resolution (dictionary with min and max, both shoudl be float)


## favorite

    ellipsis.path.favorite()

Add path to favorites.

**Mandatory arguments**

- pathId (uuid)
- token (string)

## unfavorite

    ellipsis.path.unfavorite()

Remove path from favorites.

**Mandatory arguments**

- pathId (uuid)
- token (string)

## editPublicAccess

    ellipsis.path.editPublicAccess()

Update the public access of a path.

**Mandatory arguments**

- pathId (uuid)
- token (string)

**Optional arguments**

- geoFence (object)
- accessLevel (integer)
- processingUnits (integer)
- hidden (boolean)

## editMetadata

    ellipsis.path.editMetadata()

Update the metadata of a path.

**Mandatory arguments**

- pathId (uuid)
- token (string)

**Optional arguments**

- attribution (string)
- description (string)
- properties (object)

## get

    ellipsis.path.get()

Retrieves a path.

**Mandatory arguments**

- pathId (uuid)

**Optional arguments**

- token (string)

## move

    ellipsis.path.move()

Moves paths to a different folder.

**Mandatory arguments**

- pathIds (array of uuids)

**Optional arguments**

- token (string)
- parentId (uuid)

## rename

    ellipsis.path.rename()

Rename a path.

**Mandatory arguments**

- pathId (uuid)

**Optional arguments**

- token (string)
- name (string)

## trash

    ellipsis.path.trash()

Place path in trash.

**Mandatory arguments**

- pathId (uuid)

**Optional arguments**

- token (string)

## delete

    ellipsis.path.delete()

Delete a path.

**Mandatory arguments**

- pathId (uuid)

**Optional arguments**

- recursive (boolean)
- token (string)

## recover

    ellipsis.path.recover()

Recover a path.

**Mandatory arguments**

- pathId (uuid)

**Optional arguments**

- token (string)
