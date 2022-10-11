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

def listRoot(rootName, pathType, token, pageStart = None, listAll = True):
    token = sanitize.validString('token', token, True)
    rootName = sanitize.validString('rootName', rootName, True)
    pageStart = sanitize.validUuid('pageStart', pageStart, False)
    listAll = sanitize.validBool('listAll', listAll, True)        
    if type(pathType) != type('x') or (pathType != 'folder' and pathType !='layer' ) :
        raise ValueError("pathType must be one of 'layer' or 'folder'")
        
    isFolder = False
    if pathType == 'folder':
        isFolder = True        

    url = "/account/root/" + rootName
    body = {"isFolder": isFolder, "pageStart": pageStart}


    def f(body):
        r = apiManager.get(url, body, token)
        return r

    r = recurse(f, body, listAll)
        
    return r




