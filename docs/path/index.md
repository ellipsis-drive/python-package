# Path

```{toctree}
---
maxdepth: 5
---
invites/index
hashtags/index
members/index
raster/index
vector/index
```

## searchRaster

    ellipsis.path.searchRaster()

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
- fuzzySearchOnLayerName (bool)

## searchFolder

    ellipsis.path.searchFolder()

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

**Mandatory arguments**

- pathId (uuid)
- token (string)
-

## unfavorite

    ellipsis.path.unfavorite()

**Mandatory arguments**

- pathId (uuid)
- token (string)

## editPublicAccess

    ellipsis.path.editPublicAccess()

**Mandatory arguments**

- pathId (uuid)
- token (string)

**Optional arguments**

- geoFence (object)
- accessLevel (int)
- processingUnits (integer)
- hidden (boolean)

## listMaps

    ellipsis.path.listMaps()

**Mandatory arguments**

- pathId (uuid)

**Optional arguments**

- token (string)
- pageStart (uuid)
- listAll (boolean)

## listFolders

    ellipsis.path.listFolders()

**Mandatory arguments**

- pathId (uuid)

**Optional arguments**

- token (string)
- pageStart (uuid)
- listAll (boolean)

## editMetadata

    ellipsis.path.editMetadata()

**Mandatory arguments**

- pathId (uuid)
- token (string)

**Optional arguments**

- attribution (string)
- description (string)
- properties (object)

## get

    ellipsis.path.get()

**Mandatory arguments**

- pathId (uuid)

**Optional arguments**

- token (string)

## move

    ellipsis.path.move()

**Mandatory arguments**

- pathIds (array of uuids)

**Optional arguments**

- token (string)
- parentId (uuid)

## rename

    ellipsis.path.rename()

**Mandatory arguments**

- pathId (uuid)

**Optional arguments**

- token (string)
- name (string)

## trash

    ellipsis.path.trash()

**Mandatory arguments**

- pathId (uuid)

**Optional arguments**

- token (string)

## add

    ellipsis.path.add()

**Mandatory arguments**

- pathType (string)
- name (string)
- token (string)

**Optional arguments**

- parentId (uuid)
- metadata (object)
- publicAccess (object)
-

## delete

    ellipsis.path.delete()

**Mandatory arguments**

- pathId (uuid)

**Optional arguments**

- recursive (boolean)
- token (string)

## recover

    ellipsis.path.recover()

**Mandatory arguments**

- pathId (uuid)

**Optional arguments**

- token (string)
