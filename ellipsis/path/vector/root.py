from ellipsis import apiManager
from ellipsis import sanitize

def add( name, token, parentId = None, publicAccess =None, metadata=None):
    name = sanitize.validString('name', name, True)
    token = sanitize.validString('token', token, True)
    parentId = sanitize.validUuid('parentId', parentId, False)
    metadata = sanitize.validObject('metadata', metadata, False)
    publicAccess = sanitize.validObject('publicAccess', publicAccess, False)

    body = {'name': name, 'parentId':parentId, 'publicAccess':publicAccess, 'metadata':metadata }

    return apiManager.post('/path/vector', body, token)

def editRendering(pathId, maxZoom, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('parentId', pathId, True)
    maxZoom = sanitize.validInt('maxZoom', maxZoom, True)

    body = {"method":"vector tiles","parameters":{"zoom":maxZoom,"mb":2,"step":1000,"amount":1000},"centerPointOnly":False,"lod":6}
    r = apiManager.put('/path/' + pathId + '/vector/renderOptions' , body, token)
    return r


def editFilter(pathId, propertyFilter, token):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    token = sanitize.validString('token', token, True)
    propertyFilter = sanitize.validObject('propertyFilter', propertyFilter, True)
    
    body = {'filter': propertyFilter}
    r = apiManager.post('/path/' + pathId + '/vector/filter' , body, token)
    return r

def computeAllVectorTiles(pathId, timestampId, token):
    pathId = sanitize.validUuid('pathId', pathId, True)
    timestampId = sanitize.validUuid('timestampId', timestampId, True)
    token = sanitize.validString('token', token, True)

    r = apiManager.post('/path/' + pathId + '/vector/timestamp/' + timestampId + '/precompute/completeVectorTile' , {}, token)

    return r




