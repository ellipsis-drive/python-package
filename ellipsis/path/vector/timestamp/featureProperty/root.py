from ellipsis import apiManager
from ellipsis import sanitize



def add(pathId, timestampId, name, featurePropertyType, token, private = False, required = False):

    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    name = sanitize.validString('name', name, True)
    featurePropertyType = sanitize.validString('featurePropertyType', featurePropertyType, True)
    private = sanitize.validBool('private', private, True)
    required = sanitize.validBool('required', required, True)
    token = sanitize.validString('token', token, True)


    body = {'name': name, 'private':private, 'required': required, 'type':featurePropertyType}

    r = apiManager.post('/path/' + pathId + '/vector/timestamp/' + timestampId + '/property', body, token)
    return r
    
def edit(pathId, timestampId, featurePropertyId, token, private=False, required = False):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    featurePropertyId = sanitize.validUuid('featurePropertyId', featurePropertyId, True) 
    private = sanitize.validBool('private', private, True)
    required = sanitize.validBool('required', required, True)
    token = sanitize.validString('token', token, True)


    body = {'private':private, 'required': required}

    r = apiManager.patch('/path/' + pathId + '/vector/timestamp/' + timestampId + '/property/' + featurePropertyId, body, token)
    return r


def delete(pathId, timestampId, featurePropertyId, token):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    featurePropertyId = sanitize.validUuid('featurePropertyId', featurePropertyId, True) 
    token = sanitize.validString('token', token, True)

    body = {'deleted': True}
    r = apiManager.put('/path/' + pathId + '/vector/timestamp/' + timestampId + '/property/' + featurePropertyId + '/deleted', body, token)
    return r


def recover(pathId, timestampId, featurePropertyId, token):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    featurePropertyId = sanitize.validUuid('featurePropertyId', featurePropertyId, True) 
    token = sanitize.validString('token', token, True)

    body = {'deleted': False}
    r = apiManager.put('/path/' + pathId + '/vector/timestamp/' + timestampId + '/property/' + featurePropertyId + '/deleted', body, token)
    return r



    


