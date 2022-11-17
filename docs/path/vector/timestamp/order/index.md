# order

## get

    ellipsis.path.vector.timestamp.order.get()

**Mandatory arguments**
- token (string)

## add

    ellipsis.path.vector.timestamp.order.add()

**Mandatory arguments**
- pathId (uuid)
- timestampId (uuid)
- token (string)

**Optional arguments**
- extent (dictionary, with properties xMin, xMax, yMin and yMax of type float)
- uploadId (uuid)

## download

    ellipsis.path.vector.timestamp.order.download()

**Mandatory arguments**
- orderId (uuid)
- filePath (string)
- token (string)
