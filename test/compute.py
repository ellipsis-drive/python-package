import ellipsis as el


def f(params):
    from rasterio.features import rasterize
    import numpy as np

    timestampId_dem = '5297251c-cb9a-4569-a601-2c728ffc29e4'
    timestampId_poly = '2f84fce0-bfd0-42e9-961b-200a275b1c53'

    r = params[timestampId_dem]['raster']
    transform = params[timestampId_dem]['transform']
    aoi = params[timestampId_poly]
    poly = aoi['geomery'].values[0]

    geometry_raster = rasterize(shapes=[(poly, 1)], fill=0, transform=transform, out_shape=(r.shape[1], r.shape[2]), all_touched=True)

    s = np.sum( r[geometry_raster==1]-11.8)*0.0001

    return float(s)

r = el.compute.execute(computeId = computeId, f=f, token=token)























import time


el.apiManager.baseUrl

token = el.account.logIn('demo_user', 'demo_user')

pathId = 'b0622936-cc30-42d5-a807-bae44b40e985'
timestampId = '99568a54-c0a9-43c5-94e4-f4817974fbfc'
fileId = 'ebd4f391-0f30-4132-84ac-6ad18045619d'
nodes = 2


def f(params):
    import numpy as np
    import time
    timestampId = '99568a54-c0a9-43c5-94e4-f4817974fbfc'
    fileId = 'ebd4f391-0f30-4132-84ac-6ad18045619d'
    file = params[fileId]
    r = params[timestampId]['raster']
    return r.shape

    l = []
    for i in range(1000000):
        print('step ', i)
        time.sleep(2)
        x = np.array(r, copy=True)
        l.append(x)
    s = np.sum(r)
    return s

times = []
requirements = ['numpy']
interpreter = 'python3.12'
layers = [{'pathId': pathId, 'timestampId': timestampId}]
files = [fileId]
computeId = el.compute.createCompute(layers=layers, token=token, nodes=nodes, interpreter=interpreter, files = files,
                                     requirements=requirements)['id']

r = el.compute.execute(computeId = computeId, f=f, token=token)

el.compute.terminateCompute(computeId=computeId, token = token)
print(times)
el.compute.terminateAll(token = token)

pathId = 'c08b3c19-9d95-499e-9217-42e5e9f38021'


###########################




pathId_dem = 'c1792258-9896-43a5-9823-c6251aefa572'
timestampId_dem = '5297251c-cb9a-4569-a601-2c728ffc29e4'

pathId_poly = 'e44160e6-0dd7-4a5e-886f-77036e7e551a'
timestampId_poly = '2f84fce0-bfd0-42e9-961b-200a275b1c53'

requirements = ['numpy', 'rasterio']
interpreter = 'python3.12'
layers = [{'pathId': pathId_dem, 'timestampId': timestampId_dem},{'pathId': pathId_poly, 'timestampId': timestampId_poly}]
nodes = 1

computeId = el.compute.createCompute(layers=layers, token=token, nodes=nodes, interpreter=interpreter, requirements=requirements)['id']




def f(params):
    from rasterio.features import rasterize
    import numpy as np

    timestampId_dem = '5297251c-cb9a-4569-a601-2c728ffc29e4'
    timestampId_poly = '2f84fce0-bfd0-42e9-961b-200a275b1c53'


    r = params[timestampId_dem]['raster']
    transform = params[timestampId_dem]['transform']
    aoi = params[timestampId_poly]
    poly = aoi['geomery'].values[0]

    geometry_raster = rasterize(shapes=[(poly, 1)], fill=0, transform=transform, out_shape=(r.shape[1], r.shape[2]), all_touched=True)

    s = np.sum( r[geometry_raster==1])

    return float(s)

times = []
requirements = ['numpy']
interpreter = 'python3.12'
layers = [{'pathId': pathId, 'timestampId': timestampId}]
computeId = el.compute.createCompute(layers=layers, token=token, nodes=nodes, interpreter=interpreter,
                                     requirements=requirements)['id']

r = execute(computeId = computeId, f=f, token=token)

el.compute.terminateCompute(computeId=computeId, token = token)
print(times)
el.compute.terminateAll(token = token)


########################################3
















timestampId = el.path.raster.timestamp.add(pathId = pathId, token =  token)['id']

writeToLayer = {'pathId':pathId, 'timestampId':timestampId}

requirements = ['rasterio','ellipsis']
nodes = 1
interpreter='python3.12'
layers = [{'pathId':'ea854f7d-7adf-4a4e-9b93-b6ca58c9e9dc', 'timestampId':'e945fe03-bcfc-4d3f-ab10-4d117006d609'} ]
computeId = createCompute(layers = layers, token=token, nodes = nodes,interpreter=interpreter, requirements = requirements, largeResult= True)['id']

def f(params):
    from io import BytesIO
    from ellipsis.util import saveRaster
    r = params['e945fe03-bcfc-4d3f-ab10-4d117006d609']['raster']
    transform = params['e945fe03-bcfc-4d3f-ab10-4d117006d609']['transform']
    extent = params['e945fe03-bcfc-4d3f-ab10-4d117006d609']['extent']

    r = r.astype('float32')
    r = r-1 #apply model
    dataset = saveRaster(r, epsg=3857, targetFile = BytesIO(), transform=transform)
    return dataset

el.compute.execute(computeId=computeId, token=token, f=f, writeToLayer=writeToLayer)



el.compute.terminateCompute(computeId = computeId,token=token)
