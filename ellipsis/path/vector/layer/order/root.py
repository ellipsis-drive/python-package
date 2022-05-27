
from ellipsis import sanitize
from ellipsis import apiManager

def get(token):
    r = apiManager.get('/path/vector/layer/order', None, token)
    return r

def order(pathId, layerId, token, bounds = None, uploadId = None):
    
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)
    layerId = sanitize.validUuid('layerId', layerId, True)
    bounds = sanitize.validBounds('bounds', bounds, False)
    uploadId = sanitize.validUuid('uploadId', uploadId, False)

    body = {'uploadId': uploadId, 'bounds':bounds, 'format' :'geojson'}
    
    r = apiManager.post('/path/' + pathId + '/vector/layer/' + layerId + '/order', body, token)    

    return r  

def download(orderId, filePath, token):
    
    token = sanitize.validString('token', token, True)
    orderId = sanitize.validUuid('orderId', orderId, True)
    filePath = sanitize.validString('filePath', filePath, True)

    if filePath[len(filePath)-4 : len(filePath) ] != '.zip':
        raise ValueError('filePath must end with .zip')

    apiManager.download('/path/vector/layer/order/' + orderId + '/download', filePath, token)
