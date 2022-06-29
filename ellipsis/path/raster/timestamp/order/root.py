
from ellipsis import sanitize
from ellipsis import apiManager

def get(token):
    token = sanitize.validString('token', token, True)
    r = apiManager.get('/path/raster/timestamp/order', None, token)
    return r

def order(pathId, timestampId, token, bounds = None, uploadId = None):
    
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)
    timestampId = sanitize.validUuid('timestampId', timestampId, True)
    bounds = sanitize.validBounds('bounds', bounds, False)
    uploadId = sanitize.validUuid('uploadId', uploadId, False)

    body = {'uploadId': uploadId, 'bounds':bounds}
    
    r = apiManager.post('/path/' + pathId + '/raster/timestamp/' + timestampId + '/order', body, token)    

    return r

def download(orderId, filePath, token):
    
    token = sanitize.validString('token', token, True)
    orderId = sanitize.validUuid('orderId', orderId, True)
    filePath = sanitize.validString('filePath', filePath, True)

    if filePath[len(filePath)-4 : len(filePath) ] != '.tif':
        raise ValueError('filePath must end with .tif')

    apiManager.download('/path/raster/timestamp/order/' + orderId + '/download', filePath, token)
