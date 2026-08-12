import ellipsis as el

#in this example I select 2 plots of interest and retrieve all relevant inputs for these two plots

#read only token created in the UI
token = 'epat_CYLOpuytqpghrttlGM2t49wc8KsXSyxt6tJAlXu5N2FaRaQPgfwh4E3kVfPxvmaj'

#ids of relevant data
soil_pathId = '101bfc95-5b8d-410e-9699-5a0274750122'
soil_timestampId = 'bdde791b-fdcc-48e1-9709-9a9a0130684c'

et_deficit_pathId = '8aa2be2a-649e-4917-9a90-39c3b41b26c9'

plots_pathId = '33014abd-2bbe-4c42-bab0-b697fb56b63d'
plots_timestampId = '10358ee0-2110-4f60-bca0-7a69aab2eb20'

#2 plots of interest (chosen randomly from the layer)

feature1_id = '0dfc3bea-b931-4cf5-9e19-e30ee31d6983'
feature2_id = '1f2c1ea1-59e5-4e64-b2e2-20b62548844d'

#fetch the features
sh = el.path.vector.timestamp.getFeaturesByIds(pathId = plots_pathId, timestampId=plots_timestampId, featureIds=[feature1_id, feature2_id], token = token)['result']
sh['center'] = sh['geometry'].centroid

#get soil type
locations = [  (p.x, p.y) for p in  sh['center'].values ]
r = el.path.vector.timestamp.getLocationInfo(pathId = soil_pathId, timestampId = soil_timestampId, locations=locations, token=token)

print( 'feature 1 has soil type' ,r[0][0]['soilclassification'])

print( 'feature 2 has soil type' ,r[1][0]['soilclassification'])

#fetch et_deficit timeseries
#Either use the single location
info = el.path.get(pathId = et_deficit_pathId, token = token)
timestampIds = [t['id'] for t in info['raster']['timestamps'] if t['status'] == 'active']
g1 = sh['geometry'].values[0].simplify(1)
g2 = sh['geometry'].values[1].simplify(1)


plot1_series = el.path.raster.timestamp.analyse(pathId=et_deficit_pathId, timestampIds=timestampIds, geometry=g1, returnType='all', token=token)
print(plot1_series)
plot2_series = el.path.raster.timestamp.analyse(pathId=et_deficit_pathId, timestampIds=timestampIds, geometry=g2, returnType='all', token=token)
print(plot2_series)
#From the ids of the two plots we fetched their geometries, soil types and a time series with et_deficit you can now process this into what you wish to show

