
from ellipsis import sanitize
from ellipsis import apiManager

def get(token):
    r = apiManager.get('/path/timestamp/order', None, token)
    return r

def order(pathId, timestampId, token, bounds = None, uploadId = None):
    
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)
    timestampId = sanitize.validUuid('timestampId', timestampId, True)
    bounds = sanitize.validBounds('bounds', bounds, False)
    uploadId = sanitize.validUuid('uploadId', uploadId, False)

    body = {'uploadId': uploadId, 'bounds':bounds}
    
    r = apiManager.post('/path/' + pathId + '/timestamp/' + timestampId + '/order', body, token)    

    return r  

def download(orderId, filePath, token):
    
    token = sanitize.validString('token', token, True)
    orderId = sanitize.validUuid('orderId', orderId, True)
    filePath = sanitize.validString('filePath', filePath, True)

    apiManager('/path/raster/timestamp/order/' + orderId, filePath, token)
