import ellipsis as el

token = el.account.logIn('daan', 'Brooksrange24')


requirements = ['rasterio']
nodes = 2
#drought 'c80a4d58-16a5-4fe8-9ebc-3adcdd7d5d54'
#locations 'af13078d-67ed-42a9-9b39-6e67cfb2c33f'
layers = [{'pathId':'c80a4d58-16a5-4fe8-9ebc-3adcdd7d5d54', 'timestampId':'b90d8f74-60a4-4bd5-8419-afad0504085f'},{'pathId':'af13078d-67ed-42a9-9b39-6e67cfb2c33f', 'timestampId':'77b2ca83-e22b-472e-a09d-02c170e097c5'} ]
computeId1 = el.compute.createCompute(layers = layers, token=token, nodes = nodes,interpreter='python3.12', requirements = requirements)['id']

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

r = el.compute.execute(computeId=computeId1, token=token, f=f)
print(r)

def f(params):
    raise ValueError('nice')


el.compute.terminateAll(token=token)


requirements = ['rasterio', 'ellipsis']
nodes = 2
#drought 'c80a4d58-16a5-4fe8-9ebc-3adcdd7d5d54'
#locations 'af13078d-67ed-42a9-9b39-6e67cfb2c33f'
layers = [{'pathId':'c80a4d58-16a5-4fe8-9ebc-3adcdd7d5d54', 'timestampId':'b90d8f74-60a4-4bd5-8419-afad0504085f'},{'pathId':'af13078d-67ed-42a9-9b39-6e67cfb2c33f', 'timestampId':'77b2ca83-e22b-472e-a09d-02c170e097c5'} ]
computeId2 = createCompute(layers = layers, token=token, nodes = nodes,interpreter='python3.12', requirements = requirements, largeResult=True)['id']


def f(params):
    from ellipsis.util import saveRaster
    from rasterio.io import MemoryFile
    from io import BytesIO

    r = params['b90d8f74-60a4-4bd5-8419-afad0504085f']['raster']
    transform = params['b90d8f74-60a4-4bd5-8419-afad0504085f']['transform']

    r = r.astype('float32')

    dataset = saveRaster(r, epsg=3857, targetFile = BytesIO(), transform=transform)
    return dataset


res = execute(computeId=computeId2, token=token, f=f)

url = '/compute/8e7dc023-69d2-4c7f-84f7-eddecb82a37f/file/b3968970-74bb-46cb-a715-472aea67f483'
downloadFile(url, '/home/daniel/Downloads/out.tif', token)

terminateAll(token=token)



