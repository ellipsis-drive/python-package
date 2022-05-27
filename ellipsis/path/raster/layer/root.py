from ellipsis import apiManager
from ellipsis import sanitize

def add(pathId, name, method, parameters, token, description = None):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)    
    method = sanitize.validString('method', method, True)    
    name = sanitize.validString('name', name, True)    
    description = sanitize.validString('description', description, False)    
    parameters = sanitize.validObject('parameters', parameters, True)

    body = {'name':name, 'method': method, 'parameters':parameters, 'description': description}
    r = apiManager.post('/path/' + pathId + '/raster/layer', body, token)
    return r

    
def delete(pathId, layerId, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)    
    layerId = sanitize.validUuid('layerId', layerId, True)    

    r = apiManager.delete('/path/' + pathId + '/raster/layer/' + layerId, None, token)
    return r


def edit(pathId, layerId, method, parameters, token, description = None):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)    
    method = sanitize.validString('method', method, True)    
    description = sanitize.validString('description', description, False)    
    parameters = sanitize.validObject('parameters', parameters, True)

    body = {'method': method, 'parameters':parameters, 'description': description}
    r = apiManager.patch('/path/' + pathId + '/raster/layer/' + layerId, body, token)
    return r

