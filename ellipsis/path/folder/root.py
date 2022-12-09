from ellipsis import apiManager
from ellipsis import sanitize
from ellipsis.util.root import recurse



def listFolder(pathId, pathTypes = None, pageStart=None, listAll = True, includeTrashed=False, token=None):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    pageStart = sanitize.validUuid('pageStart', pageStart, False)
    listAll = sanitize.validBool('listAll', listAll, False)
    includeTrashed = sanitize.validBool('includeTrashed', includeTrashed, True)
    pathTypes = sanitize.validObject('pathTypes', pathTypes, False)

    if type(pathTypes) == type(None):
        pathTypes = ['folder', 'raster', 'vector', 'file']
    

    body  = {'pageStart': pageStart, 'type':pathTypes, 'includeTrashed':includeTrashed}
    
    def f(body):
        
        return apiManager.get(f'/path/{pathId}/list', body, token)

    r = recurse(f, body, listAll)
    return r

def add( name, token, parentId = None, publicAccess =None, metadata=None):
    name = sanitize.validString('name', name, True)
    token = sanitize.validString('token', token, True)
    parentId = sanitize.validUuid('parentId', parentId, False)
    metadata = sanitize.validObject('metadata', metadata, False)
    publicAccess = sanitize.validObject('publicAccess', publicAccess, False)

    body = {'name': name, 'parentId':parentId, 'publicAccess':publicAccess, 'metadata':metadata }

    return apiManager.post('/path/folder', body, token)

