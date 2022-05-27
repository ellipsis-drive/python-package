from ellipsis import apiManager
from ellipsis import sanitize
from ellipsis.util.root import recurse

def logIn(username, password, validFor = None):

        username = sanitize.validString('username', username, True)
        password = sanitize.validString('password', password, True)
        validFor = sanitize.validInt('validFor', validFor, False)

        json = {'username': username, 'password': password, 'validFor': validFor}


        r = apiManager.post('/account/login', json)
        token = r['token']

        return(token)

def listRootMaps(rootName, token, pageStart = None, listAll = True):
    token = sanitize.validString('token', token, True)
    rootName = sanitize.validString('rootName', rootName, True)
    pageStart = sanitize.validUuid('pageStart', pageStart, False)
    listAll = sanitize.validBool('listAll', listAll, True)        


    url = "/account/root/" + rootName
    body = {"isFolder": False, "pageStart": pageStart}


    def f(body):
        r = apiManager.get(url, body, token)
        return r

    r = recurse(f, body, listAll)
        
    return r


def listRootFolders(rootName, token, pageStart = None, listAll = True):
    token = sanitize.validString('token', token, True)
    rootName = sanitize.validString('rootName', rootName, True)
    pageStart = sanitize.validUuid('pageStart', pageStart, False)
    listAll = sanitize.validBool('listAll', listAll, True)        


    url = "/account/root/" + rootName
    body = {"isFolder": True, "pageStart": pageStart}


    def f(body):
        r = apiManager.get(url, body, token)
        return r

    r = recurse(f, body, listAll)
        
    return r

