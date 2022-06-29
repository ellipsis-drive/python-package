# Order

## order

    ellipsis.path.raster.timestamp.order.order()

Order a download.

**Mandatory arguments**

- token (string)
- pathId (uuid)
- timestampId (uuid)

**Optional arguments**

- bounds (bounds)
- uploadId (uuid)

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
