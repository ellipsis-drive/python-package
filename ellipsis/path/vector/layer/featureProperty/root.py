from ellipsis import apiManager
from ellipsis import sanitize



def add(pathId, layerId, name, featurePropertyType, token, private = False, required = False):

    pathId = sanitize.validUuid('pathId', pathId, True) 
    layerId = sanitize.validUuid('layerId', layerId, True) 
    name = sanitize.validString('name', name, True)
    featurePropertyType = sanitize.validString('featurePropertyType', featurePropertyType, True)
    private = sanitize.validBool('private', private, True)
    required = sanitize.validBool('required', required, True)
    token = sanitize.validString('token', token, True)


    body = {'name': name, 'private':private, 'required': required, 'type':featurePropertyType}

    r = apiManager.post('/path/' + pathId + '/vector/layer/' + layerId + '/property', body, token)
    return r
    
def edit(pathId, layerId, featurePropertyId, token, private=False, required = False):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    layerId = sanitize.validUuid('layerId', layerId, True) 
    featurePropertyId = sanitize.validUuid('featurePropertyId', featurePropertyId, True) 
    private = sanitize.validBool('private', private, True)
    required = sanitize.validBool('required', required, True)
    token = sanitize.validString('token', token, True)


    body = {'private':private, 'required': required}

    r = apiManager.patch('/path/' + pathId + '/vector/layer/' + layerId + '/property/' + featurePropertyId, body, token)
    return r


def delete(pathId, layerId, featurePropertyId, token):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    layerId = sanitize.validUuid('layerId', layerId, True) 
    featurePropertyId = sanitize.validUuid('featurePropertyId', featurePropertyId, True) 
    token = sanitize.validString('token', token, True)

    body = {'deleted': True}
    r = apiManager.put('/path/' + pathId + '/vector/layer/' + layerId + '/property/' + featurePropertyId + '/deleted', body, token)
    return r


def recover(pathId, layerId, featurePropertyId, token):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    layerId = sanitize.validUuid('layerId', layerId, True) 
    featurePropertyId = sanitize.validUuid('featurePropertyId', featurePropertyId, True) 
    token = sanitize.validString('token', token, True)

    body = {'deleted': False}
    r = apiManager.put('/path/' + pathId + '/vector/layer/' + layerId + '/property/' + featurePropertyId + '/deleted', body, token)
    return r



    


