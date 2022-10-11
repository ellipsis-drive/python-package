# Raster style

## add

    ellipsis.path.raster.style.add()

Adds a raster style.

**Mandatory arguments**
- pathId (uuid),
- method (string),
- parameters (object), containing
- token (uuid), your token

**Optional arguments**

- default (boolean), default value is True

## edit

    ellipsis.path.raster.style.edit()

Edit a raster style.

**Mandatory arguments**
- pathId (uuid),
- styleId (uuid),
- token (string)

**Optional arguments**

- method (string)
- parameters (object)
- token (string)
- default (boolean)


## delete

    ellipsis.path.raster.style.delete()

Delete a raster style.

**Mandatory arguments**

- pathId (uuid),
- styleId (uuid), 
- token (string)

