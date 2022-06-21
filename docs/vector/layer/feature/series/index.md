# Series

## get

    ellipsis.path.vector.layer.feature.series.get()

**Mandatory arguments**

- pathId (uuid)
- layerId (uuid)
- featureId (uuid)

**Optional arguments**

- pageStart (uuid)
- dateTo (date object)
- userId (uuid)
- seriesProperty (string)
- deleted (boolean)
- listAll (boolean)
- token (string)

## info

    ellipsis.path.vector.layer.feature.series.info()

**Mandatory arguments**

- pathId (uuid)
- layerId (uuid)
- featureId (uuid)

**Optional arguments**

- token (string)

## add

    ellipsis.path.vector.layer.feature.series.add()

**Mandatory arguments**

- pathId (uuid)
- layerId (uuid)
- featureId (uuid)
- seriesData (pandas dataframe)
- token (uuid)

## delete

    ellipsis.path.vector.layer.feature.series.delete()

**Mandatory arguments**

- pathId (uuid)
- layerId (uuid)
- featureId (uuid)
- seriesIds (array of uuids)
- token (string)

## recover

    ellipsis.path.vector.layer.feature.series.recover()

**Mandatory arguments**

- pathId (uuid)
- layerId (uuid)
- featureId (uuid)
- seriesIds (array of uuids)
- token (string)

## changelog

    ellipsis.path.vector.layer.feature.series.changelog()

**Mandatory arguments**

- pathId (uuid)
- layerId (uuid)
- featureId (uuid)

**Optional arguments**

- listAll (boolean), default False
- actions (array of strings)
- userId (uuid)
- pageStart (uuid)
- token (string)
