# Timestamp

```{toctree}
---
maxdepth: 2
---
order/index
file/index
```


## add

fetchPoints(pathId, timestampId, extent, token= None, epsg = 3857, zoom = None, showProgress = True)

Fetch points within a certain extent

**Mandatory arguments**

- pathId (pathId)
- timestampId (pathId)
- extent (dictionary with xMin, xMax, yMin, yMax as float)


**Optional arguments**
- token (string)
- epsg (espg code of extent as int)
- zoom (at which zoom to fetch the points, defaults to highest zoomlevel)
- showProgress (boolean indicating whether to show a loading bar)


## add

    ellipsis.path.pointCloud.timestamp.add()

Add a timestamp to a point cloud layer.

**Mandatory arguments**

- token (string)
- pathId (pathId)

**Optional arguments**

- date (dictionary with properties to and from, both of type date)
- description (string)

## edit

    ellipsis.path.pointCloud.timestamp.edit()

Edit a timestamp of a pointCloud layer.

**Mandatory arguments**

- token (string)
- pathId (pathId)
- timestampId (uuid)

**Optional arguments**

- date (dictionary with properties to and from, both of type date)
- description (string)

## delete

    ellipsis.path.pointCloud.timestamp.delete()

Delete a timestamp of a point cloud layer.

**Mandatory arguments**

- token (string)
- pathId (uuid)
- timestampId (uuid)

## activate

    ellipsis.path.pointCloud.timestamp.activate()

Activate a timestamp.

**Mandatory arguments**

- token (string)
- pathId (uuid)
- timestampId (uuid)

## deactivate

    ellipsis.path.pointCloud.timestamp.deactivate()

Deactivate a timestamp.

**Mandatory arguments**

- token (string)
- pathId (uuid)
- timestampId (uuid)

## getBounds

    ellipsis.path.pointCloud.timestamp.getBounds()

Request to obtain the aggregated data for a certain geometry.

**Mandatory arguments**

- pathId (uuid)
- timestampId (uuid)

**Optional arguments**

- token (string)



## trash

    ellipsis.path.pointCloud.timestamp.trash()

Place a timestamp in the trash.

**Mandatory arguments**

- token (string)
- pathId (uuid)
- timestampId (uuid)

## recover

    ellipsis.path.pointCloud.timestamp.recover()

Recover a timestamp from your trash.

**Mandatory arguments**

- token (string)
- pathId (uuid)
- timestampId (uuid)
