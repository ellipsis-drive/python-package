import ellipsis as el
from uuid import UUID


def search(username, fuzzySearch= True):
    
    if type(username) != type('x'):
        raise ValueError('username must be of type string')

    if type(fuzzySearch) != type(True):
        raise ValueError('fuzzySearch must be of type boolean')

    
    body = {'username': username, 'fuzzySearch':fuzzySearch}
    r = el.apiManager.get(url = '/user', parameters = body)

    return r


def get(userId):
    try:
        UUID(userId, version=2)
    except:
        raise ValueError('userId must be of type string and be a uuid')
    
    r = el.apiManager.get(url = '/user/' + userId, parameters = None)
    return r



