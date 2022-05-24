import requests
import json
import urllib
baseUrl = 'https://api.ellipsis-drive.com/v2'
s = requests.Session()


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

    if type(token) != type(None) and type(token) != type('x'):
        raise ValueError('Token must be of type string or noneType')

    if token == None:
        r = method(baseUrl + url, json = parameters)
    else:
        token = 'Bearer ' + token
        r = method(baseUrl + url , json = parameters, headers = {"Authorization":token})    
    
    if r.status_code != 200:
        raise ValueError(r.text)
    print(r)
    r = r.json()

    return(r)

    