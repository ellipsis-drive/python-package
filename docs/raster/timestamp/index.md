# Timestamp

```{toctree}
---
maxdepth: 2
---
order/index
upload/index
```

## add

    ellipsis.path.raster.timestamp.add()

**Mandatory arguments**

- token (string)
- pathId (pathId)

**Optional arguments**

- dateFrom (date), default current time
- dateTo (date), default current time
- description (string)
- appendToTimestampId (uuid)

## edit

    ellipsis.path.raster.timestamp.edit()

**Mandatory arguments**

- token (string)
- pathId (pathId)
- timestampId (uuid)

**Optional arguments**

- dateFrom (date)
- dateTo (date)
- description (string)

## delete

    ellipsis.path.raster.timestamp.delete()

**Mandatory arguments**

- token (string)
- pathId (uuid)
- timestampId (uuid)

## activate

    ellipsis.path.raster.timestamp.activate()

**Mandatory arguments**

- token (string)
- pathId (uuid)
- timestampId (uuid)

## getBounds

    ellipsis.path.raster.timestamp.getBounds()

**Mandatory arguments**

- pathId (uuid)
- timestampId (uuid)

**Optional arguments**

- token (string)

## getAggregatedData

    ellipsis.path.raster.timestamp.getAggregatedData()

**Mandatory arguments**

- pathId (uuid)
- timestampIds (array of uuids)
- approximate (boolean)
- geometry (shapely geometry)

**Optional arguments**

- token (string)

## getRaster

    ellipsis.path.raster.timestamp.getRaster()

**Mandatory arguments**

- extent (bounds)
- threads (integer)
- pathId (uuid)
- timestampId (uuid)

**Optional arguments**

- token (string)
- layer (object)

## getDownsampledRaster

    ellipsis.path.raster.timestamp.getDownsampledRaster()

**Mandatory arguments**

- pathId (uuid)
- timestampId (uuid)
- extent (bounds object)

**Optional arguments**

- layer (object)
- token (string)

## trash

    ellipsis.path.raster.timestamp.trash()

**Mandatory arguments**

- token (string)
- pathId (uuid)
- timestampId (uuid)

## recover

    ellipsis.path.raster.timestamp.recover()

**Mandatory arguments**

- token (string)
- pathId (uuid)
- timestampId (uuid)
