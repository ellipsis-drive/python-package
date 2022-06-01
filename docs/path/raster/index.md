# Raster

## editBand

    ellipsis.path.raster.editBand()

Edit Band

### Mandatory parameters
- pathId (uuid), the id of the map
- bandNumber (int), the number of the band
- name (string), the new name of the band
- token (string), your token

### Optional parameters

## editMap

    ellipsis.path.raster.editMap()

Edit map

### Mandatory parameters
- pathId (uuid), the id of the map
- token (string), your token

### Optional parameters
- interpolation (string), interpolation method to be used, 'nearest' or 'linear'
- includesTransparent (string), Whether the last band of uploaded rasters is the transparancy band.