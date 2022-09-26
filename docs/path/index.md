# Path

```{toctree}
---
maxdepth: 5
---
raster/index
vector/index
invites/index
hashtags/index
member/index
```

## searchRaster

    ellipsis.path.searchRaster()

Search for rasters matching specified search criteria.

**Optional arguments**

- token (string)
- root (array of strings)
- listAll (boolean)
- name (string)
- fuzzySearchOnName (boolean)
- userId (uuid)
- disabled (boolean)
- canView (boolean)
- pageStart (uuid)
- hashtag (string)
- bounds (bounds object)
- bands (array of strings)
- dateFrom (date object)
- dateTo (date object)
- hasTimestamp (boolean)
- timestampSize (float)
- resolution (array of floats)

## searchVector

    ellipsis.path.searchVector()

Search for vectors matching specified search criteria.

**Optional arguments**

- token (string)
- root (array of strings)
- listAll (boolean)
- name (string)
- fuzzySearchOnName (boolean)
- userId (uuid)
- disabled (boolean)
- canView (boolean)
- pageStart (uuid)
- hashtag (string)
- bounds (bounds object)
- hasVectorLayers (boolean)
- layerNAme (string)
- fuzzySearchOnLayerName (boolean)

## searchFolder

    ellipsis.path.searchFolder()

Search for folders matching specified search criteria.

**Optional arguments**

- token (string)
- listAll (boolean)
- root (array of strings)
- name (string)
- fuzzySearchOnName (boolean)
- userId (uuid)
- pageStart (uuid)

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

## listMaps

    ellipsis.path.listMaps()

List all maps in a pathId.

**Mandatory arguments**

- pathId (uuid)

**Optional arguments**

- token (string)
- pageStart (uuid)
- listAll (boolean)

## listFolders

    ellipsis.path.listFolders()

List all folders in a pathId.

**Mandatory arguments**

- pathId (uuid)

**Optional arguments**

- token (string)
- pageStart (uuid)
- listAll (boolean)

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

## add

    ellipsis.path.add()

Create a new folder or map.

**Mandatory arguments**

- pathType (string), should be 'folder', 'raster' or 'vector'
- name (string)
- token (string)

**Optional arguments**

- parentId (uuid)
- metadata (object), object with properties, attribution and description
- publicAccess (object)

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
