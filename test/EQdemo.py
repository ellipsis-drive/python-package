import ellipsis as el
token = el.account.logIn('YOUR_USERNAME', 'YOUR_PASSWORD')
layer = {'id'}

requirements = ['ellipsis', 'numpy','keras']
nodes = 4
layers = [ {'pathId':layer['id'], 'timestampId': t['id']} for t in layer['raster']['timestamps']]
el.compute.createCompute(layers = layers, token=token, nodes = 4, interpreter='python3.12', requirements = requirements)






def f(params):
    from io import BytesIO
    import ellipsis as el
    import numpy as np

    r = params['523caede-9f96-49fa-a855-3e546bcd365d']['raster']
    extent = params['523caede-9f96-49fa-a855-3e546bcd365d']['extent']

    ndvi = (r[7,:,:] - r[3,:,:])/(r[3,:,:] + r[7,:,:])
    ndvi = np.expand_dims(ndvi, axis = 0)

    b = BytesIO()
    memfile = el.util.saveRaster(ndvi, 3857, b, extent = extent)

    return memfile

computeId = 2


el.compute.terminateCompute(computeId=computeId, token=token)







