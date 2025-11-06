import ellipsis as el

token = el.account.logIn('demo_user', 'demo_user')


pathId = 'c08b3c19-9d95-499e-9217-42e5e9f38021'

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
