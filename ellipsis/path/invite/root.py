from ellipsis import apiManager, sanitize


def send(pathId, access, token, userId=None, email=None, sendMail=None):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, True)
    userId = sanitize.validUuid('userId', userId, False)
    email = sanitize.validString('email', email, False)
    access = sanitize.validObject('access', access, True)
    sendMail = sanitize.validBool('sendMail', sendMail, False)

    return apiManager.post(f'/path/{pathId}/invite', {
        'userId': userId,
        'email': email,
        'access': access,
        'sendMail': sendMail
    }, token)


def revoke(pathId, inviteId, token):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    inviteId = sanitize.validUuid('inviteId', inviteId, True)
    return apiManager.delete(f'/path/{pathId}/invite/{inviteId}', None, token)


def accept(pathId, inviteId, token):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    inviteId = sanitize.validUuid('inviteId', inviteId, True)

    return apiManager.post(f'/path/{pathId}/invite/{inviteId}/accept', {
        'accept': True
    }, token)

def decline(pathId, inviteId, token):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    inviteId = sanitize.validUuid('inviteId', inviteId, True)

    return apiManager.post(f'/path/{pathId}/invite/{inviteId}/accept', {
        'accept': False
    }, token)


def getYourInvites(token):
    token = sanitize.validString('token', token, True)
    return apiManager.get('/path/invite', None, token)


def getPathInvites(pathId, token):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    return apiManager.get(f'/path/{pathId}/invite', None, token)
