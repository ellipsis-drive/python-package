# style

## add

    ellipsis.path.vector.style.add()

**Mandatory arguments**

- pathId (uuid)
- parameters (object), See https://docs.ellipsis-drive.com/developers/api-v3/path-vector/styles/add-style for how to format the parameters
- token (string)

**Optional arguments**

- default (boolean), default value is True

## edit

    ellipsis.path.vector.style.edit()

**Mandatory arguments**

- pathId (uuid)
- styleId (uuid)
- token (string)

**Optional arguments**

- parameters (object)
- token (string)
- default (boolean)

## delete

    ellipsis.path.vector.style.delete()

**Mandatory arguments**

- pathId (uuid)
- styleId (uuid)
- token (string)
