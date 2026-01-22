from six import BytesIO

import ellipsis as el
import numpy as np

from ellipsis.compute import addToLayer
from ellipsis.compute.root import terminateAll
from test.pointCloud import timestampId

from test.compute import computeId1



requirements = ['rasterio']
nodes = 2

#In this example I will find locations of maximum risk for landslides along pipe lines in the USA.

#I will use a raster layer containing landslide risk
pathId_landslide = '08d3742a-8fe6-4ada-b244-d73431fe368c'
timestampId_landSlide = '455a5d70-cfe4-4a89-820e-f9eb90a0b9e4'

#the layer can be browsed using the following link:
'https://app.ellipsis-drive.com/view?pathId=08d3742a-8fe6-4ada-b244-d73431fe368c'

#and a vector layer containing pipe lines
pathId_pipLines = 'e8a1d394-5ad0-4635-9201-3621239798ba'
timestampId_pipeLines  = 'ea07f895-f16d-44b2-b3d0-e4c19ead6b1e'

#the layer can be browsed using the following link:
'https://app.ellipsis-drive.com/view?pathId=e8a1d394-5ad0-4635-9201-3621239798ba'


#exploration
#let's retrieve an overview of the land slide layer


extent_usa ={'xMin': -127.37982051819313,
 'xMax': -64.82830000032217,
 'yMin': 21.5796570423334,
 'yMax': 58.5185612283739}



r = el.path.raster.timestamp.getSampledRaster(pathId = pathId_landslide, timestampId=timestampId_landSlide, token=token, epsg = 4326, width = 1024, height=1024, extent = extent_usa)


el.util.plotRaster(r['raster'])


#now let's plot an overview of the pipe line layer
r = el.path.vector.timestamp.listFeatures(pathId = pathId_pipLines, timestampId=timestampId_pipeLines, token=token)
r['result'].plot()


#With these datasets at the ready we can now perform the needed analytics. The first step will be the specify the enviroment

layers = [{'pathId': pathId_landslide, 'timestampId':timestampId_landSlide}, {'pathId': pathId_pipLines, 'timestampId': timestampId_pipeLines}]

requirements = ['rasterio']


computeId = createCompute(layers=layers, nodes = 2, requirements=requirements, token=token, largeResult=False)['id']

#create a function that finds the max risk along each pipe line and returns this max risk per pipe line
def f(params):
    from rasterio.features import rasterize
    timestampId_pipeLines = 'ea07f895-f16d-44b2-b3d0-e4c19ead6b1e'
    timestampId_landSlide = '455a5d70-cfe4-4a89-820e-f9eb90a0b9e4'
    r = params[timestampId_landSlide]['raster']
    sh = params[timestampId_pipeLines]['vector']
    transform = params[timestampId_landSlide]['transform']

    sh['geometry'] = sh.buffer(0.0000001)
    lines = zip(sh['geometry'].values, range(sh['geometry'].shape[0]))
    geometry_raster = rasterize(shapes=[(line[0], line[1]) for line in lines], fill=-1, transform=transform, out_shape=(r.shape[1], r.shape[2]), all_touched=True)

    risks = []
    for i in range(sh.shape[0]):
        N = np.max(r[0, geometry_raster==i], initial=0)
        risks = risks + [{'Pipename': sh['Pipename'].values[i], 'maxRisk': float(N)} ]
    return risks


res = execute(computeId=computeId, f=f, token=token)

print(res)



terminateAll(token=token)


#####################################################################

pathId_storm = '6d608956-5fd1-4d9f-b1ac-0dba1da49a28'
timestampId_storm = '5c7c9aa9-a459-4679-b935-c6a57c2cd514'

layers = [{'pathId': pathId_storm, 'timestampId':timestampId_storm}]

requirements = ['ellipsis']


computeId = createCompute(layers=layers, nodes = 1, requirements=requirements, token=token, largeResult=True)['id']

def f(params):
    import ellipsis as el
    from io import BytesIO
    timestampId_storm = '5c7c9aa9-a459-4679-b935-c6a57c2cd514'

    r = params[timestampId_storm]['raster']
    extent = params[timestampId_storm]['extent']
    D = 1000*1000
    extent['xMin'] = extent['xMin'] + D
    extent['xMax'] = extent['xMax'] +D

    memfile = el.util.saveRaster(r=r, epsg = 3857, targetFile=BytesIO(), extent=extent)

    return memfile

res = execute(computeId=computeId, f=f, token=token)

folderId = '2d6e414e-49ea-4100-bcd9-b155dce6c2f9'
pathId = el.path.raster.add(name = 'output', token = token, parentId=folderId)['id']
timestampId = el.path.raster.timestamp.add(pathId=pathId, token = token)['id']
addToLayer(response=res, pathId = pathId, timestampId=timestampId,token=token)


terminateAll(token=token)

############################
pathId_insuredLocations = 'c91aff84-4d8c-4bb5-9b93-5624a6a1e118'
timestampId_insuredLocations = '954b6094-5910-4aed-97e6-626d719fecdb'

layers = [{'pathId': pathId, 'timestampId':timestampId}, {'pathId': pathId_insuredLocations, 'timestampId':timestampId_insuredLocations}]

requirements = ['rasterio']
computeId = createCompute(layers=layers, nodes = 1, requirements=requirements, token=token, largeResult=False)['id']

def f(params):
    timestampId ='a11de9e6-c139-421e-85ae-432d824241e1'
    timestampId_insuredLocations = '954b6094-5910-4aed-97e6-626d719fecdb'
    from rasterio.io import MemoryFile
    r = params[timestampId]['raster']
    sh = params[timestampId_insuredLocations]['vector']
    transform = params[timestampId]['transform']

    r = r.astype('float32')

    memfile =  MemoryFile()

    dataset = memfile.open( driver='GTiff', dtype='float32', height=r.shape[1], width=r.shape[2], count = r.shape[0], crs= 'EPSG:3857', transform=transform)
    dataset.write(r)

    values = list(dataset.sample([p for p in zip(sh.bounds['minx'].values, sh.bounds['miny'].values)]))
    memfile.close()

    values = [v[0] for v in values][0]
    return values

res = execute(computeId=computeId, f=f, token=token)

print(res)
terminateAll(token=token)
##########################################














#drought 'c80a4d58-16a5-4fe8-9ebc-3adcdd7d5d54'
#locations 'af13078d-67ed-42a9-9b39-6e67cfb2c33f'
layers = [{'pathId':'c80a4d58-16a5-4fe8-9ebc-3adcdd7d5d54', 'timestampId':'b90d8f74-60a4-4bd5-8419-afad0504085f'},{'pathId':'af13078d-67ed-42a9-9b39-6e67cfb2c33f', 'timestampId':'77b2ca83-e22b-472e-a09d-02c170e097c5'} ]
computeId = el.compute.createCompute(layers = layers, token=token, nodes = nodes,interpreter='python3.12', requirements = requirements)['id']


def f(params):
    from rasterio.io import MemoryFile
    r = params['b90d8f74-60a4-4bd5-8419-afad0504085f']['raster']
    sh = params['77b2ca83-e22b-472e-a09d-02c170e097c5']['vector']
    transform = params['b90d8f74-60a4-4bd5-8419-afad0504085f']['transform']
    extent = params['b90d8f74-60a4-4bd5-8419-afad0504085f']['extent']

    r = r.astype('float32')

    memfile =  MemoryFile()

    dataset = memfile.open( driver='GTiff', dtype='float32', height=r.shape[1], width=r.shape[2], count = r.shape[0], crs= 'EPSG:3857', transform=transform)
    dataset.write(r)

    values = list(dataset.sample([p for p in zip(sh.bounds['minx'].values, sh.bounds['miny'].values)]))
    memfile.close()

    values = [v[0] for v in values][0]
    return values


r = el.compute.execute(computeId=computeId, token=token, f=f)


print(r)


terminateAll(token = token)


layers = [{'pathId':'99cd8e85-0e64-4c06-a6ca-da65493169ea', 'timestampId':'8225cb9f-b8bf-4641-a14b-63bcc0220c90'}]
computeId = el.compute.createCompute(layers = layers, token=token, nodes = nodes,interpreter='python3.12', requirements = requirements)['id']

def f(params):
    sh = params['8225cb9f-b8bf-4641-a14b-63bcc0220c90']['vector']
    n = 0
    if 'carrier' in sh.columns:
        n = sh[sh['carrier'] == '647-010'].shape[0]

    return n


r = el.compute.execute(computeId=computeId, token=token, f=f)


print(np.sum(r))

terminateAll(token = token)

import geopandas as gpd
from shapely import Polygon
coords = ((-5.28595, 44.0932), (-5.28595, 49.94618), (9.01905, 49.94618), (9.01905, 44.0932), (-5.28595, 44.0932))

polygon = Polygon(coords)

region = gpd.GeoDataFrame({'geometry':[polygon]})
region.crs = 'EPSG:4326'
region = region.to_crs('EPSG:3857')
