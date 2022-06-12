# Feature

## add

    ellipsis.path.vector.layer.feature.add()

Add a feature.

**Mandatory arguments**
- pathId (uuid)
- layerId (uuid)
- features (geopandas dataframe)
- token (string)

**Optional arguments**
- zoomlevels (array of integers)

## edit

    ellipsis.path.vector.layer.feature.edit()

Edit a feature.

**Mandatory arguments**
- pathId (uuid)
- layerId (uuid)
- featureIds (array of uuids)
- token (string)

**Optional arguments**
- zoomlevels (array of integers)
- features (geopandas dataframe)

## delete

    ellipsis.path.vector.layer.feature.delete()

Delete a feature.

**Mandatory arguments**
- pathId (uuid)
- layerId (uuid)
- featureIds (array of uuids)
- token (string)

## recover

    ellipsis.path.vector.layer.feature.recover()

Recover a feature.

**Mandatory arguments**
- pathId (uuid)
- layerId (uuid)
- featureIds (array of uuids)
- token (string)

## versions

    ellipsis.path.vector.layer.feature.versions()

**Mandatory arguments**
- pathId (uuid)
- layerId (uuid)
- featureIds (array of uuids)

**Optional arguments**
- pageStart (uuid)
- listAll (bool), whether to list all results or only the first page (default False)
- token (string)
