from ellipsis import apiManager
from ellipsis import sanitize


def get(pathId, token=None):
    token = sanitize.validString('token', token, False)
    pathId = sanitize.validUuid('pathId', pathId, True)

    r = apiManager.get('/path/' + pathId + '/bookmark', {}, token)
        
    return r



def add(name, bookmark, token, parentId = None, publicAccess = None, metadata=None):
    token = sanitize.validString('token', token, True)
    bookmark = sanitize.validObject('bookmark', bookmark, True)
    name = sanitize.validString('pathId', name, False)
    metadata = sanitize.validObject('metadata', metadata, False)
    publicAccess = sanitize.validObject('publicAccess', publicAccess, False)
    parentId = sanitize.validUuid('parentId', parentId, False)

    r = apiManager.post('/path/bookmark', {'name':name, 'bookmark':bookmark , 'parentId':parentId, 'publicAccess':publicAccess, 'metadata':metadata}, token)
        
    return r


def edit(pathId, token, layers=None, dems=None):
    layers = sanitize.validObject('layers', layers, False)
    dems = sanitize.validObject('dems', dems, False)
    pathId = sanitize.validUuid('pathId', pathId, True)

    r = apiManager.patch('/path/' + pathId + '/bookmark', {'layers':layers, 'dems':dems}, token)
        
    return r




