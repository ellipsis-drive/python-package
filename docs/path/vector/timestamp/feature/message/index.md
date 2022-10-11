# Message

## get

    ellipsis.path.vector.timestamp.feature.message.get()

Get all messages on a feature.

**Mandatory arguments**

- pathId (uuid),
- timestampId (uuid),

**Optional arguments**

- token (string), your token
- messageIds (array of uuids),
- userId (uuid),
- extent (a dictionary with properties xMin, xMax, yMin, yMax of type float)
- pageStart (uuid),
- listAll (boolean), default False
- deleted (boolean), default False

## getImage

    ellipsis.path.vector.timestamp.feature.message.getImage()

Get the image of a message.

**Mandatory arguments**

- pathId (uuid),
- timestampId (uuid),
- messageId

**Optional arguments**

- token (string), your token

## add

    ellipsis.path.vector.timestamp.feature.message.add()

Add message to a feature.

**Mandatory arguments**

- pathId (uuid),
- timestampId (uuid),
- featureId (uuid)
- token (string), your token

**Optional arguments**

- text (string)
- image (image)

## trash

    ellipsis.path.vector.timestamp.feature.message.trash()

Delete a message.

**Mandatory arguments**

- pathId (uuid),
- timestampId (uuid),
- messageId (uuid)
- token (string), your token

## recover

    ellipsis.path.vector.timestamp.feature.message.recover()

Recover a message.

**Mandatory arguments**

- pathId (uuid),
- timestampId (uuid),
- featureId (uuid)
- token (string), your token
