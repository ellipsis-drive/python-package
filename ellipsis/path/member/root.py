from ellipsis import apiManager, sanitize

def get(pathId, token=None, memberType=['inherited','direct']):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    memberType = sanitize.validStringArray('memberType', memberType, False)

    body = {
        'type': memberType
    }
    
    return apiManager.get(f'/path/{pathId}/member', body, token)
    

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
