from ellipsis import apiManager
from ellipsis import sanitize

def add(pathId, name, parameters, token, default=True, method = None):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)    
    method = sanitize.validString('method', method, False)
    name = sanitize.validString('name', name, True)    
    default = sanitize.validBool('default', default, True)    
    parameters = sanitize.validObject('parameters', parameters, True)
    if type(method) == type(None):
        body = {'name':name, 'parameters':parameters, 'default':default}
    else:
        body = {'name':name, 'method': method, 'parameters':parameters, 'default':default}
    r = apiManager.post('/path/' + pathId + '/raster/style', body, token)
    return r

    
def delete(pathId, styleId, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)    
    styleId = sanitize.validUuid('styleId', styleId, True)    

    r = apiManager.delete('/path/' + pathId + '/raster/style/' + styleId, None, token)
    return r


def edit(pathId, styleId, method, parameters, token, name=None, default = None):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)    
    method = sanitize.validString('method', method, True)    
    parameters = sanitize.validObject('parameters', parameters, True)
    default = sanitize.validBool('default', default, False)    

    body = {'method': method, 'parameters':parameters, 'default':default, 'name':name}
    r = apiManager.patch('/path/' + pathId + '/raster/style/' + styleId, body, token)
    return r

