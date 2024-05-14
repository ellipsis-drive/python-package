# Feature

```{toctree}
---
maxdepth: 3
---
message/index
series/index
```

## add

    ellipsis.path.vector.timestamp.feature.add()

Add a feature.

**Mandatory arguments**

- pathId (uuid)
- timestampId (uuid)
- features (geopandas dataframe)
- token (string)



## edit

    ellipsis.path.vector.timestamp.feature.edit()

Edit a feature.

**Mandatory arguments**

- pathId (uuid)
- timestampId (uuid)
- featureIds (array of uuids)
- token (string)
- features (geopandas dataframe)


## trash

    ellipsis.path.vector.timestamp.feature.trash()

Delete a feature.

**Mandatory arguments**

- pathId (uuid)
- timestampId (uuid)
- featureIds (array of uuids)
- token (string)

## recover

    ellipsis.path.vector.timestamp.feature.recover()

Recover a feature.

**Mandatory arguments**

- pathId (uuid)
- timestampId (uuid)
- featureIds (array of uuids)
- token (string)

## versions

    ellipsis.path.vector.timestamp.feature.versions()

**Mandatory arguments**

- pathId (uuid)
- timestampId (uuid)
- featureIds (array of uuids)

**Optional arguments**

- pageStart (uuid)
- listAll (boolean), whether to list all results or only the first page (default False)
- token (string)
