from ellipsis import apiManager, sanitize
from ellipsis.util.root import recurse

def create(description, accessList, token, validFor= None):
    token = sanitize.validString('token', token, True)
    description = sanitize.validString('description', description, True)
    accessList = sanitize.validObject('accessList', accessList, True)
    validFor = sanitize.validInt('validFor', validFor, False)



    return apiManager.post('/account/security/accessToken', {
        'description': description,
        'validFor': validFor,
        'accessList': accessList,
        'scope': 'all'
    }, token)


def revoke(accessTokenId, token):
    accessTokenId = sanitize.validUuid('accessTokenId', accessTokenId, True)
    token = sanitize.validString('token', token, True)

    return apiManager.delete(f'/account/security/accessToken/{accessTokenId}', None, token)


def get(token, pageStart = None, listAll = False):
    pageStart = sanitize.validObject('pageStart', pageStart, False)
    token = sanitize.validString('token', token, True)
    listAll = sanitize.validBool('listAll', listAll, True)

    body = {'pageStart':pageStart}

    def f(body):
        return apiManager.get('/account/security/accessToken', body, token)
    
    r = recurse(f, body, listAll)
    return r