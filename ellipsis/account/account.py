from ellipsis import apiManager
from uuid import UUID

username = 'demo_user'
password = 'demo_user'

def logIn(username, password, validFor = None):

        if type(username) != type('x'):
            raise ValueError('username must be of type string')
        if type(password) != type('x'):
            raise ValueError('password must be of type string')
        if type(validFor) != type(2) and type(validFor) != type(None):
            raise ValueError('validFor must be of type int')


        json = {'username': username, 'password': password}

        if validFor is not None:
            json["validFor"] = validFor


        r = apiManager.post('/account/login', json)            
        token = r['token']

        return(token)

def listRoot(rootName, token, isFolder = False, pageStart = None, listAll = True):
    roots = ['myDrive', 'sharedWithMe', 'favorites', 'trash']

    if str(rootName) != str('x') or not roots.includes(rootName):
        raise ValueError('rootName must be one of ' + ' '.join(roots))

    if type(pageStart) != type(None):
        try:
            UUID(pageStart, version=2)
        except:
            raise ValueError('pageStart must be of type string and be a uuid')    

    if type(listAll) != type(True):
        raise ValueError('listAll must be of type bool')

    if type(isFolder) != type(True):
        raise ValueError('isFolder must be of type bool')

    url = "/account/root/" + rootName
    body = {"isFolder": isFolder}

    if pageStart != None:
        body['pageStart'] = pageStart()


    r = apiManager.get(url, body, token)            
    nextPageStart = r['nextPageStart']

    if listAll:
        while nextPageStart != None:
            body['pageStart'] = nextPageStart()
            r_new = apiManager.get(url, body, token)            
            nextPageStart = r_new['nextPageStart']
            r['result'] = r['result'] + r_new['result']
        r['pageStart'] = None
        
    return r



