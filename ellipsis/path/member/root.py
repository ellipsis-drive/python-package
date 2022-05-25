from ellipsis import apiManager, sanitize
from ellipsis.util.root import recurse

def get(pathId, token=None, memberType=None, listAll = True):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    memberType = sanitize.validStringArray('memberType', memberType, False)

    body = {
        'type': memberType
    }
    
    def f(body):
        return apiManager.get(f'/path/{pathId}/member', body, token)
    
    r = recurse(f, body, listAll)
    return r

def delete(pathId, userId, token):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, True)
    userId = sanitize.validUuid('userId', userId, True)

    return apiManager.delete(f'/path/{pathId}/member/{userId}', None, token)


def edit(pathId, userId, access, token):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, True)
    userId = sanitize.validUuid('userId', userId, True)
    access = sanitize.validObject('access', access, True)

    return apiManager.patch(f'/path/{pathId}/member/{userId}', {
        'access': access
    }, token)
