# Util

## reprojectRaster

    ellipsis.util.reprojectRaster()

Reproject a numpy array raster.

**Mandatory arguments**

- r (3D numpy array), the raster to be reprojected
- sourceExtent (dictionary), dictionary with xMin, xMax, yMin, yMax giving the extent of the raster
- targetExtent (dictionary), dictionary with xMin, xMax, yMin, yMax giving the extent of target raster
- sourceEpsg (ing) epsg code of the raster
- targetEpsg (ing) epsg code of the target raster
- targetWidth (int) width of the target raster
- targetHeight (int) height of the target raster

**Optional arguments**

- interpolation (string) one of bilinear or nearest

## reprojectVector

    ellipsis.util.reprojectVector()

Reprojects a geopandas dataframe

**Mandatory arguments**

- features (geopandas dataframe) geopandas dataframe to be reprojected
- targetEpsg (int) epsg to reproject to

**Optional arguments**

- cores (int) number of processes to use


## saveRaster

    ellipsis.util.saveRaster()

Saves numpy array as tif

**Mandatory arguments**

- targetFile (string) path to write ot
- r (3D numpy array) numpy array of the data of the raster to write
- epsg (int) epsg code of the raster

**Optional arguments**

- extent (dictionary), dictionary with xMin, xMax, yMin, yMax giving the extent of the raster
- transform (rasterio transform), the transform of the raster

## saveVector

    ellipsis.util.saveVector()

Saves geopandas as shape

**Mandatory arguments**

- targetFile (string) path to write ot
- features (geopandas data frame) a geopandas dataframe to save



## plotRaster

    ellipsis.util.plotRaster()

Plots a numpy array containing raster data

**Mandatory arguments**

- r (numpy array) numpy array of the data of the raster to write


## plotVector

    ellipsis.util.plotVector()

Plots a geopandas data frame

**Mandatory arguments**

- features (geopandas dataframe) a geopandas dataframe with features to plot


## plotPointCloud

    ellipsis.util.plotPointCloud()

Plots a pandas containing the points of a point cloud. Pandas should be of the form as returned by ellipsis.path.pointCloud.timestamp.fetchPoints()

**Mandatory arguments**

- df (pandas data frame holding the points)

**Optional arguments**
- method (which method to use for plotting. Must be one of cloud, mesh or voxel, defautl cloud)
- width (width of the plot as int, default 800)
- height (height of the plot as int, default 600)
- scale (precision of the plot as float, default 0.003)


## simplifyGeometries

    ellipsis.util.simplifyGeometries()

Simplifies geometries in a geopandas dataframe. Can be used in the creation of vector tiles.

**Mandatory arguments**

- features (geopandas dataframe) a geopandas dataframe with geometries to simplify
- tolerance (float) the precision to retain

**Optional arguments**

- preserveTopology (boolean), whether the topology needs to be preserved
- removeIslands (boolean), whether to remove polygons within multipolygons that are smaller than the tolerance.
- cores (int), number of processes to commit.



## cover

    ellipsis.util.cover()

Cover a given shapely polygon or multi polygon with tiles of a given width

**Mandatory arguments**

- bounds (shapely polygon or mulitpolygon) a geometry indicating the region to cover
- width (float) size of the tiles to cover the region with in meters.




