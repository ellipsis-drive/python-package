from ...util import *
from ....ellipsis import apiManager, sanitize


def listMembers(pathId=None, token=None, types=None):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    types = sanitize.validStringArray('types', types, False)

    return apiManager.get(f'/path/{pathId}/member', {
        'type': types
    }, token)


def removeMember(pathId=None, token=None, userId=None):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    userId = sanitize.validUuid('userId', userId, True)

    return apiManager.delete(f'/path/{pathId}/member/{userId}', None, token)


def editMember(pathId=None, token=None, userId=None, access=None):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    userId = sanitize.validUuid('userId', userId, True)
    access = sanitize.validDict('access', access, True)

    return apiManager.patch(f'/path/{pathId}/member/{userId}', {
        'access': access
    }, token)
