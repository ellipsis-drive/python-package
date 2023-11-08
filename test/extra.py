import ellipsis as el
import geopandas as gpd
extent = gpd.read_file("/home/daniel/Downloads/extent.geojson").to_crs(4326)
el_extent = dict(zip(['xMin', 'yMin', 'xMax', 'yMax'], extent.total_bounds))



result = getFeaturesByExtent(
    pathId="12550222-266e-4d6e-875d-f48b0c02ea94",
    timestampId="4be865e8-8203-4bd9-bec9-b4653296db4c",
    extent=el_extent,
    epsg=4326,
    token=token,
    levelOfDetail=1
)


result

