# Order

## add

    ellipsis.path.raster.timestamp.order.add()

Order a download.

**Mandatory arguments**

- token (string)
- pathId (uuid)
- timestampId (uuid)
- extent (dictionary, with properties xMin, xMax, yMin and yMax of type float)

## get

    ellipsis.path.raster.timestamp.order.get()

Retrieve information on all your vector downloads.

**Mandatory arguments**

- token (string)

## download

    ellipsis.path.raster.timestamp.order.download()

Download the ordered file.

**Mandatory arguments**

- token (string)
- orderId (uuid)
- filePath (string)
