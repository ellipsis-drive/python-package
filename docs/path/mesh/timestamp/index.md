# Timestamp

```{toctree}
---
maxdepth: 2
---
file/index
```

## add

    ellipsis.path.mesh.timestamp.add()

Add a timestamp

**Mandatory arguments**

- token (string)
- pathId (pathId)

**Optional arguments**

- date (dictionary with properties to and from, both of type date)
- description (string)

## edit

    ellipsis.path.mesh.timestamp.edit()

Edit a timestamp.

**Mandatory arguments**

- token (string)
- pathId (pathId)
- timestampId (uuid)

**Optional arguments**

- date (dictionary with properties to and from, both of type date)
- description (string)

## delete

    ellipsis.path.mesh.timestamp.delete()

Delete a timestamp.

**Mandatory arguments**

- token (string)
- pathId (uuid)
- timestampId (uuid)

## activate

    ellipsis.path.mesh.timestamp.activate()

Activate a timestamp.

**Mandatory arguments**

- token (string)
- pathId (uuid)
- timestampId (uuid)

## deactivate

    ellipsis.path.mesh.timestamp.deactivate()

Deactivate a timestamp.

**Mandatory arguments**

- token (string)
- pathId (uuid)
- timestampId (uuid)

## getBounds

    ellipsis.path.mesh.timestamp.getBounds()

Request to obtain the exact geometric bounds of a timestamp.

**Mandatory arguments**

- pathId (uuid)
- timestampId (uuid)

**Optional arguments**

- token (string)

## trash

    ellipsis.path.mesh.timestamp.trash()

Place a timestamp in the trash.

**Mandatory arguments**

- token (string)
- pathId (uuid)
- timestampId (uuid)

## recover

    ellipsis.path.mesh.timestamp.recover()

Recover a timestamp from your trash.

**Mandatory arguments**

- token (string)
- pathId (uuid)
- timestampId (uuid)
