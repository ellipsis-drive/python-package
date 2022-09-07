# Raster

```{toctree}
---
maxdepth: 2
---
style/index
timestamp/index
```

## editBand

    ellipsis.raster.editBand()

Change the name of a band.

**Mandatory arguments**

- token (string)
- pathId (uuid)
- bandNumber (integer)
- name (string)

## editMap

    ellipsis.raster.editMap()

Edit raster map attributes.

**Mandatory arguments**

- token (string)
- pathid (uuid)

**Optional arguments**

- interpolation (string)
- includesTransparant (boolean)
