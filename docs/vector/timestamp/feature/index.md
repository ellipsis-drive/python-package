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

**Optional arguments**

- zoomlevels (array of integers)
- levelOfDetail1 (Geoseries or array of shapely geometries)
- levelOfDetail2 (Geoseries or array of shapely geometries)
- levelOfDetail3 (Geoseries or array of shapely geometries)
- levelOfDetail4 (Geoseries or array of shapely geometries)
- levelOfDetail5 (Geoseries or array of shapely geometries)

## edit

    ellipsis.path.vector.timestamp.feature.edit()

Edit a feature.

**Mandatory arguments**

- pathId (uuid)
- timestampId (uuid)
- featureIds (array of uuids)
- token (string)

**Optional arguments**

- features (geopandas dataframe)
- zoomlevels (array of integers)
- levelOfDetail1 (Geoseries or array of shapely geometries)
- levelOfDetail2 (Geoseries or array of shapely geometries)
- levelOfDetail3 (Geoseries or array of shapely geometries)
- levelOfDetail4 (Geoseries or array of shapely geometries)
- levelOfDetail5 (Geoseries or array of shapely geometries)

## delete

    ellipsis.path.vector.timestamp.feature.delete()

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
