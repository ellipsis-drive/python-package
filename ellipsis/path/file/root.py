from ellipsis import apiManager
from ellipsis import sanitize

import os


def download(pathId, filePath, token=None):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    filePath = sanitize.validString('filePath', filePath, True)


    apiManager.download('/path/' + pathId + '/file/data', filePath, token)
    


def add( filePath, token, parentId = None, publicAccess =None, metadata=None):
    token = sanitize.validString('token', token, True)
        
    seperator = os.path.sep    
    fileName = filePath.split(seperator)[len(filePath.split(seperator))-1 ]
        
    body = {'name':fileName, 'publicAccess':publicAccess, 'metadata':metadata, 'parentId':parentId}
    r = apiManager.upload('/path/file' , filePath, body, token, key = 'data')
    return r