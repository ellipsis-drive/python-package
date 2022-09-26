# Vector timestamp

```{toctree}
---
maxdepth: 3
---
feature/index
order/index
style/index
upload/index
```

## add

    ellipsis.path.vector.timestamp.add()

Adds a vector timestamp.

**Mandatory arguments**

- pathId (uuid),
- name (string),
- token (uuid), your token

**Optional arguments**

- properties (object), containing
- description (string),

## edit

    ellipsis.path.vector.timestamp.edit()

Edits a vector timestamp.

**Mandatory arguments**

- pathId (uuid),
- timestampId (uuid),
- name (string),
- token (uuid), your token

**Optional arguments**

- description (string),

## archive

    ellipsis.path.vector.timestamp.archive()

Archives a vector timestamp.

**Mandatory arguments**

- pathId (uuid),
- timestampId (uuid),
- token (uuid), your token

## recover

    ellipsis.path.vector.timestamp.recover()

Recovers a vector timestamp.

**Mandatory arguments**

- pathId (uuid),
- timestampId (uuid),
- token (uuid), your token

## delete

    ellipsis.path.vector.timestamp.delete()

Delete a vector timestamp.

**Mandatory arguments**

- pathId (uuid),
- timestampId (uuid),
- token (uuid), your token

## getBounds

    ellipsis.path.vector.timestamp.getBounds()

Gets the bounds of a vector timestamp.

**Mandatory arguments**

- pathId (uuid),
- timestampId (uuid),
- token (uuid), your token

## getChanges

    ellipsis.path.vector.timestamp.getChanges()

**Mandatory arguments**

- pathId (uuid),
- timestampId (uuid),

**Optional arguments**

- listAll (boolean), whether to list all results (default False)
- pageStart (object),
- actions (object),
- token (uuid), your token

## editFilter

    ellipsis.path.vector.timestamp.editFilter()

**Mandatory arguments**

- pathId (uuid),
- timestampId (uuid),
- token (uuid), your token
- propertyFilter (object)

## getFeaturesByIds

    ellipsis.path.vector.timestamp.getFeaturesByIds()

**Mandatory arguments**

- pathId (uuid),
- timestampId (uuid),
- featureIds (list of uuids),

**Optional arguments**

- token (uuid), your token

## getFeaturesByExtent

    ellipsis.path.vector.timestamp.getFeaturesByIds()

**Mandatory arguments**

- pathId (uuid),
- timestampId (uuid),
- extent (bounds object)

**Optional arguments**

- token (uuid), your token
- propertyFilter
- pageStart
- listAll (boolean), whether to list all results (default False)

## listFeatures

    ellipsis.path.vector.timestamp.listFeatures()

**Mandatory arguments**

- pathId (uuid),
- timestampId (uuid),

**Optional arguments**

- token (uuid), your token
- pageStart
- listAll (boolean), whether to list all results (default False)


## activate

    ellipsis.path.vector.timestamp.activate()

Activate a timestamp.

**Mandatory arguments**

- token (string)
- pathId (uuid)
- timestampId (uuid)

## pause

    ellipsis.path.vector.timestamp.pause()

Pause a timestamp.

**Mandatory arguments**

- token (string)
- pathId (uuid)
- timestampId (uuid)
