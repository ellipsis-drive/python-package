# Vector layer


```{toctree}
---
maxdepth: 3
---
feature/index
featureProperty/index
order/index
style/index
upload/index
```

## add

    ellipsis.path.vector.layer.add()

Adds a vector layer.

**Mandatory arguments**
- pathId (uuid),
- name (string),
- token (uuid), your token

**Optional arguments**
- properties (object), containing
- description (string), 

## edit

    ellipsis.path.vector.layer.edit()

Edits a vector layer.

**Mandatory arguments**
- pathId (uuid),
- layerId (uuid),
- name (string),
- token (uuid), your token

**Optional arguments**
- description (string), 

## archive

    ellipsis.path.vector.layer.archive()

Archives a vector layer.

**Mandatory arguments**
- pathId (uuid),
- layerId (uuid),
- token (uuid), your token

## recover

    ellipsis.path.vector.layer.recover()

Recovers a vector layer.

**Mandatory arguments**
- pathId (uuid),
- layerId (uuid),
- token (uuid), your token

## delete

    ellipsis.path.vector.layer.delete()

Delete a vector layer.

**Mandatory arguments**
- pathId (uuid),
- layerId (uuid),
- token (uuid), your token

## getBounds

    ellipsis.path.vector.layer.getBounds()

Gets the bounds of a vector layer.

**Mandatory arguments**
- pathId (uuid),
- layerId (uuid),
- token (uuid), your token

## getChanges

    ellipsis.path.vector.layer.getChanges()

**Mandatory arguments**
- pathId (uuid),
- layerId (uuid),

**Optional arguments**
- listAll (bool), whether to list all results (default False)
- pageStart (object),
- actions (object),
- token (uuid), your token

## editFilter

    ellipsis.path.vector.layer.editFilter()

**Mandatory arguments**
- pathId (uuid),
- layerId (uuid),
- token (uuid), your token
- propertyFilter (object)

## getFeaturesByIds

    ellipsis.path.vector.layer.getFeaturesByIds()

**Mandatory arguments**
- pathId (uuid),
- layerId (uuid),
- featureIds (list of uuids),

**Optional arguments**
- token (uuid), your token

## getFeaturesByExtent

    ellipsis.path.vector.layer.getFeaturesByIds()

**Mandatory arguments**
- pathId (uuid),
- layerId (uuid),
- extent (bounds object)

**Optional arguments**
- token (uuid), your token
- propertyFilter
- pageStart
- listAll (bool), whether to list all results (default False)

## listFeatures

    ellipsis.path.vector.layer.listFeatures()

**Mandatory arguments**
- pathId (uuid),
- layerId (uuid),

**Optional arguments**
- token (uuid), your token
- pageStart
- listAll (bool), whether to list all results (default False)