# Series

## get

    ellipsis.path.vector.timestamp.feature.series.get()

**Mandatory arguments**

- pathId (uuid)
- timestampId (uuid)
- featureId (uuid)

**Optional arguments**

- pageStart (uuid)
- dateTo (date object)
- userId (uuid)
- seriesProperty (string)
- trashed (boolean)
- listAll (boolean)
- token (string)

## info

    ellipsis.path.vector.timestamp.feature.series.info()

**Mandatory arguments**

- pathId (uuid)
- timestampId (uuid)
- featureId (uuid)

**Optional arguments**

- token (string)

## add

    ellipsis.path.vector.timestamp.feature.series.add()

**Mandatory arguments**

- pathId (uuid)
- timestampId (uuid)
- featureId (uuid)
- seriesData (pandas dataframe)
- token (uuid)

## trash

    ellipsis.path.vector.timestamp.feature.series.trash()

**Mandatory arguments**

- pathId (uuid)
- timestampId (uuid)
- featureId (uuid)
- seriesIds (array of uuids)
- token (string)

## recover

    ellipsis.path.vector.timestamp.feature.series.recover()

**Mandatory arguments**

- pathId (uuid)
- timestampId (uuid)
- featureId (uuid)
- seriesIds (array of uuids)
- token (string)

## changelog

    ellipsis.path.vector.timestamp.feature.series.changelog()

**Mandatory arguments**

- pathId (uuid)
- timestampId (uuid)
- featureId (uuid)

**Optional arguments**

- listAll (boolean), default False
- actions (array of strings)
- userId (uuid)
- pageStart (uuid)
- token (string)
