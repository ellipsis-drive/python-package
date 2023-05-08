import requests
import json
import urllib
import os
from requests_toolbelt import MultipartEncoder

baseUrl = 'https://api.ellipsis-drive.com/v3'


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
            
    r = call( method = requests.get, url = url, body = None, token = token, crash = crash )


    return r


def post(url, body, token=None):
    r = call(method=requests.post, url=url, body=body, token=token)
    return r


def put(url, body, token=None):
    r = call(method=requests.put, url=url, body=body, token=token)
    return r


def patch(url, body, token=None):
    r = call(method=requests.patch, url=url, body=body, token=token)
    return r

    
def delete(url, body, token = None):
    r = call( method = requests.delete, url = url, body = body, token = token )
    return r


def call(method, url, body = None, token = None, crash = True):

    body = filterNone(body)
    if type(body) != type(None) and type(body) != type({}):
        raise ValueError(
            'body of an API call must be of type dict or noneType')

    if type(token) != type(None) and type(token) != type('x'):
        raise ValueError('Token must be of type string or noneType')

    if token == None:
        r = method(baseUrl + url, json=body)
    else:
        if not 'Bearer' in token:
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


def upload(url, filePath, body, token, key = 'data', memfile= None):
    body = filterNone(body)
    seperator = os.path.sep    
    fileName = filePath.split(seperator)[len(filePath.split(seperator))-1 ]

    if str(type(memfile)) == str(type(None)):
        conn_file = open(filePath, 'rb')
    else:
        conn_file = memfile
    
    payload = MultipartEncoder(fields = {**body, key: (fileName, conn_file, 'application/octet-stream')})
    
    
    for k in body.keys():
        body[k] = str(body[k])


    token = 'Bearer ' + token
        
    r = requests.post(baseUrl + url, headers = {"Authorization":token, "Content-Type": payload.content_type}, data=payload)
    
    if str(type(memfile)) == str(type(None)):
        conn_file.close()
    
    if r.status_code != 200:
        raise ValueError(r.text)
    return r.json()

def download(url, filePath, token = None, memfile = None):
    if type(token) == type(None):
        with requests.get(baseUrl + url, stream=True) as r:
            r.raise_for_status()
            if str(type(memfile)) == str(type(None)):
                with open(filePath, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192): 
                        # If you have chunk encoded response uncomment if
                        # and set chunk_size parameter to None.
                        #if chunk: 
                        f.write(chunk)
            else:
                for chunk in r.iter_content(chunk_size=8192): 
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    #if chunk: 
                    memfile.write(chunk)
    
        
        
    else:
        token = 'Bearer ' + token
        with requests.get(baseUrl + url, stream=True, headers={"Authorization": token}) as r:
            r.raise_for_status()
            if str(type(memfile)) == str(type(None)):
                with open(filePath, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192): 
                        # If you have chunk encoded response uncomment if
                        # and set chunk_size parameter to None.
                        #if chunk: 
                        f.write(chunk)
            else:
                for chunk in r.iter_content(chunk_size=8192): 
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    #if chunk: 
                    memfile.write(chunk)
    

    
    
