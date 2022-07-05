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

Add a timestamp to a raster map.

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

Edit a timestamp of a raster map.

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

Delete a timestamp of a raster map.

**Mandatory arguments**

- token (string)
- pathId (uuid)
- timestampId (uuid)

## activate

    ellipsis.path.raster.timestamp.activate()

Activate a timestamp.

**Mandatory arguments**

- token (string)
- pathId (uuid)
- timestampId (uuid)

## getBounds

    ellipsis.path.raster.timestamp.getBounds()

Request to obtain the aggregated data for a certain geometry.

**Mandatory arguments**

- pathId (uuid)
- timestampId (uuid)

**Optional arguments**

- token (string)

## getAggregatedData

    ellipsis.path.raster.timestamp.getAggregatedData()

Request to obtain the aggregated data for a certain geometry.

**Mandatory arguments**

- pathId (uuid)
- timestampIds (array of uuids)
- approximate (boolean)
- geometry (shapely geometry), a GeoJSON of the area of interest in WGS84

**Optional arguments**

- token (string)

## getRaster

    ellipsis.path.raster.timestamp.getRaster()

Get a raster.

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

Get a downsampled raster.

**Mandatory arguments**

- pathId (uuid)
- timestampId (uuid)
- extent (bounds object)

**Optional arguments**

- layer (object)
- token (string)

## trash

    ellipsis.path.raster.timestamp.trash()

Place a timestamp in the trash.

**Mandatory arguments**

- token (string)
- pathId (uuid)
- timestampId (uuid)

## recover

    ellipsis.path.raster.timestamp.recover()

Recover a timestamp from your trash.

**Mandatory arguments**

- token (string)
- pathId (uuid)
- timestampId (uuid)
