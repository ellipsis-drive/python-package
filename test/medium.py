import ellipsis as el
pathId = 'fe5cb352-ccda-470b-bb66-12631c028def'
timestampId = '7dd94eac-f145-4a8a-b92d-0a22a289fe21'
extent = {    'xMin':5.7908,'xMax':5.79116,'yMin':51.93303,'yMax':51.93321}
epsg = 4326



df = el.path.pointCloud.timestamp.fetchPoints(pathId = pathId, timestampId = timestampId, extent = extent,  epsg = epsg)

print(df)

el.util.plotPointCloud(df, method = 'cloud')
el.util.plotPointCloud(df, method = 'voxel', scale = 0.01)
el.util.plotPointCloud(df, method = 'mesh', scale = 0.06)