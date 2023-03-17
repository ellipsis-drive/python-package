# Raster

```{toctree}
---
maxdepth: 2
---
style/index
timestamp/index
```

## add

    ellipsis.path.raster.add()

Adds a raster.

**Mandatory arguments**

- name (string) name for the folder
- token (string), your token

**Optional arguments**

- parentId (uuid) id of folder to place the new folder in
- publicAccess (dict) dictionary describing the public access of the folder
- metadata (dict) dictionary describing the metadata of the folder


## editBand

    ellipsis.raster.editBand()

Change the name of a band.

**Mandatory arguments**

- token (string)
- pathId (uuid)
- bandNumber (integer)
- name (string)

## edit

    ellipsis.raster.edit()

Edit raster map attributes.

**Mandatory arguments**

- token (string)
- pathid (uuid)

**Optional arguments**

- interpolation (string)
- includesTransparant (boolean)
- compressionQuality (int between 0 and 100)
