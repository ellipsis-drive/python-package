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

- date (dictionary with properties to and from, both of type date)
- description (string)

## edit

    ellipsis.path.raster.timestamp.edit()

Edit a timestamp of a raster map.

**Mandatory arguments**

- token (string)
- pathId (pathId)
- timestampId (uuid)

**Optional arguments**

- date (dictionary with properties to and from, both of type date)
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

## deactivate

    ellipsis.path.raster.timestamp.deactivate()

Deactivate a timestamp.

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

## analyse

    ellipsis.path.raster.timestamp.analyse()

Request to obtain the aggregated data for a certain geometry.

**Mandatory arguments**

- pathId (uuid)
- timestampIds (array of uuids)
- geometry (shapely geometry), a GeoJSON of the area of interest in WGS84

**Optional arguments**
- approximate (boolean) default True
- token (string)
- returnType (one of 'all' or 'statistics') default 'all'

## getRaster

    ellipsis.path.raster.timestamp.getRaster()

Get a raster.

**Mandatory arguments**

- extent (a dictionary with properties xMin, xMax, yMin, yMax of type float)
- pathId (uuid)
- timestampId (uuid)

**Optional arguments**

- token (string)
- style (either uuid or dictionary describing a style). If no style given raw data is returned. Also see https://docs.ellipsis-drive.com/developers/api-v3/path-raster/styles/add-style
- threads (integer) default 1
- showProgress (bool) default True

## getDownsampledRaster

    ellipsis.path.raster.timestamp.getDownsampledRaster()

Get a downsampled raster.

**Mandatory arguments**

- pathId (uuid)
- timestampId (uuid)
- extent (a dictionary with properties xMin, xMax, yMin, yMax of type float)
- width (int)
- height (int)

**Optional arguments**

- style (either uuid or dictionary describing a style). If no style given raw data is returned. Also see https://docs.ellipsis-drive.com/developers/api-v3/path-raster/styles/add-style
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
