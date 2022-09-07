from ellipsis import apiManager
from ellipsis import sanitize



def add(pathId, name, method, parameters, token, default = True):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    method = sanitize.validString('method', method, True)
    parameters = sanitize.validObject('parameters', parameters, True)
    token = sanitize.validString('token', token, True)
    default = sanitize.validBool('default', default, True)

    body = {'name': name, 'default':default, 'method': method, 'parameters':parameters}

    r = apiManager.post('/path/' + pathId + '/vector/style', body, token)
    return r


def edit(pathId, styleId, token, name = None, method = None, parameters = None, default = None):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    styleId = sanitize.validUuid('styleId', styleId, True) 
    method = sanitize.validString('method', method, False)
    parameters = sanitize.validObject('parameters', parameters, False)
    token = sanitize.validString('token', token, True)
    default = sanitize.validBool('default', default, False)
    name = sanitize.validString('name', name, False)

    body = {'name': name, 'default':default, 'method': method, 'parameters':parameters}

    r = apiManager.patch('/path/' + pathId + '/vector/style/' + styleId, body, token)
    return r
    
    
def delete(pathId, styleId, token):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    styleId = sanitize.validUuid('styleId', styleId, True) 
    token = sanitize.validString('token', token, True)
    

    r = apiManager.delete('/path/' + pathId + '/vector/style/' + styleId, None, token)
    return r
    


