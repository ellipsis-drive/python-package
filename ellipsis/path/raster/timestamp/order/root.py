
from ellipsis import sanitize
from ellipsis import apiManager

def get(token):
    token = sanitize.validString('token', token, True)
    r = apiManager.get('/path/raster/timestamp/order', None, token)
    return r

def add(pathId, timestampId, token, extent = None, epsg=4326):
    
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)
    timestampId = sanitize.validUuid('timestampId', timestampId, True)
    extent = sanitize.validBounds('extent', extent, True)
    epsg = sanitize.validInt('epsg', epsg, True)

    body = {'extent':extent, 'epsg':epsg}
    r = apiManager.post('/path/' + pathId + '/raster/timestamp/' + timestampId + '/order', body, token)    

    return r

def download(orderId, filePath, token):
    
    token = sanitize.validString('token', token, True)
    orderId = sanitize.validUuid('orderId', orderId, True)
    filePath = sanitize.validString('filePath', filePath, True)

    if filePath[len(filePath)-4 : len(filePath) ] != '.tif':
        raise ValueError('filePath must end with .tif')

    apiManager.download('/path/raster/timestamp/order/' + orderId + '/data', filePath, token)
