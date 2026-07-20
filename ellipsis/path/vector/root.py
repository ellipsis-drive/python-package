from ellipsis import apiManager
from ellipsis import sanitize
from ellipsis.path import get as getPath

def add( name, token, parentId = None, publicAccess =None, metadata=None):
    name = sanitize.validString('name', name, True)
    token = sanitize.validString('token', token, True)
    parentId = sanitize.validUuid('parentId', parentId, False)
    metadata = sanitize.validObject('metadata', metadata, False)
    publicAccess = sanitize.validObject('publicAccess', publicAccess, False)

    body = {'name': name, 'parentId':parentId, 'publicAccess':publicAccess, 'metadata':metadata }

    return apiManager.post('/path/vector', body, token)

def editRendering(pathId, token, maxZoom=None, properties=None):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('parentId', pathId, True)
    maxZoom = sanitize.validInt('maxZoom', maxZoom, False)
    properties = sanitize.validStringArray('properties', properties, False)

    info = getPath(pathId=pathId, token=token)
    definedProperties = [p for p in info['vector']['properties'] if not p['trashed'] ]
    renderOptions = info['vector']['renderOptions']
    if type(renderOptions) != type(None):
        if type(maxZoom) != type(None):
            renderOptions['parameters']['zoom'] = maxZoom
        if type(properties) != type(None):
            submitProperties = []
            for p in properties:
                newP = None
                for pr in definedProperties:
                    if pr['name'] == p:
                        newP = pr
                if type(newP) == type(None):
                    raise ValueError('property ', p , ' does not exist for this layer')
                submitProperties = submitProperties + [newP]
            renderOptions['properties'] = submitProperties

    body = renderOptions
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




