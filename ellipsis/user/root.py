from ellipsis import apiManager
from ellipsis import sanitize

def search(username, fuzzySearch= True):
    
    sanitize.validString('username', username, True)

    sanitize.validBool('fuzzySearch', fuzzySearch, True)

    
    body = {'username': username, 'fuzzySearch':fuzzySearch}
    r = apiManager.get('/user', body, None)

    return r


def get(userId):
    sanitize.validUuid('userId', userId, True)
    
    r = apiManager.get('/user/' + userId, None, None)
    return r

