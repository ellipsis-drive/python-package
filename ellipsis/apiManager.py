import requests
import json
import urllib
<<<<<<< HEAD
=======
import os
from requests_toolbelt import MultipartEncoder

>>>>>>> rewrite
baseUrl = 'https://api.ellipsis-drive.com/v2'
s = requests.Session()


<<<<<<< HEAD
def get(url, parameters = None, token = None):
    if type(parameters) != type(None):
        if type(parameters) != type({}):
            raise ValueError('parameters of an API call must be of type dict or noneType')
        else:
            for k in parameters.keys():
                if type(parameters[k]) != type('x'):
                    parameters[k] = json.dumps(parameters[k]) 

            parameters = urllib.parse.urlencode(parameters)
            url = url + '?' + parameters
            parameters = None
            
    r = call( method = s.get, url = url, parameters = parameters, token = token )
    return r

def post(url, parameters, token = None):
    r = call( method = s.post, url = url, parameters = parameters, token = token )
    return r
def put(url, parameters, token = None):
    r = call( method = s.put, url = url, parameters = parameters, token = token )
    return r
def patch(url, parameters, token = None):
    r = call( method = s.patch, url = url, parameters = parameters, token = token )
    return r
    
def call(method, url, parameters = None, token = None):

    print(url)
    print(parameters)
    print(token)
    if type(parameters) != type(None) and type(parameters) != type({}):
        raise ValueError('parameters of an API call must be of type dict or noneType')
=======
def filterNone(body):
    if type(body) == type(None):
        return body

    params = {}
    for k in body.keys():
        if type(body[k]) != type(None):
            params[k] = body[k]
    return params

def get(url, body = None, token = None, crash = True):
    if body == None:
        body = {'token': token}
    else:
        body['token'] = token
    body = filterNone(body)
    
    for k in body.keys():
        if type(body[k]) != type('x') :
            body[k] = json.dumps(body[k])


    body = urllib.parse.urlencode(body)

    url = url + '?' + body
            
    r = call( method = s.get, url = url, body = None, token = token, crash = crash )


    return r


def post(url, body, token=None):
    r = call(method=s.post, url=url, body=body, token=token)
    return r


def put(url, body, token=None):
    r = call(method=s.put, url=url, body=body, token=token)
    return r


def patch(url, body, token=None):
    r = call(method=s.patch, url=url, body=body, token=token)
    return r

    
def delete(url, body, token = None):
    r = call( method = s.delete, url = url, body = body, token = token )
    return r


def call(method, url, body = None, token = None, crash = True):
    body = filterNone(body)
    if type(body) != type(None) and type(body) != type({}):
        raise ValueError(
            'body of an API call must be of type dict or noneType')
>>>>>>> rewrite

    if type(token) != type(None) and type(token) != type('x'):
        raise ValueError('Token must be of type string or noneType')

    if token == None:
<<<<<<< HEAD
        r = method(baseUrl + url, json = parameters)
    else:
        r = method(baseUrl + url , json = parameters, headers = {"Authorization":token})    
    
    if r.status_code != 200:
        raise ValueError(r.text)
    print(r)
    r = r.json()

    return(r)

    
=======
        r = method(baseUrl + url, json=body)
    else:
        token = 'Bearer ' + token
        r = method(baseUrl + url , json = body, headers = {"Authorization":token})    

    if crash:
        if r.status_code != 200:
            raise ValueError(r.text)
        try:
            r = r.json()
        except:
            r = r.text
    
        return r
    else:
        return r


def upload(url, filePath, body, token):
    body = filterNone(body)

    seperator = os.path.sep    
    fileName = filePath.split(seperator)[len(filePath.split(seperator))-1 ]


    conn_file = open(filePath, 'rb')

    payload = MultipartEncoder(fields = {**body, 'fileToUpload': (fileName, conn_file, 'application/octet-stream')})

    token = 'Bearer ' + token
        
    r = s.post(baseUrl + url, headers = {"Authorization":token, "Content-Type": payload.content_type}, data=payload)
    conn_file.close()
    
    if r.status_code != 200:
        raise ValueError(r.text)
    return r.json()

def download(url, filePath, token):

    if token == None:    
        r = s.get(baseUrl + url, headers={"Authorization": token})
    else:
        r = s.get(baseUrl + url)

    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

    open(filePath , 'wb').write(r.content)    
    
    
>>>>>>> rewrite
