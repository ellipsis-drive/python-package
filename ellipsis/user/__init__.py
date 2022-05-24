from ellipsis import apiManager
from ellipsis import sanitize

def search(username, fuzzySearch= True):
    
    sanitize.validString('username', username, True)

    sanitize.validBool('fuzzySearch', fuzzySearch, True)

    
    body = {'username': username, 'fuzzySearch':fuzzySearch}
    r = apiManager.get(url = '/user', parameters = body)

    return r


def get(userId):
    sanitize.validUuid('userId', userId)
    
    r = apiManager.get(url = '/user/' + userId, parameters = None)
    return r

