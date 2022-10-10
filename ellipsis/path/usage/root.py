from ellipsis import apiManager, sanitize
from ellipsis.util.root import recurse


def getActiveUsers(pathId, token, listAll = True, pageStart = None):
    pageStart = sanitize.validUuid('pageStart', pageStart, False)
    token = sanitize.validString('token', token, True)
    listAll = sanitize.validBool('listAll', listAll, True)
    pathId = sanitize.validUuid('pathId', pathId, True)


    body = { 'pageStart':pageStart }


    def f(body):
        return apiManager.get('/path/' + pathId + '/usage/user', body, token)

    r = recurse(f, body, listAll)
    return r




def getUsage(pathId, userId, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)
    userId = sanitize.validUuid('userId', userId, True)

    return apiManager.get('/path/' + pathId + '/usage/user/' + userId + '/processingUnits', None, token)


def getAggregatedUsage(pathId, loggedIn, token):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, True)
    loggedIn = sanitize.validBool('loggedIn', loggedIn, True)


    return apiManager.get('/path/' + pathId + '/usage/processingUnits', {'loggedIn': loggedIn}, token)
