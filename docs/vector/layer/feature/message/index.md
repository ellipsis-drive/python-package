# Message

## get

    ellipsis.path.vector.layer.feature.message.get()

Get all messages on a feature.

**Mandatory arguments**

- pathId (uuid),
- layerId (uuid),

**Optional arguments**

- token (string), your token
- messageIds (array of uuids),
- userId (uuid),
- bounds (bounds object),
- pageStart (uuid),
- listAll (boolean), default False
- deleted (boolean), default False

## getImage

    ellipsis.path.vector.layer.feature.message.getImage()

Get the image of a message.

**Mandatory arguments**

- pathId (uuid),
- layerId (uuid),
- messageId

**Optional arguments**

- token (string), your token

## add

    ellipsis.path.vector.layer.feature.message.add()

Add message to a feature.

**Mandatory arguments**

- pathId (uuid),
- layerId (uuid),
- featureId (uuid)
- token (string), your token

**Optional arguments**

- text (string)
- image (image)

## delete

    ellipsis.path.vector.layer.feature.message.delete()

Delete a message.

**Mandatory arguments**

- pathId (uuid),
- layerId (uuid),
- messageId (uuid)
- token (string), your token

## recover

    ellipsis.path.vector.layer.feature.message.recover()

Recover a message.

**Mandatory arguments**

- pathId (uuid),
- layerId (uuid),
- featureId (uuid)
- token (string), your token
