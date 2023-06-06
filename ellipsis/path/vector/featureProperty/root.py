from ellipsis import apiManager
from ellipsis import sanitize



def add(pathId, name, featurePropertyType, token, private = False, required = False):

    pathId = sanitize.validUuid('pathId', pathId, True) 
    name = sanitize.validString('name', name, True)
    featurePropertyType = sanitize.validString('featurePropertyType', featurePropertyType, True)
    private = sanitize.validBool('private', private, True)
    required = sanitize.validBool('required', required, True)
    token = sanitize.validString('token', token, True)


    body = {'name': name, 'private':private, 'required': required, 'type':featurePropertyType}
    r = apiManager.post('/path/' + pathId + '/vector/property', body, token)
    return r
    
def edit(pathId, featurePropertyId, token, private=False, required = False):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    featurePropertyId = sanitize.validUuid('featurePropertyId', featurePropertyId, True) 
    private = sanitize.validBool('private', private, True)
    required = sanitize.validBool('required', required, True)
    token = sanitize.validString('token', token, True)


    body = {'private':private, 'required': required}

    r = apiManager.patch('/path/' + pathId + '/vector/property/' + featurePropertyId, body, token)
    return r


def trash(pathId, featurePropertyId, token):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    featurePropertyId = sanitize.validUuid('featurePropertyId', featurePropertyId, True) 
    token = sanitize.validString('token', token, True)

    body = {'trashed': True}
    r = apiManager.put('/path/' + pathId + '/vector/property/' + featurePropertyId + '/trashed', body, token)
    return r


def recover(pathId, featurePropertyId, token):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    featurePropertyId = sanitize.validUuid('featurePropertyId', featurePropertyId, True) 
    token = sanitize.validString('token', token, True)

    body = {'trashed': False}
    r = apiManager.put('/path/' + pathId + '/vector/property/' + featurePropertyId + '/trashed', body, token)
    return r



    


