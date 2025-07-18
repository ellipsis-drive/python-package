from ellipsis import apiManager
from ellipsis import sanitize

import os
import pickle
from io import BytesIO
import json
import pandas as pd


def add(  token, filePath=None, memFile=None, parentId = None, publicAccess =None, metadata=None,name=None):
    token = sanitize.validString('token', token, True)
    parentId = sanitize.validUuid('parentId', parentId, False)
    publicAccess = sanitize.validObject('publicAccess', publicAccess, False)
    metadata = sanitize.validObject('metadata', metadata, False)
    filePath = sanitize.validString('filePath', filePath, False)
    name = sanitize.validString('name', name, False)
    if type(memFile) == type(None) and type(filePath) == type(None):
        raise ValueError('You need to specify either a filePath or a memFile')
    if type(memFile) != type(None) and type(name) == type(None):
        raise ValueError('Parameter name is required when using a memory file')

    seperator = os.path.sep    
    fileName = filePath.split(seperator)[len(filePath.split(seperator))-1 ]
    if len(fileName) > 64:
        fileName = fileName[0:63]
    body = {'name':fileName, 'publicAccess':publicAccess, 'metadata':metadata, 'parentId':parentId}
    if type(memFile) == type(None):
        r = apiManager.upload('/path/file' , filePath, body, token, key = 'data')
    else:
        r = apiManager.upload('/path/file' , filePath , name, body, token, memfile = memFile)

    return r


def download(pathId, filePath, token=None):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    filePath = sanitize.validString('filePath', filePath, True)


    apiManager.download('/path/' + pathId + '/file/data', filePath, token)
    


def addCsv(df, name, token, parentId = None, publicAccess =None, metadata=None):
    token = sanitize.validString('token', token, True)
    name = sanitize.validString('name', name, True)
    df = sanitize.validPandas('df', df, True)

    parentId = sanitize.validUuid('parentId', parentId, False)
    publicAccess = sanitize.validObject('publicAccess', publicAccess, False)
    metadata = sanitize.validObject('metadata', metadata, False)
    
    memfile = BytesIO()
    df.to_csv(memfile)
    

    body = {'name':name, 'publicAccess':publicAccess, 'metadata':metadata, 'parentId':parentId}
    r = apiManager.upload('/path/file' , name,  body, token, key='data', memfile = memfile)

    
    return r

def getCsv(pathId, token=None):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)


    r = apiManager.get('/path/' + pathId + '/file/data', {}, token)


    memfile = BytesIO(bytes(r, 'utf-8'))
    try:
        df =  pd.read_csv(memfile)
    except:
        raise ValueError('Read file is not a valid CSV')
    return df



def addJson(d, name, token, parentId = None, publicAccess =None, metadata=None):
    token = sanitize.validString('token', token, True)
    name = sanitize.validString('name', name, True)
    d = sanitize.validObject('d', d, True)

    parentId = sanitize.validUuid('parentId', parentId, False)
    publicAccess = sanitize.validObject('publicAccess', publicAccess, False)
    metadata = sanitize.validObject('metadata', metadata, False)
    
    memfile = BytesIO()
    d = json.dumps(d)
    memfile.write(bytes(d, 'utf-8'))
    

    body = {'name':name, 'publicAccess':publicAccess, 'metadata':metadata, 'parentId':parentId}
    r = apiManager.upload('/path/file' , name,  body, token, key='data', memfile = memfile)

    
    return r


def getJson(pathId, token=None):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)

    memfile = BytesIO()
    apiManager.download('/path/' + pathId + '/file/data', '', token, memfile)    
    memfile.seek(0)
    try:
        x = json.load(memfile)
    except:
        raise ValueError('Read file not a valid pickle file')


    return x



def addPickle(x, name, token, parentId = None, publicAccess =None, metadata=None):
    token = sanitize.validString('token', token, True)
    name = sanitize.validString('name', name, True)
    parentId = sanitize.validUuid('parentId', parentId, False)
    publicAccess = sanitize.validObject('publicAccess', publicAccess, False)
    metadata = sanitize.validObject('metadata', metadata, False)
    
    memfile = BytesIO()
    pickle.dump(x, memfile)

    body = {'name':name, 'publicAccess':publicAccess, 'metadata':metadata, 'parentId':parentId}
    r = apiManager.upload('/path/file' , name,  body, token, key='data', memfile = memfile)

    return r
    

def getPickle(pathId, token=None):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)

    memfile = BytesIO()
    apiManager.download('/path/' + pathId + '/file/data', '', token, memfile)    
    memfile.seek(0)
    try:
        x = pickle.load(memfile)
    except:
        raise ValueError('Read file not a valid pickle file')


    return x






