from ellipsis import apiManager, sanitize


def inviteUser(pathId=None, token=None, userId=None, email=None, access=None):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    userId = sanitize.validUuid('userId', userId, False)
    email = sanitize.validString('email', email, False)
    access = sanitize.validBool('access', access, True)

    if(userId == None and email == None):
        raise ValueError("Email and userId cannot both be None")

    return apiManager.post(f'/path/{pathId}/invite', {
        'userId': userId,
        'email': email,
        'access': access
    }, token)


def revokeInvite(pathId=None, token=None, inviteId=None):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    inviteId = sanitize.validUuid('inviteId', inviteId, True)
    return apiManager.delete(f'/path/{pathId}/invite/{inviteId}', None, token)


def acceptInvite(pathId=None, token=None, inviteId=None, accept=None):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    inviteId = sanitize.validUuid('inviteId', inviteId, True)
    accept = sanitize.validBool('accept', accept, False)

    return apiManager.post(f'/path/{pathId}/invite/{inviteId}/accept', {
        'accept': accept
    }, token)


def getYourInvites(token=None):
    token = sanitize.validString('token', token, False)
    return apiManager.get('/path/invite', None, token)


def getPathInvites(pathId=None, token=None):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    return apiManager.get(f'/path/{pathId}/invite', None, token)
