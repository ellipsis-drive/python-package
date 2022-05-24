from ellipsis import apiManager
from ellipsis import sanitize

username = 'demo_user'
password = 'demo_user'

def logIn(username, password, validFor = None):

        username = sanitize.validString('username', username, True)
        password = sanitize.validString('password', password, True)
        validFor = sanitize.validInt('validFor', validFor, False)

        json = {'username': username, 'password': password, 'validFor': validFor}


        r = apiManager.post('/account/login', json)
        token = r['token']

        return(token)

def listRoot(rootName, token, isFolder = False, pageStart = None, listAll = True):

    rootName = sanitize.validRoot('rootName', rootName, True)
    pageStart = sanitize.validUuid('pageStart', pageStart, False)
    listAll = sanitize.validBool('listAll', listAll, True)        
    isFolder = sanitize.validBool('isFolder', isFolder, True)        


    url = "/account/root/" + rootName
    body = {"isFolder": isFolder, "pageStart": pageStart}


    r = apiManager.get(url, body, token)            
    nextPageStart = r['nextPageStart']

    if listAll:
        while nextPageStart != None:
            body['pageStart'] = nextPageStart
            r_new = apiManager.get(url, body, token)            
            nextPageStart = r_new['nextPageStart']
            r['result'] = r['result'] + r_new['result']
        r['pageStart'] = None
        
    return r



