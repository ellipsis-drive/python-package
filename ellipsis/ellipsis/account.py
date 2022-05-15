# login
from util import URL
from util import session as s

def logIn(username, password, validFor = None):

        json = {'username': username, 'password': password}

        if validFor is not None:
            json["validFor"] = validFor

        r =s.post(f"{URL}/account/login/", json=json)
        if r.status_code != 200:
            raise ValueError(r.text)
            
        token = r.json()
        token = token['token']
        token = 'Bearer ' + token
        return(token)

def listRoot(rootName, isFolder = False, token = None):
    # rootName should be of myDrive, sharedWithMe, favorites or trash
    
    url = f"{URL}/account/root/{rootName}"
    body = {"isFolder": isFolder}
    
    if token == None:
        r = s.get(url, json = body, timeout=10)
    else:
        r = s.get(url, headers = {"Authorization":token}, json = body, timeout=10)

    if r.status_code != 200:
        raise ValueError(r.text)

    r  = r.json()['result'][0]
    return r