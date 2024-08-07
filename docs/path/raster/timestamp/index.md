# Timestamp

```{toctree}
---
maxdepth: 2
---
order/index
file/index
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

Request to obtain pixel values within a certain geometry.

**Mandatory arguments**

- pathId (uuid)
- timestampIds (array of uuids)
- geometry (shapely geometry in WGS84)

**Optional arguments**
- approximate (boolean) default True
- token (string)
- returnType (one of 'all' or 'statistics') default 'all'


## contour

    ellipsis.path.raster.timestamp.contour()

Request to obtain the contour lines for a raster in a certain extent

**Mandatory arguments**

- pathId (uuid)
- timestampId (uuid)
- extent (a dictionary with properties xMin, xMax, yMin, yMax of type float)

**Optional arguments**
- bandNumber (int) band number of the raster to get the contour lines for. Count starts at 1
- interval (float) contour interval to use, required if intervals not given
- intervals (list of floats) exact intervals of the desired contour lines
- token (string)
- epsg (int) the espg code of the coordinate system of the coordinates of the extent


## getRaster

    ellipsis.path.raster.timestamp.getRaster()

Get a raster.

**Mandatory arguments**

- extent in the coordinates of the epsg specified (a dictionary with properties xMin, xMax, yMin, yMax of type float)
- pathId (uuid)
- timestampId (uuid)

**Optional arguments**

- token (string)
- reproject (boolean) whether to reproject the output raster to the coordiante system of the given extent
- showProgress (bool) default True
- epsg (int), epsg code of the coordinate system of the extent. default 3857 (webmercator)

## getSampledRaster

    ellipsis.path.raster.timestamp.getDownsampledRaster()

Get a downsampled raster.

**Mandatory arguments**

- pathId (uuid)
- timestampId (uuid)
- extent (a dictionary with properties xMin, xMax, yMin, yMax of type float)
- width (int)
- height (int)

**Optional arguments**

- epsg (int), epsg code of the coordinate system of the extent. default 3857 (webmercator)
- token (string)

## getLocationInfo

    ellipsis.path.raster.timestamp.getLocationInfo()

Get raster values for a list of locations.

**Mandatory arguments**

- pathId (uuid)
- timestampId (uuid)
- locations. List containing points of interest. Each element in the list should be a list with two floats (list)

**Optional arguments**

- epsg (int), epsg code of the coordinate system of the input locations default 4326 (WGS84)
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
