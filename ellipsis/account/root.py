from ellipsis import apiManager
from ellipsis import sanitize
from ellipsis.util.root import recurse
import requests

def logIn(username, password, validFor = None):

        username = sanitize.validString('username', username, True)
        password = sanitize.validString('password', password, True)
        validFor = sanitize.validInt('validFor', validFor, False)

        json = {'username': username, 'password': password, 'validFor': validFor}

        r = apiManager.call(requests.post,'/account/login', body=json, token=None, crash=False)
        if r.status_code == 400:
            x = r.json()
            if x['message'] == "No password configured.":
                raise ValueError("You cannot login with your Google credentials in the Python module. You need to configure an Ellipsis Drive specific password. You can do this on https://app.ellipsis-drive.com/account-settings/security")
        if r.status_code != 200:
            raise ValueError(r.text)

        r = r.json()
        token = r['token']

        return(token)

def listRoot(rootName, token, pathTypes= None, pageStart = None, listAll = True):
    token = sanitize.validString('token', token, True)
    rootName = sanitize.validString('rootName', rootName, True)
    pageStart = sanitize.validUuid('pageStart', pageStart, False)
    listAll = sanitize.validBool('listAll', listAll, True)        
    pathTypes = sanitize.validObject('pathTypes', pathTypes, False)
    if type(pathTypes) == type(None):
        pathTypes = ['folder', 'raster', 'vector', 'file']
        

    url = "/account/root/" + rootName
    body = {"type": pathTypes, "pageStart": pageStart}


    def f(body):
        r = apiManager.get(url, body, token)
        return r

    r = recurse(f, body, listAll)
        
    return r




